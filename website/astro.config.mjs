// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import mdx from "@astrojs/mdx";

import { SITE } from "./src/config.js";

export default defineConfig({
  site: SITE.url,
  integrations: [
    mdx(),
    sitemap({
      // Affiliate redirects must never appear in the sitemap.
      filter: (page) => !page.includes("/go/"),
    }),
  ],
  build: { format: "directory" },
});
