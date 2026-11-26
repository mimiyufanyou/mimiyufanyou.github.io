---
title: "A work desk where AI agents pick up tickets, and a person still decides"
org: "Independent"
years: "2026"
summary: "A ticket board that starts coding agents on work I've approved, routes each ticket to a model by size, and stops at review gates before anything ships."
outcome: "93 tickets through the gate in one week for $201. Small tickets cost $1.21 each on the smaller model against $4.07 on the largest."
tools: ["Claude Code", "TypeScript", "Next.js", "Postgres", "Supabase"]
order: 3
draft: true
---

## The problem

<!-- DRAFT: from the 11-26 brief. Numbers are from the live board. The product it serves is deliberately not named. -->

I run a small product alone. The work was piling up in chat sessions: each small fix done inside a long, expensive conversation, with no record of what was asked, who did it, or what it cost.

## What I did

- Built a board where every piece of work is a ticket with a size, an area and an owner.
- A timer (no model involved) starts an agent session for each ticket I've marked Ready, choosing the model by ticket size.
- Agents work on their own branch, attach proof, and stop at review. Nothing reaches production without my word.
- Every session's token use is counted, so each ticket carries its own cost.

## What changed

- In one week the gate ran 100 sessions on 93 tickets; 74 reached Done.
- The whole week cost $201. A ticket averaged $1.21 on the smaller model and $4.07 on the largest, so routing by size mattered.
- Since late October, 142 tasks have reached Done: 108 by agents, 34 by me.
