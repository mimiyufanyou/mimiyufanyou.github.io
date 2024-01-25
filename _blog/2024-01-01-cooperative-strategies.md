---
title: Dominance of Cooperative Strategies in Iterated Prisoner's Dilemma with Axelrod Python Library 
type: blog
date: 2024-01-20
imageurl: /Iterated_Prisoners_Dilemma_Venn-Diagram.png
authors: Mimi Yufan You
---

### Introduction: The Iterated Game's Intrigue

The Iterated Prisoner's Dilemma (IPD) transcends its simple, two-player, non-zero-sum game structure, presenting a complex tableau of human interaction, trust, and betrayal. Unlike its one-shot counterpart, the IPD unfolds over numerous rounds, allowing players to adapt strategies based on their opponent's previous actions. This dynamic elevates the IPD from a mere theoretical construct to a powerful tool for understanding behaviors in economics, politics, and social sciences.

### The Core Principles: Repeated Encounters and Strategy Evolution

Foundation of the Dilemma: Each round of the IPD involves two players independently deciding whether to cooperate or defect. The highest collective payoff arises from cooperation, yet the individual temptation to defect for greater personal gain persists, risking mutual betrayal and the lowest payoff.

Iterative Nature: The essence of the IPD lies in its repetition. Players remember past actions and modify strategies, fostering a complex interplay of trust, prediction, and potential retaliation.

Strategy Evolution: Over iterations, strategies evolve. Tit-for-tat, a strategy of mirroring the opponent's previous move, emerged as an effective approach in early computer tournaments organized by Robert Axelrod. Its success highlighted the importance of reciprocity in the IPD.

