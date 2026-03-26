# Example: ML training optimization (Karpathy-style)

## Setup

```
/autoresearch "minimize val_bpb" "uv run train.py > run.log 2>&1 && grep '^val_bpb:' run.log" "train.py"
```

## What happens

This is the original autoresearch use case. Claude modifies `train.py` to try
different architectures, hyperparameters, and training strategies. Each
experiment trains for 5 minutes, measures val_bpb, and keeps or discards.

Overnight (8 hours sleep), you can expect ~96 experiments at 5 min each.

## Sample results.tsv

```
commit	metric	status	description
a1b2c3d	0.997900	keep	baseline
b2c3d4e	0.993200	keep	increase LR to 0.04
c3d4e5f	1.005000	discard	switch to GeLU activation
d4e5f6g	0.000000	crash	double model width (OOM)
e5f6g7h	0.989100	keep	add cosine LR schedule
f6g7h8i	0.991000	discard	rotary embeddings (no improvement)
g7h8i9j	0.985400	keep	QK norm before RoPE
h8i9j0k	0.985600	discard	increase batch size 2x
i9j0k1l	0.982100	keep	weight decay 0.1 -> 0.05
```
