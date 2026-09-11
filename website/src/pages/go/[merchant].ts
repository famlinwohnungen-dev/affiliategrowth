import type { APIRoute, GetStaticPaths } from "astro";
import { MERCHANTS, merchantUrl } from "../../config.js";

/**
 * Affiliate redirect. Routing every outbound link through /go/<merchant>/ means
 * tracking URLs are defined once in config.js - when the Awin programmes are
 * approved, set trackingUrl there and every article updates at once.
 *
 * Emitted as a static meta-refresh page so it works on any static host.
 * robots.txt disallows /go/ and the sitemap excludes it.
 */
export const getStaticPaths: GetStaticPaths = () =>
  Object.keys(MERCHANTS).map((merchant) => ({ params: { merchant } }));

export const GET: APIRoute = ({ params }) => {
  const key = params.merchant as string;
  const target = merchantUrl(key);

  return new Response(
    `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0; url=${target}">
<link rel="canonical" href="${target}">
<title>Weiterleitung …</title>
</head>
<body>
<p>Du wirst weitergeleitet zu <a href="${target}" rel="sponsored nofollow noopener">${target}</a>.</p>
</body>
</html>`,
    { headers: { "Content-Type": "text/html; charset=utf-8" } },
  );
};
