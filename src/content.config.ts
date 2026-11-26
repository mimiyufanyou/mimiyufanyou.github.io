import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Blog posts. The file name is the URL: blog/2024-01-20-cooperative-strategies.md
// → /blog/2024-01-20-cooperative-strategies (same address as the old Jekyll site).
// `draft: true` shows in `npm run dev` only, never in the build.
const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    date: z.coerce.date(),
    image: z.string().optional(),
    wip: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

// Personal projects. Each links out to its own site; `order` sorts them (lowest first).
const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: z.object({
    title: z.string(),
    url: z.string().url(),
    years: z.string(),
    summary: z.string(),
    image: z.string(),
    order: z.number().default(99),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog, projects };