![IPD](https://upload.wikimedia.org/wikipedia/commons/d/d6/Iterated_Prisoners_Dilemma_Venn-Diagram.svg)
[^1]: Image Credit: Jplotkin8, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons

### History: Recreating the First Tournament 

In Axelrod's seminal work, "The Evolution of Cooperation" he outlined four common characteristics of winning strategies in IPD: 

+ **Nice:** The strategy will not defect before its opponent does (this is sometimes referred to as an "optimistic" algorithm). Almost all the top-scoring strategies were nice. A purely selfish strategy will not "cheat" on its opponent for purely self-interested reasons first.
+ **Retaliating:** The strategy must sometimes retaliate. An example of a non-retaliating strategy is Always Cooperate, a very bad choice that will frequently be exploited by "nasty" strategies.
+ **Forgiving:** Successful strategies must be forgiving. Though players will retaliate, they will cooperate again if the opponent does not continue to defect. This can stop long runs of revenge and counter-revenge, maximizing points.
+ **Non-envious:** The strategy must not strive to score more than the opponent.
+ **Clarity:** Communication is key for cooperation. This is one aspect I would like to explore further with a miscommunication transformer. 

In Robert Axelrod's original Prisoner's Dilemma tournament, as detailed in his 1980 paper "Effective Choice in the Prisoner’s Dilemma," the specific setup for repetitions and turns was not rigidly fixed. Instead, the tournament was structured to simulate an indefinite number of interactions, reflecting the real-world scenario where individuals cannot be certain about how many times they will interact with others.

To achieve this, Axelrod used a probabilistic approach. Each pair of strategies would play against each other for an indefinite number of turns, with the game having a fixed probability of ending after each turn. This approach effectively simulated an environment where the players could not predict the exact number of interactions they would have, thus encouraging strategies that were robust over a range of possible game lengths.

The probability chosen meant that the expected number of turns in each encounter was 200, but the actual number varied, introducing uncertainty and encouraging participants to develop strategies that could adapt to both short-term and long-term interactions. This design was crucial in evaluating the effectiveness of various strategies in a setting that closely mimics the unpredictability of real-life interactions.

Using the Axelrod library available here:  <https://axelrod.readthedocs.io/en/stable/index.html> we can simulate Axelrod's infamous first tournament using the original set of strategies submitted handily with _axelrod.axelrod_first_strategies_ I've used the Plotly Express library for visualizations instead of the Axelrod plotting functions based on personal preference and interactivity. With the luxury of processing power now but a fairly low amount of patience to watch things run, I set the tournament to 100 turns with 1000 repetitions. 

#### Strategies from Axelrod's First Tournament 
<div>
<iframe title="Strategies from Axelrod's First Tournament" 
        src="https://rawcdn.githack.com/mimiyufanyou/mimiyufanyou.github.io/aead09bceac0697fcca991c430071aa2cd956dcf/assets/axelrod_first_tournament.html"
        style="width: 100%; 
               height: 500px; 
               border: none;">
</iframe>
</div>

[^1]: Axelrod Library: <https://axelrod.readthedocs.io/en/stable/index.html> 

While we can see how the top individual strategies performed above, which are already colored by their overall cooperation rating, summarizing the tournament results by cooperation rating bins here, we can show the results even more concisely. 

#### Median Score by Binned Cooperation Rating 
<div>
<iframe title="Median Score by Binned Cooperation Rating" 
        src="https://rawcdn.githack.com/mimiyufanyou/mimiyufanyou.github.io/423719743c4597729efa2922d498f0ca64db14e0/assets/cooperation_ratings.html"
        style="width: 100%; 
               height: 500px; 
               border: none;">
</iframe>
</div>

### ESS - An Evolutionarily Stable Strategy
While in the short term depending on the tournament parameters, a variety of strategies can succeed, given continued repetition and rounds, Tit-for-Tat and a crop of other strategies that generally abide by Axelrod's outlined characteristics, echoing Tit-for-Tat's retaliatory but cooperative leaning, emerging more consistently than strategies of any other extremes. 

The concept of an Evolutionarily Stable Strategy (ESS) is pivotal in understanding the dynamics of the Iterated Prisoner's Dilemma (IPD). Originating from evolutionary biology and later adopted into game theory, ESS provides a framework for analyzing strategies that persist over time under evolutionary pressure.

Many notable ESS are retaliatory but also generous - especially in noisy environments where there are high degrees of miscommunication. 

### Defining ESS
An ESS, in the context of the IPD, is a strategy that, if adopted by a population, cannot be invaded or replaced by an alternative strategy. It's a strategy that, when prevalent in a group, proves to be the most effective against its own kind. The resilience of an ESS comes from its ability to outperform or neutralize alternative strategies, ensuring its dominance over time.

### ESS in the IPD: 
In the IPD, strategies evolve through repeated interactions, influenced by the outcomes of previous encounters. A strategy becomes an ESS if it can withstand the invasion of alternative strategies within this evolutionary context. For example, 'Tit-for-Tat', a strategy that cooperates on the first move and then replicates the opponent's previous move, has been identified as an ESS in many IPD simulations. It balances retaliation and cooperation, making it robust against both exploitative and overly cooperative strategies.

### Mechanics of ESS in the IPD:

**Retaliation and Forgiveness:** ESS strategies in the IPD often incorporate elements of retaliation against defection and forgiveness following cooperation. This balance ensures that a strategy is neither too aggressive (which could lead to endless cycles of retaliation) nor too passive (which could be easily exploited).

**Stability and Adaptability:** An ESS must be stable enough to resist invasion by alternative strategies but adaptable to the changing behaviors of opponents. This adaptability is crucial in the iterated nature of the game, where static strategies can become predictable and thus exploitable.

**Population Dynamics:** The success of an ESS also depends on the composition of the population. In a diverse strategic environment, an ESS must be robust against a wide range of strategies. However, in a more homogeneous population, an ESS might only need to defend against a few similar strategies.

Using a replicator equation overlaid on the existing tournament logic - the first game dynamics studied in connection with evolutionary game theory. We predict the evolutionary outcome of population behavior using payoff translated as 'fitness' or reproductive success. Essentially, the fitness calculation uses each generation's payoff as a multiplier to its existing population. 

```
fitness[i] += sum(payoff) * population[j]
```

#### Evolution of Strategies from Axelrod's First Tournament
<div>
<iframe title="Evolution of Strategies from Axelrod's First Tournament" 
        src="https://rawcdn.githack.com/mimiyufanyou/mimiyufanyou.github.io/0cbe2fa4e823adea989161d01e3496eecd338e0f/assets/ess.html"
        style="width: 100%; 
               height: 500px; 
               border: none;">
</iframe>
</div>


### Advanced Insights: Beyond Simple Strategies
**Complex Strategy Landscape:** The landscape of IPD strategies is vast and varied, ranging from always cooperating to more complex conditional strategies. These strategies can be adaptive, history-dependent, and research is continuing to progress in numerous directions building on Axelrod's work. Recent papers have explored adding multi-layer networks, ethical bounds, imitation, particle swarms, spatial IPD, the expression of emotion as strategy for promoting cooperation, as well as selective attention or limited horizons for attention or memory. Each paper that builds on this initial research has found evidence for age-old wisdom such as forgiveness and forgetting as an adaptive memory management strategy. 

**Real-World Applications:** The IPD framework has been instrumental in understanding phenomena like the stability of trade agreements, the dynamics of political alliances, and what I am personally most interested in, the evolution of altruism in biological systems.

**Emergence of Cooperation:** In a world seemingly dominated by self-interest, the IPD intriguingly demonstrates conditions under which cooperation can emerge and stabilize. Factors like the shadow of the future (the ongoing nature of interaction) significantly influence cooperative behavior.


### Conclusion: A Microcosm of Human Interaction
The Iterated Prisoner's Dilemma is not just a theoretical construct but a reflection of the complexities of human interaction. It illustrates how repeated interactions, memory, and the potential for future encounters shape our decisions. From fostering cooperation in a competitive environment to understanding the dynamics of social and biological systems, the IPD remains a pivotal concept in deciphering the intricate dance of conflict and collaboration in our world.

### Books Referenced 
<a target="_blank" href="https://www.amazon.com/Evolution-Cooperation-Revised-Robert-Axelrod/dp/0465005640/ref=sr_1_1?crid=UX8B7K5K69VQ&amp;keywords=evolution+of+cooperation&amp;qid=1706171872&amp;sprefix=evoluation+of+cooperation%252Caps%252C135&amp;sr=8-1&_encoding=UTF8&tag=githubpostsmi-20&linkCode=ur2&linkId=5a70641bfddc648cd5a8f503c1acb59f&camp=1789&creative=9325">Evolution of Cooperation - Robert Axelrod</a>

### Papers Referenced 
@article{Li2021Evolutionary,title={Evolutionary game on a growing multilayer network},author={Gang Li and X. Sun},journal={Physica A-statistical Mechanics and Its Applications},year={2021},volume={578},pages={126110},doi={10.1016/J.PHYSA.2021.126110}}

@article{Turker2021Forgiveness,title={Forgiveness is an Adaptation in Iterated Prisoner's Dilemma with Memory},author={Melik Z. Turker and H. Bingol},journal={ArXiv},year={2021},volume={abs/2112.07894},doi={}}

