"""Ejercicio 5: 2-aproximación para TSP métrico vía MST (Prim + recorrido preorden)."""
import numpy as np


def prim_mst(D):
    n = len(D)
    in_t = np.zeros(n, bool); in_t[0] = True
    key = D[0].copy(); parent = np.zeros(n, int)
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        k = np.where(in_t, np.inf, key)
        v = int(np.argmin(k))
        in_t[v] = True
        adj[parent[v]].append(v); adj[v].append(parent[v])
        upd = (D[v] < key) & ~in_t
        key[upd] = D[v][upd]; parent[upd] = v
    return adj


def mst_tour(D, root=0):
    adj = prim_mst(D)
    tour, seen, stack = [], set(), [root]
    while stack:  # DFS preorden = atajos sobre el recorrido euleriano
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u); tour.append(u)
        stack.extend(sorted(adj[u], reverse=True))
    return tour
