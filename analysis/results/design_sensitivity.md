# Sensitivity of the Table A9 fit to the fitting-set construction

Designs: `run-final` = one target per run at its final compute; `log200` = 200 log-spaced targets in [1e18, 1e23] FLOPs. Tolerance = maximum distance (GFLOPs) between a target and a run's nearest logged point for that run to be considered; the original scripts carry 1e9 (active for the CLM row) and None (active for the MLM row).
From the paper's initialisation the published CLM row is reached only when a matching tolerance is applied (`log200` at 1e8 or 1e9, `run-final` at 1e9, historical D); every other construction, and the best of 101 starts on every construction, ends in the low-beta basin. The MLM initialisation result is likewise construction-dependent (0.10 or about 0.49), while the best of 101 starts is 0.05 to 0.11 throughout.

| objective | design | tolerance | D | n | paper-p0 fit E, alpha, beta | best of 101 starts E, alpha, beta | best obj | obj at published |
|---|---|---|---|---|---|---|---|---|
| CLM | run-final | None | D_row | 115 | 4.23e-31, 0.042, 0.067 | 1.6e-90, 0.042, 0.067 | 4.047e-04 | 1.377e-03 |
| CLM | run-final | None | D_c6n | 115 | 3.67e-76, 0.042, 0.068 | 3.67e-76, 0.042, 0.068 | 3.986e-04 | 1.361e-03 |
| CLM | run-final | 1e+09 | D_row | 115 | 2.12, 0.362, 0.498 | 7.4e-70, 0.043, 0.064 | 4.053e-04 | 1.353e-03 |
| CLM | run-final | 1e+09 | D_c6n | 115 | 4.76e-32, 0.043, 0.065 | 9.66e-47, 0.043, 0.064 | 3.995e-04 | 1.337e-03 |
| CLM | log200 | None | D_row | 200 | 2.07e-15, 0.054, 0.066 | 1.47e-16, 0.054, 0.065 | 1.039e-03 | 5.220e-03 |
| CLM | log200 | None | D_c6n | 200 | 0.000203, 0.052, 0.068 | 0, 0.054, 0.066 | 1.025e-03 | 5.198e-03 |
| CLM | log200 | 1e+08 | D_row | 108 | 2.18, 0.366, 0.509 | 1.48e-54, 0.040, 0.057 | 2.831e-04 | 1.161e-03 |
| CLM | log200 | 1e+08 | D_c6n | 108 | 2.18, 0.367, 0.509 | 1.79e-08, 0.040, 0.057 | 2.740e-04 | 1.143e-03 |
| CLM | log200 | 1e+09 | D_row | 129 | 2.13, 0.371, 0.495 | 8.77e-37, 0.043, 0.060 | 4.560e-04 | 1.439e-03 |
| CLM | log200 | 1e+09 | D_c6n | 129 | 0.00305, 0.042, 0.061 | 6.25e-260, 0.042, 0.061 | 4.490e-04 | 1.416e-03 |
| CLM | log200 | 3e+09 | D_row | 141 | 1.26e-63, 0.042, 0.067 | 1.51e-23, 0.042, 0.067 | 5.826e-04 | 1.932e-03 |
| CLM | log200 | 3e+09 | D_c6n | 141 | 3.75e-47, 0.042, 0.068 | 0, 0.042, 0.068 | 5.758e-04 | 1.911e-03 |
| MLM | run-final | None | D_row | 82 | 2.96e-127, 0.042, 0.100 | 4.19e-09, 0.042, 0.100 | 4.536e-04 | 4.544e-04 |
| MLM | run-final | None | D_c6n | 82 | 0.00633, 0.034, 0.499 | 1.22e-49, 0.042, 0.104 | 5.083e-04 | 5.131e-04 |
| MLM | run-final | 1e+09 | D_row | 82 | 0.016, 0.034, 0.484 | 1.02e-06, 0.042, 0.099 | 4.565e-04 | 4.570e-04 |
| MLM | run-final | 1e+09 | D_c6n | 82 | 5.3e-32, 0.042, 0.105 | 0, 0.042, 0.104 | 5.123e-04 | 5.156e-04 |
| MLM | log200 | None | D_row | 200 | 0.0136, 0.035, 0.480 | 1.55e-68, 0.046, 0.103 | 1.107e-03 | 1.505e-03 |
| MLM | log200 | None | D_c6n | 200 | 4.22e-10, 0.046, 0.105 | 0, 0.046, 0.105 | 1.162e-03 | 1.593e-03 |
| MLM | log200 | 1e+08 | D_row | 111 | 0.774, 0.043, 0.494 | 6.47e-08, 0.052, 0.057 | 4.303e-04 | 7.231e-04 |
| MLM | log200 | 1e+08 | D_c6n | 111 | 2.03, 0.371, 0.736 | 0.0112, 0.047, 0.064 | 4.401e-04 | 7.435e-04 |
| MLM | log200 | 1e+09 | D_row | 136 | 1.06, 0.056, 0.486 | 3.6e-208, 0.059, 0.054 | 8.668e-04 | 1.267e-03 |
| MLM | log200 | 1e+09 | D_c6n | 136 | 0.989, 0.053, 0.487 | 4.35e-16, 0.055, 0.057 | 9.395e-04 | 1.249e-03 |
| MLM | log200 | 3e+09 | D_row | 150 | 0.00103, 0.050, 0.063 | 2.07e-21, 0.051, 0.063 | 9.880e-04 | 1.341e-03 |
| MLM | log200 | 3e+09 | D_c6n | 150 | 5.78e-63, 0.049, 0.067 | 3.51e-07, 0.050, 0.066 | 1.021e-03 | 1.318e-03 |
