# UI-Regeln — Mobil zuerst

Verbindlich für jede neue Komponente und jede Änderung an einer bestehenden.

Der Grund ist nicht Prinzipientreue: Suchanfragen wie „g data vs bitdefender"
kommen überwiegend vom Telefon, oft unterwegs, oft einhändig. Wer dort
abspringt, klickt auch keinen Affiliate-Link.

---

## Die fünf Regeln

### 1. Tippziele mindestens 44 × 44 px

Gilt für **alles**, was angetippt wird: Knöpfe, Navigationslinks, das Logo,
Aufklapp-Fragen, Formularfelder. WCAG 2.5.8 nennt 44 px als Untergrenze — das
ist keine Empfehlung für den Idealfall, sondern das Minimum für einen Daumen.

Ausgenommen sind ausschließlich Links **im Fließtext**, die dort mitlaufen.

Praktisch: Höhe kommt über `min-height: 2.75rem` plus `display: inline-flex;
align-items: center`, nicht über eine feste Zeilenhöhe.

### 2. Keine Schrift unter 12 px

`0.75rem` ist die Untergrenze — auch für Auszeichnungen, Tabellenköpfe und
Marker. Was auf dem 27-Zoll-Bildschirm noch elegant wirkt, ist auf einem
Telefon in der Bahn nicht mehr lesbar.

**Beschriftung gehört nicht in ein SVG.** In einem SVG mit `viewBox` skaliert
die Schrift mit der Elementbreite: `font-size: 11px` kommt in einer 272 px
breiten Spalte als 9,1 px an. Zeichne im SVG nur Formen und Linien, setze
jede Beschriftung als HTML-Text daneben oder darunter. Der Nebeneffekt ist
angenehm: HTML-Text bricht um, ist markierbar und durchsuchbar.

### 3. Die Seite scrollt nie waagerecht

Breite Inhalte — Tabellen, Codeblöcke, Diagramme — scrollen **in ihrem eigenen
Container** (`.scroller` mit `overflow-x: auto`), niemals der `body`. Eine
waagerecht verschiebbare Seite fühlt sich kaputt an.

**Ein `.scroller` ist die Notlösung, nicht die Lösung.** Er verhindert, dass
die Seite kaputtgeht — er macht den Inhalt nicht lesbar. Niemand sieht einem
Container an, dass rechts noch etwas kommt, und quer zu wischen, während die
Seite senkrecht scrollt, geht auf dem Telefon regelmäßig daneben.

Für **Vergleichstabellen gilt deshalb: stapeln statt schieben.** Unter 34 rem
wird das Merkmal zur Zeile über den Werten, die Produkte bleiben nebeneinander
(siehe `VergleichsTabelle.astro`). Der Prüfwert dafür ist
`scroller.scrollWidth - scroller.clientWidth` — er muss **0** sein. Das Skript
unten nimmt `.scroller` von der Überstands-Prüfung aus, misst also genau das
nicht.

### 4. Nichts ragt aus dem Sichtbereich

Kein Element darf über den rechten Rand hinausstehen. Häufigste Ursachen:
feste Pixelbreiten, lange Wörter ohne Umbruch, Raster mit zu großem `minmax`.

### 5. Raster: eine Spalte oder die volle Zahl — nie dazwischen

Drei Karten in zwei Spalten lassen eine Zelle leer, und die Rasterfarbe
scheint als grauer Block durch. Entweder `1fr` oder `repeat(3, 1fr)`, per
Medienabfrage umgeschaltet.

---

## Prüfen, nicht schätzen

Vor jedem Commit an der Oberfläche: bauen, ausliefern, und dieses Skript in
der Konsole laufen lassen — bei **320, 375 und 768 px**.

