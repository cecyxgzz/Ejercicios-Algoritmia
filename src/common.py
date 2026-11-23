"""Utilidades compartidas para los problemas TSP."""
import numpy as np


def random_instance(n, rng):
    """n ciudades uniformes en [0,1]^2 (distancia euclidiana => cumple desigualdad triangular)."""
    pts = rng.random((n, 2))
    return pts, dist_matrix(pts)


def dist_matrix(pts):
    d = pts[:, None, :] - pts[None, :, :]
    return np.sqrt((d ** 2).sum(-1))


def tour_cost(tour, D):
    t = np.asarray(tour)
    return float(D[t, np.roll(t, -1)].sum())


def random_tour(n, rng):
    return list(rng.permutation(n))


def nearest_neighbor(D, start):
    n = len(D)
    visited = np.zeros(n, bool)
    tour = [start]
    visited[start] = True
    for _ in range(n - 1):
        d = D[tour[-1]].copy()
        d[visited] = np.inf
        nxt = int(np.argmin(d))
        tour.append(nxt)
        visited[nxt] = True
    return tour


def held_karp(D):
    """Óptimo exacto por programación dinámica O(n^2 2^n). Útil hasta n~12."""
    n = len(D)
    N = 1 << (n - 1)  # subconjuntos de {1..n-1}
    INF = float("inf")
    dp = np.full((N, n - 1), INF)
    for j in range(n - 1):
        dp[1 << j][j] = D[0][j + 1]
    for mask in range(1, N):
        for j in range(n - 1):
            if not (mask >> j) & 1 or dp[mask][j] == INF:
                continue
            for k in range(n - 1):
                if (mask >> k) & 1:
                    continue
                nm = mask | (1 << k)
                v = dp[mask][j] + D[j + 1][k + 1]
                if v < dp[nm][k]:
                    dp[nm][k] = v
    full = N - 1
    return float(min(dp[full][j] + D[j + 1][0] for j in range(n - 1)))
