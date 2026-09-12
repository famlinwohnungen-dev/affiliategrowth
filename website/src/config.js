/**
 * Site-wide configuration.
 *
 * Domain is a placeholder until registered - update SITE.url before the first
 * deploy, since it feeds canonical URLs, the sitemap and Open Graph tags.
 */
export const SITE = {
  /**
   * Auf `true` setzen, sobald Impressum und Datenschutzerklärung ausgefüllt
   * sind und die echte Domain verbunden ist. Solange `false`, liefert jede
   * Seite `noindex` und robots.txt sperrt alles — damit Google keine Version
   * mit Platzhalter-Impressum indexiert (in Deutschland abmahnfähig).
   */
  indexable: false,

  url: "https://schutzlotse.de",
  name: "Schutzlotse",
  tagline: "Virenschutz ehrlich verglichen",
  description:
    "Unabhängige Vergleiche von Virenschutz-Software für Privatnutzer und kleine Unternehmen in Deutschland.",
  language: "de",
  locale: "de_DE",
  author: "Song Lin",
};

/**
 * Awin merchants.
 *
 * `trackingUrl` stays null until each programme is approved - Awin only issues
 * tracking links to accepted publishers. Until then /go/<id> falls back to the
 * merchant's own site, so links work and nothing silently 404s.
 *
 * Awin deep link format once approved:
 *   https://www.awin1.com/cread.php?awinmid=<advertiserId>&awinaffid=<publisherId>&ued=<encoded target>
 */
export const PUBLISHER_ID = "3083037";

/**
 * Cloudflare Web Analytics.
 *
 * Cookielos — es wird nichts auf dem Endgerät gespeichert, deshalb ist keine
 * Einwilligung und kein Banner nötig (§ 25 Abs. 2 TDDDG).
 *
 * Token aus dem Cloudflare-Dashboard: Web Analytics → Seite hinzufügen →
 * "Manual setup". Solange hier null steht, wird kein Beacon eingebunden.
 *
 * Wichtig: Der Beacon muss auch auf den /go/-Weiterleitungsseiten liegen,
 * sonst tauchen Affiliate-Klicks in der Statistik gar nicht auf.
 */
// Der Beacon-Token steht im ausgelieferten HTML jeder Seite und ist kein
// Geheimnis: Er erlaubt nur das Melden von Aufrufen, keinen Kontozugriff.
export const CF_ANALYTICS_TOKEN = "e2f2c8159f8b4461a7a7f0fb2aa200cf"; // öffentlich: Beacon

/**
 * `kurz`, `land` und `staerke` speisen die Anbieterkarten auf der Startseite.
 * Bewusst nur belegbare Fakten — keine erfundenen Testnoten oder Bewertungen.
 */
export const MERCHANTS = {
  eset: {
    name: "ESET",
    advertiserId: "15751",
    homepage: "https://www.eset.com/de/",
    trackingUrl: null,
    epc: 0.25,
    primary: true,
    land: "Slowakei",
    kurz: "Schlanker Client mit vielen Einstellmöglichkeiten.",
    staerke: "Für Nutzer, die Kontrolle über Details wollen",
  },
  bitdefender: {
    name: "Bitdefender",
    advertiserId: "11660",
    homepage: "https://www.bitdefender.de",
    trackingUrl: null,
    epc: 0.21,
    primary: true,
    land: "Rumänien",
    kurz: "Cloudgestützte Analyse, stark automatisiert.",
    staerke: "Für alle, die sich nicht damit beschäftigen wollen",
  },
  gdata: {
    name: "G DATA",
    advertiserId: "14693",
    homepage: "https://www.gdata.de/",
    trackingUrl: null,
    epc: 0.03,
    primary: false,
    land: "Deutschland",
    kurz: "Deutscher Anbieter mit Sitz und Entwicklung in Bochum.",
    staerke: "Wenn Datenverarbeitung in Deutschland zählt",
  },
  kaspersky: {
    name: "Kaspersky",
    advertiserId: "14098",
    homepage: "https://www.kaspersky.com/de/",
    trackingUrl: null,
    epc: 0.07,
    primary: false,
    land: "Russland",
    kurz: "Technisch stark, politisch umstritten.",
    staerke: "Nur mit Blick auf die BSI-Warnung zu bewerten",
    // Das BSI warnte im März 2022 vor dem Einsatz von Kaspersky-Software.
    // Für deutsche Leser ist das der entscheidende Punkt — er gehört auf jede
    // Seite, die Kaspersky erwähnt, nicht ins Kleingedruckte.
    hinweis: "BSI-Warnung seit März 2022",
  },
};

export function merchantUrl(key) {
  const m = MERCHANTS[key];
  if (!m) throw new Error(`Unknown merchant: ${key}`);
  return m.trackingUrl ?? m.homepage;
}
