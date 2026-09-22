#!/usr/bin/env python3
"""Reproducible refit of the Table A9 parametric scaling law (Cheng et al., NeurIPS 2024)
from the released validation curves in data/training_logs/{gpt,mlm}_valid/approach3_flops.

Objective (as in the original fitting code and Eq. 9 of the paper, with the LSE/log L
ordering as implemented):  sum_i Huber_delta( LSE(a - alpha ln N_i, b - beta ln D_i, e) - ln L_i ),
delta = 1e-3, E = exp(e), A = exp(a), B = exp(b), minimised with L-BFGS-B, no bounds.

Input designs (both are "lower envelope" constructions, one point per target compute value C:
the loss of the run that is lowest at that C, read at its nearest logged point):
  log200   : 200 log-spaced targets in [1e18, 1e23] FLOPs, a run contributes only if its nearest
             logged point is within 1e18 FLOPs of the target  (this reproduces the published CLM row)
  run-final: one target per run, at min of the run's last 10 logged FLOPs values, no tolerance
             (this reproduces the published MLM row; it is also what the released notebook does)
Token-count definitions:
  D_row : evaluation index x (batch x 1024 x 300 steps), the historical definition
  D_c6n : C / (6 N), the definition used for the IsoFLOP frontier fits in the main figure

Usage:  cd analysis && python3 refit_table_a9.py [--bootstrap]
Writes: results/table_a9_refit.json, results/table_a9_refit.md,
        results/envelope_{CLM,MLM}_{log200,run-final}.csv, results/per_run_table.csv
"""
import os, re, sys, json, time, itertools, argparse
import numpy as np, pandas as pd
from multiprocessing import Pool
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "training_logs")
OUT = os.path.join(HERE, "results")
DELTA = 1e-3
CORPUS_TOKENS = 2.0e11          # UniMeta200B; implied by C/(6N) / epoch label, median 2.00e11
MODEL_SIZE = {'3M':3538944,'6M':6291456,'10M':9830400,'13M':13192320,'20M':19267584,'25M':25165824,'34M':33690624,'40M':39813120,'47M':47775744,'65M':65728000,'85M':84934656,'106M':106168320,'127M':127699968,'154M':154448288,'170M':170233344,'200M':202309632,'230M':231211008,'300M':302426080,'393M':393216000,'470M':472435184,'550M':550502400,'650M':650930624,'680M':680205312,'880M':886308864,'1.2B':1208881136,'1.5B':1528823808,'1.7B':1784851968,'2B':2044723200,'2.4B':2359296000,'2.8B':2834283904,'3.4B':3425697792,'4B':4076863488,'5B':4917322640,'6B':6165626880,'7B':7247758312,'10B':10682105856}
PUBLISHED = {"CLM": dict(E=2.122563756382614, A=143.97531038760354, B=22036.528838204948, alpha=0.36658655987525074, beta=0.4955892608715566),
             "MLM": dict(E=1.2339262055489964e-65, A=3.365188326974265, B=7.56855502024196, alpha=0.042286642359660905, beta=0.09943255550337665)}
P0_PAPER = [1, 5, 10, 0.5, 0.5]
GRID = [list(p) for p in itertools.product([-1,-0.5,0,0.5,1],[0,5,10,15,20,25],[0,5,10,15,20,25],[0,0.5,1,1.5,2],[0,0.5,1,1.5,2])]

# ----------------------------------------------------------------------------- data
def load_runs(obj):
    root = os.path.join(DATA, "gpt_valid" if obj == "CLM" else "mlm_valid", "approach3_flops")
    runs = []
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d); key = d.split('_')[0]
        if not os.path.isdir(p): continue
        for f in sorted(os.listdir(p)):
            if not f.endswith(".csv"): continue
            raw = pd.read_csv(os.path.join(p, f))                       # columns: Wall time, Step (GFLOPs), Value (loss)
            hist = raw.iloc[1:].reset_index(drop=True)                  # the original code used skiprows=2: header + first row
            runs.append(dict(obj=obj, dir=d, file=f, key=key, N=MODEL_SIZE.get(key), used=f.startswith("run") and key in MODEL_SIZE,
                             interval=(1024*1024*300 if key.endswith('B') else 512*1024*300), raw=raw, hist=hist))
    return runs

def envelope(runs, design):
    runs = [r for r in runs if r["used"]]
    if design == "log200":
        targets, tol = np.power(10, np.linspace(9, 14, 200)), 1e9
    else:
        targets, tol = sorted(min(r["hist"]["Step"].values.tolist()[-10:]) for r in runs), None
    best = {}
    for r in runs:
        F = r["hist"]["Step"].values; L = r["hist"]["Value"].values
        for t in targets:
            diff = np.abs(F - t); i = int(np.argmin(diff))
            if tol is not None and diff[i] > tol: continue
            T = t * 1e9
            if T not in best or L[i] < best[T]["L"]:
                best[T] = dict(C_target=T, C_matched=F[i]*1e9, N=r["N"], L=L[i], D_row=(i+1)*r["interval"], D_c6n=F[i]*1e9/(6*r["N"]), run=r["file"])
    return pd.DataFrame([best[k] for k in sorted(best)])

