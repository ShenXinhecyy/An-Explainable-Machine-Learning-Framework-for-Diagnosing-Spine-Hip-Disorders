#!/usr/bin/env python3
"""
Bifurcation analysis of the BOLD model (diabetes parameterisation).

Two complementary computations:
  1. Equilibrium continuation (Newton root-finding via fsolve) of the three
     steady-state branches across k_ROS in [0, 0.8], exported as a CSV for the
     bifurcation figure.
  2. A bisection refinement of the saddle-node fold of the inflammatory branch,
     k_ROS* ~ 0.333 (same algorithm as hysteresis_analysis.fold_forward, kept
     here as a local function to avoid a circular import).
  3. Finite-time grid scan (simulation to t = 200 from the inflamed initial
     state [0.7, 0.15, 0.20]); numerically less precise but more intuitive
     estimator, transition at k_ROS = 0.338.

FIX (P1): the original reported the fold as
    fold = df.loc[df['RS_inflammatory'].notna(), 'k_ROS'].max() + 0.0025
i.e. a grid maximum plus half a step, while the docstring/README claimed
"Newton + bisection". The fold is now actually refined by bisection.

Outputs: Figure4_bifurcation_data.csv (k_ROS, RS_inflammatory, RS_unstable,
RS_regenerative).
"""

import numpy as np
import pandas as pd
from scipy.optimize import fsolve
from ode_model import DEFAULT_PARAMS_DM, ode_system, simulate, get_final_state, regscore


def steady(control, guess, params=DEFAULT_PARAMS_DM):
    """Newton solve for a steady state near `guess`; returns None if not physical."""
    x, info, ier, msg = fsolve(lambda s: ode_system(0, s, params, control),
                               guess, full_output=True)
    if ier == 1 and np.all(x > -1e-6) and np.all(x < 1 + 1e-6):
        return np.clip(x, 0, 1)
    return None


def fold_forward_bisection(params=DEFAULT_PARAMS_DM, lo=0.0, hi=0.9, n_iter=45):
    """Bisection refinement of the inflammatory-branch saddle-node fold.

    A point k is "inflammatory" if the Newton solve started from the inflamed
    guess still converges to an attractor with X > 0.4. The fold is the last
    k at which the inflammatory attractor still exists.
    """
    def inflamed(k):
        s = steady({'k_ROS': float(k)}, [0.79, 0.14, 0.06], params)
        return s is not None and s[0] > 0.4

    if not inflamed(lo):
        return np.nan
    for _ in range(n_iter):
        mid = (lo + hi) / 2
        if inflamed(mid):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def equilibrium_bifurcation(path='Figure4_bifurcation_data.csv'):
    ks = np.round(np.arange(0, 0.801, 0.005), 3)
    rows = []
    for k in ks:
        c = {'k_ROS': float(k)}
        s_inf = steady(c, [0.79, 0.14, 0.06])   # inflammatory branch
        s_reg = steady(c, [0.05, 0.80, 0.95])   # regenerative branch
        s_mid = steady(c, [0.35, 0.35, 0.35])   # unstable (saddle) branch
        # keep only genuine branch members (Newton can jump basins)
        if s_inf is not None and not s_inf[0] > 0.4:
            s_inf = None
        if s_reg is not None and not (s_reg[2] > 0.8 and s_reg[0] < 0.2):
            s_reg = None
        rs_inf = regscore(*s_inf) if s_inf is not None else np.nan
        rs_reg = regscore(*s_reg) if s_reg is not None else np.nan
        rs_mid = regscore(*s_mid) if s_mid is not None else np.nan
        if s_mid is not None:
            if s_inf is not None and np.allclose(s_mid, s_inf, atol=1e-4):
                rs_mid = np.nan
            if s_reg is not None and np.allclose(s_mid, s_reg, atol=1e-4):
                rs_mid = np.nan
        rows.append((k, rs_inf, rs_mid, rs_reg))
    df = pd.DataFrame(rows, columns=['k_ROS', 'RS_inflammatory',
                                     'RS_unstable', 'RS_regenerative'])
    df.to_csv(path, index=False)

    grid_fold = df.loc[df['RS_inflammatory'].notna(), 'k_ROS'].max() + 0.0025
    bisect_fold = fold_forward_bisection()
    print(f"Grid estimate (max + half-step): k_ROS* = {grid_fold:.4f}")
    print(f"Bisection refinement:           k_ROS* = {bisect_fold:.4f}")
    print(f"Agreement within: {abs(bisect_fold - grid_fold):.4f}")
    return df


def grid_scan(init=(0.7, 0.15, 0.20), t_span=(0, 200)):
    """Finite-time grid scan (the 't = 200 grid' estimator)."""
    for k in np.arange(0, 0.801, 0.001):
        sol = simulate(DEFAULT_PARAMS_DM, {'k_ROS': float(k)}, list(init),
                       t_span=t_span)
        X, Y, Z = get_final_state(sol)
        rs = regscore(X, Y, Z)
        if rs > 0.5:
            print(f"Finite-time grid transition: k_ROS = {k:.3f}")
            return k
    return None


if __name__ == '__main__':
    equilibrium_bifurcation()
    grid_scan()
