/**
 * Die Entscheidungshilfe auf der Startseite.
 *
 * Wichtigster Punkt: Sie darf nie ins Leere zeigen. Ihre Ziele haengen davon
 * ab, welche Artikel veroeffentlicht sind — genau die Art von Verknuepfung,
 * die still bricht, wenn ein Artikel auf draft gesetzt wird.
 */
import { test, expect } from "@playwright/test";

const ZWEIGE = [
  { geraete: "ein", systeme: "windows", anlass: "neu" },
  { geraete: "wenige", systeme: "windows", anlass: "verlaengerung" },
  { geraete: "wenige", systeme: "gemischt", anlass: "neu" },
  { geraete: "viele", systeme: "windows", anlass: "neu" },
  { geraete: "wenige", systeme: "windows", anlass: "erstmals" },
];

async function antworten(page, wahl) {
  for (const [frage, wert] of Object.entries(wahl)) {
    await page.locator(`input[name="${frage}"][value="${wert}"]`).check();
  }
}

test("zeigt kein Ergebnis, bevor alle drei Fragen beantwortet sind", async ({ page }) => {
  await page.goto("/");
  const ergebnis = page.locator("#hilfe-ergebnis");
  await expect(ergebnis).toBeHidden();

  await page.locator('input[name="geraete"][value="ein"]').check();
  await expect(ergebnis, "ein Ergebnis nach einer Antwort waere geraten").toBeHidden();

  await page.locator('input[name="systeme"][value="windows"]').check();
  await expect(ergebnis).toBeHidden();

  await page.locator('input[name="anlass"][value="neu"]').check();
  await expect(ergebnis).toBeVisible();
});

for (const wahl of ZWEIGE) {
  const name = Object.values(wahl).join(" / ");
  test(`Zweig ${name} fuehrt auf eine erreichbare Seite`, async ({ page, request }) => {
    await page.goto("/");
    await antworten(page, wahl);

    const ergebnis = page.locator("#hilfe-ergebnis");
    await expect(ergebnis).toBeVisible();
    await expect(ergebnis.locator("h3")).not.toBeEmpty();
    await expect(ergebnis.locator("p")).not.toBeEmpty();

    const ziel = await ergebnis.locator("a.weiter").getAttribute("href");
    expect(ziel, "Ziel muss ein interner Pfad sein").toMatch(/^\//);
    const antwort = await request.get(ziel);
    expect(antwort.status(), `Zweig ${name} zeigt auf ${ziel}`).toBe(200);
  });
}

/**
 * Entscheidung: Das Ergebnis nennt ein Kriterium, kein Produkt. Eine
 * Produktempfehlung nach drei Klicks waere nicht belegbar — und die
 * Startseite bleibt ohnehin frei von Partnerlinks.
 */
test("das Ergebnis verlinkt nie auf einen Partnerlink", async ({ page }) => {
  await page.goto("/");
  for (const wahl of ZWEIGE) {
    await antworten(page, wahl);
    const ziel = await page.locator("#hilfe-ergebnis a.weiter").getAttribute("href");
    expect(ziel, `Partnerlink im Ergebnis: ${ziel}`).not.toContain("/go/");
  }
});

test("laesst sich auf dem Telefon bedienen", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto("/");
  const zuKlein = await page.locator("#hilfe-form label").evaluateAll((els) =>
    els
      .map((e) => ({ t: e.textContent.trim(), h: e.getBoundingClientRect().height }))
      .filter((x) => x.h < 40),
  );
  expect(zuKlein, "Antwortknoepfe unter 44 px").toEqual([]);

  await antworten(page, ZWEIGE[0]);
  await expect(page.locator("#hilfe-ergebnis")).toBeVisible();
});
