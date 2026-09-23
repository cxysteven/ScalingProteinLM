# IsoFLOP tables rebuilt from the released curves

Per run: last logged validation loss (as in the paper) and the mean of the last five logged losses. Runs trained to a standard budget only; duplicates counted once; the MLM 1.2B all-1-epoch curve (wrong FLOPs axis) excluded.

## CLM: 116 distinct curves, 77 used across 7 budgets; runs per budget: 1e+18: 6, 3e+18: 10, 1e+19: 12, 3e+19: 14, 1e+20: 14, 3e+20: 11, 1e+21: 10
Final compute within budget: median C/budget 1.000, range 0.907 to 1.148. Last-5 window spans 2.4% of compute (median); within-window loss sd median 0.0060.

Provenance of the 73 hand-entered values (a released run at that budget with loss within 0.003): same size as the label 44; size matches only the file-name label 2; only runs of another size 17; no released run within 0.003: 10.
Entries with no released run within 0.003: 1e+19 300M (2.568, nearest released loss 0.004 away); 3e+19 470M (2.469, nearest released loss 0.004 away); 1e+21 1.2B (2.187, nearest released loss 0.016 away); 1e+21 1.5B (2.181, nearest released loss 0.022 away); 1e+21 1.7B (2.18, nearest released loss 0.023 away); 1e+21 2B (2.186, nearest released loss 0.017 away); 1e+21 2.4B (2.183, nearest released loss 0.020 away); 1e+21 2.8B (2.2, nearest released loss 0.003 away); 1e+21 5B (2.242, nearest released loss 0.006 away); 1e+21 7B (2.293, nearest released loss 0.005 away)

