import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import random_instance, random_tour
from tsp import simulated_annealing

N, SEEDS = 50, 8
SCHEDS = ["lineal", "exponencial", "logaritmico"]
BUDGETS = [20_000, 60_000, 150_000]
T0, TF = 0.5, 0.005
inst_rng = np.random.default_rng(1)
_, D = random_instance(N, inst_rng)
out = {s: {b: {"cost": [], "time": []} for b in BUDGETS} for s in SCHEDS}
curves = {}
for s in SCHEDS:
    for b in BUDGETS:
        for seed in range(SEEDS):
            rng = np.random.default_rng(seed)
            t0 = random_tour(N, rng)
            _, c, el, h = simulated_annealing(D, t0, s, b, rng, T0, TF, log_every=b // 300)
            out[s][b]["cost"].append(c); out[s][b]["time"].append(el)
            if b == BUDGETS[1] and seed == 0:
                curves[s] = h
        print(s, b, "costo medio=%.3f  t=%.2fs" % (np.mean(out[s][b]["cost"]), np.mean(out[s][b]["time"])))

colors = {"lineal": "#4C78A8", "exponencial": "#F58518", "logaritmico": "#54A24B"}
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
for s in SCHEDS:
    it, cur, best, T = curves[s]
    ax[0].plot(it, cur, color=colors[s], alpha=.8, label=s)
    ax[1].plot(T, cur, color=colors[s], alpha=.8, label=s)
ax[0].set_xlabel("Iteración"); ax[0].set_ylabel("Costo actual"); ax[0].set_title("Costo vs. iteraciones")
ax[1].set_xlabel("Temperatura"); ax[1].set_xscale("log"); ax[1].invert_xaxis()
ax[1].set_ylabel("Costo actual"); ax[1].set_title("Costo vs. temperatura")
for a in ax: a.grid(alpha=.3); a.legend()
fig.suptitle(f"Ejercicio 4: convergencia de SA (K={BUDGETS[1]:,}, semilla 0)")
plt.tight_layout(); plt.savefig("results/ex4_convergence.png", dpi=150)

plt.figure(figsize=(7, 5))
for s in SCHEDS:
    mt = [np.mean(out[s][b]["time"]) for b in BUDGETS]; mc = [np.mean(out[s][b]["cost"]) for b in BUDGETS]
    sd = [np.std(out[s][b]["cost"]) for b in BUDGETS]
    plt.errorbar(mt, mc, yerr=sd, fmt="o-", color=colors[s], capsize=3, label=s)
    for b, x, y in zip(BUDGETS, mt, mc): plt.annotate(f"{b//1000}k", (x, y), textcoords="offset points", xytext=(4, 5), fontsize=8)
plt.xlabel("Tiempo de ejecución (s)"); plt.ylabel("Costo final medio (± desv. est.)")
plt.title("Ejercicio 4: tiempo vs. calidad"); plt.grid(alpha=.3); plt.legend(); plt.tight_layout()
plt.savefig("results/ex4_time_quality.png", dpi=150)
json.dump({s: {str(b): v for b, v in out[s].items()} for s in SCHEDS}, open("results/ex4.json", "w"))
