import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Evolutionary game theory exercise: Horiuchi (2004)

    ## Models in Population Biology

    This notebook implements the exercise plan in `EVOL_GAME_THEORY.md`.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.integrate import solve_ivp

    sns.set_context("talk")
    sns.set_palette("muted")
    return mo, np, plt, sns, solve_ivp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise tasks

    1. Implement payoffs and replicator dynamics.
    2. Run one trajectory and interpret the result.
    3. Explore trajectories from many initial conditions in phase space.
    4. Sweep ecological pressure $D_S$ for low and high violence pressure $D_C$.
    5. Test whether initial conditions lead to different outcomes at fixed parameters.

    Model definitions:

    $$ z = 1 - x - y $$

    $$ W_{DH} = x(V + C)/2 + y(V + C) - C $$

    $$ W_{DD} = yV/2 $$

    $$ W_{AS} = x(V/2 - D_C) + yV/2 + V/2 - D_S $$

    $$ \bar{W} = x W_{DH} + y W_{DD} + z W_{AS} $$

    $$ \frac{dx}{dt} = x (W_{DH} - \bar{W}) $$

    $$ \frac{dy}{dt} = y (W_{DD} - \bar{W}) $$
    """)
    return


@app.cell
def _(mo):
    V_ui = mo.ui.slider(start=0.2, stop=2.0, step=0.1, value=1.0, label="V")
    C_ui = mo.ui.slider(start=0.3, stop=4.0, step=0.1, value=2.0, label="C")
    DS_ui = mo.ui.slider(start=0.0, stop=1.5, step=0.05, value=0.6, label="D_S")
    DC_ui = mo.ui.slider(start=0.0, stop=1.5, step=0.05, value=0.7, label="D_C")
    mo.vstack([
        mo.md("### Parameters"),
        mo.hstack([V_ui, C_ui]),
        mo.hstack([DS_ui, DC_ui]),
    ])
    return C_ui, DC_ui, DS_ui, V_ui


@app.cell
def _(C_ui, DC_ui, DS_ui, V_ui):
    V = float(V_ui.value)
    C = float(C_ui.value)
    D_S = float(DS_ui.value)
    D_C = float(DC_ui.value)
    return C, D_C, D_S, V


@app.cell
def _(np):
    def validate_state(x, y):
        if x < 0 or y < 0 or x + y > 1:
            raise ValueError("state must satisfy x>=0, y>=0, x+y<=1")

    def payoffs(x, y, V, C, D_S, D_C):
        z = 1.0 - x - y
        W_DH = x * (V + C) / 2.0 + y * (V + C) - C
        W_DD = y * V / 2.0
        W_AS = x * (V / 2.0 - D_C) + y * V / 2.0 + V / 2.0 - D_S
        return np.array([W_DH, W_DD, W_AS])

    return payoffs, validate_state


@app.cell
def _(payoffs):
    def replicator_rhs(t, xy, V, C, D_S, D_C):
        x, y = xy
        z = 1.0 - x - y

        # Small out-of-simplex drift can happen numerically near boundaries.
        if x < -1e-10 or y < -1e-10 or z < -1e-10:
            return [0.0, 0.0]

        x = max(0.0, x)
        y = max(0.0, y)
        z = max(0.0, z)
        s = x + y + z
        x, y, z = x / s, y / s, z / s

        W_DH, W_DD, W_AS = payoffs(x, y, V, C, D_S, D_C)
        W_bar = x * W_DH + y * W_DD + z * W_AS

        dx = x * (W_DH - W_bar)
        dy = y * (W_DD - W_bar)
        return [dx, dy]

    return (replicator_rhs,)


@app.cell
def _(np, replicator_rhs, solve_ivp):
    def simulate(x0, y0, V, C, D_S, D_C, tmax=250.0, n_steps=1200):
        t_eval = np.linspace(0.0, tmax, n_steps)
        sol = solve_ivp(
            replicator_rhs,
            (0.0, tmax),
            (x0, y0),
            t_eval=t_eval,
            args=(V, C, D_S, D_C),
            rtol=1e-7,
            atol=1e-9,
            max_step=1.0,
        )
        x = sol.y[0]
        y = sol.y[1]
        z = 1.0 - x - y
        return sol.t, x, y, z

    return (simulate,)


@app.cell
def _(mo):
    x0_ui = mo.ui.slider(start=0.01, stop=0.95, step=0.01, value=0.20, label="x0 (DH)")
    y0_ui = mo.ui.slider(start=0.01, stop=0.95, step=0.01, value=0.20, label="y0 (DD)")
    mo.vstack([
        mo.md("### Task 2: single trajectory"),
        mo.hstack([x0_ui, y0_ui]),
    ])
    return x0_ui, y0_ui


@app.cell
def _(C, D_C, D_S, V, mo, plt, simulate, validate_state, x0_ui, y0_ui):
    x0 = float(x0_ui.value)
    y0 = float(y0_ui.value)

    if x0 + y0 >= 1:
        mo.md("Choose x0 and y0 such that x0 + y0 < 1.")
        return

    validate_state(x0, y0)
    t, x, y, z = simulate(x0, y0, V, C, D_S, D_C)

    plt.plot(t, x, label="DH (x)")
    plt.plot(t, y, label="DD (y)")
    plt.plot(t, z, label="AS (z)")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.ylim(0, 1)
    plt.legend()
    plt.gcf()
    return t, x, y, z


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 3: phase plane from many initial conditions

    Each line is one simulation in $(x,y)$ space. The simplex boundary is shown by $x \ge 0$, $y \ge 0$, and $x+y \le 1$.
    """)
    return


