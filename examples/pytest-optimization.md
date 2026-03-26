# Example: Optimize pytest pass rate

## Setup

```
/autoresearch "maximize pytest pass count" "pytest --tb=no -q 2>&1 | tail -1" "src/"
```

## What happens

1. Claude creates `autoresearch/mar26` branch
2. Runs baseline: `23 passed, 5 failed`
3. Starts experimenting:
   - Fix type error in `src/parser.py` → 24 passed → **keep**
   - Add null check in `src/api.py` → 24 passed → discard (no improvement)
   - Fix off-by-one in `src/pagination.py` → 25 passed → **keep**
   - Refactor retry logic → crash → revert
   - Fix edge case in date parsing → 26 passed → **keep**
   - ...continues until all tests pass or you stop it

## Sample results.tsv

```
commit	metric	status	description
a1b2c3d	23	keep	baseline
b2c3d4e	24	keep	fix type error in parser.py line 42
c3d4e5f	24	discard	add null check in api.py (no improvement)
d4e5f6g	25	keep	fix off-by-one in pagination.py
e5f6g7h	0	crash	refactor retry logic (import error)
f6g7h8i	26	keep	fix date parsing edge case for leap years
```
