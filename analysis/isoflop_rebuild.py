#!/usr/bin/env python3
"""Rebuild the IsoFLOP tables of the main figure directly from the released curves, with less noise.

For every released run trained to one of the seven compute budgets (budget label in the file name, final
compute within 15% of it), take (i) the last logged validation loss, as the paper did, and (ii) the mean
of the last five logged validation losses (the learning rate is at its floor there, so the curve is flat
and the average removes most of the evaluation-sampling and random-masking noise). Byte-identical
exports stored under two size directories are counted once. Curves whose FLOPs axis is known to be
wrong (the MLM 1.2B all-1-epoch curve) or that were not trained to a standard budget are excluded.
Then: compare with the 145 hand-entered values, re-derive the per-budget minima (raw and parabola) and
the model-size exponent, and repeat under run-to-run noise.

Usage: cd analysis && python3 isoflop_rebuild.py  ->  results/isoflop_rebuild.md, results/isoflop_rebuilt_points.csv
"""
import os, re, hashlib, numpy as np, pandas as pd
from isoflop_uncertainty import SIZE, MLM as HAND_MLM, load_clm, minima as hand_minima, slope
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "data", "training_logs"); OUT = os.path.join(HERE, "results")
BUDGETS = [1e18, 3e18, 1e19, 3e19, 1e20, 3e20, 1e21]; K = 5
def parse_size(name):
    m = re.search(r'(?:gpt|mlm)_(\d+(?:\.\d+)?)([MmBb])', name); return float(m.group(1)) * (1e6 if m.group(2).lower() == 'm' else 1e9) if m else np.nan
def load(obj):
    root = os.path.join(DATA, "gpt_valid" if obj == "CLM" else "mlm_valid", "approach3_flops"); rows = []
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d); key = d.split('_')[0]
        if not os.path.isdir(p) or key not in SIZE: continue
        for f in sorted(os.listdir(p)):
            if not f.endswith(".csv") or not f.startswith("run"): continue
            raw = open(os.path.join(p, f), "rb").read(); t = pd.read_csv(os.path.join(p, f)); C = t["Step"].values * 1e9; L = t["Value"].values
            b = re.search(r'(\d+(?:\.\d+)?e\d+)flops', f); budget = float(b.group(1)) if b else np.nan
            rows.append(dict(obj=obj, dir=d, run=f, sha=hashlib.sha256(raw).hexdigest(), N_dir=SIZE[key], N_file=parse_size(f), budget_label=budget,
                             C_final=C[-1], L_last=L[-1], L_last5=L[-K:].mean(), L_last5_sd=L[-K:].std(ddof=1), span_last5=(C[-1]-C[-K])/C[-1], n=len(L),
                             bad_axis="mlm_1b_all1ep_noreg_tk200b" in f))
    T = pd.DataFrame(rows)
    # one row per distinct content: keep the copy whose directory size agrees best with the size in the file name
    T["dir_vs_file"] = np.abs(np.log(T.N_dir / T.N_file.fillna(T.N_dir)))
    T = T.sort_values("dir_vs_file").drop_duplicates("sha").sort_values(["budget_label", "N_dir"])
    # budget assignment: label if present, else nearest standard budget within 15%
    near = np.array([min(BUDGETS, key=lambda b: abs(np.log(c / b))) for c in T.C_final]); ok = np.abs(np.log(T.C_final.values / near)) < np.log(1.15)
    label_std = T.budget_label.apply(lambda b: min(BUDGETS, key=lambda s: abs(np.log(b / s))) if pd.notna(b) and any(abs(np.log(b / s)) < 0.01 for s in BUDGETS) else np.nan)
    T["budget"] = np.where(label_std.notna(), label_std, np.where(ok, near, np.nan))   # standard budgets only
    T["C_over_budget"] = T.C_final / T.budget
    T["used"] = T.budget.notna() & ~T.bad_axis & (np.abs(np.log(T.C_over_budget.fillna(1))) < np.log(1.15))
    return T
