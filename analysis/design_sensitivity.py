#!/usr/bin/env python3
"""How the Table A9 exponents depend on how the fitting set is built.

For each objective, build the lower-envelope fitting set with each target-compute design and matching
tolerance that appears (active or commented out) in the original scripts, then fit the paper's
objective from the paper's initialisation and from a 101-start subset of the appendix grid.
Writes results/design_sensitivity.md.  Usage: cd analysis && python3 design_sensitivity.py
"""
import os, itertools, numpy as np, pandas as pd
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "data", "training_logs"); OUT = os.path.join(HERE, "results")
from refit_table_a9 import MODEL_SIZE, PUBLISHED, P0_PAPER, GRID, obj_fn, obj_grad, unpack
def load(obj):
    root = os.path.join(DATA, "gpt_valid" if obj == "CLM" else "mlm_valid", "approach3_flops"); runs = []
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d); key = d.split('_')[0]
        if not os.path.isdir(p) or key not in MODEL_SIZE: continue
        for f in sorted(os.listdir(p)):
            if not f.startswith("run"): continue
            h = pd.read_csv(os.path.join(p, f)).iloc[1:]; runs.append((MODEL_SIZE[key], 1024*1024*300 if key.endswith('B') else 512*1024*300, h["Step"].values, h["Value"].values))
    return runs
def envelope(runs, design, tol):
    targets = np.power(10, np.linspace(9, 14, 200)) if design == "log200" else sorted(min(F[-10:]) for _, _, F, _ in runs)
    best = {}
    for N, interval, F, L in runs:
        for t in targets:
            diff = np.abs(F - t); i = int(np.argmin(diff))
            if tol is not None and diff[i] > tol: continue
            if t not in best or L[i] < best[t][2]: best[t] = (N, (i+1)*interval, L[i], F[i]*1e9/(6*N))
    v = [best[k] for k in sorted(best)]
    return np.array([x[0] for x in v], float), np.array([x[1] for x in v], float), np.array([x[3] for x in v]), np.array([x[2] for x in v])
def fit(p0, N, D, L):
    r = minimize(obj_grad, p0, args=(N, D, L), jac=True, method="L-BFGS-B", options={"maxiter": 10000}); return r.x, r.fun
def main():
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(v, "1")
    starts = [P0_PAPER] + GRID[::45]                     # paper p0 + 100 evenly spaced grid points
    md = ["# Sensitivity of the Table A9 fit to the fitting-set construction\n",
          "Designs: `run-final` = one target per run at its final compute; `log200` = 200 log-spaced targets in [1e18, 1e23] FLOPs. Tolerance = maximum distance (GFLOPs) between a target and a run's nearest logged point for that run to be considered; the original scripts carry 1e9 (active for the CLM row) and None (active for the MLM row).",
          "From the paper's initialisation the published CLM row is reached only when a matching tolerance is applied (`log200` at 1e8 or 1e9, `run-final` at 1e9, historical D); every other construction, and the best of 101 starts on every construction, ends in the low-beta basin. The MLM initialisation result is likewise construction-dependent (0.10 or about 0.49), while the best of 101 starts is 0.05 to 0.11 throughout.\n",
          "| objective | design | tolerance | D | n | paper-p0 fit E, alpha, beta | best of 101 starts E, alpha, beta | best obj | obj at published |", "|---|---|---|---|---|---|---|---|---|"]
    for obj in ["CLM", "MLM"]:
        runs = load(obj); q = PUBLISHED[obj]; pub = [np.log(q["E"]), np.log(q["A"]), np.log(q["B"]), q["alpha"], q["beta"]]
        for design, tols in [("run-final", [None, 1e9]), ("log200", [None, 1e8, 1e9, 3e9])]:
            for tol in tols:
                N, Drow, Dc6n, L = envelope(runs, design, tol)
                for dname, D in [("D_row", Drow), ("D_c6n", Dc6n)]:
                    pp, pf = fit(P0_PAPER, N, D, L); res = [fit(p0, N, D, L) for p0 in starts]; bp, bf = min(res, key=lambda r: r[1])
                    a, b = unpack(pp), unpack(bp)
                    md.append(f"| {obj} | {design} | {tol if tol is None else f'{tol:.0e}'} | {dname} | {len(L)} | {a['E']:.3g}, {a['alpha']:.3f}, {a['beta']:.3f} | {b['E']:.3g}, {b['alpha']:.3f}, {b['beta']:.3f} | {bf:.3e} | {obj_fn(pub, N, D, L):.3e} |")
                    print(md[-1], flush=True)
    open(os.path.join(OUT, "design_sensitivity.md"), "w").write("\n".join(md) + "\n")
if __name__ == "__main__": main()
