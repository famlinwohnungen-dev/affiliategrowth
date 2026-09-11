import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const artikel = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/artikel" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    // The keyword this article targets, straight from content/PLAN.md.
    keyword: z.string(),
    published: z.coerce.date(),
    updated: z.coerce.date().optional(),
    // "vergleich" gets Review schema; "ratgeber" gets plain Article schema.
    type: z.enum(["vergleich", "ratgeber", "test"]).default("vergleich"),
    // Merchant keys from src/config.js, in the order they're discussed.
    merchants: z.array(z.string()).default([]),
    // Recommended product for comparison articles - drives the verdict box.
    empfehlung: z.string().optional(),
    faq: z
      .array(z.object({ frage: z.string(), antwort: z.string() }))
      .default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { artikel };
