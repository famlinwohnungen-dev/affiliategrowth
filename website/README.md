# Website — Virenschutz-Vergleiche

Astro + Markdown. Statisch gebaut, kein Server, keine Datenbank.

```bash
npm run dev      # localhost:4321
npm run build    # → dist/
npm run preview  # gebautes dist/ lokal testen
```

## Einen Artikel schreiben

Neue Datei unter `src/content/artikel/<slug>.mdx`. Der Dateiname wird die URL:
`src/content/artikel/eset-vs-bitdefender.mdx` → `/artikel/eset-vs-bitdefender/`.

Frontmatter-Felder sind in `src/content.config.ts` definiert und werden beim
Build validiert — ein Tippfehler bricht den Build, statt still kaputt zu gehen.
`draft: true` hält einen Artikel aus Build und Sitemap heraus.

Für Vergleichstabellen und Affiliate-Buttons die Komponenten importieren, siehe
`g-data-vs-bitdefender.mdx` als Vorlage.

## Affiliate-Links

Alle ausgehenden Links laufen über `/go/<merchant>/`. Die Ziel-URLs stehen an
genau einer Stelle: `src/config.js`.

Solange die Awin-Programme nicht freigegeben sind, steht dort `trackingUrl:
null` und es wird auf die Händler-Website weitergeleitet — die Links
funktionieren also, verdienen aber nichts. **Nach der Freigabe** dort die
Awin-Deeplinks eintragen:

```
https://www.awin1.com/cread.php?awinmid=<advertiserId>&awinaffid=3083037&ued=<Ziel-URL>
```

`/go/` ist per `robots.txt` gesperrt und aus der Sitemap ausgeschlossen; die
Links tragen `rel="sponsored nofollow"` — beides von Google für bezahlte Links
verlangt.

## Vor dem Livegang

- [ ] **Domain registrieren.** `schutzlotse.de` ist nur ein Platzhalter und
      nicht auf Verfügbarkeit geprüft. Danach in dieser Reihenfolge:
  - [ ] `SITE.url` in `src/config.js` setzen (Canonical-URLs, Sitemap, OG-Tags)
  - [ ] Domain im Cloudflare-Projekt verbinden
  - [ ] **Neuen Web-Analytics-Token holen.** Der Token hängt am Hostnamen; der
        für `*.workers.dev` sammelt danach nichts mehr. Neue Seite im
        Cloudflare-Dashboard anlegen und `CF_ANALYTICS_TOKEN` ersetzen — die
        Markierung `// öffentlich: Beacon` in der Zeile stehen lassen, sonst
        blockiert der Pre-Commit-Hook.
  - [ ] Erst zum Schluss `SITE.indexable = true`
- [x] ~~Google Fonts lokal einbinden.~~ Erledigt: Schriften liegen in
      `public/fonts/`, eingebunden über `src/styles/fonts.css`. Keine Anfragen
      mehr an Google.
- [ ] **Impressum ausfüllen** (`src/pages/impressum.astro`) — Pflicht nach § 5 DDG.
- [ ] **Datenschutzerklärung finalisieren** (`src/pages/datenschutz.astro`) —
      das Gerüst ist keine Rechtsberatung; mit einem Generator eines
      Fachanwalts abgleichen.
- [ ] **Awin-Programme beantragen**: ESET DACH (`15751`), Bitdefender DE (`11660`).
- [ ] **Google Search Console** einrichten und Sitemap einreichen.

## Deployment — Cloudflare Workers (Static Assets)

Deployt automatisch bei jedem Push auf `main`, über die GitHub-Integration.
Es liegen keine Cloudflare-Zugangsdaten mehr lokal.

### Erforderliche Dashboard-Einstellung

Cloudflare legt bei einer neuen Git-Verbindung ein **Workers**-Projekt an (das
frühere Pages ist im Auslaufen). Unter Workers & Pages → `affiliategrowth` →
Settings → Build muss gesetzt sein:

| Feld | Wert |
|---|---|
| Root directory | `website` |
| Build command | `npm run build` |
| Deploy command | `npx wrangler deploy` |

**Root directory ist der entscheidende Punkt.** Ohne ihn baut Cloudflare im
Wurzelverzeichnis des Repos, wo kein Node-Projekt liegt — daran ist der erste
Build gescheitert.

### Manueller Deploy (optional)

Nur nötig, wenn ohne Commit deployt werden soll. Vorher einmalig per OAuth
anmelden — kein API-Token, keine IP-Freigabe:

```bash
npx wrangler login
npm run deploy
```

### Warum kein Pages mehr

Cloudflare migriert Pages zu Workers. Ein Pages-Projekt, das per
Direct-Upload angelegt wurde, lässt sich nachträglich **nicht** mit Git
verbinden — der Deployment-Typ ist bei der Erstellung fest. Deshalb ist das
alte Projekt gelöscht und durch ein Workers-Projekt ersetzt worden.

Wrangler ist bewusst auf `4.131.1` festgenagelt: Die Migration läuft, ein
Minor-Update kann den Deploy brechen.

### Nach dem ersten Deploy

- [ ] **Auftragsverarbeitungsvertrag akzeptieren.** Cloudflare-Dashboard →
      Manage Account → Configurations → Privacy. Ohne AVV ist der Einsatz
      eines US-Dienstleisters nach Art. 28 DSGVO nicht zulässig. Die
      Datenschutzerklärung nennt Cloudflare bereits als Auftragsverarbeiter.
- [ ] **Eigene Domain verbinden**: Pages-Projekt → Custom domains. Danach
      `SITE.url` in `src/config.js` und die Sitemap-Zeile in
      `public/robots.txt` anpassen.

### Später: Umzug zu einem deutschen Hoster

Die Seite ist rein statisch — ein Umzug bedeutet nur, `dist/` woanders
hinzukopieren:

```bash
npm run build
rsync -avz --delete dist/ user@host:/var/www/html/
```

Bei einem Hoster in Deutschland (Hetzner, Netcup, Uberspace) entfällt die
Drittlandübermittlung; dann den Abschnitt „Hosting" in
`src/pages/datenschutz.astro` entsprechend ersetzen.

## Redaktionsplan

Die 18 geplanten Artikel mit Ziel-Keywords und Reihenfolge stehen in
`../content/PLAN.md`.
