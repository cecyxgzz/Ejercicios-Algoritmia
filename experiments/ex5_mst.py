import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import random_instance, random_tour, nearest_neighbor, held_karp, tour_cost
from mst_approx import mst_tour
from tsp import two_opt_local_search, simulated_annealing

N, INST = 9, 100
rng = np.random.default_rng(2026)
rows = {k: [] for k in ["opt", "mst", "mst2opt", "ls_rand", "ls_nn", "sa"]}
for i in range(INST):
    _, D = random_instance(N, rng)
    rows["opt"].append(held_karp(D))
    tm = mst_tour(D); rows["mst"].append(tour_cost(tm, D))
    rows["mst2opt"].append(two_opt_local_search(tm, D)[1])
    rows["ls_rand"].append(two_opt_local_search(random_tour(N, rng), D)[1])
    rows["ls_nn"].append(two_opt_local_search(nearest_neighbor(D, int(rng.integers(N))), D)[1])
    sa_rng = np.random.default_rng(i)
    rows["sa"].append(simulated_annealing(D, random_tour(N, sa_rng), "exponencial", 5000, sa_rng, 0.5, 0.005)[1])
A = {k: np.array(v) for k, v in rows.items()}
ratio = {k: A[k] / A["opt"] for k in A if k != "opt"}
for k, r in ratio.items():
    print(f"{k:<8} razón media={r.mean():.4f} máx={r.max():.4f} mediana={np.median(r):.4f}  óptimo en {(r<1+1e-9).sum()}/{INST}")

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
ax[0].hist(ratio["mst"], bins=20, color="#4C78A8", edgecolor="w")
ax[0].axvline(2, color="r", ls="--", label="Límite teórico = 2")
ax[0].axvline(ratio["mst"].mean(), color="k", ls=":", label=f"Media = {ratio['mst'].mean():.3f}")
ax[0].set_xlim(1, 2.1); ax[0].set_xlabel("C_obtenido / C_óptimo"); ax[0].set_ylabel("Frecuencia")
ax[0].set_title("Razón de aproximación (MST puro)"); ax[0].legend()
ax[1].scatter(range(INST), ratio["mst"], s=14, color="#4C78A8")
ax[1].axhline(2, color="r", ls="--", label="Límite = 2"); ax[1].axhline(1, color="g", ls=":", label="Óptimo")
ax[1].set_xlabel("Instancia"); ax[1].set_ylabel("Razón"); ax[1].set_ylim(.95, 2.1); ax[1].legend()
ax[1].set_title("Razón por instancia")
plt.tight_layout(); plt.savefig("results/ex5_ratio.png", dpi=150)

order = ["mst", "mst2opt", "ls_rand", "ls_nn", "sa"]
names = ["MST puro", "MST + 2-opt", "2-opt\n(aleatorio)", "2-opt\n(NN)", "Recocido\nsimulado"]
plt.figure(figsize=(9, 4.8))
plt.boxplot([A[k] for k in order], tick_labels=names)
plt.axhline(A["opt"].mean(), color="g", ls="--", label=f"Costo óptimo medio = {A['opt'].mean():.3f}")
plt.ylabel("Costo del tour"); plt.title("Ejercicio 5: costo obtenido por método (100 instancias, 9 ciudades)")
plt.grid(alpha=.3); plt.legend(); plt.tight_layout(); plt.savefig("results/ex5_methods.png", dpi=150)
json.dump({k: v.tolist() for k, v in A.items()}, open("results/ex5.json", "w"))
