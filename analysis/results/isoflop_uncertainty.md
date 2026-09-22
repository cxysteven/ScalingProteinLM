# Uncertainty of the IsoFLOP model-size exponents

Inputs: the (budget, model size, loss) tables behind the main figure; 7 budgets, 72 MLM and 73 CLM runs.
Noise levels: 0.006 = eval-to-eval jitter of one run (eval_iters = 3 batches); 0.010 and 0.016 = RMS difference between reruns of one configuration (154M and 3B UR50 pairs).

| objective | raw-min exponent | parabola-min exponent | gap best vs 2nd-best loss per budget |
|---|---|---|---|
| MLM | 0.767 | 0.757 | 0.0001 to 0.0070 |
| CLM | 0.571 | 0.635 | 0.0001 to 0.0010 |

## Exponents under run-to-run noise (2000 perturbations of every loss value)

| noise sd | method | MLM 95% | CLM 95% | P(MLM exponent > CLM exponent) |
|---|---|---|---|---|
| 0.006 | raw | [0.679, 0.835] | [0.531, 0.713] | 0.982 |
| 0.006 | para | [0.704, 0.827] | [0.615, 0.657] | 1.000 |
| 0.01 | raw | [0.652, 0.851] | [0.515, 0.724] | 0.962 |
| 0.01 | para | [0.680, 0.839] | [0.601, 0.683] | 0.996 |
| 0.016 | raw | [0.597, 0.862] | [0.495, 0.742] | 0.909 |
| 0.016 | para | [0.657, 0.853] | [0.572, 0.736] | 0.956 |

## MLM 1.2B FLOPs-axis error at the 1e21 budget

The 1.2B MLM curve's exported FLOPs axis was generated with N = 1e9 instead of the true 1.2086e9, so its compute is understated by 17%. Re-read on the corrected axis its 1e21 loss is 1.987 against 1.986 for 1.5B: a tie within noise.
MLM raw-min exponent with the 1e21 minimum at 1.2B (as published): 0.767; at 1.5B: 0.789.

