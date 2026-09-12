# Schreibweise — verbindlich für alle Texte

Gilt für jeden Artikel und für die Startseite.

---

## HAC: Hook, Analogie, Context

Die ersten drei bis vier Sätze entscheiden, ob weitergelesen wird. Sie folgen
immer dieser Reihenfolge.

### 1. Hook — der erste Satz muss stoppen

Ein Hook ist keine Ankündigung, sondern eine Behauptung, ein Widerspruch oder
eine Zahl, die man nicht erwartet hat.

| Nicht so | Sondern so |
|---|---|
| „In diesem Artikel vergleichen wir G DATA und Bitdefender." | „Beide erkennen praktisch jede Schadsoftware. Trotzdem ist die Wahl nicht egal." |
| „Virenschutz ist ein wichtiges Thema." | „Der teuerste Fehler beim Virenschutz passiert nicht beim Kauf, sondern im zweiten Jahr." |

**Regel:** Der Hook enthält keine Selbstbeschreibung des Artikels. Wer „In
diesem Beitrag …" schreibt, hat den Hook nicht geschrieben, sondern angekündigt.

### 2. Analogie — das Abstrakte greifbar machen

Sicherheitssoftware ist unsichtbar. Eine Analogie übersetzt sie in etwas, das
der Leser schon kennt — Versicherungen, Schlösser, Winterreifen, Wartung.

> „Es ist wie bei Versicherungen: Der Schutz ähnelt sich bei allen Anbietern.
> Der Unterschied steckt im Kleingedruckten und im Preis nach dem ersten Jahr."

**Regel:** Eine Analogie pro Text, an prominenter Stelle. Mehrere Analogien
hintereinander wirken beliebig und heben sich gegenseitig auf.

### 3. Context — warum das jetzt für *dich* zählt

Der Übergang vom Allgemeinen zur Lage des Lesers. Nennt die konkrete
Entscheidungssituation.

> „Wenn du gerade vor der Verlängerung stehst oder einen neuen Rechner
> eingerichtet hast, ist genau das die Frage, die zählt."

---

## Informationsdichte — die eigentliche Regel

Nicht die Länge entscheidet, sondern der Ertrag pro Absatz. Ein langer Text,
der laufend etwas Brauchbares liefert, fühlt sich kurz an. Ein kurzer Text ohne
Ertrag fühlt sich lang an.

Der Hook öffnet eine Lücke. Was den Leser danach hält, sind viele kleine
Einlösungen: eine konkrete Zahl, eine benannte Falle, ein Rat, den er sofort
anwenden kann.

### Der Absatztest

**Jeder Absatz muss etwas enthalten, das der Leser vorher nicht wusste und
jemandem weitererzählen könnte.** Ist das nicht der Fall: streichen. Nicht
kürzen — streichen.

| Ohne Ertrag | Mit Ertrag |
|---|---|
| „Die Systemlast ist ein wichtiger Faktor bei der Auswahl." | „Auf einem vier Jahre alten Notebook merkst du den Doppel-Engine-Ansatz vor allem beim ersten vollständigen Scan." |
| „Auch der Preis spielt eine Rolle." | „Der Verlängerungspreis liegt regelmäßig über dem Neukundenpreis — kündigen und neu abschließen ist oft günstiger." |
| „Im Folgenden betrachten wir die Unterschiede." | *(ersatzlos streichen)* |

### Ertrag nach vorn

Der erste Satz eines Abschnitts enthält die Erkenntnis, nicht die Hinführung.
Die meisten Leser überfliegen — wer nur die ersten Sätze liest, muss trotzdem
alles Wesentliche mitnehmen.

> **Nicht:** „Bei der Systemlast gibt es einige Aspekte zu beachten. Zunächst
> muss man wissen, dass … Daher zeigt sich, dass G DATA mehr Ressourcen braucht."
>
> **Sondern:** „G DATA braucht spürbar mehr Rechenleistung — der Grund sind zwei
> parallel laufende Scan-Engines."

### Diese Formulierungen nie

Sie kündigen an, statt zu liefern, und kosten den Leser Zeit ohne Gegenwert:

- „In diesem Artikel …", „Im Folgenden …", „Wie bereits erwähnt …"
- „Es ist wichtig zu wissen, dass …" → einfach den Inhalt schreiben
- „Zusammenfassend lässt sich sagen …" → die Zusammenfassung selbst schreiben
- „Natürlich", „grundsätzlich", „letztendlich" als Satzfüller

## Bilder und Grafiken

Eine gute Grafik trägt mehr als drei Absätze — aber nur an der richtigen Stelle.

