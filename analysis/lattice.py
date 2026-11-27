"""Spatial Prisoner's Dilemma on square lattices, one or more layers. Plain numpy.

The game is the "weak" Prisoner's Dilemma of Nowak & May (1992): mutual
cooperation pays 1, a defector exploiting a cooperator gets b (the temptation,
b > 1), everything else pays 0. Each player meets its four nearest neighbours
(von Neumann neighbourhood, wrapping at the edges).

Strategy updates use the Fermi rule of Szabó & Tőke (1998): a player x copies
a random neighbour y with probability 1 / (1 + exp((U_x - U_y) / K)), where U is
the player's utility. K is the noise in that decision; K = 0.1 throughout.

Updating: in each sub-step a random 10% of players consider copying, and ten
sub-steps make one Monte Carlo step (MCS), about one chance per player. This
keeps the vectorised update close to the usual one-at-a-time (asynchronous) rule.

Three setups share this code:
- single:          one lattice, U = own payoff.
- interdependent:  two lattices, player x in layer A has a partner x' in layer B
                   (same position). U_x = (1 - alpha) * P_x + alpha * P_x'.
                   Strategies only spread within a layer.
- multiplex:       the same players sit on M layers, each a lattice with the
                   players shuffled into different positions, so their neighbours
                   differ per layer. A player has a separate strategy per layer,
                   and its fitness is its total payoff over all layers.
"""

import numpy as np

SHIFTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def payoffs(s, b):
    """s: 2-D array of 1 (cooperate) / 0 (defect). Returns each player's total payoff."""
    coop_neighbours = sum(np.roll(s, sh, axis=(0, 1)) for sh in SHIFTS)
    # Cooperator earns 1 per cooperating neighbour; defector earns b per cooperating neighbour.
    return np.where(s == 1, coop_neighbours * 1.0, coop_neighbours * b)


def fermi_step(strats, utils, rng, K=0.1, frac=0.1):
    """One sub-step on each layer: a random fraction of players may copy one random neighbour."""
    out = []
    for s, u in zip(strats, utils):
        L = s.shape[0]
        pick = rng.integers(0, 4, size=s.shape)
        ns = np.empty_like(s)
        nu = np.empty_like(u)
        for k, sh in enumerate(SHIFTS):
            m = pick == k
            ns[m] = np.roll(s, sh, axis=(0, 1))[m]
            nu[m] = np.roll(u, sh, axis=(0, 1))[m]
        z = np.clip((u - nu) / K, -50, 50)
        copy = (rng.random(s.shape) < frac) & (rng.random(s.shape) < 1 / (1 + np.exp(z)))
        out.append(np.where(copy, ns, s))
    return out


def run(mode, b, L=80, mcs=1500, alpha=0.0, layers=1, seed=0, keep=200, snapshots=()):
    """Returns (cooperation level averaged over the last `keep` MCS, per-MCS cooperation, snapshots)."""
    rng = np.random.default_rng(seed)
    n_layers = 2 if mode == "interdependent" else layers
    strats = [(rng.random((L, L)) < 0.5).astype(np.int8) for _ in range(n_layers)]

    # Multiplex: layer l holds player perm[l][i] at flat position i.
    if mode == "multiplex":
        perms = [np.arange(L * L)] + [rng.permutation(L * L) for _ in range(n_layers - 1)]
        inv = [np.argsort(p) for p in perms]

    def utilities(strats):
        pays = [payoffs(s, b) for s in strats]
        if mode == "single":
            return pays
        if mode == "interdependent":
            a, c = pays
            return [(1 - alpha) * a + alpha * c, (1 - alpha) * c + alpha * a]
        # multiplex: total payoff per player (indexed by player id), mapped back to each layer
        total = np.zeros(L * L)
        for l, p in enumerate(pays):
            total[perms[l]] += p.ravel()
        return [total[perms[l]].reshape(L, L) for l in range(n_layers)]

    history, snaps = [], {}
    for t in range(mcs):
        for _ in range(10):
            strats = fermi_step(strats, utilities(strats), rng)
        history.append(float(np.mean([s.mean() for s in strats])))
        if t in snapshots:
            snaps[t] = strats[0].copy()
    return float(np.mean(history[-keep:])), history, snaps
