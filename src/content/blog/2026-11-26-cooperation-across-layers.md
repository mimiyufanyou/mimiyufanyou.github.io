---
title: "Cooperation Across Layers: The Prisoner's Dilemma on Grids, Coupled Networks and Multiplexes"
summary: "Who you play with matters as much as how you play. Simulating the Prisoner's Dilemma on one grid, on two coupled grids, and on several layers at once, following the network-reciprocity research."
date: 2026-11-26
image: /img/multilayer_banner.png
draft: true
---

![Cooperators (yellow) and defectors (purple) after 1,000 steps: one grid on the left, one of two coupled grids on the right](/img/multilayer_banner.png)

The first two posts in this series ([part 1](/blog/2024-01-20-cooperative-strategies), [part 2](/blog/2026-11-26-noise-forgiveness-extortion)) had everyone meet everyone. In a tournament every strategy plays every other, and in the replicator equation each strategy meets the whole population in proportion to its share. Real life is lumpier. We mostly deal with neighbours, coworkers and family, and we belong to several of those circles at once.

Part 1 listed a **multi-layer cooperative network simulation** as a next step. This post builds one, in three stages that follow the research: one grid, two coupled grids, and the same people on several grids at once.

### The Setup

Everything here uses the same small game, the "weak" Prisoner's Dilemma of Nowak and May (1992). Two cooperators each get 1. A defector who meets a cooperator gets **b**, the temptation, which is a little more than 1. Everything else pays 0. The bigger b is, the more defection pays.

Each player sits on a square grid and plays its four neighbours (up, down, left and right, wrapping round at the edges). Nobody has a clever strategy any more: each player simply cooperates or defects. What changes is who copies whom. After each round a player picks a random neighbour and copies its choice with a probability that rises the better that neighbour did:

```
P(copy) = 1 / (1 + exp((my_payoff - their_payoff) / K))
```

This is the Fermi rule of Szabó and Tőke (1998). K is how noisy the copying is; I use K = 0.1, the usual choice. Every grid starts half cooperators and half defectors at random, and runs for 1,500 Monte Carlo steps (about one chance to change per player per step). The numbers below average the last 300 steps. The sweeps use 60 × 60 grids (three runs per point for one grid, one run per point for the rest), and the pictures use 100 × 100. The simulation is about a hundred lines of plain numpy, in the site's repository under `analysis/`.

### One Grid: Cooperators Survive in Clusters

In a well-mixed population a defector always out-earns a cooperator, so cooperation dies whatever b is. On a grid it doesn't, because cooperators can form clumps. A cooperator in the middle of a clump earns 4 from four cooperating neighbours. A defector on the edge can only exploit the one or two cooperators it touches. Nowak and May (1992) showed this with their spatial games, and the effect is now usually called **network reciprocity**. Ohtsuki and colleagues (2006) later boiled it down to a simple rule for many kinds of networks: cooperation can win when the benefit it gives outweighs its cost by more than the number of neighbours each player has.

<figure class="chart">
  <iframe src="/charts/ml_lattice.html" title="Yellow cooperates, purple defects" loading="lazy" style="height:450px"></iframe>
  <figcaption>Press Play, or drag the slider. Left: one grid at b = 1.03. Right: one of two coupled grids (more below) at the much higher temptation b = 1.10.</figcaption>
</figure>

On the left, the random start breaks up within ten steps, and the survivors pull together into clumps that hold their ground. But the protection only goes so far.

<figure class="chart">
  <iframe src="/charts/ml_single.html" title="One layer: cooperation against temptation" loading="lazy" style="height:420px"></iframe>
  <figcaption>Share of the grid cooperating at each temptation b, averaged over three runs.</figcaption>
</figure>

At b = 1.00, 64% of the grid cooperates. At b = 1.03 it's 22%, and by b = 1.05 cooperation is gone. A 5% bonus for defecting is enough to wear down every clump. That sharp edge is what Szabó and Tőke (1998) found with this rule, and it's the baseline the next two setups try to beat.

### Two Coupled Grids: Caring About Your Other Self

Now give every player a counterpart on a second grid: the same person in a different setting, like work and home. Each grid plays its own game and strategies only spread within a grid, but a player's success now mixes both:

```
utility = (1 - α) × my_payoff + α × my_partner's_payoff_on_the_other_grid
```

α is how much the two lives are tied together. At α = 0 they're independent grids, and at α = 0.8 a player cares mostly about how its other self is doing. This follows the interdependent-network work of Wang, Szolnoki and Perc (2012, 2013), which uses utilities that mix a player's own payoff with its partner's on another network.

<figure class="chart">
  <iframe src="/charts/ml_interdependent.html" title="Two coupled layers" loading="lazy" style="height:520px"></iframe>
  <figcaption>Share cooperating on two coupled grids at each temptation b, one line per coupling strength α. α = 0 is two independent grids.</figcaption>
</figure>

The coupling stretches how far cooperation survives, and the stronger the coupling, the further:

| Coupling α | Highest b with over 5% cooperating | Cooperating at b = 1.10 |
| --- | --- | --- |
| 0 (independent) | b = 1.02 | 0% |
| 0.2 | b = 1.06 | 0% |
| 0.4 | b = 1.12 | 30% |
| 0.6 | b = 1.18 | 56% |
| 0.8 | b = 1.24 | 58% |

