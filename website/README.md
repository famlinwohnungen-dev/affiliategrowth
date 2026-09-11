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

- [ ] **Domain registrieren** und `SITE.url` in `src/config.js` sowie die
      Sitemap-Zeile in `public/robots.txt` anpassen. `schutzlotse.de` ist nur
      ein Platzhalter und nicht auf Verfügbarkeit geprüft.
- [x] ~~Google Fonts lokal einbinden.~~ Erledigt: Schriften liegen in
      `public/fonts/`, eingebunden über `src/styles/fonts.css`. Keine Anfragen
      mehr an Google.
- [ ] **Impressum ausfüllen** (`src/pages/impressum.astro`) — Pflicht nach § 5 DDG.
- [ ] **Datenschutzerklärung finalisieren** (`src/pages/datenschutz.astro`) —
      das Gerüst ist keine Rechtsberatung; mit einem Generator eines
      Fachanwalts abgleichen.
- [ ] **Awin-Programme beantragen**: ESET DACH (`15751`), Bitdefender DE (`11660`).
- [ ] **Google Search Console** einrichten und Sitemap einreichen.

## Deployment — Cloudflare Pages

Kostenloser Account genügt (keine Kreditkarte).

**Laufender Deploy** (Projekt besteht bereits):

```bash
npm run deploy
```

Das baut und lädt hoch. Zugangsdaten kommen aus `.env`
(`CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`) — vorher exportieren:

```bash
set -a && . ./.env && set +a && npm run deploy
```

**Alternative: Git-Integration** im Cloudflare-Dashboard → Workers & Pages →
Create → Pages → Repo verbinden. Build-Befehl `npm run build`, Output `dist`,
Root-Verzeichnis `website`. Dann deployt jeder Push automatisch und `.env`
wird nicht gebraucht.

### Projekt neu anlegen

`wrangler pages project create` funktioniert ab wrangler 4.x **nicht** mit
einer Pages-Konfiguration — es erwartet einen Worker-Entrypoint. Projekt
stattdessen über die REST-API anlegen:

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"name":"schutzlotse","production_branch":"main"}'
```

Wrangler ist bewusst auf `4.131.1` festgenagelt: Cloudflare migriert Pages
schrittweise zu Workers, ein Minor-Update kann den Deploy brechen.

### API-Token

Der Token braucht die Berechtigung **Cloudflare Pages: Edit** auf Account-
Ebene. Fehlermeldungen und ihre Ursache:

| Fehler | Ursache |
|---|---|
| `Cannot use the access token from location: <IP>` (9109) | Token hat eine IP-Beschränkung, die diese IP nicht einschließt |
| `Authentication error` (10000) | Token fehlt die Pages-Berechtigung |
| `Invalid API Token` bei `/user/tokens/verify` | Normal bei Account-Token (`cfat_…`) — stattdessen `/accounts/<id>/tokens/verify` nutzen |

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