Hand-entered values matched to a released run: 67 of 73; unmatched: 6. Hand minus last-logged loss: median -0.0007, MAD 0.0042; 29 entries differ by more than 0.005:
| budget | size | hand-entered | last logged | last-5 mean | run |
|---|---|---|---|---|---|
| 1e+18 | 7 | 2.6239 | 2.6409 | 2.6373 | run-tensorboard_gpt_25.1M_1024l_1e18flops_all0.03ep-tag-lm-l |
| 1e+18 | 7 | 2.64 | 2.6336 | 2.6251 | run-gpt_47M_1024l_1e18flops_bsz250k_all0.02ep-tag-lm-loss-va |
| 3e+18 | 7 | 2.591 | 2.5969 | 2.5914 | run-tensorboard_gpt_25.1M_1024l_3e18flops_all0.1ep-tag-lm-lo |
| 3e+18 | 7 | 2.593 | 2.5841 | 2.5883 | run-gpt_85M_1024l_3e18flops_all0.03ep-tag-lm-loss-validation |
| 1e+19 | 7 | 2.509 | 2.4945 | 2.5130 | run-gpt_85M_1024l_1e19flops_all0.1ep-tag-lm-loss-validation_ |
| 1e+19 | 7 | 2.5069 | 2.5156 | 2.5133 | run-gpt_130M_1024l_1e19flops_all0.07ep-tag-lm-loss-validatio |
| 1e+19 | 7 | 2.533 | 2.5387 | 2.5319 | run-tensorboard_gpt_230M_1024l_1e19flops_all0.04ep-tag-lm-lo |
| 3e+19 | 7 | 2.475 | 2.4828 | 2.4728 | run-gpt_49M_1024l_3e19flops_all0.38ep-tag-lm-loss-validation |
| 3e+19 | 7 | 2.463 | 2.4734 | 2.4637 | run-gpt_85M_1024l_3e19flops_all0.3ep-tag-lm-loss-validation_ |
| 3e+19 | 7 | 2.454 | 2.4609 | 2.4545 | run-tensorboard_gpt_106M_1024l_3e19flops_all0.24ep-tag-lm-lo |
| 3e+19 | 7 | 2.447 | 2.4329 | 2.4350 | run-gpt_154M_1024l_3e19flops_all0.16ep-tag-lm-loss-validatio |
| 3e+19 | 7 | 2.445 | 2.4360 | 2.4390 | run-gpt_170M_1024l_3e19flops_all0.15ep-tag-lm-loss-validatio |
| 1e+20 | 7 | 2.41 | 2.4198 | 2.4071 | run-tensorboard_gpt_106M_1024l_1e20flops_all0.78ep-tag-lm-lo |
| 1e+20 | 7 | 2.39 | 2.3793 | 2.3911 | run-gpt_154M_1024l_1e20flops_all0.5ep-tag-lm-loss-validation |
| 1e+20 | 7 | 2.363 | 2.3766 | 2.3709 | run-gpt_393M_1024l_1e20flops_all0.21ep-tag-lm-loss-validatio |
| 1e+20 | 7 | 2.362 | 2.3543 | 2.3630 | run-gpt_470M_1024l_1e20flops_all0.18ep-tag-lm-loss-validatio |
| 1e+20 | 7 | 2.385 | 2.3751 | 2.3839 | run-gpt_880M_1024l_1e20flops_all0.09ep-tag-lm-loss-validatio |
| 1e+20 | 7 | 2.42 | 2.4474 | 2.4437 | run-gpt_1b_1024l_1e20flops_all0.07ep-tag-lm-loss-validation_ |
| 1e+20 | 7 | 2.442 | 2.4282 | 2.4350 | run-gpt_1.5b_1024l_1e20flops_all0.05ep-tag-lm-loss-validatio |
| 3e+20 | 7 | 2.294 | 2.3003 | 2.3008 | run-gpt_880M_1024l_3e20flops_all0.28ep-tag-lm-loss-validatio |
| 3e+20 | 7 | 2.331 | 2.3242 | 2.3321 | run-gpt_1.7b_1024l_3e20flops_all0.14ep-tag-lm-loss-validatio |
| 1e+21 | 7 | 2.187 | 2.2072 | 2.2070 | run-gpt_1b_1024_lr3.0_noreg_all0.75ep_bf16-tag-lm-loss-valid |
| 1e+21 | 7 | 2.181 | 2.2144 | 2.2142 | run-gpt_1.5b_1024l_1e21flops_all0.5ep-tag-lm-loss-validation |
| 1e+21 | 7 | 2.18 | 2.2038 | 2.2033 | run-gpt_1.7b_1024_noreg_all0.5ep_bf16-tag-lm-loss-validation |
| 1e+21 | 7 | 2.183 | 2.2110 | 2.2106 | run-gpt_2.4b_1024l_1e21flops_all0.35ep-tag-lm-loss-validatio |
| 1e+21 | 7 | 2.2 | 2.2212 | 2.2145 | run-gpt_3b_1024l_1e21flops_all0.3ep-tag-lm-loss-validation_v |
| 1e+21 | 7 | 2.203 | 2.2313 | 2.2278 | run-gpt_3.4b_1024l_1e21flops_all0.25ep-tag-lm-loss-validatio |
| 1e+21 | 7 | 2.242 | 2.2484 | 2.2550 | run-gpt_5b_1024l_1e21flops_all0.17ep-tag-lm-loss-validation_ |
| 1e+21 | 7 | 2.293 | 2.3010 | 2.2975 | run-gpt_7b_1024l_1e21flops_all0.11ep_wu10-tag-lm-loss-valida |

Unmatched hand-entered entries: 1e+18 7; 1e+18 7; 3e+19 7; 1e+20 7; 1e+21 7; 1e+21 7

| source of losses | raw-min exponent | parabola-min exponent | raw-min 95% under noise 0.005 | under noise 0.010 |
|---|---|---|---|---|
| hand-entered table (paper) | 0.571 | 0.635 | | |
| rebuilt, last logged loss | 0.675 | 0.624 | [0.560, 0.763] | [0.491, 0.772] |
| rebuilt, mean of last 5 | 0.660 | 0.626 | [0.504, 0.711] | [0.484, 0.735] |

Per-budget minimum (mean of last 5): 1e+18: N=13,192,320 (gap to 2nd best 0.0041, 6 runs), 3e+18: N=47,775,744 (gap to 2nd best 0.0033, 10 runs), 1e+19: N=106,168,320 (gap to 2nd best 0.0006, 12 runs), 3e+19: N=154,448,288 (gap to 2nd best 0.0040, 14 runs), 1e+20: N=550,502,400 (gap to 2nd best 0.0022, 13 runs), 3e+20: N=550,502,400 (gap to 2nd best 0.0055, 11 runs), 1e+21: N=1,784,851,968 (gap to 2nd best 0.0037, 10 runs)

## MLM: 81 distinct curves, 70 used across 7 budgets; runs per budget: 1e+18: 7, 3e+18: 8, 1e+19: 10, 3e+19: 11, 1e+20: 12, 3e+20: 12, 1e+21: 10
Final compute within budget: median C/budget 1.000, range 0.994 to 1.088. Last-5 window spans 2.1% of compute (median); within-window loss sd median 0.0053.

