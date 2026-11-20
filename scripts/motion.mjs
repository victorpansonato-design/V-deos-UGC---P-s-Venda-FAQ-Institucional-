import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { extname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const root = fileURLToPath(new URL("../", import.meta.url));
const [command, scene = "pratica", asset] = process.argv.slice(2);
if (!["check", "preview", "render"].includes(command) || !["pratica", "encerramento", "editorial", "ilustrado"].includes(scene)) {
  throw new Error("Escolha check, preview ou render e a cena pratica, editorial, ilustrado ou encerramento.");
}

const composition = join(root, "motion", scene);
const assets = join(composition, "assets");
const minimumVideoSeconds = { editorial: 9, ilustrado: 55 / 30 }[scene];
if (scene !== "encerramento") {
  if (minimumVideoSeconds) {
    if (extname(asset ?? "").toLowerCase() !== ".mp4") {
      throw new Error(`Informe um MP4 aprovado com ao menos ${minimumVideoSeconds.toFixed(2)} s de imagem.`);
    }
    const probe = spawnSync("ffprobe", ["-v", "error", "-select_streams", "v:0",
      "-show_entries", "stream=duration", "-of", "csv=p=0", resolve(asset)], { encoding: "utf8" });
    if (probe.error) throw new Error("Instale o FFmpeg com ffprobe no PATH para validar a mídia.");
    const seconds = Number(probe.stdout.trim());
    if (probe.status !== 0 || !Number.isFinite(seconds) || seconds < minimumVideoSeconds) {
      throw new Error("O trecho de campus está mais curto que a passagem da composição ou não é decodificável.");
    }
  }
  const fontDirectory = join(assets, "fonts");
  mkdirSync(fontDirectory, { recursive: true });
  copyFileSync(join(root, "node_modules", "@fontsource-variable", "inter", "files",
    "inter-latin-wght-normal.woff2"), join(fontDirectory, "inter.woff2"));
  if (minimumVideoSeconds) copyFileSync(resolve(asset), join(assets, "campus.mp4"));
} else {
  const suffix = extname(asset ?? "").toLowerCase();
  if (![".svg", ".png"].includes(suffix)) {
    throw new Error("Informe o SVG ou PNG transparente oficial aprovado para o encerramento.");
  }
  mkdirSync(assets, { recursive: true });
  const logo = join(assets, "logo-local.svg");
  if (suffix === ".svg") {
    copyFileSync(resolve(asset), logo);
  } else {
    const png = readFileSync(resolve(asset));
    if (png.length < 24 || png.subarray(0, 8).toString("hex") !== "89504e470d0a1a0a") {
      throw new Error("O arquivo informado não é um PNG válido.");
    }
    const width = png.readUInt32BE(16);
    const height = png.readUInt32BE(20);
    writeFileSync(logo, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}">
      <image width="${width}" height="${height}" href="data:image/png;base64,${png.toString("base64")}" />
    </svg>\n`);
  }
}

const output = join(root, "motion-" + scene + ".mp4");
const flags = command === "render" ? ["--output", output, "--quality", "delivery", "--workers", "2"] : [];
const cli = join(root, "node_modules", "hyperframes", "bin", "hyperframes.mjs");
const result = spawnSync(process.execPath, [cli, command, composition, ...flags], {
  cwd: root,
  env: { ...process.env, HYPERFRAMES_NO_TELEMETRY: "1" },
  stdio: "inherit",
});
if (result.error) throw result.error;
process.exitCode = result.status ?? 1;
