"""Ejecuta todos los experimentos y genera las gráficas en results/."""
import subprocess, sys
for f in ["ex1_speedup", "ex2_knapsack", "ex3_2opt", "ex4_sa", "ex5_mst"]:
    print(f"\n===== {f} =====", flush=True)
    subprocess.run([sys.executable, f"experiments/{f}.py"], check=True)
