/**
 * Statischer Server fuer dist/client — nur fuer die Tests.
 *
 * Warum nicht `wrangler dev`: Es braucht in der CI deutlich laenger, startet
 * unzuverlaessig und bringt fuer reine Oberflaechentests nichts dazu. Alle
 * geprueften Seiten sind vorgerendert; die einzige dynamische Route
 * (/api/feedback) wird hier nicht getestet.
 *
 * Bildet das Verhalten von Cloudflare Static Assets nach: /pfad/ liefert
 * /pfad/index.html, fehlende Dateien liefern 404 mit der 404-Seite.
 */
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize } from "node:path";

const WURZEL = new URL("../dist/client/", import.meta.url).pathname;
const PORT = Number(process.env.PORT ?? 4321);

const TYPEN = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".ico": "image/x-icon",
  ".png": "image/png",
  ".webp": "image/webp",
};

async function datei(pfad) {
  try {
    const s = await stat(pfad);
    if (s.isFile()) return await readFile(pfad);
  } catch {}
  return null;
}

createServer(async (req, res) => {
  const pfad = decodeURIComponent(new URL(req.url, "http://x").pathname);
  // normalize + Praefixpruefung: kein Ausbrechen aus dist/client via "..".
  const innen = normalize(join(WURZEL, pfad));
  if (!innen.startsWith(WURZEL)) {
    res.writeHead(403).end("Forbidden");
    return;
  }

  const kandidaten = pfad.endsWith("/")
    ? [join(innen, "index.html")]
    : [innen, innen + ".html", join(innen, "index.html")];

  for (const k of kandidaten) {
    const inhalt = await datei(k);
    if (inhalt) {
      res.writeHead(200, { "content-type": TYPEN[extname(k)] ?? "application/octet-stream" });
      res.end(inhalt);
      return;
    }
  }

  const vierNullVier = await datei(join(WURZEL, "404.html"));
  res.writeHead(404, { "content-type": "text/html; charset=utf-8" });
  res.end(vierNullVier ?? "404");
}).listen(PORT, () => console.log(`dist/client auf http://localhost:${PORT}`));
