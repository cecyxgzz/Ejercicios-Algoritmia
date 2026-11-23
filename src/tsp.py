"""Ejercicios 3 y 4: 2-opt, búsqueda local y recocido simulado."""
import math
import time
import numpy as np
from common import tour_cost


def two_opt_local_search(tour, D):
    """2-opt con 'primera mejora' hasta óptimo local. Devuelve (tour, costo, n_mejoras)."""
    t = list(tour); n = len(t); improvements = 0
    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                a, b = t[i], t[i + 1]
                c, d = t[j], t[(j + 1) % n]
                if D[a][c] + D[b][d] < D[a][b] + D[c][d] - 1e-12:
                    t[i + 1:j + 1] = reversed(t[i + 1:j + 1])
                    improvements += 1
                    improved = True
    return t, tour_cost(t, D), improvements


def make_schedule(kind, T0, Tf, K):
    """Esquemas de enfriamiento T(k), k en [0, K)."""
    if kind == "lineal":
        return lambda k: T0 - (T0 - Tf) * k / (K - 1)
    if kind == "exponencial":
        alpha = (Tf / T0) ** (1.0 / (K - 1))
        return lambda k: T0 * alpha ** k
    if kind == "logaritmico":
        c = (T0 / Tf - 1) / math.log(K)
        return lambda k: T0 / (1 + c * math.log(1 + k))
    raise ValueError(kind)


def simulated_annealing(D, tour0, schedule, K, rng, T0, Tf, log_every=100):
    """SA con movimiento 2-opt aleatorio (inversión de segmento)."""
    sched = make_schedule(schedule, T0, Tf, K)
    t = list(tour0); n = len(t)
    cost = tour_cost(t, D)
    best, best_cost = list(t), cost
    h_it, h_cur, h_best, h_T = [], [], [], []
    t0 = time.perf_counter()
    for k in range(K):
        T = sched(k)
        i, j = sorted(rng.choice(n, 2, replace=False))
        if j - i >= 2 and not (i == 0 and j == n - 1):
            a, b, c, d = t[i], t[i + 1], t[j], t[(j + 1) % n]
            delta = D[a][c] + D[b][d] - D[a][b] - D[c][d]
            if delta < 0 or rng.random() < math.exp(-delta / T):
                t[i + 1:j + 1] = reversed(t[i + 1:j + 1])
                cost += delta
                if cost < best_cost - 1e-12:
                    best, best_cost = list(t), cost
        if k % log_every == 0:
            h_it.append(k); h_cur.append(cost); h_best.append(best_cost); h_T.append(T)
    elapsed = time.perf_counter() - t0
    return best, tour_cost(best, D), elapsed, (h_it, h_cur, h_best, h_T)
