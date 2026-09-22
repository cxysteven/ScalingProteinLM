# What the raw training logs establish

Source: the private archive `cxysteven/ScalingProteinLM-rawlogs` (September 2026), which holds the
original experiment directory, twelve Megatron stdout logs (eleven mixed-objective runs and the dense
MLM 1.2B run), and two independent audit reports. No raw TensorBoard event files survive for the 209
dense runs; the released CSVs are their only record.

## Training recipe (from the Megatron argument tables, identical across all twelve logs)

- Learning rate: cosine decay from `lr` to `min_lr = lr/10` over `lr_decay_samples = train_samples`,
  i.e. the schedule is set to the run's own budget and reaches its floor at the last step. Linear
  warm-up over 2.5% of samples. Verified step by step in the MLM 1.2B log (3e-4 at 2.5%, 1.70e-4 at
  50%, 3.0e-5 at 100%). This rules out the schedule-truncation bias that inflated Kaplan et al.'s
  exponents: every IsoFLOP point is a fully decayed run at its own budget.
- Peak `lr` scales with size: 6e-4 (25M-49M), 5.5e-4 (85M-130M), 5e-4 (200M-230M), 4e-4 (470M),
  3.5e-4 (880M), 3e-4 (1B+). Batch 512 sequences below 1B, 1024 at 1B and above; sequence length 1024.
- AdamW beta2 0.95, weight decay 0.1, gradient clipping 1.0, bf16. MLM: `mask_prob = 0.15`, GLM-style
  span masking with `bert_prob = 1.0`.
- Data mix (UniMeta): UniRef50 8.5%, UniRef90 19.5%, ColabFold "c" 19.5%, ColabFold "m" 52.5%.
- Parameter counts: the 1.2B model has 1,208,881,136 parameters in total and 1,208,618,992 without
  embeddings; `model_size_map` uses the total. With a 128-token vocabulary the difference is 0.02%.

## Evaluation

- `eval_interval = 300` steps, `eval_iters = 3`: each validation point is the mean over 3 batches,
  about 3.1M tokens (about 470K supervised positions for MLM). Consecutive validation points of one run
  jitter with sd 0.0055 (MLM) to 0.0069 (CLM) once training is past 60% of its budget.
- Reruns of one configuration differ by RMS 0.010 (154M MLM on UR50) to 0.016 (3B MLM on UR50) at
  matched token counts. That is the noise relevant to choosing the best model size at a budget.
- The best and second-best losses at each IsoFLOP budget differ by 0.0001 to 0.007. The per-budget
  optimum is therefore chosen within noise; see `results/isoflop_uncertainty.md` for the effect.
- Data split: the MLM 1.2B run used `split = 949,50,1`; the mixed-objective runs used `979,20,1`.
  Whether all dense runs shared one validation split is not recoverable from the surviving logs.

## Known data defects (from the two audits, confirmed here)

- The MLM 1.2B CSV was reconstructed from the text log with `extract_loss.py`, which computed FLOPs
  as `iteration * 6 * 1024 * 1024`, i.e. with N = 1e9. Its FLOPs are 17% low; multiply by 1.2086 to
  correct. On the corrected axis its 1e21 loss ties with the 1.5B model, which moves the main-figure
  MLM exponent from 0.767 to 0.789 depending on which is taken as the minimum.
- Three CLM curves are stored byte-identically under two different model-size directories, and one
  local MLM 650M export has a "samples" axis mislabelled as FLOPs (not in the public release).
- The historical token count in the fitting scripts came from the CSV row index (see
  `README.md`); nine paired token/FLOPs exports confirm D = C/(6N) to within 0.13% in N.

## What is still missing

- Raw event files or text logs for the other 208 dense runs (only the MLM 1.2B log survives).
- The exact 149 CLM and 110 MLM fitting points used for Table A9 in 2024.
- The mapping from each hand-entered value in the main-figure tables to its source run and export.
- Seeded replicates at fixed (N, C): the only reruns are on UR50, not on the IsoFLOP grid.
