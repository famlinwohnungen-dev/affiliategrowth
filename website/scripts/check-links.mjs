/**
 * Prüft nach dem Build, ob jeder interne Link auf eine tatsächlich erzeugte
 * Datei zeigt.
 *
 * Anlass: Die Affiliate-Links zeigten auf `/go/<anbieter>/` mit Schrägstrich,
 * der Build erzeugte aber die Datei `/go/<anbieter>` ohne. Jeder einzelne
 * Affiliate-Link lief damit ins Leere — die Seite hätte nie etwas verdienen
 * können, und im Quelltext sah alles richtig aus.
 *
 * Läuft automatisch als `postbuild` und bricht mit Exit-Code 1 ab, damit ein
 * kaputter Link den Deploy stoppt statt still live zu gehen.
 */
import { readFileSync, existsSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { glob } from "node:fs/promises";

// Mit dem Cloudflare-Adapter liegen die statischen Dateien unter dist/client,
// ohne Adapter direkt unter dist. Beides unterstützen, statt einen Pfad zu raten.
const KANDIDATEN = [resolve("dist/client"), resolve("dist")];
const DIST = KANDIDATEN.find((k) => existsSync(k)) ?? KANDIDATEN[1];

const seiten = [];
for await (const datei of glob("**/*.html", { cwd: DIST })) seiten.push(datei);

/** Löst einen URL-Pfad auf die Datei auf, die der Hoster ausliefern würde. */
function aufloesbar(pfad) {
  const ohneQuery = pfad.split(/[?#]/)[0];
  const rel = decodeURIComponent(ohneQuery).replace(/^\//, "");
  const kandidaten = [
    join(DIST, rel),
    join(DIST, rel, "index.html"),
    join(DIST, `${rel}.html`),
  ];
  return kandidaten.some((k) => existsSync(k) && statSync(k).isFile());
}

// Serverseitige Routen erzeugen kein statisches File — sie werden zur
// Laufzeit beantwortet und dürfen nicht als toter Link gelten.
const LAUFZEIT_ROUTEN = [/^\/api\//];

const fehler = [];
const geprueft = new Set();

for (const seite of seiten) {
  const html = readFileSync(join(DIST, seite), "utf8");
  for (const treffer of html.matchAll(/(?:href|src)="(\/[^"]*)"/g)) {
    const ziel = treffer[1];
    const schluessel = `${seite} → ${ziel}`;
    if (geprueft.has(schluessel)) continue;
    geprueft.add(schluessel);
    if (LAUFZEIT_ROUTEN.some((r) => r.test(ziel))) continue;
    if (!aufloesbar(ziel)) fehler.push({ seite, ziel });
  }
}

if (fehler.length > 0) {
  console.error(`\n❌ ${fehler.length} interne(r) Link(s) ohne Ziel:\n`);
  for (const f of fehler) console.error(`   ${f.seite}\n     → ${f.ziel}`);
  console.error("");
  process.exit(1);
}

console.log(`✓ ${geprueft.size} interne Links geprüft, alle auflösbar`);
