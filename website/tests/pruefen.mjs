/**
 * Gemeinsame Pruefungen fuer alle Testdateien.
 *
 * Bewusst als eine Datei: Die Regeln stehen in UI-REGELN.md, und es soll
 * genau eine Stelle geben, an der sie in Code uebersetzt sind.
 */

/** Breiten, bei denen jede Seite geprueft wird. */
export const BREITEN = [
  { name: "320 (iPhone SE, Einstiegs-Android)", width: 320, height: 700 },
  { name: "360 (haeufigste Android-Breite)", width: 360, height: 740 },
  { name: "375 (iPhone)", width: 375, height: 812 },
  { name: "414 (grosse Telefone)", width: 414, height: 896 },
  { name: "667x375 (Telefon quer)", width: 667, height: 375 },
  { name: "768 (Tablet)", width: 768, height: 1024 },
];

/** Alle oeffentlichen Seiten. Neue Seite? Hier eintragen. */
export const SEITEN = [
  "/",
  "/artikel/",
  "/artikel/g-data-vs-bitdefender/",
  "/anbieter/",
  "/methodik/",
  "/impressum/",
  "/datenschutz/",
];

/**
 * Die Oberflaechenpruefung aus UI-REGELN.md, im Browser ausgefuehrt.
 * Rueckgabe: Liste der Befunde. Leer = bestanden.
 */
export async function befunde(page) {
  return page.evaluate(() => {
    const vw = innerWidth;
    const p = [];

    // Regel 3: die Seite selbst scrollt nie waagerecht.
    if (document.documentElement.scrollWidth > vw + 1) p.push("SEITE SCROLLT WAAGERECHT");

    // Regel 4: nichts ragt aus dem Sichtbereich.
    document.querySelectorAll("body *").forEach((el) => {
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden") return;
      const r = el.getBoundingClientRect();
      if (!r.width) return;
      if (el.closest(".honigtopf")) return;
      const elternScrollt = getComputedStyle(el.parentElement || el).overflowX === "auto";
      if ((r.right > vw + 1 || r.left < -1) && !elternScrollt)
        p.push(`RAGT HERAUS: ${el.tagName.toLowerCase()}.${el.className.baseVal ?? el.className}`);
    });

    // Regel 1: Tippziele mindestens 44 px. Fliesstextlinks ausgenommen,
    // ebenso hinter Labels versteckte Radiobuttons.
    document.querySelectorAll("a,button,input,textarea,summary,label").forEach((el) => {
      if (el.closest(".honigtopf")) return;
      if (el.tagName === "A" && el.closest("p,li")) return;
      if (el.tagName === "INPUT" && el.type === "radio") return;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      if (r.height < 40)
        p.push(`ZU KLEIN ${Math.round(r.width)}x${Math.round(r.height)}: ${el.textContent.trim().slice(0, 30)}`);
    });

    // Regel 2: keine Schrift unter 12 px.
    document
      .querySelectorAll("p,li,td,th,span,label,button,a,figcaption,legend,dt,dd,summary")
      .forEach((el) => {
        if (!el.textContent.trim() || el.closest(".sr-only")) return;
        const fs = parseFloat(getComputedStyle(el).fontSize);
        if (fs && fs < 11.5)
          p.push(`SCHRIFT ${fs.toFixed(1)}px: ${el.textContent.trim().slice(0, 30)}`);
      });

    // Regel 2, SVG-Fall: SVG-Text skaliert mit der Elementbreite, es zaehlt
    // die gerenderte Groesse. Genau das hat einmal 9,1 px durchgelassen.
    document.querySelectorAll("svg").forEach((svg) => {
      const r = svg.getBoundingClientRect();
      const vb = svg.viewBox.baseVal;
      const k = vb && vb.width ? r.width / vb.width : 1;
      svg.querySelectorAll("text,tspan").forEach((t) => {
        if (!t.textContent.trim()) return;
        const eff = parseFloat(getComputedStyle(t).fontSize) * k;
        if (eff < 11.5)
          p.push(`SVG-SCHRIFT ${eff.toFixed(1)}px: ${t.textContent.trim().slice(0, 30)}`);
      });
    });

    // Regel 3, Nachtrag: ein .scroller darf nichts verstecken. Er ist von der
    // Ueberstands-Pruefung ausgenommen und war deshalb der blinde Fleck, in
    // dem die Vergleichstabelle 91 px verlor.
    document.querySelectorAll(".scroller").forEach((sc) => {
      const versteckt = sc.scrollWidth - sc.clientWidth;
      if (versteckt > 0) p.push(`SCROLLER VERSTECKT ${versteckt}px`);
    });

    return [...new Set(p)];
  });
}
