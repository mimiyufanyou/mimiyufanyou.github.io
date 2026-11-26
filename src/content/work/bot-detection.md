---
title: "Telling bots from players across millions of daily events"
org: "Amazon Games"
years: "2023–2026"
summary: "Gradient-boosted bot detection in production, where every false positive is a real player locked out. Features from session timing, click patterns, device and network signals."
outcome: "Better detection precision and less manual review, weighed against the cost of flagging real players."
tools: ["XGBoost", "LightGBM", "SageMaker", "Airflow", "Redshift"]
order: 2
draft: true
---

## The problem

<!-- DRAFT: public-safe version, built only from the CV lines. Nothing here names a system, threshold or signal weight. -->

Bots distort a game's economy and its matchmaking, but a detector that's too eager bans paying players. The work sat between those two costs.

## What I did

- Built behavioural and network-level features: session timing, click patterns, device fingerprinting, and IP and request metadata.
- Deployed and iterated on XGBoost and LightGBM classifiers in production with the engineering team, shipping small improvements one at a time.
- Studied bot behaviour across large-scale traffic to find new signal sources and edge cases, which fed the next round of features.

## What changed

Model precision improved and the manual review queue shrank, with each change judged by its effect on legitimate players as well as on bots.
