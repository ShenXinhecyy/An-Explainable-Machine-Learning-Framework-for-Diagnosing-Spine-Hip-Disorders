#!/usr/bin/env python3
"""
Compare different therapeutic strategies for the Diabetes Mellitus model.

FIX (P0): the original script only tested a *supra-threshold* ROS arm
(k_ROS = 0.5), so "ROS + AMPK" was identical to "ROS alone" and the
sub-threshold synergy reported in the manuscript could not be reproduced.

This version adds the two sub-threshold arms that the manuscript relies on
and prints the heuristic additive expectation explicitly:

    RS_additive = RS(ROS 0.3) + RS(AMPK 0.35) - RS(none)

so that the synergy excess is directly visible from the output.
"""

import numpy as np
from ode_model import DEFAULT_PARAMS_DM, simulate, get_final_state, regscore


def final_rs(params, control, init):
    sol = simulate(params, control, init)
    X, Y, Z = get_final_state(sol)
    return X, Y, Z, regscore(X, Y, Z)


def main():
    params = DEFAULT_PARAMS_DM
    init_state = [0.7, 0.15, 0.20]
    none = {'k_ROS': 0.0, 'alpha_AMPK': 0.0, 'E_matrix': 0.0}

    strategies = [
        ('None (control)',           {'k_ROS': 0.0, 'alpha_AMPK': 0.0,  'E_matrix': 0.0}),
        ('Sub-threshold ROS only',   {'k_ROS': 0.3, 'alpha_AMPK': 0.0,  'E_matrix': 0.0}),
        ('AMPK activation only',     {'k_ROS': 0.0, 'alpha_AMPK': 0.35, 'E_matrix': 0.0}),
        ('Stiffness only',           {'k_ROS': 0.0, 'alpha_AMPK': 0.0,  'E_matrix': 0.2}),
        ('Supra-threshold ROS only', {'k_ROS': 0.5, 'alpha_AMPK': 0.0,  'E_matrix': 0.0}),
        ('Sub-threshold ROS + AMPK', {'k_ROS': 0.3, 'alpha_AMPK': 0.35, 'E_matrix': 0.0}),
        ('Triple Push-Pull',         {'k_ROS': 0.5, 'alpha_AMPK': 0.35, 'E_matrix': 0.2}),
    ]

    print("=" * 78)
    print("Therapeutic Strategy Comparison (Diabetes Model)")
    print("=" * 78)
    print(f"{'Strategy':28s}  {'X':>8s}  {'Y':>8s}  {'Z':>8s}  {'RS':>8s}")
    print("-" * 78)

    rs = {}
    for sname, control in strategies:
        X, Y, Z, r = final_rs(params, control, init_state)
        rs[sname] = r
        print(f"  {sname:28s}  {X:>8.4f}  {Y:>8.4f}  {Z:>8.4f}  {r:>8.4f}")

    # ----- heuristic additive expectation (manuscript value) -----
    r_none = rs['None (control)']
    r_ros3 = rs['Sub-threshold ROS only']
    r_ampk = rs['AMPK activation only']
    r_combo = rs['Sub-threshold ROS + AMPK']

    additive = r_ros3 + r_ampk - r_none
    excess = r_combo - additive

    print()
    print("-" * 78)
    print(f"  Sub-threshold combo            RS = {r_combo:.4f}")
    print(f"  Heuristic additive expectation RS = {additive:.4f}  "
          f"(= {r_ros3:.4f} + {r_ampk:.4f} - {r_none:.4f})")
    print(f"  Synergy excess                 = {excess:+.4f}")
    print()
    print("  NOTE: the additive value is a bounded-score heuristic reference,")
    print("        not a formal no-interaction (factorial) model.")
    print()


if __name__ == "__main__":
    main()
