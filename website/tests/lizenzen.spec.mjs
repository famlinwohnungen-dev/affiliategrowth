/**
 * Urheberrechtliche Zusagen der Seite.
 *
 * Anlass: Die Schriften stehen unter der SIL Open Font License. Sie erlaubt
 * die kommerzielle Nutzung, verlangt aber, dass Copyright-Vermerk und
 * Lizenztext mitgeliefert werden. Selbsthosten ist Weitergabe — der Browser
 * laedt die Datei herunter. Der Lizenztext lag anfangs nicht im Repo.
 */
import { test, expect } from "@playwright/test";
import { readdir, readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const OEFFENTLICH = fileURLToPath(new URL("../public/", import.meta.url));

test("der OFL-Lizenztext wird mit ausgeliefert", async ({ request }) => {
  const antwort = await request.get("/fonts/OFL.txt");
  expect(antwort.status(), "OFL.txt muss erreichbar sein").toBe(200);
  const text = await antwort.text();
  expect(text).toContain("SIL OPEN FONT LICENSE Version 1.1");
  expect(text).toContain("PERMISSION & CONDITIONS");
});

test("jede Schriftfamilie ist mit Copyright verzeichnet", async () => {
  const hinweis = await readFile(new URL("../public/fonts/SCHRIFTEN.md", import.meta.url), "utf8");
  const dateien = await readdir(new URL("../public/fonts/", import.meta.url));

  const familien = new Set(
    dateien.filter((d) => d.endsWith(".woff2")).map((d) => d.split("-")[0]),
  );
  expect(familien.size, "es sollten Schriften vorhanden sein").toBeGreaterThan(0);

  // Dateiname und Fliesstext schreiben sich unterschiedlich ("IBMPlexMono"
  // gegen "IBM Plex Mono"). Verglichen wird deshalb ohne Leerzeichen.
  const flach = (x) => x.toLowerCase().replace(/[^a-z0-9]/g, "");
  const hinweisFlach = flach(hinweis);

  for (const familie of familien) {
    expect(
      hinweisFlach.includes(flach(familie)),
      `Schrift ${familie} fehlt in SCHRIFTEN.md`,
    ).toBe(true);
  }
});

/**
 * Bilder sind die haeufigste Quelle von Urheberrechts-Abmahnungen. Solange
 * die Seite keine hat, ist das Risiko null. Kommt eines dazu, soll dieser
 * Test auffallen und zur Herkunftsangabe zwingen — nicht das Bild verbieten.
 */
test("kein Bild ohne Herkunftsnachweis", async () => {
  const nachweis = await readFile(new URL("../public/BILDER.md", import.meta.url), "utf8").catch(
    () => "",
  );

  async function bilder(verzeichnis, praefix = "") {
    const eintraege = await readdir(verzeichnis, { withFileTypes: true });
    const treffer = [];
    for (const e of eintraege) {
      const pfad = `${praefix}${e.name}`;
      if (e.isDirectory()) treffer.push(...(await bilder(`${verzeichnis}${e.name}/`, `${pfad}/`)));
      else if (/\.(png|jpe?g|webp|avif|gif)$/i.test(e.name)) treffer.push(pfad);
    }
    return treffer;
  }

  const gefunden = await bilder(OEFFENTLICH);
  const ohneNachweis = gefunden.filter((b) => !nachweis.includes(b));
  expect(
    ohneNachweis,
    "Neue Bilder brauchen einen Eintrag in public/BILDER.md mit Quelle und Lizenz",
  ).toEqual([]);
});

/**
 * Selbst gehostete Schriften statt Google Fonts: Das LG Muenchen I sah 2022
 * in der Einbindung vom Google-Server einen Verstoss gegen das allgemeine
 * Persoenlichkeitsrecht (Az. 3 O 17493/20); es folgte eine Abmahnwelle.
 */
test("keine Schriften von fremden Servern", async ({ page }) => {
  const fremd = [];
  page.on("request", (r) => {
    const url = new URL(r.url());
    if (url.hostname !== "localhost" && /font|\.woff2?$/i.test(url.href)) fremd.push(r.url());
  });
  await page.goto("/");
  await page.goto("/artikel/g-data-vs-bitdefender/");
  expect(fremd, "Schrift von einem fremden Server geladen").toEqual([]);
});
