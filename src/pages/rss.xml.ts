import rss from "@astrojs/rss";
import type { APIContext } from "astro";
import { getPosts } from "../data";
import { SITE } from "../site";

export async function GET(context: APIContext) {
  const posts = await getPosts();
  return rss({
    title: SITE.name,
    description: SITE.description,
    site: context.site!,
    items: posts.map((p) => ({
      title: p.data.title,
      description: p.data.summary,
      pubDate: p.data.date,
      link: `/blog/${p.id}`,
    })),
  });
}
