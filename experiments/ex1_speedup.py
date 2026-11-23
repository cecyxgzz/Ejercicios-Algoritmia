import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pi_parallel import benchmark


def main():
    procs = [1, 2, 4, 8]
    times = benchmark(total_points=400_000_000, procs=procs, repeats=3)
    speedup = [times[1] / times[p] for p in procs]
    plt.figure(figsize=(6.5, 4.8))
    plt.plot(procs, speedup, "o-", label="Speedup medido")
    plt.plot(procs, procs, "k--", label="Speedup ideal")
    ps = np.linspace(1, 8, 50)
    plt.plot(ps, 1 / ((1 - 0.95) + 0.95 / ps), ":", color="gray",
             label="Ley de Amdahl (f paralela = 95%, ilustrativa)")
    plt.xlabel("Número de procesos"); plt.ylabel("Speedup  T(1)/T(p)")
    plt.title(f"Ejercicio 1: speedup de estimate_pi (CPUs: {os.cpu_count()})")
    plt.xticks(procs); plt.grid(alpha=.3); plt.legend(fontsize=8); plt.tight_layout()
    plt.savefig("results/ex1_speedup.png", dpi=150)
    json.dump({"cpus": os.cpu_count(), "times": times, "speedup": speedup},
              open("results/ex1.json", "w"), indent=1)
    print("speedup:", speedup)


if __name__ == "__main__":  # obligatorio en macOS (multiprocessing usa 'spawn')
    main()