### Nie vor dem Hook

Der erste Bildschirm gehört dem Text. Ein Bild ganz oben zwingt den Leser,
zuerst etwas zu entschlüsseln, statt in einen Satz hineinzukippen. Er
investiert Aufmerksamkeit, bevor er einen Grund dazu hat — und springt eher ab.

**Regel:** Das erste Bild kommt frühestens nach dem „Kurz vorweg", also nachdem
der Leser bereits weiß, worum es geht und was ihn erwartet.

### Was ein Bild rechtfertigt

Ein Bild muss etwas zeigen, das in Prosa umständlich wäre:

- **Vergleich mehrerer Werte** → Balken statt Aufzählung
- **Ablauf oder Architektur** → etwa lokale Engine gegen Cloud-Analyse
- **Etwas, das man gesehen haben muss** → eine Einstellung, ein Warnfenster

Kein Bild rechtfertigen: Stimmung, Auflockerung, „der Text war so lang".
Ein Symbolfoto mit Kapuzenpulli und grünen Zeichen sagt dem Leser nichts, das
er nicht schon wusste, und kostet Ladezeit.

### Für diese Seite: lieber zeichnen als fotografieren

Selbst erstellte SVG-Diagramme schlagen Fotos in fast jeder Hinsicht:

| | SVG-Diagramm | Foto / Screenshot |
|---|---|---|
| Rechte | eigene Arbeit, keine Fragen | Lizenz nötig, Herstellerrechte |
| Ladezeit | wenige Kilobyte | schnell mehrere hundert |
| Dunkelmodus | passt sich über die Farbtokens an | zwei Fassungen nötig |
| Aussage | genau das, was gemeint ist | meist ungefähr |

### Bildrechte — in Deutschland ein echtes Risiko

Fotoabmahnungen sind hierzulande ein eingespieltes Geschäft. Deshalb:

- **Keine Herstellerlogos** ohne Freigabe. Nach der Awin-Aufnahme stellen die
  Programme in der Regel Werbemittel bereit — die sind ausdrücklich freigegeben.
- **Keine Produkt-Screenshots** ohne Prüfung der Nutzungsbedingungen.
- **Keine Bilder aus der Bildersuche.** Auch nicht „nur kurz".
- Bei Stockmaterial die Lizenz und die Pflicht zur Urhebernennung dokumentieren.

### Technisch

- Bilder **selbst hosten** (`src/assets/`), nie von fremden Servern. Sonst
  entstehen wieder externe Anfragen — dieselbe Falle wie bei Google Fonts.
- Astros `<Image />` benutzen: erzeugt WebP und setzt Breite und Höhe, damit
  beim Laden nichts springt (Core Web Vitals).
- **Alt-Text ist Pflicht** und beschreibt die Aussage, nicht das Motiv:
  nicht „Diagramm", sondern „G DATA benötigt rund doppelt so viel
  Arbeitsspeicher wie Bitdefender".
- Faustregel: höchstens ein Bild pro zwei Bildschirmlängen Text.

## Struktur eines Vergleichsartikels

1. **HAC** (3–4 Sätze)
2. **Kurz vorweg** — die Empfehlung sofort, mit Geltungsbereich. Wer nur das
   liest, hat bekommen, wofür er gekommen ist.
3. **Vergleichstabelle**
4. **Zwei bis vier Abschnitte** zu den Punkten, an denen sich die Produkte
   tatsächlich unterscheiden
5. **Fazit** mit klarer Zuordnung: *für dich, wenn …* / *nicht für dich, wenn …*
6. **Rückmeldung und Teilen** (automatisch)

---

## Sprache

- **Du**, nicht Sie. Konsequent.
- Aktiv statt Passiv.
- Keine Superlative ohne Beleg. „Der beste Virenschutz" ist eine Behauptung,
  „geringste Systemlast im AV-TEST vom März 2026" eine Aussage.
- Keine erfundenen Zahlen. Lieber keine Zahl als eine plausible.
- Fachbegriffe beim ersten Mal erklären, danach benutzen.

---

## Warum Ehrlichkeit hier verkauft

Der Leser kommt mit Misstrauen — er weiß, dass Vergleichsseiten Provision
bekommen. Eine Empfehlung, die auch sagt, wann sie *nicht* gilt, wirkt
glaubwürdiger als eine, die alles gut findet. Genau diese Glaubwürdigkeit ist
der Grund, warum am Ende jemand klickt.

Das ist keine moralische Position, sondern die wirtschaftlich bessere: Wer
allen alles empfiehlt, wird niemandem geglaubt.
