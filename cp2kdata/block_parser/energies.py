import regex as re
import numpy as np

ENERGIES_RE = re.compile(
    r"""
    \sENERGY\|\sTotal\sFORCE_EVAL\s\(\sQS\s\)\senergy\s(\S+\s?){1,3}:\s+(?P<energy>[\s-]\d+\.\d+)
    |\sENERGY\|\sTotal\sFORCE_EVAL\s\(\sQS\s\)\senergy\s\[hartree\]\s+(?P<energy>[\s-]\d+\.\d+)
    """,
    re.VERBOSE
)


def parse_energies_list(output_file):
    energies_list = []
    for match in ENERGIES_RE.finditer(output_file):
        energy = match["energy"]
        if energy is not None:
            energies_list.append(energy)
    if energies_list:
        return np.array(energies_list, dtype=float)
    else:
        return None