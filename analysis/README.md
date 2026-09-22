# Refit of the Table A9 parametric scaling law

`refit_table_a9.py` re-derives the parametric fit L(N, D) = E + A/N^alpha + B/D^beta (Table A9 of the
paper, Appendix "Combined Power-law") from the released validation curves alone, using the objective
of the original fitting code: log-space Huber loss with delta = 1e-3 on
LSE(a - alpha ln N, b - beta ln D, e) - ln L, minimised with L-BFGS-B, parameters in log space,
no bounds. Results are written to `results/`.

```bash
pip install -r ../requirements.txt
cd analysis && python3 refit_table_a9.py --bootstrap     # ~20 min on 4 cores; drop --bootstrap for ~3 min
```

## What the refit establishes

1. **Both published rows are reproducible from the released curves**, but they were produced with
   two different constructions of the fitting set. Each construction is a lower envelope with one
   point per target compute value C (the run with the lowest loss at that C, read at its nearest
   logged point). The CLM row corresponds to 200 log-spaced targets in [1e18, 1e23] FLOPs with a
   1e18-FLOP matching tolerance (129 points from the release). The MLM row corresponds to one
   target per run at its final compute (82 points). Starting from the paper's initialisation
   [e, a, b, alpha, beta] = [1, 5, 10, 0.5, 0.5], the CLM design gives
   E = 2.13, A = 145, B = 22040, alpha = 0.371, beta = 0.495 (published 2.12, 143.9, 22036.5, 0.367, 0.496)
   and the MLM design gives E ~ 0, A = 3.41, B = 7.37, alpha = 0.042, beta = 0.100
   (published ~0, 3.365, 7.569, 0.042, 0.099). The paper's "149 and 110 samples" are counts of such
   envelope points on the 2024 working copy of the curves, not counts of training runs.

2. **The published CLM coefficients are a local optimum, not the minimiser of the objective.** Over
   the full 4500-point initialisation grid described in the paper, the global optimum on the CLM
   design is E ~ 0, alpha = 0.043, beta = 0.060 with an objective value about three times lower than
   at the published coefficients; only 3 of 4500 starts converge near the published (alpha, beta).
   The published MLM coefficients are the global optimum of their design. The same low-beta basin is
   the global optimum for CLM under every construction and token-count definition tested.

3. **The quantity the paper uses from this fit is stable across basins.** The compute-optimal
   model-size exponent implied by the parametric fit, beta/(alpha + beta), is 0.58 at the global
   optimum and 0.575 at the published coefficients, against 0.578 from the IsoFLOP profiles in the
   main text. The individual values of E, alpha and beta are poorly identified by this data; the
   allocation exponent is not.

4. **Token count.** The original code derived D from the row index of the TensorBoard export times an
   assumed batch size and evaluation interval. That is wrong by up to 2x for runs with non-default
   batch sizes and by 20-50% for exports capped at 1000 points. Refitting with D = C/(6N) changes
   the global optimum by less than 0.01 in beta for both objectives.

5. **Intervals.** The paper reports no confidence interval on these exponents; the bands in the
   frontier figure are a hand-set IsoLoss tolerance of 0.25 dex. Bootstrap percentile intervals on
   beta (`--bootstrap`) are dominated by replicates that jump between the two basins, so they are
   wide and their block-versus-point ratio is not stable across designs; see `results/table_a9_refit.md`.

Two errata in the paper follow from the above: Equation 9 places -ln L_i inside the LSE (the
implementation subtracts it after the LSE), and the appendix describes the fitting set as "the final
loss points of all the CLM and MLM that are run" whereas the code fits a lower envelope in which
most runs' final points are replaced by a better run at the same compute.

## Definitions used throughout

- N: non-embedding parameter count, from the directory name via the size map in the notebook.
- C: FLOPs as logged by Megatron, `6 * N_no_embed * tokens`; the CSV "Step" column is in GFLOPs.
- D_row: historical token count, `(row index + 1) * batch * 1024 * 300`; D_c6n: `C / (6 N)`.
- L: validation loss at the matched logged point; curves are TensorBoard exports (max 1000 points).
- `results/per_run_table.csv`: one row per released curve with these quantities at the final point.
- `results/envelope_*.csv`: the fitting sets, with the run that supplied each point.
