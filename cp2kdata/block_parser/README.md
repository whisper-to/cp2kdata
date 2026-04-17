# cp2kdata-cp2k2025-fix

Fix: cp2kdata dpdata fails to parse CP2K 2025.1 output files

## Problem

When using `dpdata` with `fmt="cp2kdata/e_f"` to read CP2K 2025.1 output files, the parser fails to extract energies, forces, and stress tensors correctly. This is because CP2K 2025.1 changed the format of these output blocks compared to older versions (e.g., 2023.1).

Specifically:
- **Energies**: the unit label changed from a 6-character token to `[hartree]`
- **Forces**: the output block changed from `ATOMIC FORCES in [a.u.]` to a `FORCES|` prefixed format with scientific notation and an extra `|f|` column
- **Stress tensor**: the unit changed from `[GPa]` to `[bar]` with a `STRESS|` prefixed format

## Fix

The three modified parser files are provided in this repository:

- `block_parser/energies.py`
- `block_parser/forces.py`
- `block_parser/stress.py`

To apply the fix, simply copy these three files into your local cp2kdata installation:
```bash
cp energies.py forces.py stress.py \
  $(python3 -c "import cp2kdata; import os; print(os.path.join(os.path.dirname(cp2kdata.__file__), 'block_parser'))")
```

Or locate the directory manually:
```bash
python3 -c "import cp2kdata; print(cp2kdata.__file__)"
# then copy into the block_parser/ subdirectory
```

## Validation

The fix was validated by running a single-point energy+force calculation on the same structure using both CP2K 2023.1 and CP2K 2025.1, then comparing the parsed outputs with `dpdata`. The differences are at the level of floating point rounding between the two CP2K versions and are physically negligible.
