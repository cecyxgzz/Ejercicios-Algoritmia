"""Ejercicio 1: estimación de pi por Monte Carlo en paralelo."""
import time
import numpy as np
from multiprocessing import Pool


def _count_inside(args, batch=5_000_000):
    """Cuenta puntos dentro del círculo en lotes (mantiene bajo el uso de RAM)."""
    n, seed = args
    rng = np.random.default_rng(seed)
    inside, left = 0, n
    while left > 0:
        m = min(batch, left)
        x, y = rng.random(m), rng.random(m)
        inside += int(np.count_nonzero(x * x + y * y <= 1.0))
        left -= m
    return inside


def estimate_pi(total_points, processes, seed=0):
    chunk = total_points // processes
    jobs = [(chunk, seed + i) for i in range(processes)]
    if processes == 1:
        inside = _count_inside(jobs[0])
    else:
        with Pool(processes) as p:
            inside = sum(p.map(_count_inside, jobs))
    return 4.0 * inside / (chunk * processes)


def benchmark(total_points=400_000_000, procs=(1, 2, 4, 8), repeats=3):
    times = {}
    for p in procs:
        best = []
        for r in range(repeats):
            t0 = time.perf_counter()
            est = estimate_pi(total_points, p, seed=r * 100)
            best.append(time.perf_counter() - t0)
        times[p] = float(np.median(best))
        print(f"procesos={p}: t={times[p]:.3f}s  pi~{est:.6f}")
    return times
