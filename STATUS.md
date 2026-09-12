# Projektstand — Stand 12.09.2026

Übergabe für eine neue Sitzung. Was existiert, was entschieden wurde, was als
Nächstes ansteht.

---

## Das Vorhaben

Deutschsprachige Affiliate-Vergleichsseite für **Virenschutz-Software**.
Einnahmen über Awin-Provisionen, wenn Leser nach einem Vergleich kaufen.

**Warum diese Nische** — datengestützt aus 166 untersuchten Nischen:

- Als einzige geprüfte Nische mit **echten Awin-Händlern für Deutschland** und
  **niedrigem Wettbewerb** (Index 32 bei 9,05 € CPC)
- Belegte SERP-Lücke: Für `g data vs bitdefender` rankt SourceForge — eine
  dünne, englische Vorlagenseite. Es gibt also keine starke deutsche Seite.
- Fachliche Glaubwürdigkeit vorhanden (Song arbeitet in Enterprise-IT)

Vollständige Begründung und Redaktionsplan: `content/PLAN.md`

---

## Vier Awin-Programme

| Programm | Awin-ID | EPC | Einsatz |
|---|---|---|---|
| ESET DACH | 15751 | 0,25 € | primär |
| Bitdefender DE | 11660 | 0,21 € | primär |
| Kaspersky DE | 14098 | 0,07 € | nur erwähnen, **BSI-Warnung** |
| G DATA DE | 14693 | 0,03 € | nur erwähnen |

**Noch nicht beworben.** Erst nach 4–6 veröffentlichten Artikeln und mit echter
Domain — vorher droht Ablehnung.

---

## Was steht

**Website** (`website/`) — Astro 7 + Cloudflare Workers, live unter
`schutzlotse.famlinwohnungen.workers.dev`, **noindex** bis zum Livegang.

- Seiten: Start, Artikelliste, Artikel, Anbieter, Methodik, Impressum, Datenschutz
- Eigenes Logo (Schild + Kompassnadel), Schriften selbst gehostet
- Affiliate-Links über `/go/<anbieter>/?from=<seite>` — Quelle wird mitgezählt
- Cloudflare Web Analytics, cookielos, deshalb **kein Cookie-Banner**
- Teilen-Leiste, Rückmeldung (Ja/Nein + Freitext) in **D1**, Info-Widget,
  Nach-oben-Knopf
- Deploy automatisch bei Push auf `main`

**Daten** (`data/`) — 21.250 Awin-Programme, 166 Nischen mit Google-Trends- und
Keyword-Planner-Daten, Ranglisten.

**Regeln** — `content/SCHREIBWEISE.md` (HAC, Informationsdichte, Bilder),
`website/UI-REGELN.md` (mobil zuerst), `.githooks/pre-commit` (Secret-Scanner).

---

## Getroffene Entscheidungen (nicht neu aufrollen)

| Thema | Entscheidung | Grund |
|---|---|---|
| Google Ads API | verworfen | Basic Access braucht Brand-Verification, die eine Domain voraussetzt — zirkulär |
| DataForSEO | verworfen | 50 $ Mindesteinzahlung |
| Analytics | Cloudflare, cookielos | kein Banner nötig, spart Leser |
| Startseite | **keine** Affiliate-Links | „thin affiliate page" wird von Google abgewertet |
| Kaspersky | kein Affiliate-Link | BSI-Warnung glaubwürdig halten; EPC ohnehin 0,07 € |
| Werbekennzeichnung | Sternchen + Fußzeile | § 5a Abs. 4 UWG — darf **nicht** hinter einen Klick |

---

## Offen — in dieser Reihenfolge

1. **Domain registrieren.** Blockiert alles Weitere. Danach: `SITE.url`,
   Domain in Cloudflare verbinden, **neuen Analytics-Token** (hängt am
   Hostnamen), zuletzt `SITE.indexable = true`.
2. **Impressum ausfüllen** — braucht eine ladungsfähige Anschrift. Das Repo ist
   **öffentlich**; ob die Privatadresse dorthin soll, ist Songs Entscheidung.
3. **Datenschutzerklärung** mit einem Generator eines Fachanwalts abgleichen.
4. **Cloudflare-AVV** im Dashboard annehmen (Manage Account → Privacy).
5. **17 Artikel schreiben** nach `content/PLAN.md`, Phase 1 zuerst.
6. **Awin-Programme beantragen**, wenn 4–6 Artikel stehen.

### Dauerhafte Pflichten

- **Löschfrist Rückmeldungen: 12 Monate** — in der Datenschutzerklärung
  zugesagt, nichts erzwingt sie. Befehl in `website/README.md`.
- Bei jeder Oberflächenänderung: Prüfskript aus `website/UI-REGELN.md` bei
  320, 375 und 768 px laufen lassen.

---

## Wichtig für Artikel

**Fakten prüfen.** Die Entwürfe enthalten bewusst keine erfundenen
Erkennungsraten, Preise oder Benchmarks. Jeder Entwurf trägt oben einen
`PRÜFEN`-Block mit dem, was gegen AV-TEST und die Herstellerseiten abzugleichen
ist. Eine plausible erfundene Zahl schadet mehr als eine fehlende.

**Preise nie nennen** — sie veralten schneller, als Artikel aktualisiert werden.

---

## Fallstricke, die schon zugeschlagen haben

- **Affiliate-Links waren alle tot** — `/go/x/` mit Schrägstrich, Datei ohne.
  Behoben; `npm run build` prüft das jetzt und bricht sonst ab.
- **Awin-Token lag im öffentlichen Repo.** Rotiert; Pre-Commit-Hook eingebaut.
- **Deploy scheiterte zweimal** an Bindings ohne gültige ID (D1, SESSION-KV).
  Beide sind jetzt fest eingetragen.
- **`Astro.locals.runtime.env` gibt es ab Astro 6 nicht mehr** — stattdessen
  `import { env } from "cloudflare:workers"`.
- **Sieben Mobil-Probleme** waren am Schreibtisch unsichtbar (Tippziele 22 px,
  Schrift 9,9 px). Deshalb messen statt schauen.