```js
(() => {
  const vw = innerWidth, p = [];
  if (document.documentElement.scrollWidth > vw + 1) p.push('SEITE SCROLLT WAAGERECHT');
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const r = el.getBoundingClientRect();
    if (!r.width) return;
    if ((r.right > vw + 1 || r.left < -1) && !el.closest('.scroller') && !el.closest('.honigtopf')
        && getComputedStyle(el.parentElement || el).overflowX !== 'auto')
      p.push('RAGT HERAUS: ' + el.tagName.toLowerCase());
  });
  document.querySelectorAll('a,button,input,textarea,summary,label').forEach(el => {
    if (el.closest('.honigtopf')) return;
    if (el.tagName === 'A' && el.closest('p,li,td')) return;   // Fließtextlinks
    if (el.tagName === 'INPUT' && el.type === 'radio') return; // getarnt hinter dem label
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    if (r.height < 40) p.push('ZU KLEIN ' + Math.round(r.width) + 'x' + Math.round(r.height)
      + ': ' + el.textContent.trim().slice(0, 24));
  });
  document.querySelectorAll('p,li,td,th,span,label,button,a,figcaption,legend,dt,dd,summary').forEach(el => {
    if (!el.textContent.trim() || el.closest('.sr-only')) return;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs && fs < 11.5) p.push('SCHRIFT ' + fs.toFixed(1) + 'px: ' + el.textContent.trim().slice(0, 24));
  });
  // SVG-Text skaliert mit der Elementbreite — die gerenderte Groesse zaehlt,
  // nicht die im Stylesheet notierte.
  document.querySelectorAll('svg').forEach(svg => {
    const r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal;
    const k = vb && vb.width ? r.width / vb.width : 1;
    svg.querySelectorAll('text,tspan').forEach(t => {
      if (!t.textContent.trim()) return;
      const eff = parseFloat(getComputedStyle(t).fontSize) * k;
      if (eff < 11.5) p.push('SVG-SCHRIFT ' + eff.toFixed(1) + 'px: ' + t.textContent.trim().slice(0, 24));
    });
  });
  return [...new Set(p)];
})();
```

Leeres Ergebnis auf allen drei Breiten = bestanden.

**320 px nicht überspringen.** Es ist die schmalste realistische Breite
(iPhone SE der ersten Generationen, Android-Geräte im Einstiegssegment) und
bricht zuverlässig Dinge, die bei 375 px noch passen.

**Interaktive Bauteile im Endzustand prüfen, nicht nur im Ausgangszustand.**
Ein Ergebnisblock, der erst nach drei Klicks erscheint, wird sonst nie
gemessen. Erst durchklicken, dann das Skript laufen lassen.

Bei größeren Änderungen zusätzlich: 360 px (verbreitetste Android-Breite),
390 und 414 px sowie einmal quer (667 × 375). Querformat ist der Fall, in
dem zweispaltige Bereiche zu früh umbrechen.

---

## Beim letzten Durchgang gefunden

Alles davon sah auf dem Schreibtisch tadellos aus:

| Fund | Vorher | Behoben durch |
|---|---|---|
| Navigationslinks | 22 px hoch | `min-height: 2.75rem` |
| Logo-Link | 26 × 26 px | Innenabstand |
| „Alle ansehen" | 23 px hoch | `min-height: 2.75rem` |
| Tabellenköpfe | 11,0 px | `0.75rem` |
| Empfehlungs-Marker | 9,9 px | `0.72rem` |
| Artikel-Auszeichnung | 10,9 px | `0.75rem` |
| FAQ-Aufklapper | 26 px hoch | `min-height` + eigener Marker |

Sieben Befunde in einem Durchgang, keiner davon am Schreibtisch sichtbar.
Genau deshalb wird gemessen statt geschaut.

## Nachtrag: der Fund, den das Skript selbst verpasst hat

Das Startseiten-Schaubild war ein SVG mit eingebauter Beschriftung. Bei
320 px kam sie mit **9,1 px** an — das Skript meldete nichts, weil es nur
HTML-Elemente abfragte. Behoben in zwei Schritten: Das Schaubild besteht
jetzt aus HTML und CSS mit reinem Linien-SVG, und das Skript misst
SVG-Text mit.

Die Lehre steht über der Tabelle: Ein Prüfskript belegt nur, was es abfragt.
Wenn ein neues Bauteil eine Darstellungsform mitbringt, die das Skript nicht
kennt, gehört die Prüfung erweitert — sonst ist ein leeres Ergebnis kein
Freispruch, sondern eine Lücke.

## Nachtrag 2: die Vergleichstabelle, gemeldet von einem echten Telefon

Bei 375 px war die Tabelle 418 px breit in einem 327 px breiten Container.
**91 px lagen ausserhalb — darunter die Empfehlungsspalte.** Das Skript
schwieg, weil `.scroller` von der Überstands-Prüfung ausgenommen ist: Der
Zustand war regelkonform und trotzdem unbrauchbar.

Gefunden hat das kein Skript, sondern Song auf seinem Telefon. Zwei Dinge
folgen daraus: Regel 3 sagt jetzt, dass ein `.scroller` keine Lösung ist,
und der versteckte Überstand wird als Zahl geprüft
(`scrollWidth - clientWidth === 0`) statt per Ausnahme übergangen.

Beim Beheben kam eine zweite Falle dazu: `tbody tr { display: grid }` schlug
`.cta-zeile { display: block }`, weil Astro an **jeden** Selektor ein
`[data-astro-cid-…]` hängt — aus (0,0,2) und (0,1,0) werden (0,2,2) und
(0,2,0). In Astro-Komponenten deshalb nicht nach Klassenspezifität schätzen,
sondern messen.
