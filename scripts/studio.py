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
WIDTH, HEIGHT, FPS = 1080, 1920, 30
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


def build_timeline(plano, folder):
    clips = plano.get("clipes")
    if not isinstance(clips, list) or not 1 <= len(clips) <= 20:
        raise ValueError("O plano deve ter de 1 a 20 clipes.")
    args, filters, inputs = [], [], []
    audio_final = plano.get("audio_final")
    total_frames = 0
    for index, clip in enumerate(clips):
        if not isinstance(clip, dict):
            raise ValueError(f"Clipe {index + 1} deve ser um objeto.")
        source = media_path(folder, clip.get("arquivo"))
        info = probe(source)
        video = stream(info, "video")
        if not video or video.get("color_transfer") in HDR_TRANSFERS:
            raise ValueError(f"Use um intermediário de vídeo SDR: {source.name}")
        if video.get("sample_aspect_ratio") not in (None, "0:1", "1:1", "N/A"):
            raise ValueError(f"Normalize a proporção do pixel antes de usar {source.name}.")
        duration = has_duration(info)
        start = bounded_number(clip.get("inicio"), "inicio", 0, duration)
        end = bounded_number(clip.get("fim"), "fim", start, duration)
        frames = round((end - start) * FPS)
        if frames < 1:
            raise ValueError(f"Clipe {index + 1} tem menos de um quadro.")
        length = f"{frames / FPS:.9f}"
        total_frames += frames
        framing = clip.get("quadro", "conter")
        if framing not in ("conter", "preencher"):
            raise ValueError("quadro deve ser conter ou preencher.")
        if type(clip.get("mutar", False)) is not bool:
            raise ValueError("mutar deve ser true ou false.")
        focus_x = bounded_number(clip.get("foco_x", 0.5), "foco_x", 0, 1)
        focus_y = bounded_number(clip.get("foco_y", 0.5), "foco_y", 0, 1)
        resize = f"scale={WIDTH}:{HEIGHT}:flags=lanczos:"
        if framing == "conter":
            frame_filter = (resize + "force_original_aspect_ratio=decrease:force_divisible_by=2,"
                            f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2:color=0x071f3e")
        else:
            frame_filter = (resize + "force_original_aspect_ratio=increase:force_divisible_by=2,"
                            f"crop={WIDTH}:{HEIGHT}:(iw-ow)*{focus_x}:(ih-oh)*{focus_y}")
        known_color = all(video.get(key) not in (None, "unknown", "unspecified")
                          for key in ("color_space", "color_transfer", "color_primaries"))
        color = "colorspace=all=bt709:range=tv"
        if not known_color:
            color += ":iall=bt709"
        args.extend(["-ss", str(start), "-i", str(source)])
        filters.append(f"[{index}:v:0]setpts=PTS-STARTPTS,fps={FPS},{frame_filter},"
                       f"setsar=1,format=yuv420p,{color},tpad=stop_mode=clone:stop_duration=0.1,"
                       f"trim=duration={length}[v{index}]")
        inputs.append(f"[v{index}]")
        if not audio_final:
            if stream(info, "audio") and not clip.get("mutar", False):
                filters.append(f"[{index}:a:0]asetpts=PTS-STARTPTS,aresample=48000,"
                               f"aformat=channel_layouts=stereo,apad,atrim=duration={length}[a{index}]")
            else:
                filters.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={length}[a{index}]")
            inputs.append(f"[a{index}]")
    duration = total_frames / FPS
    if duration > MAX_SECONDS:
        raise ValueError(f"Monte até {MAX_SECONDS} segundos. O plano ficou com {duration:.3f} s.")
    if audio_final:
        soundtrack = media_path(folder, audio_final)
        source_info = probe(soundtrack)
        if not stream(source_info, "audio") or abs(has_duration(source_info) - duration) > 0.25:
            raise ValueError("O áudio final deve acompanhar a duração do plano (tolerância: 0,25 s).")
        args.extend(["-i", str(soundtrack)])
        filters.append("".join(inputs) + f"concat=n={len(clips)}:v=1:a=0[video]")
        filters.append(f"[{len(clips)}:a:0]asetpts=PTS-STARTPTS,apad,"
                       f"atrim=duration={duration:.9f}[audio]")
    else:
        filters.append("".join(inputs) + f"concat=n={len(clips)}:v=1:a=1[video][audio]")
    filters.append("[audio]loudnorm=I=-16:TP=-2:LRA=7,aresample=48000[master_audio]")
    return args, filters, duration


def encode(args, filters, duration, folder, name, caption_style=None):
    filters = list(filters)
    output = "[video]"
    if caption_style:
        filters.append(f"[video]subtitles=legendas.srt:force_style='{caption_style}'[com_legenda]")
        output = "[com_legenda]"
    run(["ffmpeg", "-hide_banner", "-v", "error", "-nostdin", "-filter_complex_threads", "2",
         *args, "-filter_complex", ";".join(filters), "-map", output, "-map", "[master_audio]",
         "-r", str(FPS), "-c:v", "libx264", "-threads", "4", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
         "-color_trc", "bt709", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2",
         "-map_metadata", "-1", "-map_chapters", "-1", "-movflags", "+faststart",
         "-t", f"{duration:.9f}", name], cwd=folder)


def montar(plan, target):
    plano = json_file(plan)
    if not isinstance(plano, dict):
        raise ValueError("O plano deve ser um objeto JSON.")
    args, filters, duration = build_timeline(plano, plan.resolve().parent)
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
            srt, warnings = check_srt(media_path(plan.resolve().parent, captions), duration)
            (work / "legendas.srt").write_text(srt, encoding="utf-8")
            run(["ffmpeg", "-v", "error", "-i", "legendas.srt", "legendas.vtt"], cwd=work)
        encode(args, filters, duration, work, "entrega.mp4")
        if social:
            style = ("FontName=Arial,FontSize=13,Alignment=2,MarginV=61,MarginL=18,MarginR=27,"
                     "PrimaryColour=&H00FFFFFF,OutlineColour=&H95182015,BorderStyle=3,Outline=1,Shadow=0")
            encode(args, filters, duration, work, "social.mp4", style)
        target.mkdir()
        for file in work.iterdir():
            file.replace(target / file.name)
    return {"pasta": str(target), "duracao_planejada_s": duration,
            "alertas_legenda": warnings, "status": "rascunho", "ok": True}


def validar(path):
    info = probe(path)
    video = stream(info, "video") or {}
    audio = stream(info, "audio") or {}
    duration = has_duration(info)
    issues = []
    if path.suffix.lower() != ".mp4" or "mp4" not in info["format"]["format_name"].split(","):
        issues.append("Container deve ser MP4.")
    if (video.get("width"), video.get("height"), video.get("codec_name"), video.get("pix_fmt")) != (
            WIDTH, HEIGHT, "h264", "yuv420p"):
        issues.append("Vídeo deve ser H.264 yuv420p 1080×1920.")
    if (video.get("avg_frame_rate") != "30/1" or video.get("r_frame_rate") != "30/1"
            or video.get("sample_aspect_ratio") != "1:1"):
        issues.append("Revise fps nominal/médio ou a proporção do pixel.")
    if any(video.get(key) != "bt709" for key in ("color_space", "color_transfer", "color_primaries")):
        issues.append("As etiquetas de cor devem indicar BT.709 SDR.")
    if duration > MAX_SECONDS:
        issues.append("Duração maior que 60 s.")
    if (audio.get("codec_name"), audio.get("channels"), audio.get("sample_rate")) != ("aac", 2, "48000"):
        issues.append("Áudio deve ser AAC estéreo a 48 kHz.")
    decode = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-xerror", "-i",
                  str(path.resolve()), "-map", "0:v:0?", "-map", "0:a:0?", "-f", "null", "-"])
    if decode.stderr.strip():
        issues.append("FFmpeg relatou erros ao decodificar o master.")
    loudness = peak = None
    if audio:
        measured = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path.resolve()),
                        "-map", "0:a:0", "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
        summary = measured.stderr.rsplit("Summary:", 1)[-1]
        integrated = re.search(r"\bI:\s*(-?[\d.]+)\s*LUFS", summary)
        true_peak = re.search(r"True peak:\s*Peak:\s*(-?[\d.]+)\s*dBFS", summary)
        loudness = float(integrated[1]) if integrated else None
        peak = float(true_peak[1]) if true_peak else None
        if loudness is None or not -17 <= loudness <= -15:
            issues.append("Loudness fora do alvo interno de −16 LUFS ±1.")
        if peak is None or peak > -1.5:
            issues.append("Pico verdadeiro indisponível ou acima de −1,5 dBTP.")
    return {"ok": not issues, "duracao_s": duration, "lufs": loudness, "dbtp": peak,
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
        if name == "roteiro":
            command.add_argument("--perfil", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "montar":
            report = montar(args.arquivo, args.pasta_nova)
        elif args.command == "doctor":
            report = doctor()
        elif args.command == "roteiro":
            report = roteiro(args.arquivo, args.perfil)
        else:
            functions = {"inspecionar": inspect, "validar": validar}
            report = functions[args.command](args.arquivo)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report.get("ok", True) else 1
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Falha: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
