#!/usr/bin/env python3
"""Dump TensorBoard event directories to plain files, one folder per run.

For each run directory under <tensorboard_root> (Megatron's --tensorboard-dir, one per run) this writes
  <out>/<run>/scalars.csv          every scalar series at full resolution: tag, step, wall_time, value
  <out>/<run>/text_summaries.json  every text summary, i.e. the Megatron argument table (lr, lr_decay_samples,
                                   split, eval_iters, mask_prob, seed, global_batch_size, ...)
Nothing is smoothed or subsampled (unlike the TensorBoard UI's 1000-point CSV export).

Usage:  pip install tensorboard
        python3 dump_tb_events.py /nfs_beijing/kubeflow-user/xingyi/plm_scaling_law/gpt/tensorboard  out/gpt
        python3 dump_tb_events.py /nfs_beijing/kubeflow-user/xingyi/plm_scaling_law/mlm/tensorboard  out/mlm
Then tar the output directory; it is a few MB per run.
"""
import os, sys, csv, json
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

def dump_run(run_dir, out_dir):
    ea = EventAccumulator(run_dir, size_guidance={"scalars": 0, "tensors": 0, "histograms": 1, "images": 1, "audio": 1})
    ea.Reload(); tags = ea.Tags(); os.makedirs(out_dir, exist_ok=True); n_rows = 0
    with open(os.path.join(out_dir, "scalars.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["tag", "step", "wall_time", "value"])
        for tag in sorted(tags.get("scalars", [])):
            for ev in ea.Scalars(tag): w.writerow([tag, ev.step, repr(ev.wall_time), repr(ev.value)]); n_rows += 1
    text = {}
    for tag in sorted(tags.get("tensors", [])):
        try:
            evs = ea.Tensors(tag)
            if evs and evs[0].tensor_proto.dtype == 7:            # DT_STRING: text summaries
                text[tag] = [s.decode("utf-8", "replace") for s in evs[-1].tensor_proto.string_val]
        except Exception as ex:
            text[tag] = f"<unreadable: {ex}>"
    json.dump(text, open(os.path.join(out_dir, "text_summaries.json"), "w"), indent=1)
    return len(tags.get("scalars", [])), n_rows, len(text)

def main(root, out):
    runs = sorted({os.path.dirname(os.path.join(dp, f)) for dp, _, fs in os.walk(root) for f in fs if f.startswith("events.out.tfevents")})
    print(f"{len(runs)} run directories under {root}")
    for r in runs:
        rel = os.path.relpath(r, root).replace(os.sep, "__"); rel = os.path.basename(os.path.abspath(root)) if rel == "." else rel
        try:
            n_tags, n_rows, n_text = dump_run(r, os.path.join(out, rel)); print(f"  {rel}: {n_tags} scalar tags, {n_rows} points, {n_text} text summaries")
        except Exception as ex:
            print(f"  {rel}: FAILED {ex}")

if __name__ == "__main__":
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
