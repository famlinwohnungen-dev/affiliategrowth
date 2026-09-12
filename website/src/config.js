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
 * Nach der Freigabe eines Programms genügt `beigetreten: true` — die
 * Awin-Trackinglink wird aus `advertiserId` und `PUBLISHER_ID` gebaut. Bewusst
 * KEIN von Hand eingefügter Link: Eine falsche awinmid oder ein vergessener
 * Parameter fällt niemandem auf, die Klicks laufen ins Leere oder werden nicht
 * zugeordnet — und das merkt man erst an ausbleibenden Provisionen.
 *
 * Solange `beigetreten: false`, zeigt /go/<anbieter>/ auf die Händlerseite.
 * Die Links funktionieren also, verdienen aber nichts.
 */
/**
 * Leser-Rückmeldungen (D1).
 *
 * Erst auf `true` setzen, wenn die D1-Datenbank angelegt und das Binding in
 * wrangler.toml einkommentiert ist. Solange `false`, werden die Ja/Nein-Knöpfe
 * gar nicht erst gerendert — besser keine Schaltfläche als eine, die nichts
 * tut und beim Absenden einen Fehler zeigt.
 */
export const FEEDBACK_AKTIV = false;

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
    beigetreten: false,
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
    beigetreten: false,
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
    beigetreten: false,
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
    beigetreten: false,
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

/** Awin-Deeplink nach dem dokumentierten cread.php-Schema. */
function awinDeeplink(advertiserId, ziel) {
  const u = new URL("https://www.awin1.com/cread.php");
  u.searchParams.set("awinmid", advertiserId);
  u.searchParams.set("awinaffid", PUBLISHER_ID);
  u.searchParams.set("ued", ziel);
  return u.toString();
}

/**
 * Ziel-URL für /go/<anbieter>/. Vor der Freigabe die Händlerseite, danach der
 * generierte Trackinglink. `landingUrl` erlaubt es, statt der Startseite eine
 * bestimmte Produktseite anzusteuern.
 */
export function merchantUrl(key) {
  const m = MERCHANTS[key];
  if (!m) throw new Error(`Unbekannter Anbieter: ${key}`);

  const ziel = m.landingUrl ?? m.homepage;
  if (!m.beigetreten) return ziel;

  if (!m.advertiserId) {
    throw new Error(`${key}: beigetreten, aber keine advertiserId gesetzt`);
  }
  return awinDeeplink(m.advertiserId, ziel);
}
