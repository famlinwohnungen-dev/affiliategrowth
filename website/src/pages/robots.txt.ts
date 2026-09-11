import type { APIRoute } from "astro";
import { SITE } from "../config.js";

export const GET: APIRoute = () => {
  const body = SITE.indexable
    ? `User-agent: *
Allow: /
Disallow: /go/

Sitemap: ${SITE.url}/sitemap-index.xml
`
    : `# Vorab-Deploy: Impressum und Datenschutz noch nicht final.
# SITE.indexable in src/config.js auf true setzen, um freizugeben.
User-agent: *
Disallow: /
`;

  return new Response(body, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
};