At α = 0.8, cooperation lasts to a temptation twelve times further above 1 than on a single grid (b = 1.24 against 1.02).

The two curves below show why. Both start the same way.

<figure class="chart">
  <iframe src="/charts/ml_over_time.html" title="Cooperation over time" loading="lazy" style="height:480px"></iframe>
  <figcaption>Share cooperating at each step (log scale). Grey: one grid. Teal: two coupled grids with α = 0.5.</figcaption>
</figure>

At b = 1.10 a single grid collapses: 36% cooperate after one step, 9% after ten, none by step 100. The coupled grids fall too, to 24% by step 10, the same early slump as the single grid at b = 1.03. Then they recover, climbing back to about 44% and holding there. A cooperator in a struggling clump on one grid is propped up by its partner's success on the other, which buys the clump time to grow. Each grid's reciprocity spills over to the other, the idea behind the "interdependent network reciprocity" of Wang, Szolnoki and Perc's (2013) title.

### Many Layers: The Same People in Several Circles

The last setup is a **multiplex**: the same players on M grids at once, shuffled so each grid gives them different neighbours. A player can cooperate on one grid and defect on another, but its fitness is its total over all of them. Gómez-Gardeñes and colleagues (2012) studied exactly this kind of network and found that cooperation grows more resilient as layers are added.

<figure class="chart">
  <iframe src="/charts/ml_multiplex.html" title="The same players on several layers" loading="lazy" style="height:520px"></iframe>
  <figcaption>Share cooperating, averaged over all layers, at each temptation b. One line per number of layers.</figcaption>
</figure>

My runs agree. One layer matches the single grid above, nearly gone by b = 1.04. Two layers keep cooperation to b = 1.12. With three layers, 24% still cooperate at b = 1.20, the edge of the sweep, and with five layers 37% do. At b = 1.10, cooperation goes from 0% on one layer to 43% on two, 69% on three and 76% on five.

Total fitness is what does it. A player who does well in one circle carries that success into every circle where others might copy it. A defector who wins on one grid by exploiting a few neighbours has to carry its losses from the other grids too.

### What I Take From It

Part 2 found that the right amount of forgiveness rescues cooperation when signals get noisy. This round finds a second rescue that has nothing to do with strategy: **structure**. The same naive players, who can only copy whoever did better, keep cooperating at temptations that wipe them out on their own, as long as their lives span more than one network and what happens in one carries over to the others.

It's a tidy picture of why community ties matter. Someone who is a colleague, a neighbour and a parent at the same school has reputations in several places at once. Cheating in one circle costs something in the others, and cooperation in one is backed up by the others.

### Next Steps

+ **Elinor Ostrom's design principles:** the original goal from part 1. Swap the pairwise game for a public goods game (a shared pot that multiplies contributions) and add Ostrom's (1990) monitoring and graduated sanctions on one layer, to see whether rules on one network protect commons on another
+ **Growing networks:** Li and Sun (2021) let a multilayer network grow as new players join, closer to how real communities form
+ **Uneven networks:** real social networks have hubs. Santos and Pacheco (2005) found that scale-free networks, where a few players have many links, favour cooperation on their own
+ **Smarter players on the layers:** put part 2's Generous Tit For Tat on the coupled grids, so forgiveness and structure work together

### Papers Referenced

Gómez-Gardeñes, J., Reinares, I., Arenas, A., & Floría, L. M. (2012). Evolution of cooperation in multiplex networks. *Scientific Reports, 2*, 620. https://doi.org/10.1038/srep00620

Li, G., & Sun, X. (2021). Evolutionary game on a growing multilayer network. *Physica A: Statistical Mechanics and Its Applications, 578*, 126110. https://doi.org/10.1016/j.physa.2021.126110

Nowak, M. A., & May, R. M. (1992). Evolutionary games and spatial chaos. *Nature, 359*(6398), 826–829. https://doi.org/10.1038/359826a0

Ohtsuki, H., Hauert, C., Lieberman, E., & Nowak, M. A. (2006). A simple rule for the evolution of cooperation on graphs and social networks. *Nature, 441*(7092), 502–505. https://doi.org/10.1038/nature04605

Ostrom, E. (1990). *Governing the commons: The evolution of institutions for collective action*. Cambridge University Press.

Santos, F. C., & Pacheco, J. M. (2005). Scale-free networks provide a unifying framework for the emergence of cooperation. *Physical Review Letters, 95*(9), 098104. https://doi.org/10.1103/PhysRevLett.95.098104

Szabó, G., & Tőke, C. (1998). Evolutionary prisoner's dilemma game on a square lattice. *Physical Review E, 58*(1), 69–73. https://doi.org/10.1103/PhysRevE.58.69

Wang, Z., Szolnoki, A., & Perc, M. (2012). Evolution of public cooperation on interdependent networks: The impact of biased utility functions. *EPL, 97*(4), 48001. https://doi.org/10.1209/0295-5075/97/48001

Wang, Z., Szolnoki, A., & Perc, M. (2013). Interdependent network reciprocity in evolutionary games. *Scientific Reports, 3*, 1183. https://doi.org/10.1038/srep01183

Wang, Z., Wang, L., Szolnoki, A., & Perc, M. (2015). Evolutionary games on multilayer networks: A colloquium. *The European Physical Journal B, 88*(5), 124. https://doi.org/10.1140/epjb/e2015-60270-7
