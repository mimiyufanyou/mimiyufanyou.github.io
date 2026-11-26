# mimiyufanyou.com

Personal site, built with [Astro](https://astro.build). Replaces the old Jekyll site and keeps its look (The Plain theme) and its addresses.

```bash
npm install
npm run dev      # http://localhost:4321 — drafts show here
npm run build    # static site in dist/ — drafts left out
```

- Blog posts: `src/content/blog/*.md` (file name = URL, same as the old Jekyll site)
- Projects: `src/content/projects/*.md` (`order` sorts them; `draft: true` keeps one off the live site)
- Interactive Plotly/Folium charts: `public/charts/*.html`, embedded with `<figure class="chart"><iframe …>`
- Shared words and links: `src/site.ts`
