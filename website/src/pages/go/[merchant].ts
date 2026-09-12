import type { APIRoute, GetStaticPaths } from "astro";
import { MERCHANTS, merchantUrl, CF_ANALYTICS_TOKEN } from "../../config.js";

/**
 * Affiliate-Weiterleitung. Jeder ausgehende Link läuft über /go/<merchant>/,
 * damit die Ziel-URLs an genau einer Stelle stehen: config.js. Nach der
 * Awin-Freigabe dort `trackingUrl` eintragen — alle Artikel ziehen mit.
 *
 * Die Seite wird als statisches Meta-Refresh ausgeliefert und funktioniert
 * damit auf jedem Hoster. robots.txt sperrt /go/, die Sitemap lässt es aus.
 *
 * Der Analytics-Beacon liegt hier bewusst mit drin: Ohne ihn wäre ein
 * Affiliate-Klick in der Statistik unsichtbar — und genau dieser Klick ist
 * die Kennzahl, auf die es ankommt. Die Verzögerung von 1 Sekunde gibt dem
 * Beacon Zeit, den Aufruf zu melden, bevor der Browser weiterspringt.
 */
export const getStaticPaths: GetStaticPaths = () =>
  Object.keys(MERCHANTS).map((merchant) => ({ params: { merchant } }));

export const GET: APIRoute = ({ params }) => {
  const key = params.merchant as string;
  const target = merchantUrl(key);
  const escaped = target.replace(/"/g, "&quot;");

  const beacon = CF_ANALYTICS_TOKEN
    ? `<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token":"${CF_ANALYTICS_TOKEN}"}'></script>`
    : "";

  // Ohne Beacon keine Wartezeit — dann sofort weiterleiten.
  const verzoegerung = CF_ANALYTICS_TOKEN ? "1" : "0";

  return new Response(
    `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="${verzoegerung}; url=${escaped}">
<link rel="canonical" href="${escaped}">
<title>Weiterleitung …</title>
<style>
  body{font-family:system-ui,sans-serif;margin:0;min-height:100vh;display:grid;
       place-items:center;color:#4a5856;background:#f4f6f6}
  a{color:#0e6e62}
  @media (prefers-color-scheme:dark){body{background:#0d1213;color:#a8b7b4}a{color:#45a899}}
</style>
${beacon}
</head>
<body>
<p>Du wirst weitergeleitet … <a href="${escaped}" rel="sponsored nofollow noopener">Weiter zum Anbieter</a></p>
</body>
</html>`,
    { headers: { "Content-Type": "text/html; charset=utf-8" } },
  );
};
