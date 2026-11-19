import array
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

STUDIO = Path(__file__).resolve().parents[1] / "scripts" / "studio.py"


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg ausente")
class StudioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="teste estúdio ")
        cls.addClassCleanup(cls.directory.cleanup)
        cls.folder = Path(cls.directory.name)
        cls.media("bruto.mp4", "blue", "160x284", 440, "3")
        cls.media("final.mp4", "green", "320x180", 660, "0.4")
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=f=880:d=3",
             str(cls.folder / "locução.mp3")], check=True, capture_output=True,
        )

    @classmethod
    def media(cls, name, color, dimensions, frequency, duration):
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", f"color={color}:s={dimensions}:r=25:d={duration}",
             "-f", "lavfi", "-i", f"sine=f={frequency}:d={duration}", "-c:v", "libx264",
             "-c:a", "aac", "-shortest", str(cls.folder / name)], check=True, capture_output=True,
        )

    def montar(self, project, name, progress=False):
        project.setdefault("clipes", [{"arquivo": "bruto.mp4", "inicio": 0, "fim": 3}])
        plan = self.folder / f"{name}.json"
        plan.write_text(json.dumps(project, ensure_ascii=False), encoding="utf-8")
        destination = self.folder / name
        command = self.command("montar", plan, destination, *(["--progresso"] if progress else []))
        return command, destination / "entrega.mp4"

    def command(self, *args):
        return subprocess.run(
            [sys.executable, str(STUDIO), *map(str, args)], capture_output=True, text=True,
            encoding="utf-8", timeout=60,
        )

    def frequency(self, path, time):
        result = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", str(time), "-i", str(path), "-t", "0.12",
             "-map", "0:a", "-ac", "1", "-ar", "48000", "-f", "s16le", "-"],
            capture_output=True, check=True,
        )
        samples = array.array("h", result.stdout)
        if sys.byteorder == "big":
            samples.byteswap()
        return sum(before < 0 <= after for before, after in zip(samples, samples[1:])) * 8.333

    def test_horizontal_voice_window_outro_and_progress(self):
        project = {
            "formato": "horizontal", "vinheta": "final.mp4",
            "locucao": {"arquivo": "locução.mp3", "inicio": 1, "fim": 2,
                        "inicio_arquivo": 0.25, "uso": "narracao_fora_de_quadro"},
        }
        process, output = self.montar(project, "horizontal", progress=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        report = json.loads(process.stdout)
        self.assertEqual(report["duracao_do_corpo_s"], 3)
        self.assertAlmostEqual(report["duracao_planejada_s"], 3.4)
        self.assertTrue(report["vinheta_anexada"])
        progress = [json.loads(line) for line in process.stderr.splitlines()]
        self.assertEqual(progress[-1]["estado"], "end")
        self.assertEqual(progress[-1]["frame"], 102)
        self.assertGreater(progress[-1]["segundos_processados"], 3)
        qa = self.command("validar", output, "--formato", "horizontal")
        self.assertEqual(qa.returncode, 0, qa.stdout + qa.stderr)
        for time, expected in [(0.4, 440), (1.4, 880), (2.4, 440), (3.1, 660)]:
            with self.subTest(time=time):
                self.assertAlmostEqual(self.frequency(output, time), expected, delta=12)

    def test_legacy_vertical_full_mix(self):
        process, output = self.montar({"audio_final": "locução.mp3"}, "vertical")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stderr, "")
        self.assertEqual(json.loads(process.stdout)["formato"], "vertical")
        self.assertAlmostEqual(self.frequency(output, 1), 880, delta=12)
        qa = self.command("validar", output)
        self.assertEqual(qa.returncode, 0, qa.stdout + qa.stderr)

    def test_incompatible_outro_stops_before_encoding(self):
        process, output = self.montar({"vinheta": "final.mp4"}, "incompatible", progress=True)
        self.assertEqual(process.returncode, 1)
        self.assertIn("proporção", json.loads(process.stderr)["mensagem"])
        self.assertFalse(output.exists())

    def test_lip_sync_claim_requires_review_and_can_replace_all_audio(self):
        narration = {"arquivo": "locução.mp3", "inicio": 0, "fim": 3, "uso": "mesmo_audio_lipsync"}
        process, output = self.montar({"locucao": narration}, "pending")
        self.assertEqual(process.returncode, 1)
        self.assertIn("sincronia_revisada", process.stderr)
        self.assertFalse(output.exists())

        narration["sincronia_revisada"] = True
        process, output = self.montar({"locucao": narration}, "confirmed")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertAlmostEqual(self.frequency(output, 1), 880, delta=12)


if __name__ == "__main__":
    unittest.main()
