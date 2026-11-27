"""Prisoner's Dilemma, part 2: noise, forgiveness, ZD strategies and evolution.

Follows the "Next steps" of the 2024-01-20 post. Runs with the Axelrod library
(4.13) and writes the numbers to analysis/results/ipd_part2.json. Charts are made
from that file by ipd_part2_charts.py, so the slow part runs once.

    python analysis/ipd_part2.py          # ~10-20 min on a laptop
"""

import json
import random
from pathlib import Path

import axelrod as axl
import numpy as np

SEED = 2026
TURNS = 100  # as in part 1
OUT = Path(__file__).parent / "results" / "ipd_part2.json"

# Payoffs (Axelrod's): R=3 both cooperate, T=5 temptation, S=0 sucker, P=1 both defect.
R, T, S, P = 3, 5, 0, 1


def first_field():
    return [s() for s in axl.axelrod_first_strategies]


def entrant_vs_field(make_entrant, noise, reps, seed):
    """Mean score per turn of one entrant against every first-tournament strategy."""
    scores = []
    for k, opp_cls in enumerate(axl.axelrod_first_strategies):
        for r in range(reps):
            m = axl.Match((make_entrant(), opp_cls()), turns=TURNS, noise=noise, seed=seed + 1000 * k + r)
            m.play()
            scores.append(m.final_score_per_turn()[0])
    return float(np.mean(scores))


def self_play(make_entrant, noise, reps, seed):
    """Mean score per turn when a strategy meets a copy of itself."""
    scores = []
    for r in range(reps):
        m = axl.Match((make_entrant(), make_entrant()), turns=TURNS, noise=noise, seed=seed + r)
        m.play()
        scores.append(np.mean(m.final_score_per_turn()))
    return float(np.mean(scores))


def run_tournament(players, noise, reps, seed):
    t = axl.Tournament(players, turns=TURNS, repetitions=reps, noise=noise, seed=seed)
    res = t.play(progress_bar=False, processes=2)
    return res


def main():
    out = {"turns": TURNS, "seed": SEED, "payoffs": {"R": R, "T": T, "S": S, "P": P}}

    # 1. Noise: the first tournament again, with a chance that any move is flipped.
    noise_levels = [0, 0.01, 0.02, 0.05, 0.1, 0.2]
    noise_runs = []
    for noise in noise_levels:
        res = run_tournament(first_field(), noise, reps=30, seed=SEED)
        noise_runs.append({
            "noise": noise,
            "players": list(res.players),
            "median_score": [float(np.median(s)) for s in res.normalised_scores],
            "cooperation": [float(c) for c in res.cooperating_rating],
            "ranking": [res.players[i] for i in res.ranking],
        })
        print("noise", noise, "winner", res.ranked_names[0])
    out["noise"] = noise_runs

    # 2. Forgiveness: Generous Tit For Tat forgives a defection with probability p.
    gens = [round(x, 2) for x in np.arange(0, 0.65, 0.05)]
    fnoise = [0, 0.01, 0.05, 0.1, 0.2]
    grid_field, grid_self = [], []
    for noise in fnoise:
        row_f, row_s = [], []
        for p in gens:
            make = lambda p=p: axl.GTFT(p=p)
            row_f.append(entrant_vs_field(make, noise, reps=10, seed=SEED))
            row_s.append(self_play(make, noise, reps=40, seed=SEED))
        grid_field.append(row_f)
        grid_self.append(row_s)
        print("forgiveness noise", noise, "done")
    molander = min(1 - (T - R) / (R - S), (R - P) / (T - P))
    out["forgiveness"] = {
        "generosity": gens, "noise": fnoise,
        "vs_field": grid_field, "self_play": grid_self,
        "molander_optimum": molander,
    }

    # 3. Zero-determinant strategies join the first tournament.
    zd = [axl.ZDExtort2(), axl.ZDExtort4(), axl.ZDGTFT2(), axl.ZDSet2(), axl.GTFT()]
    zd_runs = []
    for noise in [0, 0.05]:
        res = run_tournament(first_field() + zd, noise, reps=30, seed=SEED)
        n = len(res.players)
        zd_runs.append({
            "noise": noise,
            "players": list(res.players),
            "wins_share": [float(np.mean(w)) / (n - 1) for w in res.wins],
            "mean_score": [float(np.mean(s)) for s in res.normalised_scores],
            "cooperation": [float(c) for c in res.cooperating_rating],
            "payoff_matrix": [[float(x) for x in row] for row in res.payoff_matrix],
        })
        print("zd noise", noise, "winner", res.ranked_names[0])
    out["zd"] = zd_runs

    # 4. Evolution: part 1's replicator rule on the noisy ZD tournament's payoffs.
    def replicate(payoff, pop, generations=150):
        payoff = np.array(payoff)
        pop = np.array(pop, dtype=float)
        history = [pop.tolist()]
        for _ in range(generations):
            fitness = payoff @ pop  # fitness[i] = sum_j payoff[i][j] * population[j]
            pop = pop * fitness
            pop = pop / pop.sum()
            history.append(pop.tolist())
        return history

    noisy = zd_runs[1]
    n = len(noisy["players"])
    equal = replicate(noisy["payoff_matrix"], [1 / n] * n)
    rng = np.random.default_rng(SEED)
    winners = []
    for _ in range(500):
        start = rng.dirichlet(np.ones(n))
        end = replicate(noisy["payoff_matrix"], start)[-1]
        winners.append(int(np.argmax(end)))
    out["evolution"] = {
        "players": noisy["players"],
        "equal_start": equal,
        "random_starts": 500,
        "largest_at_end": [winners.count(i) for i in range(n)],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    random.seed(SEED)
    np.random.seed(SEED)
    main()
