import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Blog posts. `draft: true` shows in `npm run dev` only, never in the build.
const writing = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/writing" }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    date: z.coerce.date(),
    image: z.string().optional(),
    tags: z.array(z.string()).default([]),
    wip: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

// Case studies. `order` sorts them on the home page (lowest first).
const work = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/work" }),
  schema: z.object({
    title: z.string(),
    org: z.string(),
    years: z.string(),
    summary: z.string(),
    outcome: z.string(),
    tools: z.array(z.string()).default([]),
    order: z.number().default(99),
    draft: z.boolean().default(false),
  }),
});

export const collections = { writing, work };