def table(T, col, min_runs=3):
    # several runs of one size at one budget (different LR or batch): keep the best, as an IsoFLOP profile should
    best = T[T.used].sort_values(col).drop_duplicates(["budget", "N_dir"])
    return {b: {int(r.N_dir): r[col] for _, r in g.iterrows()} for b, g in best.groupby("budget") if len(g) >= min_runs}
def minima(tab, method, noise=0.0, rng=None):
    Cs, Ns = [], []
    for b in sorted(tab):
        sizes = np.array(sorted(tab[b])); loss = np.array([tab[b][s] for s in sizes], float)
        if noise: loss = loss + rng.normal(0, noise, len(loss))
        x = np.log10(sizes)
        if method == "raw": Ns.append(sizes[np.argmin(loss)])
        else:
            c = np.polyfit(x, loss, 2); xm = -c[1] / (2 * c[0]) if c[0] > 0 else x[np.argmin(loss)]; Ns.append(10 ** float(np.clip(xm, x.min(), x.max())))
        Cs.append(b)
    return np.array(Cs), np.array(Ns)
def main():
    os.makedirs(OUT, exist_ok=True); rng = np.random.default_rng(0); HAND = {"MLM": HAND_MLM, "CLM": load_clm()}
    md = ["# IsoFLOP tables rebuilt from the released curves\n",
          "Per run: last logged validation loss (as in the paper) and the mean of the last five logged losses. Runs trained to a standard budget only; duplicates counted once; the MLM 1.2B all-1-epoch curve (wrong FLOPs axis) excluded.\n"]
    allpts = []; summary = {}
    for obj in ["CLM", "MLM"]:
        T = load(obj); U = T[T.used]; allpts.append(T)
        md += [f"## {obj}: {len(T)} distinct curves, {len(U)} used across {U.budget.nunique()} budgets; runs per budget: " + ", ".join(f"{b:.0e}: {n}" for b, n in U.groupby('budget').size().items()),
               f"Final compute within budget: median C/budget {U.C_over_budget.median():.3f}, range {U.C_over_budget.min():.3f} to {U.C_over_budget.max():.3f}. Last-5 window spans {U.span_last5.median()*100:.1f}% of compute (median); within-window loss sd median {U.L_last5_sd.median():.4f}.\n"]
        # match hand-entered values
        rows = []
        for b, tab in HAND[obj].items():
            for lab, hand in tab.items():
                cand = U[(U.budget == b) & (np.abs(np.log(U.N_dir / SIZE[lab])) < 0.05)]
                if len(cand): r = cand.iloc[0]; rows.append(dict(budget=b, size=lab, hand=hand, last=r.L_last, last5=r.L_last5, run=r.run[:60]))
                else: rows.append(dict(budget=b, size=lab, hand=hand, last=np.nan, last5=np.nan, run="(no run trained to this budget in the release)"))
        M = pd.DataFrame(rows); M["hand_minus_last"] = M.hand - M["last"]
        prov = {"dir": 0, "file": 0, "other": 0, "none": 0}; none_rows = []
        for b, tab in HAND[obj].items():
            for lab, hand in tab.items():
                g = U[U.budget == b].copy(); g["d"] = np.minimum((g.L_last - hand).abs(), (g.L_last5 - hand).abs()); hits = g[g.d <= 0.003]
                if len(hits) == 0: prov["none"] += 1; none_rows.append(f"{b:.0e} {lab} ({hand}, nearest released loss {g.d.min() + 0 if len(g) else float('nan'):.3f} away)")
                elif any(abs(np.log(r.N_dir / SIZE[lab])) < 0.05 for _, r in hits.iterrows()): prov["dir"] += 1
                elif any(pd.notna(r.N_file) and abs(np.log(r.N_file / SIZE[lab])) < 0.12 for _, r in hits.iterrows()): prov["file"] += 1
                else: prov["other"] += 1
        md += [f"Provenance of the {len(M)} hand-entered values (a released run at that budget with loss within 0.003): same size as the label {prov['dir']}; size matches only the file-name label {prov['file']}; only runs of another size {prov['other']}; no released run within 0.003: {prov['none']}.",
               "Entries with no released run within 0.003: " + "; ".join(none_rows), ""]
        matched = M["last"].notna(); big = M[matched & (M.hand_minus_last.abs() > 0.005)]
        md += [f"Hand-entered values matched to a released run: {matched.sum()} of {len(M)}; unmatched: {(~matched).sum()}. Hand minus last-logged loss: median {M.hand_minus_last.median():.4f}, MAD {np.nanmedian(np.abs(M.hand_minus_last - M.hand_minus_last.median())):.4f}; {len(big)} entries differ by more than 0.005:"]
        md += ["| budget | size | hand-entered | last logged | last-5 mean | run |", "|---|---|---|---|---|---|"] + [f"| {r.budget:.0e} | {r.size} | {r.hand} | {r['last']:.4f} | {r.last5:.4f} | {r.run} |" for _, r in big.iterrows()]
        md += ["", "Unmatched hand-entered entries: " + "; ".join(f"{r.budget:.0e} {r.size}" for _, r in M[~matched].iterrows()), ""]
        # exponents
        res = {}
        for col in ["L_last", "L_last5"]:
            tab = table(T, col); res[col] = {m: slope(*minima(tab, m)) for m in ("raw", "para")}
            for sd in (0.005, 0.010):
                s = np.array([slope(*minima(tab, "raw", sd, rng)) for _ in range(2000)]); res[col][f"raw_sd{sd}"] = (np.percentile(s, 2.5), np.percentile(s, 97.5), s)
        hand_exp = {m: slope(*hand_minima(HAND[obj], m)) for m in ("raw", "para")}
        md += ["| source of losses | raw-min exponent | parabola-min exponent | raw-min 95% under noise 0.005 | under noise 0.010 |", "|---|---|---|---|---|",
               f"| hand-entered table (paper) | {hand_exp['raw']:.3f} | {hand_exp['para']:.3f} | | |",
               f"| rebuilt, last logged loss | {res['L_last']['raw']:.3f} | {res['L_last']['para']:.3f} | [{res['L_last']['raw_sd0.005'][0]:.3f}, {res['L_last']['raw_sd0.005'][1]:.3f}] | [{res['L_last']['raw_sd0.01'][0]:.3f}, {res['L_last']['raw_sd0.01'][1]:.3f}] |",
               f"| rebuilt, mean of last 5 | {res['L_last5']['raw']:.3f} | {res['L_last5']['para']:.3f} | [{res['L_last5']['raw_sd0.005'][0]:.3f}, {res['L_last5']['raw_sd0.005'][1]:.3f}] | [{res['L_last5']['raw_sd0.01'][0]:.3f}, {res['L_last5']['raw_sd0.01'][1]:.3f}] |", ""]
        tab5 = table(T, "L_last5"); md += ["Per-budget minimum (mean of last 5): " + ", ".join(f"{b:.0e}: N={int(n):,} (gap to 2nd best {sorted(tab5[b].values())[1]-sorted(tab5[b].values())[0]:.4f}, {len(tab5[b])} runs)" for b, n in zip(*minima(tab5, 'raw'))), ""]
        summary[obj] = res
    for sd in (0.005, 0.010):
        m = summary["MLM"]["L_last5"][f"raw_sd{sd}"][2]; c = summary["CLM"]["L_last5"][f"raw_sd{sd}"][2]
        md.append(f"P(MLM exponent > CLM exponent) on the rebuilt last-5 tables under noise {sd}: {np.mean(m > c):.3f}")
    P = pd.concat(allpts).drop(columns=["sha"]); P.to_csv(os.path.join(OUT, "isoflop_rebuilt_points.csv"), index=False)
    open(os.path.join(OUT, "isoflop_rebuild.md"), "w").write("\n".join(md) + "\n"); print("\n".join(md))
if __name__ == "__main__": main()
