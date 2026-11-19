#!/usr/bin/env python3
"""Ferramentas locais de roteiro, montagem e verificação do FAQ."""
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

CONFIG = Path(__file__).resolve().parents[1] / "config"
FORMATS = {"vertical": (1080, 1920), "horizontal": (1920, 1080)}
FPS, AUDIO_RATE = 30, 48000
MAX_SECONDS = 60
HDR_TRANSFERS = {"smpte2084", "arib-std-b67"}


def run(command, **kwargs):
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", **kwargs)
    if result.returncode:
        raise ValueError(f"{command[0]} falhou: {result.stderr.strip()[-2500:]}")
    return result


def json_file(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def probe(path):
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                           "-of", "json", str(path.resolve())]).stdout)


def stream(info, kind):
    return next((item for item in info["streams"] if item["codec_type"] == kind
                 and not item.get("disposition", {}).get("attached_pic")), None)


def has_duration(info):
    try:
        duration = float(info["format"]["duration"])
    except (KeyError, TypeError, ValueError):
        raise ValueError("Não foi possível medir a duração da mídia.") from None
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("A mídia tem duração inválida.")
    return duration


def media_path(folder, name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Informe um caminho para o arquivo no plano.")
    path = (folder / name).resolve()
    if not path.is_file():
        raise ValueError(f"Arquivo ausente: {path}")
    return path


def bounded_number(value, label, minimum, maximum):
    if (type(value) not in (int, float) or not math.isfinite(value)
            or not minimum <= value <= maximum):
        raise ValueError(f"{label} deve estar entre {minimum} e {maximum}.")
    return value


def format_dimensions(format_name):
    if not isinstance(format_name, str) or format_name not in FORMATS:
        raise ValueError("formato deve ser vertical ou horizontal.")
    return FORMATS[format_name]


def inspect(path):
    info = probe(path)
    fields = ("codec_name", "width", "height", "sample_aspect_ratio", "avg_frame_rate",
              "color_space", "color_primaries", "color_transfer", "sample_rate",
              "channels", "side_data_list")
    return {
        "duracao_s": has_duration(info),
        "streams": [{k: s[k] for k in ("codec_type", *fields) if k in s}
                    for s in info["streams"]],
    }


def doctor():
    scripts = {}
    for name in ("ffmpeg", "ffprobe", "node"):
        executable = shutil.which(name)
        scripts[name] = run([executable, "-version" if name != "node" else "--version"]).stdout.splitlines()[0] if executable else None
    required_filters = {"scale", "concat", "loudnorm", "ebur128", "subtitles", "colorspace"}
    filters = set()
    encoders = set()
    if scripts["ffmpeg"]:
        filters = {line.split()[1] for line in run(["ffmpeg", "-hide_banner", "-filters"]).stdout.splitlines()
                   if len(line.split()) >= 2}
        encoders = {line.split()[1] for line in run(["ffmpeg", "-hide_banner", "-encoders"]).stdout.splitlines()
                    if len(line.split()) >= 2}
    missing = sorted((required_filters - filters) | ({"libx264", "aac"} - encoders))
    return {"ferramentas": scripts, "recursos_ausentes": missing,
            "ok": bool(scripts["ffmpeg"] and scripts["ffprobe"] and not missing)}


def roteiro(path, profile_path=None):
    config = json_file(CONFIG / "pronuncia.json")
    script = unicodedata.normalize("NFC", path.read_text(encoding="utf-8-sig"))
    script = "\n".join(re.sub(r"\s+", " ", line).strip() for line in script.splitlines()).strip()
    if not script:
        raise ValueError("O roteiro está vazio.")
    hits = [term for term in config["listen_in_context"]
            if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", script, flags=re.IGNORECASE)]
    risky = re.findall(r"https?://\S+|(?:R\$\s*)?\d[\d/:.,-]*(?:h\d{0,2})?", script)
    # Show suggestions separately. Names of products, quotations and siglas inside
    # URLs need editorial context before a replacement is applied to spoken text.
    suggestions = {key: value for key, value in config["expansions"].items()
                   if re.search(rf"(?<!\w){re.escape(key)}(?!\w)", script)}
    count = len(re.findall(r"\b[\w]+(?:-[\w]+)*\b", script))
    report = {"roteiro_normalizado": script, "palavras": count,
              "estimativa_total_s_135_a_155_palavras_min": [round(count * 60 / rate + 1.4, 1)
                                                            for rate in (155, 135)],
              "sugestoes_de_fala": suggestions, "ouvir_em_contexto": hits,
              "validar_numeros_e_links": risky}
    if profile_path:
        profile = json_file(profile_path)
        if (not isinstance(profile, dict) or profile.get("locale") != "pt-BR"
                or profile.get("status") != "homologado"
                or not profile.get("voice_id") or not profile.get("engine")):
            raise ValueError("Selecione um perfil pt-BR homologado com voice_id e engine.")
        aliases = profile.get("aliases", {})
        if not isinstance(aliases, dict) or any(not key.strip() or not isinstance(value, str)
                                                or not value.strip() for key, value in aliases.items()):
            raise ValueError("aliases deve mapear cada termo aprovado para sua leitura.")
        if aliases:
            terms = "|".join(re.escape(key) for key in sorted(aliases, key=len, reverse=True))
            substitutions = re.compile(rf"https?://[^\s]+|(?<!\w)(?:{terms})(?!\w)")
            report["roteiro_falado"] = substitutions.sub(lambda match: aliases.get(match[0], match[0]), script)
        else:
            report["roteiro_falado"] = script
        report["perfil"] = {key: profile[key] for key in ("locale", "voice_id", "engine")}
    return report


def check_srt(path, duration):
    data = path.read_text(encoding="utf-8-sig").strip()
    if not data:
        raise ValueError("A legenda está vazia.")
    timestamp = r"(\d{2}):(\d{2}):(\d{2}),(\d{3})"
    prior_end = 0
    warnings = []
    for index, block in enumerate(re.split(r"\n\s*\n", data), start=1):
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].strip().isdigit():
            raise ValueError(f"Bloco SRT {index} inválido.")
        times = re.fullmatch(f"{timestamp} --> {timestamp}", lines[1].strip())
        if not times:
            raise ValueError(f"Bloco SRT {index} tem um timecode inválido.")
        values = [int(part) for part in times.groups()]
        if any(values[i] >= 60 for i in (1, 2, 5, 6)):
            raise ValueError(f"Bloco SRT {index} tem minutos ou segundos inválidos.")
        get_seconds = lambda v: 3600 * v[0] + 60 * v[1] + v[2] + v[3] / 1000
        start, end = get_seconds(values[:4]), get_seconds(values[4:])
        if start < prior_end or end <= start or end > duration + 0.001:
            raise ValueError(f"Bloco SRT {index} com sobreposição ou fora da timeline.")
        if len(lines) > 4 or len(" ".join(lines[2:])) / (end - start) > 17:
            warnings.append(f"Bloco {index}: revise linhas e velocidade de leitura.")
        prior_end = end
    return data + "\n", warnings


def compile_clip(index, clip, folder, dimensions, include_audio, outro=False):
    if not isinstance(clip, dict):
        raise ValueError(f"Clipe {index + 1} deve ser um objeto.")
    width, height = dimensions
    source = media_path(folder, clip.get("arquivo"))
    info = probe(source)
    video = stream(info, "video")
    if not video or video.get("color_transfer") in HDR_TRANSFERS:
        raise ValueError(f"Use um intermediário de vídeo SDR: {source.name}")
    if video.get("sample_aspect_ratio") not in (None, "0:1", "1:1", "N/A"):
        raise ValueError(f"Normalize a proporção do pixel antes de usar {source.name}.")
    duration = has_duration(info)
    if outro:
        rotation = next((side["rotation"] for side in video.get("side_data_list", [])
                         if "rotation" in side), 0)
        source_width, source_height = video["width"], video["height"]
        if rotation % 180 == 90:
            source_width, source_height = source_height, source_width
        if not math.isclose(source_width / source_height, width / height, rel_tol=0.01):
            raise ValueError("A vinheta precisa corresponder à proporção do formato escolhido.")
        start, frames = 0, math.ceil(duration * FPS - 1e-6)
    else:
        start = bounded_number(clip.get("inicio"), "inicio", 0, duration)
        end = bounded_number(clip.get("fim"), "fim", start, duration)
        frames = round((end - start) * FPS)
    if frames < 1:
        raise ValueError(f"Clipe {index + 1} tem menos de um quadro.")
    length = f"{frames / FPS:.9f}"
    framing = clip.get("quadro", "conter")
    if framing not in ("conter", "preencher"):
        raise ValueError("quadro deve ser conter ou preencher.")
    if type(clip.get("mutar", False)) is not bool:
        raise ValueError("mutar deve ser true ou false.")
    focus_x = bounded_number(clip.get("foco_x", 0.5), "foco_x", 0, 1)
    focus_y = bounded_number(clip.get("foco_y", 0.5), "foco_y", 0, 1)
    resize = f"scale={width}:{height}:flags=lanczos:"
    if framing == "conter":
        frame_filter = (resize + "force_original_aspect_ratio=decrease:force_divisible_by=2,"
                        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x071f3e")
    else:
        frame_filter = (resize + "force_original_aspect_ratio=increase:force_divisible_by=2,"
                        f"crop={width}:{height}:(iw-ow)*{focus_x}:(ih-oh)*{focus_y}")
    known_color = all(video.get(key) not in (None, "unknown", "unspecified")
                      for key in ("color_space", "color_transfer", "color_primaries"))
    color = "colorspace=all=bt709:range=tv"
    if not known_color:
        color += ":iall=bt709"
    args = ["-ss", str(start), "-i", str(source)]
    filters = [f"[{index}:{video['index']}]setpts=PTS-STARTPTS,fps={FPS},{frame_filter},"
               f"setsar=1,format=yuv420p,{color},tpad=stop_mode=clone:stop_duration=0.1,"
               f"trim=duration={length}[v{index}]"]
    if include_audio:
        audio = stream(info, "audio")
        if audio and not clip.get("mutar", False):
            filters.append(f"[{index}:{audio['index']}]asetpts=PTS-STARTPTS,aresample={AUDIO_RATE},"
                           f"aformat=channel_layouts=stereo,apad,atrim=duration={length}[a{index}]")
        else:
            filters.append(f"anullsrc=r={AUDIO_RATE}:cl=stereo,atrim=duration={length}[a{index}]")
    return args, filters, frames


def add_narration(args, filters, narration, folder, index, body_frames):
    if not isinstance(narration, dict):
        raise ValueError("locucao deve informar arquivo, inicio, fim e uso.")
    use = narration.get("uso")
    if use not in ("narracao_fora_de_quadro", "mesmo_audio_lipsync"):
        raise ValueError("Informe uso como narracao_fora_de_quadro ou mesmo_audio_lipsync.")
    if use == "mesmo_audio_lipsync" and narration.get("sincronia_revisada") is not True:
        raise ValueError("Revise a boca no início, meio e fim antes de confirmar sincronia_revisada.")
    body_duration = body_frames / FPS
    start = bounded_number(narration.get("inicio"), "locucao.inicio", 0, body_duration)
    end = bounded_number(narration.get("fim"), "locucao.fim", start, body_duration)
    start_frame, end_frame = round(start * FPS), round(end * FPS)
    if end_frame <= start_frame:
        raise ValueError("A locução deve ocupar pelo menos um quadro.")
    source = media_path(folder, narration.get("arquivo"))
    if source.suffix.lower() not in (".mp3", ".wav"):
        raise ValueError("Anexe a locução em MP3 ou WAV.")
    info = probe(source)
    audio = stream(info, "audio")
    if not audio or stream(info, "video"):
        raise ValueError("Use um arquivo MP3 ou WAV com uma faixa de áudio válida.")
    source_duration = has_duration(info)
    source_start = bounded_number(narration.get("inicio_arquivo", 0), "locucao.inicio_arquivo",
                                  0, source_duration)
    samples_per_frame = AUDIO_RATE // FPS
    start_sample = start_frame * samples_per_frame
    end_sample = end_frame * samples_per_frame
    source_start_sample = round(source_start * AUDIO_RATE)
    source_end_sample = source_start_sample + end_sample - start_sample
    if source_end_sample > round(source_duration * AUDIO_RATE):
        raise ValueError("O trecho solicitado supera a duração da locução. Ajuste os tempos na prévia.")
    args.extend(["-i", str(source)])
    filters.append(f"[{index}:{audio['index']}]aresample={AUDIO_RATE},"
                   f"aformat=channel_layouts=stereo,apad,atrim=start_sample={source_start_sample}:"
                   f"end_sample={source_end_sample},asetpts=PTS-STARTPTS[locucao]")
    outside = []
    if start_frame:
        outside.append(("antes", f"end_sample={start_sample}"))
    if end_frame < body_frames:
        outside.append(("depois", f"start_sample={end_sample}"))
    if not outside:
        filters.append("[audio_base][locucao]amix=inputs=2:weights='0 1':normalize=0:"
                       "duration=first[audio_editado]")
        return
    if len(outside) == 2:
        filters.append("[audio_base]asplit=2[base_antes][base_depois]")
    for part, trim in outside:
        source_label = f"base_{part}" if len(outside) == 2 else "audio_base"
        filters.append(f"[{source_label}]atrim={trim},asetpts=PTS-STARTPTS[{part}]")
    timeline = ("[antes]" if start_frame else "") + "[locucao]"
    if end_frame < body_frames:
        timeline += "[depois]"
    filters.append(f"{timeline}concat=n={len(outside) + 1}:v=0:a=1[audio_editado]")


def build_timeline(plano, folder, dimensions):
    clips = plano.get("clipes")
    if not isinstance(clips, list) or not 1 <= len(clips) <= 20:
        raise ValueError("O plano deve ter de 1 a 20 clipes.")
    args, filters, inputs = [], [], []
    audio_final = plano.get("audio_final")
    narration = plano.get("locucao")
    if narration is not None and audio_final:
        raise ValueError("Escolha locucao ou audio_final. Use audio_final para um mix pronto.")
    body_frames = 0
    for index, clip in enumerate(clips):
        clip_args, clip_filters, frames = compile_clip(index, clip, folder, dimensions,
                                                       include_audio=not audio_final)
        args.extend(clip_args)
        filters.extend(clip_filters)
        body_frames += frames
        inputs.append(f"[v{index}]" if audio_final else f"[v{index}][a{index}]")
    index = len(clips)
    body_duration = body_frames / FPS
    if audio_final:
        soundtrack = media_path(folder, audio_final)
        source_info = probe(soundtrack)
        audio = stream(source_info, "audio")
        if not audio or abs(has_duration(source_info) - body_duration) > 0.25:
            raise ValueError("O áudio final deve acompanhar a duração do corpo (tolerância: 0,25 s).")
        args.extend(["-i", str(soundtrack)])
        filters.append("".join(inputs) + f"concat=n={len(clips)}:v=1:a=0[video_base]")
        filters.append(f"[{index}:{audio['index']}]asetpts=PTS-STARTPTS,aresample={AUDIO_RATE},"
                       f"aformat=channel_layouts=stereo,apad,"
                       f"atrim=duration={body_duration:.9f}[audio_base]")
        index += 1
    else:
        filters.append("".join(inputs) + f"concat=n={len(clips)}:v=1:a=1[video_base][audio_base]")
    audio_label = "audio_base"
    if narration is not None:
        add_narration(args, filters, narration, folder, index, body_frames)
        audio_label = "audio_editado"
        index += 1
    outro = plano.get("vinheta")
    total_frames = body_frames
    if outro is not None:
        outro_args, outro_filters, frames = compile_clip(
            index, {"arquivo": outro}, folder, dimensions, include_audio=True, outro=True)
        args.extend(outro_args)
        filters.extend(outro_filters)
        total_frames += frames
        filters.append(f"[video_base][{audio_label}][v{index}][a{index}]"
                       "concat=n=2:v=1:a=1[video][audio]")
        audio_label = "audio"
    else:
        filters.append("[video_base]null[video]")
    duration = total_frames / FPS
    if duration > MAX_SECONDS:
        raise ValueError(f"Monte até {MAX_SECONDS} segundos incluindo a vinheta. O plano ficou com {duration:.3f} s.")
    filters.append(f"[{audio_label}]loudnorm=I=-16:TP=-2:LRA=7,aresample={AUDIO_RATE}[master_audio]")
    return args, filters, duration, body_duration


def run_with_progress(command, folder, name, duration):
    with tempfile.TemporaryFile() as error_log:
        with subprocess.Popen(command, cwd=folder, stdout=subprocess.PIPE, stderr=error_log,
                              text=True, encoding="utf-8", errors="replace") as process:
            fields = {}
            for line in process.stdout:
                key, separator, value = line.strip().partition("=")
                if not separator:
                    continue
                fields[key] = value
                if key == "progress":
                    timestamp = fields.get("out_time_us", "")
                    frame = fields.get("frame", "")
                    event = {"evento": "ffmpeg", "arquivo": name, "estado": value,
                             "duracao_planejada_s": duration,
                             "segundos_processados": int(timestamp) / 1e6 if timestamp.lstrip("-").isdigit() else None,
                             "frame": int(frame) if frame.isdigit() else None}
                    print(json.dumps(event, ensure_ascii=False), file=sys.stderr, flush=True)
                    fields.clear()
            if process.wait():
                error_log.seek(0, 2)
                error_log.seek(max(0, error_log.tell() - 2500))
                detail = error_log.read().decode("utf-8", errors="replace").strip()
                raise ValueError(f"ffmpeg falhou: {detail}")


def measure_audio(path):
    measured = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path.resolve()),
                    "-map", "0:a:0", "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    summary = measured.stderr.rsplit("Summary:", 1)[-1]
    integrated = re.search(r"\bI:\s*(-?[\d.]+)\s*LUFS", summary)
    true_peak = re.search(r"True peak:\s*Peak:\s*(-?[\d.]+)\s*dBFS", summary)
    return (float(integrated[1]) if integrated else None,
            float(true_peak[1]) if true_peak else None)


def encode(args, filters, duration, folder, name, caption_style=None, progress=False):
    filters = list(filters)
    output = "[video]"
    if caption_style:
        filters.append(f"[video]subtitles=legendas.srt:force_style='{caption_style}'[com_legenda]")
        output = "[com_legenda]"
    progress_args = ["-progress", "pipe:1", "-stats_period", "0.25"] if progress else []
    base = folder / f".mix-{name}"
    command = ["ffmpeg", "-hide_banner", "-v", "error", "-nostdin", "-filter_complex_threads", "2",
               *progress_args, *args, "-filter_complex", ";".join(filters), "-map", output,
               "-map", "[master_audio]", "-r", str(FPS), "-c:v", "libx264", "-threads", "4",
               "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
               "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "alac",
               "-ar", str(AUDIO_RATE), "-ac", "2", "-map_metadata", "-1", "-map_chapters", "-1",
               "-t", f"{duration:.9f}", str(base)]
    if progress:
        run_with_progress(command, folder, name, duration)
    else:
        run(command, cwd=folder)
    loudness, peak = measure_audio(base)
    correction = []
    if loudness is not None and peak is not None and (not -17 <= loudness <= -15 or peak > -2):
        gain = -16 - loudness
        correction = ["-af", f"volume={gain:.2f}dB,aresample=192000,"
                            f"alimiter=limit=0.78:level=false:latency=true,aresample={AUDIO_RATE}"]
    run(["ffmpeg", "-v", "error", "-nostdin", "-i", str(base), "-map", "0:v:0", "-map", "0:a:0",
         "-c:v", "copy", *correction, "-c:a", "aac", "-b:a", "160k", "-ar", str(AUDIO_RATE),
         "-ac", "2", "-map_metadata", "-1", "-map_chapters", "-1", "-movflags", "+faststart",
         "-t", f"{duration:.9f}", name], cwd=folder)
    base.unlink()


def montar(plan, target, progress=False):
    plano = json_file(plan)
    if not isinstance(plano, dict):
        raise ValueError("O plano deve ser um objeto JSON.")
    format_name = plano.get("formato", "vertical")
    dimensions = format_dimensions(format_name)
    args, filters, duration, body_duration = build_timeline(plano, plan.resolve().parent, dimensions)
    captions = plano.get("legenda_srt")
    social = plano.get("gerar_social", False)
    if type(social) is not bool or (social and not captions):
        raise ValueError("gerar_social deve ser booleano. A cópia social exige legenda_srt.")
    warnings = []
    target = target.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".montagem-", dir=target.parent) as temporary:
        work = Path(temporary)
        if captions:
            srt, warnings = check_srt(media_path(plan.resolve().parent, captions), body_duration)
            (work / "legendas.srt").write_text(srt, encoding="utf-8")
            run(["ffmpeg", "-v", "error", "-i", "legendas.srt", "legendas.vtt"], cwd=work)
        encode(args, filters, duration, work, "entrega.mp4", progress=progress)
        if social:
            style = ("FontName=Arial,FontSize=13,Alignment=2,MarginV=61,MarginL=18,MarginR=27,"
                     "PrimaryColour=&H00FFFFFF,OutlineColour=&H95182015,BorderStyle=3,Outline=1,Shadow=0")
            encode(args, filters, duration, work, "social.mp4", style, progress=progress)
        target.mkdir()
        for file in work.iterdir():
            file.replace(target / file.name)
    return {"pasta": str(target), "formato": format_name, "duracao_planejada_s": duration,
            "duracao_do_corpo_s": body_duration, "vinheta_anexada": duration > body_duration,
            "alertas_legenda": warnings, "status": "rascunho", "ok": True}