Provenance of the 72 hand-entered values (a released run at that budget with loss within 0.003): same size as the label 36; size matches only the file-name label 1; only runs of another size 17; no released run within 0.003: 18.
Entries with no released run within 0.003: 1e+18 3M (2.407, nearest released loss 0.004 away); 1e+18 13M (2.41, nearest released loss 0.007 away); 3e+18 10M (2.356, nearest released loss 0.005 away); 3e+18 13M (2.355, nearest released loss 0.006 away); 3e+18 47M (2.38, nearest released loss 0.006 away); 1e+19 154M (2.329, nearest released loss 0.017 away); 1e+19 170M (2.333, nearest released loss 0.014 away); 3e+19 300M (2.26, nearest released loss 0.005 away); 3e+19 470M (2.311, nearest released loss 0.019 away); 1e+20 550M (2.158, nearest released loss 0.005 away); 1e+20 880M (2.219, nearest released loss 0.009 away); 3e+20 1.2B (2.127, nearest released loss 0.008 away); 3e+20 1.5B (2.131, nearest released loss 0.012 away); 3e+20 2.8B (2.214, nearest released loss 0.034 away); 1e+21 3.4B (2.052, nearest released loss 0.005 away); 1e+21 4B (2.068, nearest released loss 0.008 away); 1e+21 5B (2.118, nearest released loss 0.007 away); 1e+21 7B (2.174, nearest released loss 0.026 away)

Hand-entered values matched to a released run: 60 of 72; unmatched: 12. Hand minus last-logged loss: median 0.0003, MAD 0.0037; 25 entries differ by more than 0.005:
| budget | size | hand-entered | last logged | last-5 mean | run |
|---|---|---|---|---|---|
| 1e+18 | 7 | 2.4011 | 2.3961 | 2.3964 | run-mlm_10.1M_1024l_1e18flops_all0.09ep-tag-lm-loss-validati |
| 1e+18 | 7 | 2.41 | 2.3997 | 2.3973 | run-mlm_10M_1024l_1e18flops_all0.06ep-tag-lm-loss-validation |
| 3e+18 | 7 | 2.355 | 2.3430 | 2.3479 | run-mlm_10M_1024l_3e18flops_all0.19ep-tag-lm-loss-validation |
| 3e+18 | 7 | 2.366 | 2.3741 | 2.3675 | run-mlm_25.1M_1024l_3e18flops_all0.1ep-tag-lm-loss-validatio |
| 1e+19 | 7 | 2.28 | 2.2887 | 2.2880 | run-mlm_25M_1024l_1e19flops_all0.25ep-tag-lm-loss-validation |
| 3e+19 | 7 | 2.215 | 2.2239 | 2.2154 | run-mlm_47M_1024l_3e19flops_all0.5ep-tag-lm-loss-validation_ |
| 3e+19 | 7 | 2.215 | 2.2259 | 2.2166 | run-mlm_106M_1024l_3e19flops_all0.24ep-tag-lm-loss-validatio |
| 3e+19 | 7 | 2.224 | 2.2154 | 2.2193 | run-mlm_154M_1024l_3e19flops_all0.16ep-tag-lm-loss-validatio |
| 3e+19 | 7 | 2.26 | 2.2549 | 2.2466 | run-mlm_300M_1024l_3e19flops_all0.08ep-tag-lm-loss-validatio |
| 3e+19 | 7 | 2.289 | 2.2798 | 2.2777 | run-mlm_393M_1024l_3e19flops_all0.06ep-tag-lm-loss-validatio |
| 3e+19 | 7 | 2.311 | 2.2918 | 2.2917 | run-mlm_470M_1024l_3e19flops_all0.05ep-tag-lm-loss-validatio |
| 1e+20 | 7 | 2.144 | 2.1494 | 2.1423 | run-mlm_393M_1024l_1e20flops_all0.21ep-tag-lm-loss-validatio |
| 1e+20 | 7 | 2.148 | 2.1334 | 2.1448 | run-mlm_470M_1024l_1e20flops_all0.18ep-tag-lm-loss-validatio |
| 1e+20 | 7 | 2.219 | 2.2043 | 2.2102 | run-mlm_880M_1024l_1e20flops_all0.09ep-tag-lm-loss-validatio |
| 3e+20 | 7 | 2.0591 | 2.0518 | 2.0575 | run-mlm_393M_1024l_3e20flops_all0.64ep-tag-lm-loss-validatio |
| 3e+20 | 7 | 2.127 | 2.1185 | 2.1194 | run-mlm_1b_1024l_3e20flops_all0.21ep-tag-lm-loss-validation_ |
| 3e+20 | 7 | 2.131 | 2.1182 | 2.1172 | run-mlm_1.5b_1024l_3e20flops_all0.16ep-tag-lm-loss-validatio |
| 3e+20 | 7 | 2.172 | 2.1559 | 2.1624 | run-mlm_1.7b_1024l_3e20flops_all0.14ep-tag-lm-loss-validatio |
| 3e+20 | 7 | 2.182 | 2.1568 | 2.1590 | run-mlm_2.4b_1024l_3e20flops_all0.1ep-tag-lm-loss-validation |
| 3e+20 | 7 | 2.214 | 2.1743 | 2.1799 | run-mlm_3b_1024l_3e20flops_all0.09ep-tag-lm-loss-validation_ |
| 1e+21 | 7 | 1.989 | 1.9798 | 1.9896 | run-mlm_880M_1024l_1e21flops_all0.28ep-tag-lm-loss-validatio |
| 1e+21 | 7 | 2.052 | 2.0410 | 2.0408 | run-mlm_3.4b_1024l_1e21flops_all0.25ep-tag-lm-loss-validatio |
| 1e+21 | 7 | 2.068 | 2.0573 | 2.0599 | run-mlm_4b_1024l_1e21flops_all0.2ep-tag-lm-loss-validation_v |
| 1e+21 | 7 | 2.118 | 2.1038 | 2.1112 | run-mlm_5b_1024l_1e21flops_all0.17ep-tag-lm-loss-validation_ |
| 1e+21 | 7 | 2.174 | 2.1482 | 2.1482 | run-mlm_7b_1024l_1e21flops_all0.11ep_lr1.2-tag-lm-loss-valid |

