---
title: "Teaching a local model to grade pictures the way I do"
org: "Independent"
years: "2026"
summary: "A self-hosted vision model checks generated illustrations before a person sees them. I wrote the grading rubric, labelled held-out cards, and measured agreement instead of trusting the model's confidence."
outcome: "Agreement with my grades rose from κ 0.11 to 0.47. The judge now catches 69% of bad cards, up from 21%."
tools: ["Python", "Ollama", "MLflow", "Docker", "ROCm"]
order: 4
draft: true
---

### The problem

<!-- DRAFT: from the 11-26 brief. Numbers are from the judge's model-monitoring registry. -->

Hundreds of generated illustrations needed checking: the right subject, whole, with nothing extra in frame. The first automated judge scored everything about the same, so a person still had to look at every card.

### What I did

- Wrote a rubric with two grades per card (the source photo and the repaint), each from p0 (unshippable) to p5.
- Labelled a held-out set of 189 cards by hand.
- Replaced a 0–100 score with plain yes/no questions per criterion, run on a self-hosted model on my own GPU server.
- Logged every run with the same metrics so a new model only replaces the current one when it wins on the same eval set.

### What changed

- Agreement with my grades (Cohen's κ) went from 0.106 to 0.468 on the 189 held-out cards.
- The judge catches 69% of bad cards instead of 21%.
- The cost: false flags rose from 7.5% to 18%. That trade is worth it here, because a false flag costs a glance and a missed bad card costs a reprint.
