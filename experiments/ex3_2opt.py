import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import random_instance, random_tour, nearest_neighbor, tour_cost
from tsp import two_opt_local_search

N, INST = 50, 50
rng = np.random.default_rng(42)
res = {"rand": {"imp": [], "cost": [], "init": []}, "nn": {"imp": [], "cost": [], "init": []}}
for _ in range(INST):
    _, D = random_instance(N, rng)
    t0 = random_tour(N, rng)
    t1 = nearest_neighbor(D, int(rng.integers(N)))
    for key, t in (("rand", t0), ("nn", t1)):
        _, c, k = two_opt_local_search(t, D)
        res[key]["imp"].append(k); res[key]["cost"].append(c); res[key]["init"].append(tour_cost(t, D))
for k in res:
    print(k, "mejoras media=%.1f  costo final medio=%.3f  costo inicial medio=%.3f" %
          (np.mean(res[k]["imp"]), np.mean(res[k]["cost"]), np.mean(res[k]["init"])))
fig, ax = plt.subplots(1, 2, figsize=(10, 4.5))
lab = ["Aleatoria", "Vecino más cercano"]
ax[0].boxplot([res["rand"]["imp"], res["nn"]["imp"]], tick_labels=lab)
ax[0].set_title("Nº de mejoras 2-opt hasta óptimo local"); ax[0].set_ylabel("Mejoras")
ax[1].boxplot([res["rand"]["cost"], res["nn"]["cost"]], tick_labels=lab)
ax[1].set_title("Costo del óptimo local alcanzado"); ax[1].set_ylabel("Longitud del tour")
for a in ax: a.grid(alpha=.3)
fig.suptitle(f"Ejercicio 3: 2-opt, {INST} instancias de {N} ciudades")
plt.tight_layout(); plt.savefig("results/ex3_2opt.png", dpi=150)
# diferencias pareadas
d = np.array(res["rand"]["imp"]) - np.array(res["nn"]["imp"])
res["paired_imp_diff_mean"] = float(d.mean()); res["nn_fewer_in"] = int((d > 0).sum())
print("NN requiere menos mejoras en", res["nn_fewer_in"], "de", INST, "instancias")
json.dump(res, open("results/ex3.json", "w"))
