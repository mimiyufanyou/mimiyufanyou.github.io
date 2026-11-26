import { getCollection } from "astro:content";
import { showDrafts } from "./site";

export async function getWriting() {
  const posts = await getCollection("writing", (p) => showDrafts || !p.data.draft);
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export async function getWork() {
  const items = await getCollection("work", (w) => showDrafts || !w.data.draft);
  return items.sort((a, b) => a.data.order - b.data.order);
}

export const fmtDate = (d: Date) =>
  d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric", timeZone: "UTC" });
