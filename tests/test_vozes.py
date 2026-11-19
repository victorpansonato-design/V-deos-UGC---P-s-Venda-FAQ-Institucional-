import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock
from urllib.parse import parse_qs, urlparse

from scripts import vozes


class Catalogo(unittest.TestCase):
    def test_todas_as_paginas_com_filtro_local(self):
        replies = [
            {"data": [{"voice_id": "a", "language": "pt"}], "has_more": True, "next_token": "x/y="},
            {"data": [{"voice_id": "b", "language": "pt-BR"}, {"voice_id": "c", "language": "pt-PT"}],
             "has_more": False, "next_token": None},
        ]
        fetch = Mock(side_effect=[io.BytesIO(json.dumps(p).encode()) for p in replies])
        rows = vozes.inventory("public", "chave-de-teste", fetch)
        self.assertEqual([r["triagem"] for r in rows],
                         ["portugues_para_ouvir", "brasil_declarado", "outras_ou_sem_regiao"])
        query = parse_qs(urlparse(fetch.call_args_list[1].args[0].full_url).query)
        self.assertEqual(query, {"type": ["public"], "limit": ["50"], "token": ["x/y="]})

    def test_paginacao_incompleta_e_erro(self):
        page = {"data": [], "has_more": True, "next_token": "x"}
        fetch = lambda req, timeout: io.BytesIO(json.dumps(page).encode())
        with self.assertRaisesRegex(ValueError, "Paginação"):
            vozes.inventory("public", "teste", fetch)

    def test_sem_chave_sem_requisicao(self):
        fetch = Mock()
        with self.assertRaises(ValueError):
            vozes.inventory("private", "", fetch)
        fetch.assert_not_called()


class Perfis(unittest.TestCase):
    def test_autorizacao_por_pessoa_e_inicio_idempotente(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            path = vozes.init_profiles(folder)
            profiles = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(set(profiles), set(vozes.PROFILES))
            (folder / "apresentadora.mp3").touch()
            with self.assertRaisesRegex(ValueError, "autorização"):
                vozes.reference_file(folder, "apresentadora")
            profiles["apresentadora"]["clonagem_local_autorizada"] = True
            path.write_text(json.dumps(profiles), encoding="utf-8")
            vozes.init_profiles(folder)
            self.assertEqual(vozes.reference_file(folder, "apresentadora"), folder / "apresentadora.mp3")
            with self.assertRaisesRegex(ValueError, "autorização"):
                vozes.reference_file(folder, "apresentador")

    def test_rejeita_caminho_externo(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                vozes.owned_file(Path(temp), "../mensagem.wav", ".wav")

    def test_texto_nao_pode_sobrescrever_referencia(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "perfis.json"
            vozes.save_json(path, {"origem": 1})
            with self.assertRaises(FileExistsError):
                vozes.save_json(path, {"origem": 2})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"origem": 1})


if __name__ == "__main__":
    unittest.main()
