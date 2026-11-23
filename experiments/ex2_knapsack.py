import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from knapsack import by_ratio, by_min_weight

def report(title, items, cap):
    r = by_ratio(items, cap); m = by_min_weight(items, cap)
    print(f"\n{title} (capacidad={cap})")
    print(f"{'Método':<14}{'Objetos':<28}{'Peso usado':<12}{'Valor'}")
    print(f"{'valor/peso':<14}{str(r[0]):<28}{r[1]:<12}{r[2]}")
    print(f"{'menor peso':<14}{str(m[0]):<28}{m[1]:<12}{m[2]}")
    return r, m

# Instancia aleatoria de ejemplo (semilla fija)
rng = np.random.default_rng(7)
items = [(f"o{i+1}", int(rng.integers(2, 20)), int(rng.integers(5, 60))) for i in range(10)]
print("Items (nombre, peso, valor):", items)
r1, m1 = report("Instancia A (aleatoria)", items, 40)

# Contraejemplo diseñado: menor peso pierde frente a valor/peso
ce = [("A", 3, 1), ("B", 4, 1), ("C", 5, 50)]
r2, m2 = report("Instancia B (contraejemplo)", ce, 10)

fig, ax = plt.subplots(1, 3, figsize=(12, 4))
for k, (title, r, m, cap) in enumerate([("Instancia A", r1, m1, 40), ("Instancia B", r2, m2, 10)]):
    pass
labels = ["valor/peso", "menor peso"]
for a, (title, r, m, cap) in zip(ax[:2], [("Instancia A (cap=40)", r1, m1, 40), ("Instancia B (cap=10)", r2, m2, 10)]):
    x = np.arange(2); w = .35
    a.bar(x - w/2, [r[2], m[2]], w, label="Valor total", color="#4C78A8")
    a.bar(x + w/2, [r[1], m[1]], w, label="Capacidad usada", color="#F58518")
    a.axhline(cap, color="k", ls="--", lw=1, label="Capacidad")
    for i, (rr) in enumerate([r, m]):
        a.text(i, max(rr[2], rr[1]) + 1, f"{len(rr[0])} obj.", ha="center", fontsize=9)
    a.set_xticks(x); a.set_xticklabels(labels); a.set_title(title); a.legend(fontsize=8)
ax[2].axis("off")
ax[2].text(0, .9, "Contraejemplo (cap=10):\nA(w=3,v=1) B(w=4,v=1) C(w=5,v=50)\n\n"
           f"valor/peso -> {r2[0]}  valor={r2[2]}\nmenor peso  -> {m2[0]}  valor={m2[2]}",
           va="top", family="monospace", fontsize=10)
plt.tight_layout(); plt.savefig("results/ex2_knapsack.png", dpi=150)
json.dump({"A": {"items": items, "cap": 40, "ratio": r1, "minw": m1},
           "B": {"items": ce, "cap": 10, "ratio": r2, "minw": m2}},
          open("results/ex2.json", "w"), indent=1)
