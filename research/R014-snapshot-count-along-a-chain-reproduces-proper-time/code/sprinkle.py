"""Poisson-sprinkle 1+1 Minkowski space and count snapshots as longest chains.

Three checks, all in units c = 1:

(a) rate      longest chain from the origin to (t, vt) against sqrt(1 - v^2)
(b) noise     spread of that chain length against (rho V)^(1/6)
(c) slab      elements of a rod's worldtube inside a moving observer's slab
              against rho * l * dt' * sqrt(1 - v^2)

Usage: python code/sprinkle.py [--trials N] [--seed S]
"""

from __future__ import annotations

import argparse
import bisect
import math

import numpy as np


def longest_chain(u: np.ndarray, v: np.ndarray) -> int:
    """Longest causal chain among points given in light-cone coordinates.

    y is in x's causal future iff u_y >= u_x and v_y >= v_x. Sorting by u and
    taking the longest non-decreasing subsequence of v is the standard
    O(n log n) reduction (Ulam's problem). Ties have measure zero in a
    sprinkling, so strict and non-strict agree.
    """
    order = np.lexsort((v, u))
    tails: list[float] = []
    for value in v[order]:
        i = bisect.bisect_right(tails, value)
        if i == len(tails):
            tails.append(value)
        else:
            tails[i] = value
    return len(tails)


def sprinkle_diamond(rng: np.random.Generator, rho: float, U: float, V: float):
    """Poisson sprinkle into the diamond 0<=u<=U, 0<=v<=V (area U*V/2 in t,x)."""
    area = 0.5 * U * V
    n = rng.poisson(rho * area)
    return rng.uniform(0, U, n), rng.uniform(0, V, n)


def chain_to(rng, rho: float, t: float, v: float) -> int:
    """Chain count from the origin to the event (t, x = v t), endpoints included."""
    U, V = t * (1 - v), t * (1 + v)
    u, w = sprinkle_diamond(rng, rho, U, V)
    return longest_chain(u, w) + 2


def check_rate(rng, rho: float, t: float, trials: int) -> list[tuple]:
    rows = []
    rest = np.array([chain_to(rng, rho, t, 0.0) for _ in range(trials)], float)
    for v in (0.0, 0.3, 0.6, 0.8, 0.9, 0.95, 0.99):
        L = np.array([chain_to(rng, rho, t, v) for _ in range(trials)], float)
        tau = t * math.sqrt(1 - v * v)
        rows.append((v, L.mean(), L.std(), L.mean() / rest.mean(), math.sqrt(1 - v * v), tau * math.sqrt(2 * rho)))
    return rows


def check_noise(rng, trials: int) -> tuple[list[tuple], float]:
    rows = []
    for n_expected in (1e2, 1e3, 1e4, 1e5):
        # diamond with rho*V = n_expected, shape irrelevant by invariance
        L = np.array([chain_to(rng, n_expected, 1.0, 0.0) for _ in range(trials)], float)
        rows.append((n_expected, L.mean(), L.std()))
    x = np.log([r[0] for r in rows])
    y = np.log([r[2] for r in rows])
    slope = np.polyfit(x, y, 1)[0]
    return rows, slope


def check_slab(rng, rho: float, ell: float, dt_prime: float, trials: int) -> list[tuple]:
    """Sprinkle the rod's worldtube 0<=x<=ell, 0<=t<=T and count the slab
    0 <= t' <= dt' with t' = gamma (t - v x), i.e. v x <= t <= v x + dt'/gamma."""
    rows = []
    for v in (0.0, 0.6, 0.8, 0.95):
        gamma = 1 / math.sqrt(1 - v * v)
        T = v * ell + dt_prime / gamma + 1.0
        counts = []
        for _ in range(trials):
            n = rng.poisson(rho * ell * T)
            x = rng.uniform(0, ell, n)
            t = rng.uniform(0, T, n)
            inside = (t >= v * x) & (t <= v * x + dt_prime / gamma)
            counts.append(inside.sum())
        c = np.array(counts, float)
        rows.append((v, c.mean(), c.std(), rho * ell * dt_prime * math.sqrt(1 - v * v)))
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--trials", type=int, default=200)
    p.add_argument("--seed", type=int, default=2026)
    args = p.parse_args()
    rng = np.random.default_rng(args.seed)

    rho, t = 2000.0, 1.0
    print(f"(a) rate: rho={rho:g}, reference time t={t:g}, {args.trials} trials")
    print(f"{'v':>5} {'<L>':>8} {'sd':>6} {'<L>/<L_rest>':>13} {'sqrt(1-v^2)':>12} {'tau*sqrt(2rho)':>15}")
    for v, m, s, ratio, pred, asym in check_rate(rng, rho, t, args.trials):
        print(f"{v:5.2f} {m:8.2f} {s:6.2f} {ratio:13.4f} {pred:12.4f} {asym:15.2f}")

    rows, slope = check_noise(rng, args.trials)
    print(f"\n(b) noise: sd of L against rho*V, fitted exponent {slope:.3f} (Tracy-Widom: 1/6 = 0.167)")
    print(f"{'rho*V':>8} {'<L>':>8} {'sd':>7}")
    for n, m, s in rows:
        print(f"{n:8.0f} {m:8.2f} {s:7.3f}")

    ell, dtp = 1.0, 0.05
    print(f"\n(c) slab: rho={rho:g}, rod length {ell:g}, slab thickness dt'={dtp:g}, {args.trials} trials")
    print(f"{'v':>5} {'<count>':>8} {'sd':>6} {'rho*l*dt*sqrt(1-v^2)':>22}")
    for v, m, s, pred in check_slab(rng, rho, ell, dtp, args.trials):
        print(f"{v:5.2f} {m:8.2f} {s:6.2f} {pred:22.2f}")


if __name__ == "__main__":
    main()