@app.cell
def _(C, D_C, D_S, V, np, plt, simulate):
    grid = np.linspace(0.02, 0.9, 10)
    ics = [(x0, y0) for x0 in grid for y0 in grid if x0 + y0 < 0.98]

    for x0, y0 in ics:
        _, x, y, _ = simulate(x0, y0, V, C, D_S, D_C, tmax=150, n_steps=400)
        plt.plot(x, y, color="0.2", alpha=0.15, linewidth=0.8)
        plt.scatter([x[-1]], [y[-1]], color="tab:red", s=8, alpha=0.25)

    xx = np.linspace(0, 1, 200)
    plt.plot(xx, 1 - xx, "k--", linewidth=1)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel("x = DH")
    plt.ylabel("y = DD")
    plt.title("Phase-plane trajectories")
    plt.gcf()
    return (ics,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 4: sweep ecological pressure $D_S$

    We compare two cases:

    1. low violence pressure, $D_C < V/2$
    2. high violence pressure, $D_C > V/2$
    """)
    return


@app.cell
def _(C, V, np, simulate):
    DS_values = np.linspace(0.05, 1.2, 30)
    x0, y0 = 0.2, 0.2

    def final_state_for_sweep(D_C_value):
        finals = []
        for D_S_value in DS_values:
            _, x, y, z = simulate(x0, y0, V, C, D_S_value, D_C_value, tmax=250, n_steps=900)
            finals.append((x[-1], y[-1], z[-1]))
        return np.array(finals)

    D_C_low = min(0.3, max(0.0, V / 2 - 0.1))
    D_C_high = V / 2 + 0.2

    finals_low = final_state_for_sweep(D_C_low)
    finals_high = final_state_for_sweep(D_C_high)

    return D_C_high, D_C_low, DS_values, finals_high, finals_low


@app.cell
def _(D_C_high, D_C_low, DS_values, finals_high, finals_low, plt):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)

    axes[0].plot(DS_values, finals_low[:, 0], label="x* (DH)")
    axes[0].plot(DS_values, finals_low[:, 1], label="y* (DD)")
    axes[0].plot(DS_values, finals_low[:, 2], label="z* (AS)")
    axes[0].set_title(f"Low D_C = {D_C_low:.2f}")
    axes[0].set_xlabel("D_S")
    axes[0].set_ylabel("Final frequency")
    axes[0].set_ylim(0, 1)
    axes[0].legend()

    axes[1].plot(DS_values, finals_high[:, 0], label="x* (DH)")
    axes[1].plot(DS_values, finals_high[:, 1], label="y* (DD)")
    axes[1].plot(DS_values, finals_high[:, 2], label="z* (AS)")
    axes[1].set_title(f"High D_C = {D_C_high:.2f}")
    axes[1].set_xlabel("D_S")
    axes[1].set_ylim(0, 1)

    fig.tight_layout()
    fig
    return fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 5: path dependence test

    Run two different initial conditions at the same parameters and compare final states.
    """)
    return


@app.cell
def _(mo):
    DS_path_ui = mo.ui.slider(start=0.1, stop=1.2, step=0.05, value=0.5, label="D_S for path test")
    DC_path_ui = mo.ui.slider(start=0.1, stop=1.2, step=0.05, value=0.7, label="D_C for path test")
    mo.hstack([DS_path_ui, DC_path_ui])
    return DC_path_ui, DS_path_ui


@app.cell
def _(C, DC_path_ui, DS_path_ui, V, mo, np, plt, simulate):
    D_S_path = float(DS_path_ui.value)
    D_C_path = float(DC_path_ui.value)

    ic_a = (0.05, 0.05)
    ic_b = (0.55, 0.35)

    ta, xa, ya, za = simulate(*ic_a, V, C, D_S_path, D_C_path, tmax=300, n_steps=900)
    tb, xb, yb, zb = simulate(*ic_b, V, C, D_S_path, D_C_path, tmax=300, n_steps=900)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(xa, ya, label=f"IC A={ic_a}")
    axes[0].plot(xb, yb, label=f"IC B={ic_b}")
    xx = np.linspace(0, 1, 200)
    axes[0].plot(xx, 1 - xx, "k--", linewidth=1)
    axes[0].set_xlabel("x = DH")
    axes[0].set_ylabel("y = DD")
    axes[0].set_xlim(0, 1)
    axes[0].set_ylim(0, 1)
    axes[0].legend()

    axes[1].plot(ta, za, label="AS from IC A")
    axes[1].plot(tb, zb, label="AS from IC B")
    axes[1].set_xlabel("Time")
    axes[1].set_ylabel("AS frequency (z)")
    axes[1].set_ylim(0, 1)
    axes[1].legend()

    fig.tight_layout()

    final_a = (xa[-1], ya[-1], za[-1])
    final_b = (xb[-1], yb[-1], zb[-1])

    mo.vstack([
        fig,
        mo.md(
            "Final state A (DH, DD, AS): "
            f"`({final_a[0]:.3f}, {final_a[1]:.3f}, {final_a[2]:.3f})`\\n"
            "Final state B (DH, DD, AS): "
            f"`({final_b[0]:.3f}, {final_b[1]:.3f}, {final_b[2]:.3f})`"
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reflection prompts

    1. As $D_S$ increases, which strategy family tends to gain and why?
    2. How does increasing $D_C$ affect robustness of outcomes?
    3. Which assumptions are most restrictive in this model?
    """)
    return


if __name__ == "__main__":
    app.run()
