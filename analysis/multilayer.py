"""Cooperation on one, two and many layers: the sweeps behind the multilayer post.

    python analysis/multilayer.py      # ~15-25 min with 4 processes

Writes analysis/results/multilayer.json. Model details are in lattice.py.
"""

import json
from multiprocessing import Pool
from pathlib import Path

import numpy as np

import lattice

OUT = Path(__file__).parent / "results" / "multilayer.json"
L, MCS, KEEP = 60, 1500, 300
SEED = 2026


def job(args):
    kind, b, extra, seed = args
    if kind == "single":
        c, h, _ = lattice.run("single", b, L=L, mcs=MCS, seed=seed, keep=KEEP)
    elif kind == "interdependent":
        c, h, _ = lattice.run("interdependent", b, L=L, mcs=MCS, alpha=extra, seed=seed, keep=KEEP)
    else:
        c, h, _ = lattice.run("multiplex", b, L=L, mcs=MCS, layers=extra, seed=seed, keep=KEEP)
    return kind, round(b, 3), extra, seed, c


def main():
    jobs = []
    b_single = [round(x, 3) for x in np.arange(1.0, 1.101, 0.01)]
    for b in b_single:
        for s in range(3):
            jobs.append(("single", b, None, SEED + s))
    alphas = [0.0, 0.2, 0.4, 0.6, 0.8]
    b_inter = [round(x, 3) for x in np.arange(1.0, 1.301, 0.02)]
    for a in alphas:
        for b in b_inter:
            jobs.append(("interdependent", b, a, SEED))
    layers = [1, 2, 3, 5]
    b_multi = [round(x, 3) for x in np.arange(1.0, 1.201, 0.02)]
    for m in layers:
        for b in b_multi:
            jobs.append(("multiplex", b, m, SEED))

    with Pool(4) as pool:
        results = pool.map(job, jobs, chunksize=1)

    out = {"L": L, "mcs": MCS, "keep": KEEP, "K": 0.1}
    out["single"] = {"b": b_single, "cooperation": [
        float(np.mean([r[4] for r in results if r[0] == "single" and r[1] == b])) for b in b_single]}
    out["interdependent"] = {"alpha": alphas, "b": b_inter, "cooperation": [
        [next(r[4] for r in results if r[0] == "interdependent" and r[2] == a and r[1] == b) for b in b_inter]
        for a in alphas]}
    out["multiplex"] = {"layers": layers, "b": b_multi, "cooperation": [
        [next(r[4] for r in results if r[0] == "multiplex" and r[2] == m and r[1] == b) for b in b_multi]
        for m in layers]}

    # Pictures: how the lattice looks over time, one layer vs two coupled layers.
    times = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    _, h1, s1 = lattice.run("single", 1.03, L=100, mcs=1001, seed=SEED, snapshots=times)
    _, h2, s2 = lattice.run("interdependent", 1.10, L=100, mcs=1001, alpha=0.5, seed=SEED, snapshots=times)
    _, h3, _ = lattice.run("single", 1.10, L=100, mcs=1001, seed=SEED)
    out["snapshots"] = {
        "times": times,
        "single": {"b": 1.03, "frames": [s1[t].tolist() for t in times], "history": h1},
        "interdependent": {"b": 1.10, "alpha": 0.5, "frames": [s2[t].tolist() for t in times], "history": h2},
        "single_same_b": {"b": 1.10, "history": h3},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
