import regex as re
import numpy as np

STRESS_RE = re.compile(
    r"""
    (\sSTRESS\sTENSOR\s\[GPa\]
    \n
    \s+X\s+Y\s+Z\s*\n
    \s+X
    \s+(?P<xx>[\s-]\d+\.\d+)
    \s+(?P<xy>[\s-]\d+\.\d+)
    \s+(?P<xz>[\s-]\d+\.\d+)\n
    \s+Y
    \s+(?P<yx>[\s-]\d+\.\d+)
    \s+(?P<yy>[\s-]\d+\.\d+)
    \s+(?P<yz>[\s-]\d+\.\d+)\n
    \s+Z
    \s+(?P<zx>[\s-]\d+\.\d+)
    \s+(?P<zy>[\s-]\d+\.\d+)
    \s+(?P<zz>[\s-]\d+\.\d+)\n
    |# pattern for v8.1 GPa
    \s+STRESS\|\sAnalytical\sstress\stensor\s\[GPa\]\s*\n
    \s+STRESS\|\s+x\s+y\s+z\s*\n
    \s+STRESS\|\s+x
    \s+(?P<xx>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<xy>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<xz>[\s-]\d+\.\d+E[\+\-]\d\d)\n
    \s+STRESS\|\s+y
    \s+(?P<yx>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<yy>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<yz>[\s-]\d+\.\d+E[\+\-]\d\d)\n
    \s+STRESS\|\s+z
    \s+(?P<zx>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<zy>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<zz>[\s-]\d+\.\d+E[\+\-]\d\d)\n
    |# pattern for bar unit for CP2K/2025
    \s+STRESS\|\sAnalytical\sstress\stensor\s\[bar\]\s*\n
    \s+STRESS\|\s+x\s+y\s+z\s*\n
    \s+STRESS\|\s+x
    \s+(?P<xx>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<xy>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<xz>[\s-]\d+\.\d+E[\+\-]\d\d)\n
    \s+STRESS\|\s+y
    \s+(?P<yx>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<yy>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<yz>[\s-]\d+\.\d+E[\+\-]\d\d)\n
    \s+STRESS\|\s+z
    \s+(?P<zx>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<zy>[\s-]\d+\.\d+E[\+\-]\d\d)
    \s+(?P<zz>[\s-]\d+\.\d+E[\+\-]\d\d)\n
    )
    """,
    re.VERBOSE
)

STRESS_UNIT_RE = re.compile(
    r"STRESS\|\sAnalytical\sstress\stensor\s\[(?P<unit>GPa|bar)\]"
)

BAR_TO_GPa = 1e-4


def parse_stress_tensor_list(output_file):
    unit_match = STRESS_UNIT_RE.search(output_file)
    unit = unit_match.group("unit") if unit_match else "GPa"

    stress_tensor_list = []
    for match in STRESS_RE.finditer(output_file):
        stress_tensor = [
            [match["xx"], match["xy"], match["xz"]],
            [match["yx"], match["yy"], match["yz"]],
            [match["zx"], match["zy"], match["zz"]]
        ]
        stress_tensor_list.append(stress_tensor)

    if stress_tensor_list:
        result = np.array(stress_tensor_list, dtype=float)
        if unit == "bar":
            result = result * BAR_TO_GPa
        return result
    else:
        return None