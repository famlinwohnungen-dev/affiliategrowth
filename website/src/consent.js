/**
 * Einwilligungs-Konfiguration (§ 25 TDDDG / DSGVO).
 *
 * Grundregel: Ein Banner ist nur dann nötig, wenn tatsächlich Informationen
 * auf dem Endgerät gespeichert oder ausgelesen werden, die nicht technisch
 * erforderlich sind. Solange diese Seite nichts davon tut, wäre ein Banner
 * nicht nur überflüssig, sondern inhaltlich falsch — und würde Leser vergraulen.
 *
 * Deshalb steuert sich das Banner selbst: Es erscheint automatisch, sobald
 * unten eine Kategorie mit `aktiv: true` steht. Kein separater Schalter, der
 * vergessen werden kann.
 *
 * Beim Einbau von Analytics also hier `aktiv: true` setzen — und das Skript
 * erst laden, wenn `hatEinwilligung("statistik")` true ergibt.
 */
export const KATEGORIEN = [
  {
    id: "essenziell",
    name: "Notwendig",
    beschreibung:
      "Speichert ausschließlich deine Auswahl in diesem Dialog. Ohne diese Speicherung müssten wir dich bei jedem Seitenaufruf erneut fragen.",
    // Technisch erforderlich — nach § 25 Abs. 2 TDDDG einwilligungsfrei.
    immer: true,
    aktiv: true,
  },
  {
    id: "statistik",
    name: "Statistik",
    beschreibung:
      "Hilft uns zu verstehen, welche Vergleiche gelesen werden. Wird erst gesetzt, wenn du zustimmst.",
    immer: false,
    // Auf true setzen, sobald ein Dienst eingebaut wird, der Informationen auf
    // dem Endgerät speichert. Cloudflare Web Analytics tut das nicht — deshalb
    // bleibt es hier aus und die Seite braucht kein Banner.
    aktiv: false,
  },
];

export const SPEICHER_SCHLUESSEL = "schutzlotse-einwilligung";

/** Nur Kategorien, für die überhaupt eine Einwilligung nötig ist. */
export const optionaleKategorien = KATEGORIEN.filter((k) => !k.immer && k.aktiv);

/** Banner nur zeigen, wenn es wirklich etwas einzuwilligen gibt. */
export const brauchtEinwilligung = optionaleKategorien.length > 0;
