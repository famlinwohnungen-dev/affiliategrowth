/**
 * Tests fuer inhaltliche und rechtliche Zusagen.
 *
 * Diese Regeln sind nicht Geschmack, sondern Entscheidungen mit Begruendung
 * (STATUS.md). Ein Test verhindert, dass sie beim naechsten Umbau still
 * verlorengehen.
 */
import { test, expect } from "@playwright/test";
import { SEITEN } from "./pruefen.mjs";

const HAENDLER = ["eset", "bitdefender", "gdata", "kaspersky"];

/**
 * Vorfall: Alle Affiliate-Links waren tot. Die Links zeigten auf /go/x/ mit
 * Schraegstrich, gebaut wurde eine Datei /go/x ohne. Getestet worden war der
 * Endpunkt, nicht der Link — der Unterschied kostete jeden Klick.
 */
test.describe("Affiliate-Weiterleitungen", () => {
  for (const key of HAENDLER) {
    test(`/go/${key}/ ist erreichbar`, async ({ request }) => {
      const antwort = await request.get(`/go/${key}/`);
      expect(antwort.status(), `/go/${key}/ muss ausgeliefert werden`).toBe(200);
    });
  }

  test("jeder Affiliate-Link auf der Seite loest auf", async ({ page, request }) => {
    const gesehen = new Set();
    for (const pfad of SEITEN) {
      await page.goto(pfad);
      const ziele = await page.locator('a[href^="/go/"]').evaluateAll((els) =>
        els.map((e) => e.getAttribute("href")),
      );
      for (const ziel of ziele) gesehen.add(ziel);
    }
    expect(gesehen.size, "es sollte Affiliate-Links geben").toBeGreaterThan(0);
    for (const ziel of gesehen) {
      const antwort = await request.get(ziel);
      expect(antwort.status(), `toter Affiliate-Link: ${ziel}`).toBe(200);
    }
  });
});

/**
 * § 5a Abs. 4 UWG: Werbung muss am Ort der Werbung erkennbar sein. Ein
 * Hinweis, der erst nach einem Klick sichtbar wird, genuegt nicht.
 */
test.describe("Werbekennzeichnung", () => {
  test("jeder Affiliate-Link traegt ein Sternchen", async ({ page }) => {
    await page.goto("/artikel/g-data-vs-bitdefender/");
    const ohneStern = await page.locator('a[href^="/go/"]').evaluateAll((els) =>
      els.filter((e) => !e.textContent.includes("*")).map((e) => e.getAttribute("href")),
    );
    expect(ohneStern, "Affiliate-Link ohne Kennzeichnung").toEqual([]);
  });

  test("die Aufloesung des Sternchens steht auf jeder Seite", async ({ page }) => {
    for (const pfad of SEITEN) {
      await page.goto(pfad);
      await expect(page.locator(".stern-hinweis"), `Fusszeilen-Hinweis fehlt auf ${pfad}`).toContainText(
        "Affiliate-Link",
      );
    }
  });

  test("Affiliate-Links sind als sponsored nofollow markiert", async ({ page }) => {
    await page.goto("/anbieter/");
    const falsch = await page.locator('a[href^="/go/"]').evaluateAll((els) =>
      els
        .filter((e) => {
          const rel = e.getAttribute("rel") ?? "";
          return !rel.includes("sponsored") || !rel.includes("nofollow");
        })
        .map((e) => e.getAttribute("href")),
    );
    expect(falsch).toEqual([]);
  });
});

/**
 * Entscheidung: Die Startseite bleibt frei von Partnerlinks. Eine Startseite
 * voller Affiliate-Links ohne Inhalt ist genau das, was Google als "thin
 * affiliate page" abwertet.
 */
test("die Startseite enthaelt keine Affiliate-Links", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator('a[href^="/go/"]')).toHaveCount(0);
});

/**
 * Entscheidung: kein Affiliate-Link zu Kaspersky. Die BSI-Warnung soll
 * glaubwuerdig bleiben, und der EPC war ohnehin der niedrigste.
 */
test("Kaspersky wird nirgends verlinkt", async ({ page }) => {
  for (const pfad of SEITEN) {
    await page.goto(pfad);
    await expect(
      page.locator('a[href^="/go/kaspersky"]'),
      `Kaspersky-Link auf ${pfad}`,
    ).toHaveCount(0);
  }
});

/**
 * Entscheidung: keine Messwerte aus fremden Tests, solange keine Erlaubnis
 * vorliegt. AV-Comparatives verlangt vorherige schriftliche Zustimmung.
 */
test("keine fremden Testzahlen im Text", async ({ page }) => {
  const verdaechtig = /\b9\d[.,]\d+\s*%|\bProzentpunkt/;
  for (const pfad of SEITEN) {
    await page.goto(pfad);
    const text = await page.locator("body").innerText();
    const treffer = text.match(verdaechtig);
    expect(treffer, `moegliche fremde Testzahl auf ${pfad}: ${treffer?.[0]}`).toBeNull();
  }
});

/** § 5 DDG und Art. 13 DSGVO: beides muss von jeder Seite aus erreichbar sein. */
test("Impressum und Datenschutz sind von jeder Seite erreichbar", async ({ page }) => {
  for (const pfad of SEITEN) {
    await page.goto(pfad);
    await expect(page.locator('a[href="/impressum/"]').first(), `Impressum fehlt auf ${pfad}`).toHaveCount(1);
    await expect(
      page.locator('a[href="/datenschutz/"]').first(),
      `Datenschutz fehlt auf ${pfad}`,
    ).toHaveCount(1);
  }
});

/**
 * Solange SITE.indexable false ist, darf keine Seite indexierbar sein — sonst
 * landet ein Platzhalter-Impressum bei Google, und das ist abmahnfaehig.
 */
test("noindex greift, solange die Seite nicht freigegeben ist", async ({ page, request }) => {
  const robots = await (await request.get("/robots.txt")).text();
  const gesperrt = robots.includes("Disallow: /");
  if (!gesperrt) test.skip(true, "Seite ist freigegeben, noindex entfaellt");

  for (const pfad of SEITEN) {
    await page.goto(pfad);
    await expect(
      page.locator('meta[name="robots"][content*="noindex"]'),
      `noindex fehlt auf ${pfad}`,
    ).toHaveCount(1);
  }
});
