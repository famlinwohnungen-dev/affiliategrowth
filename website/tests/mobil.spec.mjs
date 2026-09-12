/**
 * Regressionstests fuer alles, was auf Telefonen schon einmal kaputt war.
 *
 * Jeder Test nennt den Vorfall, aus dem er entstanden ist. Wer ihn spaeter
 * anfassen will, soll wissen, was er dabei aufgibt.
 */
import { test, expect } from "@playwright/test";
import { BREITEN, SEITEN, befunde } from "./pruefen.mjs";

for (const groesse of BREITEN) {
  test.describe(`Oberflaeche bei ${groesse.name}`, () => {
    test.use({ viewport: { width: groesse.width, height: groesse.height } });

    for (const pfad of SEITEN) {
      test(`${pfad} haelt die UI-Regeln ein`, async ({ page }) => {
        await page.goto(pfad);
        expect(await befunde(page), `Befunde auf ${pfad} bei ${groesse.width} px`).toEqual([]);
      });
    }
  });
}

test.describe("Vergleichstabelle", () => {
  const ARTIKEL = "/artikel/g-data-vs-bitdefender/";

  /**
   * Vorfall: Bei 375 px war die Tabelle 418 px breit in einem 327 px breiten
   * Container. 91 px lagen ausserhalb, darunter die Empfehlungsspalte. Das
   * alte Pruefskript schwieg, weil .scroller waagerecht scrollen darf.
   */
  test("versteckt auf dem Telefon nichts", async ({ page }) => {
    for (const w of [320, 360, 375, 414]) {
      await page.setViewportSize({ width: w, height: 800 });
      await page.goto(ARTIKEL);
      const versteckt = await page.evaluate(() => {
        const sc = document.querySelector(".scroller");
        return sc.scrollWidth - sc.clientWidth;
      });
      expect(versteckt, `verstecktes Stueck bei ${w} px`).toBe(0);
    }
  });

  test("stapelt auf dem Telefon und zeigt beide Produkte nebeneinander", async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 800 });
    await page.goto(ARTIKEL);
    const lage = await page.evaluate(() => {
      const zeile = document.querySelector(".scroller tbody tr");
      const [merkmal, ...werte] = [...zeile.children].map((c) => c.getBoundingClientRect());
      return {
        merkmalUeberWerten: merkmal.bottom <= werte[0].top + 1,
        werteNebeneinander: Math.abs(werte[0].top - werte[1].top) < 2,
        beideSichtbar: werte.every((r) => r.right <= innerWidth + 1),
      };
    });
    expect(lage).toEqual({
      merkmalUeberWerten: true,
      werteNebeneinander: true,
      beideSichtbar: true,
    });
  });

  test("Affiliate-Schaltflaechen stehen auf dem Telefon untereinander", async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 800 });
    await page.goto(ARTIKEL);
    const knoepfe = page.locator(".cta-zeile a");
    await expect(knoepfe).toHaveCount(2);
    const [a, b] = await knoepfe.evaluateAll((els) => els.map((e) => e.getBoundingClientRect()));
    expect(b.top, "zweiter Knopf steht unter dem ersten").toBeGreaterThan(a.bottom - 1);
    expect(a.width, "Knopf nutzt die volle Breite").toBeGreaterThan(200);
  });

  test("bleibt am Schreibtisch eine echte Tabelle", async ({ page }) => {
    await page.setViewportSize({ width: 1200, height: 900 });
    await page.goto(ARTIKEL);
    const zustand = await page.evaluate(() => {
      const t = document.querySelector(".scroller table");
      const a = [...t.querySelectorAll(".cta-zeile a")];
      return {
        anzeige: getComputedStyle(t).display,
        merkmalSpalte: getComputedStyle(t.querySelector("thead th")).display !== "none",
        knoepfeNebeneinander:
          Math.abs(a[0].getBoundingClientRect().top - a[1].getBoundingClientRect().top) < 5,
      };
    });
    expect(zustand).toEqual({
      anzeige: "table",
      merkmalSpalte: true,
      knoepfeNebeneinander: true,
    });
  });
});

test.describe("Kopfzeile", () => {
  /**
   * Vorfall: Auf dem Telefon stand nur noch das Schild, ohne "Schutzlotse".
   * Ursache war eine Regel aus der Zeit mit drei Navigationseintraegen, die
   * die Wortmarke unter 26 rem ausblendete. Ein Schild ohne Namen sagt einem
   * Leser nicht, auf welcher Seite er gelandet ist — und der Name ist das
   * Einzige, was er sich merken kann.
   */
  for (const w of [320, 360, 375, 414, 768]) {
    test(`der Seitenname steht bei ${w} px in der Kopfzeile`, async ({ page }) => {
      await page.setViewportSize({ width: w, height: 700 });
      await page.goto("/");
      const wort = page.locator(".brand .wort");
      await expect(wort, "Wortmarke fehlt").toBeVisible();
      await expect(wort).toHaveText("Schutzlotse");
    });
  }

  /**
   * Das Gegenstueck: Der Name darf nicht auf Kosten der Navigation stehen.
   * Bei 320 px bleiben zurzeit 21 px Luft zwischen Wortmarke und erstem
   * Navigationslink. Faellt dieser Test, ist die Kopfzeile zu voll geworden
   * — dann ist es Zeit fuer ein Klappmenue, nicht dafuer, den Namen wieder
   * auszublenden.
   */
  test("Name und Navigation passen bei 320 px nebeneinander", async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 700 });
    await page.goto("/");
    const lage = await page.evaluate(() => {
      const bar = document.querySelector(".bar");
      const brand = document.querySelector(".brand").getBoundingClientRect();
      const nav = document.querySelector("nav").getBoundingClientRect();
      return {
        ueberstand: bar.scrollWidth - bar.clientWidth,
        luecke: Math.round(nav.left - brand.right),
        eineZeile: Math.abs(brand.top - nav.top) < 24,
        navRechts: Math.round(nav.right),
        vw: innerWidth,
      };
    });
    expect(lage.ueberstand, "Kopfzeile laeuft ueber").toBe(0);
    expect(lage.luecke, "Wortmarke und Navigation kleben aneinander").toBeGreaterThanOrEqual(8);
    expect(lage.eineZeile, "Kopfzeile bricht um").toBe(true);
    expect(lage.navRechts).toBeLessThanOrEqual(lage.vw);
  });

  test("das Logo fuehrt zurueck zur Startseite", async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 700 });
    await page.goto("/artikel/g-data-vs-bitdefender/");
    await page.locator(".brand").click();
    await expect(page).toHaveURL(/\/$/);
  });
});

/**
 * Vorfall: Das Schaubild war ein SVG mit eingebauter Beschriftung. Bei 320 px
 * kam sie mit 9,1 px an. Die Pruefung steckt in befunde(), dieser Test haelt
 * zusaetzlich die Ursache fest, damit niemand Text ins SVG zurueckschiebt.
 */
test("Schaubild traegt keinen Text im SVG", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto("/");
  const svgTexte = await page.locator(".grafik svg text").count();
  expect(svgTexte, "Beschriftung gehoert als HTML neben das SVG, nicht hinein").toBe(0);
});
