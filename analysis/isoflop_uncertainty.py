#!/usr/bin/env python3
"""Uncertainty of the IsoFLOP-profile exponents in the main figure (N_opt ~ C^a).

The main figure selects, at each of seven compute budgets, the model size with the lowest final
validation loss and fits a power law through the seven minima. The tables below are the (budget,
model size, loss) values behind that figure (from the original merge_approach2.py). This script
re-derives the exponent with (i) the raw minimum, (ii) a parabola fit in log N per budget, and
(iii) both, after perturbing every loss by Gaussian noise at the run-to-run level measured from
replicate runs (sd 0.006 eval-to-eval jitter; 0.010 to 0.016 between reruns of one configuration).
It also shows the effect of the known FLOPs-axis error of the MLM 1.2B curve at the 1e21 budget.

Usage: cd analysis && python3 isoflop_uncertainty.py   -> results/isoflop_uncertainty.md
"""
import os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "results")
SIZE = {'3M':3538944,'6M':6291456,'10M':9830400,'13M':13192320,'15M':15192311,'20M':19267584,'25M':25165824,'34M':33690624,'40M':39813120,'47M':47775744,'65M':65728000,'85M':84934656,'106M':106168320,'127M':127699968,'154M':154448288,'170M':170233344,'200M':202309632,'230M':231211008,'300M':302426080,'393M':393216000,'470M':472435184,'550M':550502400,'680M':680205312,'880M':886308864,'1.2B':1208881136,'1.5B':1528823808,'1.7B':1784851968,'2B':2044723200,'2.4B':2359296000,'2.8B':2834283904,'3.4B':3425697792,'4B':4076863488,'5B':4917322640,'6B':6165626880,'7B':7247758312}
MLM = {1e18:{'3M':2.407,'6M':2.401,'10M':2.4011,'13M':2.410,'25M':2.428,'34M':2.431,'47M':2.433,'65M':2.454,'85M':2.463},
       3e18:{'6M':2.362,'10M':2.356,'13M':2.355,'15M':2.361,'25M':2.366,'34M':2.371,'47M':2.38,'65M':2.387,'85M':2.392,'106M':2.408,'154M':2.422},
       1e19:{'25M':2.295,'34M':2.28,'47M':2.281,'65M':2.29,'85M':2.287,'106M':2.292,'127M':2.309,'154M':2.329,'170M':2.333,'230M':2.347,'300M':2.374},
       3e19:{'47M':2.215,'85M':2.213,'106M':2.215,'127M':2.219,'154M':2.224,'170M':2.226,'300M':2.26,'393M':2.289,'470M':2.311},
       1e20:{'154M':2.143,'170M':2.135,'200M':2.131,'230M':2.133,'300M':2.14,'393M':2.144,'470M':2.148,'550M':2.158,'680M':2.188,'880M':2.219},
       3e20:{'300M':2.064,'393M':2.0591,'470M':2.059,'550M':2.06,'680M':2.076,'880M':2.109,'1.2B':2.127,'1.5B':2.131,'1.7B':2.172,'2.4B':2.182,'2.8B':2.214},
       1e21:{'880M':1.989,'1.2B':1.979,'1.5B':1.986,'1.7B':2.004,'2B':2.0,'2.4B':2.007,'2.8B':2.027,'3.4B':2.052,'4B':2.068,'5B':2.118,'7B':2.174}}
CLM = None  # filled from the original script's second table, see load_clm()
def load_clm():
    import re
    # The CLM table is kept in the same literal form; values transcribed from merge_approach2.py (second `data = {` block).
    return {1e18:{'6M':2.643, '13M':2.624, '25M':2.6239, '34M':2.6233, '47M':2.64, '65M':2.647, '85M':2.67},
            3e18:{'25M':2.591, '34M':2.585, '47M':2.583, '65M':2.5829, '85M':2.593, '106M':2.612, '127M':2.628, '154M':2.638},
            1e19:{'34M':2.534, '47M':2.523, '65M':2.51, '85M':2.509, '106M':2.507, '127M':2.5069, '154M':2.514, '170M':2.519, '230M':2.533, '300M':2.568},
            3e19:{'47M':2.488, '65M':2.475, '85M':2.463, '106M':2.454, '127M':2.448, '154M':2.447, '170M':2.445, '200M':2.445, '230M':2.444, '300M':2.447, '393M':2.458, '470M':2.469, '550M':2.483},
            1e20:{'85M':2.427, '106M':2.41, '127M':2.395, '154M':2.39, '170M':2.384, '230M':2.368, '300M':2.365, '393M':2.363, '470M':2.362, '550M':2.365, '680M':2.371, '880M':2.385, '1.2B':2.42, '1.5B':2.442},
            3e20:{'300M':2.317,'393M':2.305, '470M':2.301, '550M':2.296, '680M':2.295, '880M':2.294, '1.2B':2.306, '1.5B':2.321, '1.7B':2.331},
            1e21:{'880M':2.212, '1.2B':2.187, '1.5B':2.181, '1.7B':2.18, '2B':2.186, '2.4B':2.183, '2.8B':2.200, '3.4B':2.203, '4B':2.228, '5B':2.242,'6B':2.267,'7B':2.293}}
