#!/usr/bin/env python3
"""
Test for bistability: run the model from different initial conditions
and check whether multiple distinct steady states exist.

FIX (P1): the original used Unicode symbols (check marks, emoji) that raise
UnicodeEncodeError on Windows consoles using a GBK/locale code page and abort
the script. This version uses ASCII labels and forces UTF-8 stdout when the
platform supports it, so it runs on Windows, macOS and Linux.
"""

import sys

# Guard against non-UTF-8 consoles (Windows GBK); harmless elsewhere.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
from ode_model import DEFAULT_PARAMS_DM, simulate, get_final_state, regscore


def main():
    params = DEFAULT_PARAMS_DM
    control = {'k_ROS': 0.0, 'alpha_AMPK': 0.0, 'E_matrix': 0.0}

    initial_conditions = [
        [0.7, 0.15, 0.2],   # High inflammation start
        [0.5, 0.3, 0.4],    # Moderate start
        [0.3, 0.5, 0.6],    # Low inflammation start
        [0.1, 0.8, 0.8],    # Healing start
    ]

    print("=" * 70)
    print("Bistability Test - Bone Microenvironment ODE Model")
    print("=" * 70)

    results = {}
    for init in initial_conditions:
        sol = simulate(params, control, init)
        X, Y, Z = get_final_state(sol)
        r = regscore(X, Y, Z)
        bounds_ok = all(-0.01 <= v <= 1.01 for v in [X, Y, Z])
        status = "OK" if bounds_ok else "OUT-OF-BOUNDS"
        results[tuple(init)] = (X, Y, Z, r)
        print(f"  Init {init} -> X={X:.4f}, Y={Y:.4f}, Z={Z:.4f}, "
              f"RS={r:.4f}  [{status}]")

    unique_rs = set(round(v[3], 2) for v in results.values())
    print()
    print(f"  Distinct steady states (RS rounded to 2 dp): {len(unique_rs)}")
    if len(unique_rs) > 1:
        print("  RESULT: bistability detected (multiple attractors).")
    else:
        print("  RESULT: single attractor (no bistability from these starts).")
    print()


if __name__ == "__main__":
    main()
