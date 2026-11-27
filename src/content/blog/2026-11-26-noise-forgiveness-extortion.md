---
title: "Noise, Forgiveness and Extortion: Iterated Prisoner's Dilemma, Part 2"
summary: "Picking up part 1's next steps: what miscommunication does to Tit For Tat, how much forgiveness pays, and why extortionate zero-determinant strategies win their matches but lose the tournament."
date: 2026-11-26
image: /img/ipd2_evolution_banner.png
draft: true
---

![Population share of each strategy across 80 generations, with 5% noise and zero-determinant strategies in the mix](/img/ipd2_evolution_banner.png)

In [part 1](/blog/2024-01-20-cooperative-strategies) I recreated Axelrod's (1980) first tournament and watched cooperative strategies take over the population. That post ended with a list of next steps. This one works through three of them: a **noise or miscommunication parameter**, **zero-determinant (ZD) strategies**, and **randomized initial populations**.

The setup is the same as before: the Axelrod Python library, the fifteen strategies from the first tournament, 100 turns a match, and Plotly for the charts. The code and the raw results live in the site's repository under `analysis/`, so every number here can be rerun.

### Why Noise Matters

Axelrod's tournaments were clean. Every move landed exactly as intended. Real relationships aren't like that: a message is misread, a delivery is late, someone meant to cooperate and it came across as a slight. In the library, **noise** is the chance that any single move is flipped from cooperate to defect, or the other way, before the other player sees it.

Noise is hard on Tit For Tat. Two Tit For Tat players cooperate forever until one move is flipped. Then the first player retaliates, the second retaliates for the retaliation, and they echo defections back and forth until another flip happens to break the cycle. One mistake, endless revenge.

<figure class="chart">
  <iframe src="/charts/ipd2_noise.html" title="The first tournament, replayed with noise" loading="lazy"></iframe>
  <figcaption>The first tournament with 0% to 20% noise, 30 repetitions at each level. Tit For Tat is the thick orange line. Click names in the legend to hide them.</figcaption>
</figure>

Without noise, Tit For Tat finishes second of fifteen here, with a median of 2.59 points a turn. At 1% noise, one flipped move in every hundred, it drops to sixth. By 5% it's eighth, and at 20% ninth. The strategies that rise are the ones that hold steady when signals get messy: **Downing**, which models its opponent's responses instead of copying their last move, wins every level from 2% upward, and **Grudger**, which never forgives a defection, climbs from sixth to second. When noise turns everything into mutual defection, never trusting again stops being a cost.

### How Much Should You Forgive?

The obvious fix is forgiveness. **Generous Tit For Tat** (Nowak & Sigmund, 1992) plays Tit For Tat, but after the opponent defects it cooperates anyway with some probability *p*. Forgive too little and you're stuck in echo chains. Forgive too much and you're simply exploited.

Molander (1985) worked out the balance on paper. With Axelrod's payoffs (3 each for cooperating, 5 for a successful defection, 0 for being exploited, 1 each for mutual defection), the best level of generosity for a Tit For Tat player in a noisy world is

```
p = min(1 - (T - R) / (R - S), (R - P) / (T - P)) = min(1/3, 1/2) = 1/3
```

That made it something I could test. I ran Generous Tit For Tat at every generosity from 0% to 60%, against a copy of itself and against all fifteen first-tournament strategies, at five noise levels.

<figure class="chart">
  <iframe src="/charts/ipd2_forgiveness.html" title="How much should Tit For Tat forgive?" loading="lazy" style="height:560px"></iframe>
  <figcaption>Mean score per turn of Generous Tit For Tat by generosity, one line per noise level. Use the buttons to switch opponents. The dashed line is Molander's one third.</figcaption>
</figure>

**Against a copy of itself**, a little forgiveness goes a long way. At 1% noise, plain Tit For Tat earns 2.63 a turn. Forgiving just 5% of defections brings it to 2.88, close to the 3.0 of perfect cooperation. More forgiveness keeps helping, because the only opponent is another forgiver.

**Against the whole field**, there's a peak. With no noise, the best generosity is 30%. With 1% noise it's 35%, and with 10% it's 30% again. Past about 50% scores fall in every case, because the defectors in the field start to exploit the forgiveness. Molander's one third sits on the flat top of the curve for every noise level up to 10%.

The exception is 20% noise. There, one move in five is flipped and generosity barely matters: every setting scores between 1.98 and 2.12. When communication is that broken, no amount of forgiveness can tell an honest mistake from a real betrayal.

### Zero-Determinant Strategies: Winning the Match, Losing the Game

Press and Dyson (2012) showed that a player who remembers only the last move can set its own probabilities so that the opponent's score is tied to its own by a straight line, whatever the opponent does. One family, the **extortionate** strategies, guarantees that every point the opponent gains above mutual defection earns the extortioner two (ZD-Extort-2) or four (ZD-Extort-4). Against any one opponent, the extortioner can't lose.

