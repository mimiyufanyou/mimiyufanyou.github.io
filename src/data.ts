import { getCollection } from "astro:content";
import { showDrafts } from "./site";

export async function getPosts() {
  const posts = await getCollection("blog", (p) => showDrafts || !p.data.draft);
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export async function getProjects() {
  const items = await getCollection("projects", (w) => showDrafts || !w.data.draft);
  return items.sort((a, b) => a.data.order - b.data.order);
}

const fmt = (d: Date, o: Intl.DateTimeFormatOptions) =>
  d.toLocaleDateString("en-US", { ...o, timeZone: "UTC" });

export const longDate = (d: Date) => fmt(d, { year: "numeric", month: "long", day: "numeric" });
export const shortDate = (d: Date) => fmt(d, { month: "short", day: "2-digit" });