def minima(table, method, noise=0.0, rng=None):
    Cs, Ns = [], []
    for C in sorted(table):
        sizes = np.array([SIZE[k] for k in table[C]]); loss = np.array(list(table[C].values()))
        if noise: loss = loss + rng.normal(0, noise, len(loss))
        x = np.log10(sizes)
        if method == "raw": Ns.append(sizes[np.argmin(loss)])
        else:
            c = np.polyfit(x, loss, 2); xm = -c[1]/(2*c[0]) if c[0] > 0 else x[np.argmin(loss)]
            Ns.append(10**float(np.clip(xm, x.min(), x.max())))
        Cs.append(C)
    return np.array(Cs), np.array(Ns)
def slope(Cs, Ns): return np.polyfit(np.log10(Cs), np.log10(Ns), 1)[0]
def main():
    global CLM; CLM = load_clm(); os.makedirs(OUT, exist_ok=True); rng = np.random.default_rng(0)
    md = ["# Uncertainty of the IsoFLOP model-size exponents\n",
          "Inputs: the (budget, model size, loss) tables behind the main figure; 7 budgets, 72 MLM and 73 CLM runs.",
          "Noise levels: 0.006 = eval-to-eval jitter of one run (eval_iters = 3 batches); 0.010 and 0.016 = RMS difference between reruns of one configuration (154M and 3B UR50 pairs).\n"]
    md += ["| objective | raw-min exponent | parabola-min exponent | gap best vs 2nd-best loss per budget |", "|---|---|---|---|"]
    for name, tab in [("MLM", MLM), ("CLM", CLM)]:
        gaps = [sorted(v.values())[1]-sorted(v.values())[0] for v in tab.values()]
        md.append(f"| {name} | {slope(*minima(tab,'raw')):.3f} | {slope(*minima(tab,'para')):.3f} | {min(gaps):.4f} to {max(gaps):.4f} |")
    md += ["\n## Exponents under run-to-run noise (2000 perturbations of every loss value)\n", "| noise sd | method | MLM 95% | CLM 95% | P(MLM exponent > CLM exponent) |", "|---|---|---|---|---|"]
    for sd in (0.006, 0.010, 0.016):
        for method in ("raw", "para"):
            m = np.array([slope(*minima(MLM, method, sd, rng)) for _ in range(2000)]); c = np.array([slope(*minima(CLM, method, sd, rng)) for _ in range(2000)])
            md.append(f"| {sd} | {method} | [{np.percentile(m,2.5):.3f}, {np.percentile(m,97.5):.3f}] | [{np.percentile(c,2.5):.3f}, {np.percentile(c,97.5):.3f}] | {np.mean(m > c):.3f} |")
    # MLM 1.2B axis error: its CSV FLOPs are 17% low (N=1e9 used instead of 1.2086e9). Re-reading the curve on the corrected axis gives 1.987 at 1e21 (vs 1.979 entered), tying with 1.5B (1.986).
    Cs, Ns = minima(MLM, "raw"); alt = Ns.copy(); alt[-1] = SIZE['1.5B']
    md += ["\n## MLM 1.2B FLOPs-axis error at the 1e21 budget\n",
           "The 1.2B MLM curve's exported FLOPs axis was generated with N = 1e9 instead of the true 1.2086e9, so its compute is understated by 17%. Re-read on the corrected axis its 1e21 loss is 1.987 against 1.986 for 1.5B: a tie within noise.",
           f"MLM raw-min exponent with the 1e21 minimum at 1.2B (as published): {slope(Cs, Ns):.3f}; at 1.5B: {slope(Cs, alt):.3f}.\n"]
    open(os.path.join(OUT, "isoflop_uncertainty.md"), "w").write("\n".join(md) + "\n"); print("\n".join(md))
if __name__ == "__main__": main()
