# mimiyufanyou.com

Personal site, built with [Astro](https://astro.build). Replaces the old Jekyll theme site.

```bash
npm install
npm run dev      # http://localhost:4321 — drafts show here
npm run build    # static site in dist/ — drafts left out
```

- Blog posts: `src/content/writing/*.md`
- Case studies: `src/content/work/*.md` (`order` sorts them; `draft: true` keeps one off the live site)
- Interactive Plotly/Folium charts: `public/charts/*.html`, embedded with `<figure class="chart"><iframe …>`
- Shared words and links: `src/site.ts`
