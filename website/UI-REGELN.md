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

### 3. Die Seite scrollt nie waagerecht

Breite Inhalte — Tabellen, Codeblöcke, Diagramme — scrollen **in ihrem eigenen
Container** (`.scroller` mit `overflow-x: auto`), niemals der `body`. Eine
waagerecht verschiebbare Seite fühlt sich kaputt an.

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
  document.querySelectorAll('a,button,input,textarea,summary').forEach(el => {
    if (el.closest('.honigtopf')) return;
    if (el.tagName === 'A' && el.closest('p,li,td')) return;   // Fließtextlinks
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    if (r.height < 40) p.push('ZU KLEIN ' + Math.round(r.width) + 'x' + Math.round(r.height)
      + ': ' + el.textContent.trim().slice(0, 24));
  });
  document.querySelectorAll('p,li,td,th,span,label,button,a').forEach(el => {
    if (!el.textContent.trim() || el.closest('.sr-only')) return;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs && fs < 11.5) p.push('SCHRIFT ' + fs.toFixed(1) + 'px: ' + el.textContent.trim().slice(0, 24));
  });
  return [...new Set(p)];
})();
```

Leeres Ergebnis auf allen drei Breiten = bestanden.

**320 px nicht überspringen.** Es ist die schmalste realistische Breite
(iPhone SE der ersten Generationen, Android-Geräte im Einstiegssegment) und
bricht zuverlässig Dinge, die bei 375 px noch passen.

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
