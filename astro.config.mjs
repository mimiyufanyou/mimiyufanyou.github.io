import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://mimiyufanyou.com",
  // Pages build as about.html, blog/<slug>.html …, so they're served at /about and
  // /blog/<slug>: the same addresses the old Jekyll site used.
  build: { format: "file" },
  trailingSlash: "never",
  integrations: [sitemap()],
  markdown: {
    shikiConfig: { theme: "github-light" },
  },
});