def validar(path, format_name="vertical"):
    width, height = format_dimensions(format_name)
    info = probe(path)
    video = stream(info, "video") or {}
    audio = stream(info, "audio") or {}
    duration = has_duration(info)
    issues = []
    if path.suffix.lower() != ".mp4" or "mp4" not in info["format"]["format_name"].split(","):
        issues.append("Container deve ser MP4.")
    if (video.get("width"), video.get("height"), video.get("codec_name"), video.get("pix_fmt")) != (
            width, height, "h264", "yuv420p"):
        issues.append(f"Vídeo deve ser H.264 yuv420p {width}×{height}.")
    if (video.get("avg_frame_rate") != "30/1" or video.get("r_frame_rate") != "30/1"
            or video.get("sample_aspect_ratio") != "1:1"):
        issues.append("Revise fps nominal/médio ou a proporção do pixel.")
    if any(video.get(key) != "bt709" for key in ("color_space", "color_transfer", "color_primaries")):
        issues.append("As etiquetas de cor devem indicar BT.709 SDR.")
    if duration > MAX_SECONDS:
        issues.append("Duração maior que 60 s.")
    if (audio.get("codec_name"), audio.get("channels"), audio.get("sample_rate")) != ("aac", 2, str(AUDIO_RATE)):
        issues.append("Áudio deve ser AAC estéreo a 48 kHz.")
    decode = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-xerror", "-i",
                  str(path.resolve()), "-map", "0:v:0?", "-map", "0:a:0?", "-f", "null", "-"])
    if decode.stderr.strip():
        issues.append("FFmpeg relatou erros ao decodificar o master.")
    loudness = peak = None
    if audio:
        loudness, peak = measure_audio(path)
        if loudness is None or not -17 <= loudness <= -15:
            issues.append("Loudness fora do alvo interno de −16 LUFS ±1.")
        if peak is None or peak > -1.5:
            issues.append("Pico verdadeiro indisponível ou acima de −1,5 dBTP.")
    return {"ok": not issues, "formato": format_name, "duracao_s": duration, "lufs": loudness, "dbtp": peak,
            "pendencias": issues, "revisao_cx": "pendente"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    for name in ("roteiro", "inspecionar", "montar", "validar"):
        command = commands.add_parser(name)
        command.add_argument("arquivo", type=Path)
        if name == "montar":
            command.add_argument("pasta_nova", type=Path)
            command.add_argument("--progresso", action="store_true", help="Eventos NDJSON em stderr.")
        if name == "validar":
            command.add_argument("--formato", choices=FORMATS, default="vertical")
        if name == "roteiro":
            command.add_argument("--perfil", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "montar":
            report = montar(args.arquivo, args.pasta_nova, args.progresso)
        elif args.command == "doctor":
            report = doctor()
        elif args.command == "roteiro":
            report = roteiro(args.arquivo, args.perfil)
        elif args.command == "validar":
            report = validar(args.arquivo, args.formato)
        else:
            report = inspect(args.arquivo)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report.get("ok", True) else 1
    except (ValueError, OSError, KeyError, TypeError) as error:
        if getattr(args, "progresso", False):
            print(json.dumps({"evento": "erro", "mensagem": str(error)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"Falha: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