Unmatched hand-entered entries: 1e+18 7; 1e+18 7; 3e+18 7; 3e+18 7; 3e+18 7; 1e+19 7; 1e+19 7; 3e+19 7; 3e+19 7; 1e+20 7; 1e+21 7; 1e+21 7

| source of losses | raw-min exponent | parabola-min exponent | raw-min 95% under noise 0.005 | under noise 0.010 |
|---|---|---|---|---|
| hand-entered table (paper) | 0.767 | 0.757 | | |
| rebuilt, last logged loss | 0.708 | 0.729 | [0.668, 0.771] | [0.641, 0.789] |
| rebuilt, mean of last 5 | 0.729 | 0.736 | [0.653, 0.762] | [0.629, 0.790] |

Per-budget minimum (mean of last 5): 1e+18: N=9,830,400 (gap to 2nd best 0.0009, 7 runs), 3e+18: N=13,192,320 (gap to 2nd best 0.0132, 8 runs), 1e+19: N=47,775,744 (gap to 2nd best 0.0058, 10 runs), 3e+19: N=47,775,744 (gap to 2nd best 0.0003, 11 runs), 1e+20: N=231,211,008 (gap to 2nd best 0.0018, 12 runs), 3e+20: N=550,502,400 (gap to 2nd best 0.0005, 12 runs), 1e+21: N=1,208,881,136 (gap to 2nd best 0.0236, 9 runs)

P(MLM exponent > CLM exponent) on the rebuilt last-5 tables under noise 0.005: 0.916
P(MLM exponent > CLM exponent) on the rebuilt last-5 tables under noise 0.01: 0.875

## Compute-optimal model size at the paper's comparison budgets

| objective | budget | published law | rebuilt, raw min | rebuilt, parabola | 95% under noise 0.01 |
|---|---|---|---|---|---|
| CLM | PROGEN2-xlarge budget, 1.34e+22 FLOPs | 7.8B | 9.8B | 7.6B | 3.8 to 15.2B |
| CLM | budget of the paper's 7.2B model, 1.14e+22 FLOPs | 7.1B | 8.8B | 6.8B | 3.5 to 13.5B |
| MLM | ESM-2 3B budget, 1.68e+22 FLOPs | 10.9B | 8.8B | 7.7B | 4.7 to 13.5B |
