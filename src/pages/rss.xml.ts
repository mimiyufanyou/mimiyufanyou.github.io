import rss from "@astrojs/rss";
import type { APIContext } from "astro";
import { getWriting } from "../data";
import { SITE } from "../site";

export async function GET(context: APIContext) {
  const posts = await getWriting();
  return rss({
    title: SITE.name,
    description: SITE.description,
    site: context.site!,
    items: posts.map((p) => ({
      title: p.data.title,
      description: p.data.summary,
      pubDate: p.data.date,
      link: `/writing/${p.id}/`,
    })),
  });
}
