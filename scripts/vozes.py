"""Laboratório privado de voz. Execute com --help na raiz do repositório."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener
import wave

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "producoes" / "vozes"
MODELS = ROOT / "cache" / "chatterbox-br"
PROFILES = ("apresentadora", "apresentador")
SPACE = "ResembleAI/Chatterbox-Multilingual-TTS-pt-br"
SPACE_REV = "9e515821e826e207cd617a0fdd0223899ed108ea"
BR = "ResembleAI/Chatterbox-Multilingual-pt-br"
BR_REV = "b3952f18bc2eaa72b9bd7c17d2c4653bcad4770d"
BASE = "ResembleAI/chatterbox"
BASE_REV = "5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18"
WEIGHTS = {
    "ve.pt": (BASE, BASE_REV, "4b16d836bc598509860f6fa068165a8bb5e9ac84f05582dfcf278a5a372879f1"),
    "grapheme_mtl_merged_expanded_v1.json": (BR, BR_REV, "69632f47220a788a52ce2661d096453c5655e9bf25289d89a8d832c46ee07dbf"),
    "s3gen_v3.pt": (BR, BR_REV, "f7abce4b196dae2d08d9296cbebc6521b046079577643b42a19a03499d08721e"),
    "t3_pt_br.safetensors": (BR, BR_REV, "074aaf65255eb9cb960288f7cc72e09d3b5008f6e0b14868c0d4e5b0bd7cbb6c"),
}
ENDPOINT = "https://api.heygen.com/v3/models/audio/voices"


def owned_file(folder, name, suffix):
    if not name or Path(name).name != name or not name.lower().endswith(suffix):
        raise ValueError(f"Use somente um nome de arquivo {suffix} dentro da pasta de vozes.")
    result = (folder / name).resolve()
    if result.parent != folder.resolve():
        raise ValueError("O arquivo precisa permanecer na pasta privada.")
    return result


def save_json(path, data):
    with path.open("x", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)
        output.write("\n")


def init_profiles(folder):
    folder.mkdir(parents=True, exist_ok=True)
    profiles = {name: {"referencia": f"{name}.mp3", "clonagem_local_autorizada": False}
                for name in PROFILES}
    path = folder / "perfis.json"
    if not path.exists():
        save_json(path, profiles)
    return path


def reference_file(folder, profile):
    with (folder / "perfis.json").open(encoding="utf-8-sig") as source:
        data = json.load(source)
    item = data.get(profile, {})
    if item.get("clonagem_local_autorizada") is not True:
        raise ValueError("Registre a autorização de clonagem local da pessoa antes de sintetizar.")
    path = owned_file(folder, item.get("referencia", ""), (".mp3", ".wav"))
    if not path.is_file():
        raise ValueError(f"Coloque a referência de {profile} na pasta privada.")
    return path


def hash_file(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def verify_weights():
    for name, (_, _, digest) in WEIGHTS.items():
        path = MODELS / "pesos" / name
        if not path.is_file() or hash_file(path) != digest:
            raise ValueError(f"Peso ausente ou divergente ({name}). Rode preparar-modelo.")


def prepare():
    from huggingface_hub import hf_hub_download, snapshot_download

    snapshot_download(repo_id=SPACE, repo_type="space", revision=SPACE_REV,
                      allow_patterns=["chatterbox/*"], local_dir=str(MODELS / "fonte"))
    for name, (repo, revision, _) in WEIGHTS.items():
        hf_hub_download(repo_id=repo, filename=name, revision=revision,
                        local_dir=str(MODELS / "pesos"))
    verify_weights()


def synthesize(profile, input_name, output_name, device):
    ref = reference_file(PRIVATE, profile)
    transcript = owned_file(PRIVATE, input_name, ".txt").read_text(encoding="utf-8-sig").strip()
    if not 1 <= len(transcript) <= 300:
        raise ValueError("Para a audição, escreva de 1 a 300 caracteres por tomada.")
    out = owned_file(PRIVATE, output_name, ".wav")
    if out.exists():
        raise ValueError("A saída já existe. Escolha uma nova versão.")
    source_root = MODELS / "fonte" / "chatterbox" / "src"
    if not (source_root / "chatterbox" / "tts.py").is_file():
        raise ValueError("Rode preparar-modelo para instalar o motor regional.")
    verify_weights()
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    sys.path.insert(0, str(source_root))
    import torch
    import soundfile
    from chatterbox.tts import ChatterboxTTS

    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda" and not torch.cuda.is_available():
        raise ValueError("CUDA indisponível. Use --dispositivo cpu ou corrija o PyTorch.")
    # Use a tomada privada como única condição. O diretório contém apenas ativos oficiais.
    model = ChatterboxTTS.from_local(MODELS / "pesos", device,
                                     t3_filename="t3_pt_br.safetensors", s3gen_filename="s3gen_v3.pt")
    with TemporaryDirectory(dir=PRIVATE) as temp:
        wavref = Path(temp) / "referencia.wav"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(ref), "-map", "0:a:0",
                        "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", str(wavref)], check=True)
        with torch.inference_mode():
            audio = model.generate(transcript, language_id="pt", audio_prompt_path=str(wavref))
        rendered = Path(temp) / "take.wav"
        soundfile.write(str(rendered), audio.detach().cpu().numpy().reshape(-1), model.sr, subtype="PCM_16")
        with wave.open(str(rendered), "rb") as read:
            if read.getnframes() == 0:
                raise ValueError("O motor devolveu áudio vazio.")
        with out.open("xb") as final, rendered.open("rb") as original:
            shutil.copyfileobj(original, final)
    return out


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("A API redirecionou. Confira a documentação antes de prosseguir.")


def inventory(kind, key, fetch=None):
    if not key:
        raise ValueError("Defina HEYGEN_API_KEY na sessão local para consultar a conta.")
    fetch = fetch or build_opener(NoRedirect()).open
    params = {"type": kind, "limit": 50}
    seen, items = set(), {}
    while True:
        req = Request(f"{ENDPOINT}?{urlencode(params)}", headers={"x-api-key": key})
        with fetch(req, timeout=30) as response:
            page = json.load(response)
        if not isinstance(page.get("data"), list) or type(page.get("has_more")) is not bool:
            raise ValueError("Formato de catálogo inesperado. Confira a API.")
        for voice in page["data"]:
            row = {k: voice.get(k) for k in ("voice_id", "name", "language", "gender", "status",
                                             "mode", "preview_audio_url", "locale", "accent")}
            if not row["voice_id"]:
                raise ValueError("Resposta sem identificador de voz.")
            tags = {str(row[k] or "").strip().lower().replace("_", "-") for k in ("language", "locale", "accent")}
            brazil = bool(tags & {"pt-br", "portuguese (brazil)", "brazilian portuguese", "brazilian"})
            portuguese = bool(tags & {"pt", "portuguese", "português"})
            row["triagem"] = "brasil_declarado" if brazil else "portugues_para_ouvir" if portuguese else "outras_ou_sem_regiao"
            items[row["voice_id"]] = row
        if not page["has_more"]:
            return list(items.values())
        cursor = page.get("next_token")
        if not isinstance(cursor, str) or not cursor or cursor in seen:
            raise ValueError("Paginação incompleta na API. Nenhum catálogo foi gravado.")
        seen.add(cursor)
        params["token"] = cursor


def main():
    options = argparse.ArgumentParser(description=__doc__)
    sub = options.add_subparsers(dest="command", required=True)
    sub.add_parser("iniciar", help="Criar manifesto privado com dois perfis.")
    sub.add_parser("preparar-modelo", help="Baixar código e pesos públicos identificados por revisão.")
    take = sub.add_parser("sintetizar", help="Produzir WAV local de uma tomada para audição.")
    take.add_argument("perfil", choices=PROFILES)
    take.add_argument("texto", help="Nome de um TXT na pasta privada.")
    take.add_argument("saida", help="Nome novo do WAV na mesma pasta.")
    take.add_argument("--dispositivo", choices=("auto", "cpu", "cuda"), default="auto")
    cat = sub.add_parser("catalogo-heygen", help="Consultar todas as páginas sem gerar áudio.")
    cat.add_argument("--tipo", choices=("public", "private"), default="public")
    cat.add_argument("--saida", default="catalogo-publico.json")
    args = options.parse_args()
    if args.command == "iniciar":
        print(init_profiles(PRIVATE))
    elif args.command == "preparar-modelo":
        prepare()
        print("Código baixado e quatro arquivos do modelo verificados.")
    elif args.command == "sintetizar":
        print(synthesize(args.perfil, args.texto, args.saida, args.dispositivo))
    else:
        PRIVATE.mkdir(parents=True, exist_ok=True)
        path = owned_file(PRIVATE, args.saida, ".json")
        if path.exists():
            raise ValueError("Use --saida com um nome novo.")
        rows = inventory(args.tipo, os.getenv("HEYGEN_API_KEY"))
        save_json(path, {"consultado_em_utc": datetime.now(timezone.utc).isoformat(),
                         "tipo": args.tipo, "total": len(rows), "vozes": rows})
        print(f"{len(rows)} vozes salvas em {path}")


if __name__ == "__main__":
    try:
        main()
    except HTTPError as error:
        sys.exit(f"HeyGen HTTP {error.code}. Verifique a chave, o limite e a disponibilidade.")
    except (ImportError, OSError, RuntimeError, ValueError, URLError, subprocess.SubprocessError) as error:
        sys.exit(f"Vozes: {error}")
