"""Ejercicio 2: mochila voraz (valor/peso vs menor peso)."""


def greedy(items, cap, key):
    """items: lista de (nombre, peso, valor). key: función de ordenamiento."""
    chosen, used, val = [], 0, 0
    for name, w, v in sorted(items, key=key):
        if used + w <= cap:
            chosen.append(name); used += w; val += v
    return chosen, used, val


def by_ratio(items, cap):
    return greedy(items, cap, key=lambda it: -it[2] / it[1])


def by_min_weight(items, cap):
    return greedy(items, cap, key=lambda it: it[1])
