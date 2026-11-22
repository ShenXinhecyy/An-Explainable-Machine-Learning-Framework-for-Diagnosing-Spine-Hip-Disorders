#!/usr/bin/env python3
"""
Cross-pathology comparison: simulate Healthy, Diabetes, Osteoporosis,
and Osteomyelitis conditions, with and without therapeutic intervention.

FIX (P2): documented the provenance of the pathology-specific offsets.
These are illustrative, literature-informed choices, NOT fitted parameters.
The manuscript states this explicitly ("Parameters were transferred from the
diabetic parameterisation without direct calibration data"), so the code now
carries the same caveat.
"""

import numpy as np
from ode_model import DEFAULT_PARAMS_DM, simulate, get_final_state, regscore


def main():
    # ------------------------------------------------------------------
    # Pathology-specific parameter sets.
    #
    # Only three parameters are varied from the diabetic baseline:
    #   alpha_X         : inflammatory self-amplification drive
    #   alpha_Z         : basal metabolic repair
    #   gamma_ZX_damage : inflammation -> metabolic damage coupling
    #
    # Magnitudes are illustrative order-of-magnitude choices meant to span
    # the inflammatory-lock axis (healthy < diabetes < osteoporosis <
    # osteomyelitis). They are NOT derived from per-study fitting; the
    # manuscript acknowledges the absence of direct calibration data for the
    # non-diabetic pathologies.
    # ------------------------------------------------------------------
    params_healthy = DEFAULT_PARAMS_DM.copy()
    params_healthy['alpha_X'] = 0.25   # low inflammation drive

    params_dm = DEFAULT_PARAMS_DM.copy()   # diabetes: high alpha_X (0.80)

    params_op = DEFAULT_PARAMS_DM.copy()
    params_op['alpha_X'] = 0.55        # moderate-severe inflammation
    params_op['alpha_Z'] = 0.03        # impaired metabolic repair

    params_om = DEFAULT_PARAMS_DM.copy()
    params_om['alpha_X'] = 0.90        # extreme inflammation
    params_om['gamma_ZX_damage'] = 0.40  # severe damage coupling

    pathologies = [
        ('Healthy', params_healthy, [0.2, 0.6, 0.7]),
        ('Diabetes', params_dm, [0.7, 0.15, 0.20]),
        ('Osteoporosis', params_op, [0.7, 0.15, 0.20]),
        ('Osteomyelitis', params_om, [0.7, 0.15, 0.20]),
    ]

    # Therapeutic intervention (Triple Push-Pull)
    therapy = {'k_ROS': 0.5, 'alpha_AMPK': 0.35, 'E_matrix': 0.2}
    no_therapy = {'k_ROS': 0.0, 'alpha_AMPK': 0.0, 'E_matrix': 0.0}

    print("=" * 100)
    print("Cross-Pathology Comparison")
    print("=" * 100)
    print(f"{'Pathology':15s} {'Before (X,Y,Z,RS)':>40s} {'After (X,Y,Z,RS)':>40s} {'dRS':>8s}")
    print("-" * 105)

    for pname, pparams, init in pathologies:
        sol_before = simulate(pparams, no_therapy, init)
        sol_after = simulate(pparams, therapy, init)

        Xb, Yb, Zb = get_final_state(sol_before)
        Xa, Ya, Za = get_final_state(sol_after)
        rs_b = regscore(Xb, Yb, Zb)
        rs_a = regscore(Xa, Ya, Za)

        print(f"{pname:15s}  X={Xb:.3f} Y={Yb:.3f} Z={Zb:.3f} RS={rs_b:.3f}   "
              f"X={Xa:.3f} Y={Ya:.3f} Z={Za:.3f} RS={rs_a:.3f}   {rs_a - rs_b:+7.3f}")

    print()


if __name__ == "__main__":
    main()
