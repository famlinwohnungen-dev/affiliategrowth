import type { APIRoute } from "astro";
// Astro 6+ liefert die Worker-Bindings nicht mehr über Astro.locals.runtime.env,
// sondern über dieses Modul. Der alte Weg wirft zur Laufzeit einen Fehler.
import { env } from "cloudflare:workers";

/**
 * Nimmt Leser-Rückmeldungen entgegen und legt sie in D1 ab.
 *
 * Die einzige serverseitige Route der Seite — alle übrigen Seiten bleiben
 * vorgerendert. Deshalb hier ausdrücklich `prerender = false`.
 *
 * Datensparsamkeit ist kein Beiwerk, sondern die Auslegung: Es werden
 * bewusst KEINE IP-Adressen gespeichert, auch nicht gehasht. Gegen Spam
 * wirken stattdessen Honeypot, Längengrenzen und Cloudflares eigener
 * Bot-Schutz. Sollte das nicht reichen, ist Turnstile der nächste Schritt —
 * nicht das Protokollieren von Besuchern.
 */
export const prerender = false;

const MAX_NACHRICHT = 2000;
const MAX_EMAIL = 200;
const MAX_SEITE = 300;

const json = (daten: unknown, status = 200) =>
  new Response(JSON.stringify(daten), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });

export const POST: APIRoute = async ({ request }) => {
  const db = (env as any)?.DB;
  if (!db) {
    // Lokal ohne D1-Binding: nicht so tun, als wäre gespeichert worden.
    return json({ ok: false, fehler: "Speicher nicht verfügbar" }, 503);
  }

  let daten: Record<string, unknown>;
  try {
    daten = await request.json();
  } catch {
    return json({ ok: false, fehler: "Ungültige Anfrage" }, 400);
  }

  // Honeypot: Ein für Menschen unsichtbares Feld. Ist es ausgefüllt, war es
  // ein Bot. Wir antworten trotzdem mit 200, damit er es nicht erneut versucht.
  if (typeof daten.website === "string" && daten.website.trim() !== "") {
    return json({ ok: true });
  }

  const bewertung =
    daten.bewertung === "gut" || daten.bewertung === "schlecht" ? daten.bewertung : null;

  const nachricht =
    typeof daten.nachricht === "string" ? daten.nachricht.trim().slice(0, MAX_NACHRICHT) : "";

  const email =
    typeof daten.email === "string" ? daten.email.trim().slice(0, MAX_EMAIL) : "";

  const seite =
    typeof daten.seite === "string" ? daten.seite.trim().slice(0, MAX_SEITE) : "/";

  const quelle = daten.quelle === "widget" ? "widget" : "artikel";

  // Eine Rückmeldung ohne Bewertung und ohne Text hat keinen Inhalt.
  if (!bewertung && !nachricht) {
    return json({ ok: false, fehler: "Keine Rückmeldung übermittelt" }, 400);
  }

  // Wenn eine E-Mail angegeben wurde, muss sie wenigstens plausibel sein —
  // sonst lieber nichts speichern als etwas Unbrauchbares.
  const emailOk = email === "" || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
  if (!emailOk) {
    return json({ ok: false, fehler: "E-Mail-Adresse sieht nicht gültig aus" }, 400);
  }

  try {
    await db
      .prepare(
        `INSERT INTO feedback (erstellt_am, seite, bewertung, nachricht, email, quelle)
         VALUES (?, ?, ?, ?, ?, ?)`,
      )
      .bind(
        new Date().toISOString(),
        seite,
        bewertung,
        nachricht || null,
        email || null,
        quelle,
      )
      .run();
  } catch {
    return json({ ok: false, fehler: "Speichern fehlgeschlagen" }, 500);
  }

  return json({ ok: true });
};