I added four ZD strategies to the first tournament (two extortioners, the generous ZD-GTFT-2, and ZD-SET-2, which fixes the opponent's score), plus Generous Tit For Tat at Molander's one third.

<figure class="chart">
  <iframe src="/charts/ipd2_zd.html" title="Winning matches is not winning the tournament" loading="lazy" style="height:620px"></iframe>
  <figcaption>Each point is one strategy: the share of its matches it won outright against the share of points it earned. Orange diamonds are the five new entrants. Switch between no noise and 5% noise with the buttons.</figcaption>
</figure>

Without noise, **ZD-Extort-4 wins 95% of its matches and finishes 17th of 20**. Generous Tit For Tat wins none of its matches and finishes **first**, with ZD-GTFT-2, the generous zero-determinant strategy, second. This is Axelrod's "non-envious" principle from part 1, in numbers: an extortioner beats each opponent by dragging both of them down, so it collects small wins over small totals. The generous players lose narrowly in matches where both sides score well.

With 5% noise the field reshuffles. Downing comes first, Generous Tit For Tat and ZD-GTFT-2 stay second and third, and ZD-Extort-4 rises to ninth, because noise pulls everyone toward mutual defection, where an extortioner loses little.

### Evolution, With Extortioners in the Pool

Next I put those payoffs through the same replicator rule as part 1, where each generation's payoff multiplies its share of the population:

```
fitness[i] += sum(payoff) * population[j]
```

I used the 5% noise tournament, the harder case, with all twenty strategies starting at an equal 5% share.

<figure class="chart">
  <iframe src="/charts/ipd2_evolution.html" title="Evolution with ZD strategies and 5% noise" loading="lazy" style="height:580px"></iframe>
  <figcaption>Share of the population by generation, starting equal. Hover for each strategy's share.</figcaption>
</figure>

The extortioners never grow. Both start shrinking from the first generation, and they're under 1% of the population by generation 21 (ZD-Extort-2) and 32 (ZD-Extort-4). Grudger is gone even sooner, by generation 19. Downing, the tournament winner at this noise level, grows to 13% around generation 19 and then fades, because once the exploitable strategies are gone there's nothing left for it to feed on. By generation 25 the two generous strategies hold over half the population, and by generation 150 they hold 96%: Generous Tit For Tat 53%, ZD-GTFT-2 43%.

This is what Stewart and Plotkin (2013) found and named in their title, *From extortion to generosity*. Extortion can win a single encounter, but in a population it meets itself and its own victims too often to grow. Generosity is what survives.

### Randomized Starting Populations

The last item from part 1's list: does the ending depend on the start? I reran the evolution from 500 random starting populations, drawn evenly across all possible mixes of the twenty strategies.

<figure class="chart">
  <iframe src="/charts/ipd2_random_starts.html" title="Who ends up largest, from random starts" loading="lazy" style="height:280px"></iframe>
  <figcaption>The strategy holding the largest share after 150 generations, across 500 random starting populations.</figcaption>
</figure>

Only two strategies ever finish on top. Generous Tit For Tat does in 61% of runs and ZD-GTFT-2 in the other 39%. Neither extortioner, nor Downing, nor any other first-tournament strategy, finishes largest from any of the 500 starts.

### What I Take From It

Part 1 ended with age-old wisdom about forgiveness, and this round puts a number on it. When signals are noisy, strict reciprocity falls apart. Forgiving roughly a third of the time is enough to recover cooperation without inviting exploitation, which is what Molander predicted on paper four decades ago. And strategies that win by keeping the other side down, however reliably they win head to head, don't last in a population that meets them again and again.

The 20% noise result is the sober one. Past a certain level of miscommunication, no strategy rescues cooperation. The fix there isn't a better strategy but a clearer signal: **clarity**, the last principle on part 1's list.

### Next Steps

+ **Noise in the evolution, not only the payoffs:** a Moran process, where individuals reproduce one at a time and chance matters, instead of the smooth replicator rule
+ **Adaptive forgiveness:** strategies that estimate the noise level from what they observe and set their generosity to match
+ **Memory:** longer memories (Turker & Bingol, 2021) under noise, and whether forgetting helps
+ **Networks:** the multi-layer and spatial versions from part 1's reading list, where you only meet your neighbours

### Papers Referenced

Axelrod, R. (1980). Effective choice in the Prisoner's Dilemma. *Journal of Conflict Resolution, 24*(1), 3–25. https://doi.org/10.1177/002200278002400101

Knight, V., Campbell, O., Harper, M., Langner, K., et al. (2016). An open framework for the reproducible study of the Iterated Prisoner's Dilemma. *Journal of Open Research Software, 4*(1), e35. https://doi.org/10.5334/jors.125

Molander, P. (1985). The optimal level of generosity in a selfish, uncertain environment. *Journal of Conflict Resolution, 29*(4), 611–618. https://doi.org/10.1177/0022002785029004004

Nowak, M. A., & Sigmund, K. (1992). Tit for tat in heterogeneous populations. *Nature, 355*(6357), 250–253. https://doi.org/10.1038/355250a0

Press, W. H., & Dyson, F. J. (2012). Iterated Prisoner's Dilemma contains strategies that dominate any evolutionary opponent. *Proceedings of the National Academy of Sciences, 109*(26), 10409–10413. https://doi.org/10.1073/pnas.1206569109

Stewart, A. J., & Plotkin, J. B. (2013). From extortion to generosity, evolution in the Iterated Prisoner's Dilemma. *Proceedings of the National Academy of Sciences, 110*(38), 15348–15353. https://doi.org/10.1073/pnas.1306246110

Turker, M. Z., & Bingol, H. (2021). Forgiveness is an adaptation in iterated prisoner's dilemma with memory. *arXiv preprint arXiv:2112.07894*. https://arxiv.org/abs/2112.07894
