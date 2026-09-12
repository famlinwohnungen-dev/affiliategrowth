// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import mdx from "@astrojs/mdx";
import cloudflare from "@astrojs/cloudflare";

import { SITE } from "./src/config.js";

export default defineConfig({
  site: SITE.url,

  // Alle Seiten bleiben vorgerendert wie bisher. Nur einzelne Routen mit
  // `export const prerender = false` laufen serverseitig — konkret
  // /api/feedback. Der Rest der Seite bleibt statisches HTML.
  output: "static",
  adapter: cloudflare({ imageService: "passthrough" }),

  integrations: [
    mdx(),
    sitemap({
      // Weiterleitungen und API gehören nicht in die Sitemap.
      filter: (page) => !page.includes("/go/") && !page.includes("/api/"),
    }),
  ],
  build: { format: "directory" },
});