def per_run_table(runs):
    rows = []
    for r in runs:
        raw = r["raw"]; C = raw["Step"].iloc[-1]*1e9; ep = re.search(r'all([\d.]+)ep', r["file"]); bsz = re.search(r'bsz([\d.]+[mMkK]?)', r["file"])
        rows.append(dict(objective=r["obj"], directory=r["dir"], run_file=r["file"], N_params_no_embed=r["N"], C_final_flops=C,
                         D_final_tokens_C_over_6N=(C/(6*r["N"]) if r["N"] else np.nan), epoch_label=(float(ep.group(1)) if ep else np.nan),
                         batch_label=(bsz.group(1) if bsz else ""), L_final=raw["Value"].iloc[-1], L_min=raw["Value"].min(), n_logged_points=len(raw),
                         tensorboard_capped_1000=len(raw) == 1000, in_released_notebook_fit=bool(r["used"])))
    return pd.DataFrame(rows)

# ----------------------------------------------------------------------------- objective
def obj_fn(p, N, D, L):
    e, a, b, al, be = p
    r = np.logaddexp(np.logaddexp(a - al*np.log(N), b - be*np.log(D)), e) - np.log(L)
    return float(np.sum(np.where(np.abs(r) < DELTA, 0.5*r**2, DELTA*(np.abs(r) - 0.5*DELTA))))

def obj_grad(p, N, D, L):
    e, a, b, al, be = p; lnN = np.log(N); lnD = np.log(D)
    u = a - al*lnN; v = b - be*lnD; lse = np.logaddexp(np.logaddexp(u, v), e); r = lse - np.log(L)
    f = float(np.sum(np.where(np.abs(r) < DELTA, 0.5*r**2, DELTA*(np.abs(r) - 0.5*DELTA))))
    h = np.where(np.abs(r) < DELTA, r, DELTA*np.sign(r)); wu = np.exp(u-lse); wv = np.exp(v-lse); we = np.exp(e-lse)
    return f, np.array([np.sum(h*we), np.sum(h*wu), np.sum(h*wv), -np.sum(h*wu*lnN), -np.sum(h*wv*lnD)])

def fit(args):
    p0, N, D, L = args
    r = minimize(obj_grad, p0, args=(N, D, L), jac=True, method="L-BFGS-B", options={"maxiter": 10000})
    return [float(x) for x in r.x], float(r.fun)

def unpack(p):
    return dict(E=float(np.exp(p[0])), A=float(np.exp(p[1])), B=float(np.exp(p[2])), alpha=float(p[3]), beta=float(p[4]), a_ratio=float(p[4]/(p[3]+p[4])))

def pub_vec(obj):
    q = PUBLISHED[obj]; return [np.log(q["E"]), np.log(q["A"]), np.log(q["B"]), q["alpha"], q["beta"]]

# ----------------------------------------------------------------------------- bootstrap
BOOT_STARTS = [P0_PAPER, [0,0,0,0,0], [0.75,5,10,0.37,0.5], [-1,0,5,0,0.5]]
def multistart(args):
    idx, N, D, L, starts = args; N, D, L = N[idx], D[idx], L[idx]
    return min((fit((p0, N, D, L)) for p0 in starts), key=lambda r: r[1])

def bootstrap(C, N, D, L, pool, B=200, seed=1):
    rng = np.random.default_rng(seed)
    starts = BOOT_STARTS + [[float(rng.choice([-1,-0.5,0,0.5,1])), float(rng.choice([0,5,10,15,20,25])), float(rng.choice([0,5,10,15,20,25])), float(rng.choice([0,0.5,1,1.5,2])), float(rng.choice([0,0.5,1,1.5,2]))] for _ in range(21)]
    budget = np.round(np.log10(C)*2)/2; groups = [np.where(budget == g)[0] for g in np.unique(budget)]
    out = {}
    for scheme in ["iid", "budget", "randblk"]:
        jobs = []
        for _ in range(B):
            if scheme == "iid": blocks = [np.array([i]) for i in range(len(C))]
            elif scheme == "budget": blocks = groups
            else:
                perm = rng.permutation(len(C)); blocks = []; s = 0
                for g in groups: blocks.append(perm[s:s+len(g)]); s += len(g)
            pick = rng.integers(0, len(blocks), len(blocks)); jobs.append((np.concatenate([blocks[i] for i in pick]), N, D, L, starts))
        P = np.array([r[0] for r in pool.map(multistart, jobs, chunksize=5)]); beta = P[:,4]; alpha = P[:,3]
        out[scheme] = dict(n_blocks=len(groups) if scheme != "iid" else len(C), beta_ci95=np.percentile(beta, [2.5, 97.5]).tolist(),
                           alpha_ci95=np.percentile(alpha, [2.5, 97.5]).tolist(), a_ratio_ci95=np.percentile(beta/(alpha+beta), [2.5, 97.5]).tolist(),
                           frac_beta_below_0p2=float(np.mean(beta < 0.2)))
    return out

# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--bootstrap", action="store_true"); ap.add_argument("--workers", type=int, default=4); args = ap.parse_args()
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(v, "1")
    os.makedirs(OUT, exist_ok=True); results = {}; per_run = []
    with Pool(args.workers) as pool:
        for obj in ["CLM", "MLM"]:
            runs = load_runs(obj); per_run.append(per_run_table(runs))
            for design in ["log200", "run-final"]:
                env = envelope(runs, design); env.to_csv(os.path.join(OUT, f"envelope_{obj}_{design}.csv"), index=False)
                for dname in ["D_row", "D_c6n"]:
                    N = env["N"].values.astype(float); D = env[dname].values.astype(float); L = env["L"].values; t0 = time.time()
                    paper_p0 = fit((P0_PAPER, N, D, L))
                    grid = pool.map(fit, [(p0, N, D, L) for p0 in GRID], chunksize=25); grid.sort(key=lambda r: r[1]); best = grid[0]
                    betas = np.array([g[0][4] for g in grid]); objs = np.array([g[1] for g in grid])
                    res = dict(design=design, D_definition=dname, n_points=int(len(L)),
                               fit_from_paper_p0=dict(**unpack(paper_p0[0]), objective=paper_p0[1]),
                               grid_global_best=dict(**unpack(best[0]), objective=best[1], n_starts_within_2pct=int(np.sum(objs < 1.02*objs.min()))),
                               objective_at_published=obj_fn(pub_vec(obj), N, D, L),
                               n_grid_starts_near_published=int(np.sum((np.abs(betas - PUBLISHED[obj]["beta"]) < 0.03))))
                    if args.bootstrap: res["bootstrap"] = bootstrap(env["C_target"].values, N, D, L, pool)
                    results[f"{obj}|{design}|{dname}"] = res
                    print(f"{obj:3s} {design:9s} {dname:5s} n={len(L):3d} | paper p0 -> beta={res['fit_from_paper_p0']['beta']:.4f} | grid best beta={res['grid_global_best']['beta']:.4f} E={res['grid_global_best']['E']:.3g} obj={best[1]:.3e} | obj at published {res['objective_at_published']:.3e} | {time.time()-t0:.0f}s", flush=True)
    pd.concat(per_run).to_csv(os.path.join(OUT, "per_run_table.csv"), index=False)
    json.dump(dict(published=PUBLISHED, results=results), open(os.path.join(OUT, "table_a9_refit.json"), "w"), indent=1)
    # markdown summary
    md = ["# Table A9 refit from the released curves\n", "Published Table A9: CLM E=2.123 A=143.9 B=22036.5 alpha=0.367 beta=0.496 ; MLM E~0 A=3.365 B=7.569 alpha=0.042 beta=0.099\n",
          "| objective | design | D | n | fit from paper p0 (E, alpha, beta) | grid global best (E, alpha, beta) | best obj | obj at published | implied N_opt exponent beta/(alpha+beta) at best |", "|---|---|---|---|---|---|---|---|---|"]
    for k, r in results.items():
        o, d, dn = k.split("|"); f = r["fit_from_paper_p0"]; g = r["grid_global_best"]
        md.append(f"| {o} | {d} | {dn} | {r['n_points']} | {f['E']:.3g}, {f['alpha']:.3f}, {f['beta']:.3f} | {g['E']:.3g}, {g['alpha']:.3f}, {g['beta']:.3f} | {g['objective']:.3e} | {r['objective_at_published']:.3e} | {g['a_ratio']:.3f} |")
    if args.bootstrap:
        md += ["\n## Bootstrap 95% intervals (200 replicates, 25-start refit per replicate)\n", "| objective | design | D | scheme | blocks | beta 95% | beta/(alpha+beta) 95% | frac beta<0.2 |", "|---|---|---|---|---|---|---|---|"]
        for k, r in results.items():
            o, d, dn = k.split("|")
            for s, b in r["bootstrap"].items():
                md.append(f"| {o} | {d} | {dn} | {s} | {b['n_blocks']} | [{b['beta_ci95'][0]:.3f}, {b['beta_ci95'][1]:.3f}] | [{b['a_ratio_ci95'][0]:.3f}, {b['a_ratio_ci95'][1]:.3f}] | {b['frac_beta_below_0p2']:.2f} |")
    open(os.path.join(OUT, "table_a9_refit.md"), "w").write("\n".join(md) + "\n")
    print("wrote", OUT)

if __name__ == "__main__":
    main()
