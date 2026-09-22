# Table A9 refit from the released curves

Published Table A9: CLM E=2.123 A=143.9 B=22036.5 alpha=0.367 beta=0.496 ; MLM E~0 A=3.365 B=7.569 alpha=0.042 beta=0.099

| objective | design | D | n | fit from paper p0 (E, alpha, beta) | grid global best (E, alpha, beta) | best obj | obj at published | implied N_opt exponent beta/(alpha+beta) at best |
|---|---|---|---|---|---|---|---|---|
| CLM | log200 | D_row | 129 | 2.13, 0.371, 0.495 | 1.43e-90, 0.043, 0.060 | 4.560e-04 | 1.439e-03 | 0.582 |
| CLM | log200 | D_c6n | 129 | 0.00305, 0.042, 0.061 | 3.52e-24, 0.042, 0.061 | 4.490e-04 | 1.416e-03 | 0.591 |
| CLM | run-final | D_row | 115 | 4.23e-31, 0.042, 0.067 | 2.65e-54, 0.042, 0.067 | 4.047e-04 | 1.377e-03 | 0.616 |
| CLM | run-final | D_c6n | 115 | 3.67e-76, 0.042, 0.068 | 1.23e-21, 0.042, 0.068 | 3.986e-04 | 1.361e-03 | 0.618 |
| MLM | log200 | D_row | 136 | 1.06, 0.056, 0.486 | 5.7e-129, 0.059, 0.054 | 8.668e-04 | 1.267e-03 | 0.481 |
| MLM | log200 | D_c6n | 136 | 0.989, 0.053, 0.487 | 4.08e-190, 0.055, 0.057 | 9.395e-04 | 1.249e-03 | 0.511 |
| MLM | run-final | D_row | 82 | 2.96e-127, 0.042, 0.100 | 0, 0.042, 0.100 | 4.536e-04 | 4.544e-04 | 0.703 |
| MLM | run-final | D_c6n | 82 | 0.00633, 0.034, 0.499 | 1.32e-210, 0.042, 0.105 | 5.083e-04 | 5.131e-04 | 0.714 |

## Bootstrap 95% intervals (200 replicates, 25-start refit per replicate)

| objective | design | D | scheme | blocks | beta 95% | beta/(alpha+beta) 95% | frac beta<0.2 |
|---|---|---|---|---|---|---|---|
| CLM | log200 | D_row | iid | 129 | [0.052, 0.267] | [0.508, 0.882] | 0.96 |
| CLM | log200 | D_row | budget | 8 | [0.046, 0.269] | [0.239, 0.880] | 0.96 |
| CLM | log200 | D_row | randblk | 8 | [0.054, 0.070] | [0.530, 0.633] | 0.99 |
| CLM | log200 | D_c6n | iid | 129 | [0.051, 0.271] | [0.275, 0.884] | 0.94 |
| CLM | log200 | D_c6n | budget | 8 | [0.045, 0.279] | [0.218, 0.892] | 0.93 |
| CLM | log200 | D_c6n | randblk | 8 | [0.054, 0.265] | [0.533, 0.881] | 0.96 |
| CLM | run-final | D_row | iid | 115 | [0.059, 0.083] | [0.566, 0.684] | 0.99 |
| CLM | run-final | D_row | budget | 9 | [0.050, 0.270] | [0.399, 0.879] | 0.94 |
| CLM | run-final | D_row | randblk | 9 | [0.059, 0.083] | [0.565, 0.685] | 0.98 |
| CLM | run-final | D_c6n | iid | 115 | [0.050, 0.115] | [0.291, 0.705] | 0.97 |
| CLM | run-final | D_c6n | budget | 9 | [0.048, 0.269] | [0.329, 0.878] | 0.95 |
| CLM | run-final | D_c6n | randblk | 9 | [0.061, 0.267] | [0.570, 0.878] | 0.94 |
| MLM | log200 | D_row | iid | 136 | [0.044, 0.256] | [0.290, 0.849] | 0.97 |
| MLM | log200 | D_row | budget | 9 | [0.042, 0.261] | [0.184, 0.869] | 0.95 |
| MLM | log200 | D_row | randblk | 9 | [0.044, 0.106] | [0.316, 0.655] | 0.98 |
| MLM | log200 | D_c6n | iid | 136 | [0.046, 0.265] | [0.351, 0.846] | 0.96 |
| MLM | log200 | D_c6n | budget | 9 | [0.042, 0.254] | [0.163, 0.856] | 0.96 |
| MLM | log200 | D_c6n | randblk | 9 | [0.047, 0.114] | [0.362, 0.711] | 0.98 |
| MLM | run-final | D_row | iid | 82 | [0.078, 0.127] | [0.649, 0.754] | 0.97 |
| MLM | run-final | D_row | budget | 9 | [0.043, 0.435] | [0.267, 0.913] | 0.94 |
| MLM | run-final | D_row | randblk | 9 | [0.080, 0.475] | [0.652, 0.931] | 0.97 |
| MLM | run-final | D_c6n | iid | 82 | [0.079, 0.258] | [0.653, 0.836] | 0.97 |
| MLM | run-final | D_c6n | budget | 9 | [0.047, 0.530] | [0.377, 0.932] | 0.87 |
| MLM | run-final | D_c6n | randblk | 9 | [0.056, 0.477] | [0.540, 0.932] | 0.95 |
