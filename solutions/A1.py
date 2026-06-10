import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.integrate import solve_ivp
    from functools import partial
    import seaborn as sns
    return mo, np, partial, plt, sns, solve_ivp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Assignment 1: Continuous-time deterministic models
    ## [Models in Population Biology](https://modelspopbiol.yoavram.com/)
    ## Yoav Ram
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # General instructions

    1. When instructed to implement a function, use the given function names and parameters lists; failure to do so may cause test functions to fail during grading.
    1. When instructed to generate a plot, make sure that the plot is clear, that axes are propely labeled, and that the notebook is saved with the plot inline, so that the grader can see the plot without running the code. Make sure that you re-generate the plot if you changed the code!
    1. Cells that begin with `###` and lines that end with `###` should not be removed or modified, they are used for automatic grading.
    1. Note that the last cell in the notebook says __end of assignment__; if you are missing anything please download the origianl file from the course website.
    1. This exercise doesn't put much emphasis on efficieny or runtime. But, your code should still run within a reasonable time (a few minutes) and you should use idioms learned in class, e.g. array opreations, wherever possible.
    1. Questions regarding the exercises should be posted to the course forum. You can also visit the Office Hours, but please do not email the course staff with questions about the exercise.
    1. Intructions for submitting the exercise are on the course website.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Ex 1: Cross-feeding model

    In the following, we will work with a model introduced in the paper:
    > Ribeck, Noah, and Richard E. Lenski. 2015. "Modeling and Quantifying Frequency-Dependent Fitness in Microbial Populations with Cross-Feeding Interactions." Evolution 69 (5): 1313–20. https://doi.org/10.1111/evo.12645.

    The model uses Monod dynamics to describe the growth of two strains with concentrations $n_1$ and $n_2$, respectively.
    The first strain (or ecotype) is a glucose specialist.
    It feeds on glucose and produces acetate as a byproduct.
    The second strain is an acetate cross feeder.
    The concentration of glucose and acetate are denoted by $g$ and $a$, respectively.

    The model equations are
    $$
    \frac{d}{d t} g(t)=-\sum_{i=1}^{2} \frac{1}{y_{1, i}} \frac{r_{1, i} g(t)}{k_{1, i}+g(t)} n_{i}(t) $$$$
    \frac{d}{d t} a(t)=\sum_{i=1}^{2}\left[h_{i} \frac{r_{1, i} g(t)}{k_{1, i}+g(t)}-\frac{1}{y_{2, i}} \frac{r_{2, i} a(t)}{k_{2, i}+a(t)}\right] n_{i}(t) $$$$
    \frac{d}{d t} n_{1}(t)=\left[\frac{r_{1, 1} g(t)}{k_{1, 1}+g(t)}+\frac{r_{2, 1} a(t)}{k_{2, 1}+a(t)}\right] n_{1}(t) $$$$
    \frac{d}{d t} n_{2}(t)=\left[\frac{r_{1, 2} g(t)}{k_{1, 2}+g(t)}+\frac{r_{2, 2} a(t)}{k_{2, 2}+a(t)}\right] n_{2}(t)
    $$

    where
    - $r_{1,i}$ and $r_{2,i}$ are the maximum growth rates of type $i$ on, say, glucose and acetate, respectively
    - $k_{1,i}$ and $k_{2,i}$ are the resource concentrations that permit growth at half-maximum rate
    - $y_{1,i}$ and $y_{2,i}$ are the population yields from each unit of glucose and acetate
    - $h_i$ is the number of units of acetate produced for each unit increment of $n_i$.

    **Implement these equations in the `ode` function**
    """)
    return


@app.cell
def _(np):
    # Parameters from Ribeck & Lenski (2015), Figure 3 legend
    # r_{1,i}: maximum growth rates on glucose (per hour)
    r11 = 1.0    # strain 1 (glucose specialist) on glucose
    r12 = 0.8    # strain 2 (cross-feeder) on glucose
    # r_{2,i}: maximum growth rates on acetate (per hour)
    r21 = 0.3    # strain 1 on acetate
    r22 = 0.9    # strain 2 on acetate
    # k_{1,i}: half-saturation constants for glucose (mg/mL)
    k11 = 0.1
    k12 = 0.1
    # k_{2,i}: half-saturation constants for acetate (mg/mL)
    k21 = 0.1
    k22 = 0.1
    # y_{1,i}: cell yields per unit glucose consumed (cells/mg)
    y11 = 5e8
    y12 = 5e8
    # y_{2,i}: cell yields per unit acetate consumed (cells/mg)
    y21 = 1e9
    y22 = 1e9
    # h_i: acetate produced per unit of Monod glucose growth rate
    h1 = 0.1     # strain 1 produces acetate as a byproduct
    h2 = 0.0     # strain 2 does not produce acetate

    # Initial conditions for Figure 3A
    g0 = 0.25     # initial glucose concentration (mg/mL)
    a0 = 0.0      # no initial acetate
    N0 = 5e6      # total initial cell density
    n1_0 = N0 * 0.5
    n2_0 = N0 * 0.5
    init = [n1_0, n2_0, g0, a0]

    # Time span for one growth cycle (hours)
    t = np.linspace(0, 8, 500)

    def ode_crossfeed(t, x): ###
        n1, n2, g, a = x

        # Monod growth rates on glucose for each strain
        mu1_g = r11 * g / (k11 + g)
        mu2_g = r12 * g / (k12 + g)
        # Monod growth rates on acetate for each strain
        mu1_a = r21 * a / (k21 + a)
        mu2_a = r22 * a / (k22 + a)

        dn1dt = (
            (mu1_g + mu1_a) * n1
        )
        dn2dt = (
            (mu2_g + mu2_a) * n2
        )
        dgdt = (
            -(1/y11) * mu1_g * n1 - (1/y12) * mu2_g * n2
        )
        dadt = (
            (h1 * mu1_g - (1/y21) * mu1_a) * n1
            + (h2 * mu2_g - (1/y22) * mu2_a) * n2
        )

        return [dn1dt, dn2dt, dgdt, dadt] ###

    return (init, ode_crossfeed, t)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Reproduce Figure 3A**.

    - Note that all parameter values are given in the figure legend, expect for the initial concentrations of the two strains, which you will need to guess.
    - I think the figure has a mistake and that they confused the blue and red curve - what do you think?
    """)
    return


@app.cell
def _(ode_crossfeed, solve_ivp, np, init, t):
    sol = solve_ivp(ode_crossfeed, (t.min(), t.max()), init, t_eval=t) #
    return (sol,)


@app.cell
def _(sns, plt, sol):
    red, blue, green, purple, orange  = sns.color_palette('Set1', 5) ###
    fig, ax = plt.subplots() ###

    # Compute frequency of strain 2 (cross-feeder) over time
    n1_arr = sol.y[0]
    n2_arr = sol.y[1]
    p_t = n2_arr / (n1_arr + n2_arr)

    ax.plot(sol.t, p_t, color=blue, label='Strain 2 (cross-feeder)')
    ax.plot(sol.t, 1 - p_t, color=red, label='Strain 1 (glucose specialist)')
    ax.set_xlabel('Time (hours)')
    ax.set_ylabel('Frequency')
    ax.set_title('Figure 3A: Single growth cycle dynamics')
    ax.legend()
    ax.set_ylim(0, 1)
    plt.tight_layout()
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the actual experiment described in the paper, after each growth cycle (of 4 or more hours, it doesn't matter as growth arrests after 4 hours), the population was diluted 100-fold, and new media was introduced.

    **Implement the function `growth_cycles` that runs such an experiment for `ncycles` cycles.**
    - The function should return the frequency `p` of strain 2 (the cross-feeding strain) at each cycle, such that $p(t)=\frac{n_2(t)}{n_1(t) + n_2(t)}$.
    - The initial concentration of the strains at each cycle should be a `F`-fold dilution of the concentration at the end of the previous cycle.
    - You should decide the concentration of the two strains at the first cycle according to your choice in the previous exercise, but set strain 2 frequency to be `p0`.
    """)
    return


@app.cell
def _(ode_crossfeed, solve_ivp, init, t):
    _N0 = init[0] + init[1]  # total initial cell density from ODE cell
    _g0 = init[2]             # initial glucose concentration from ODE cell
    _a0 = init[3]             # initial acetate concentration from ODE cell
    _t_end = t.max()          # cycle duration from ODE cell

    def growth_cycles(p0, ncycles, F): ###
        n1_init = _N0 * (1 - p0)
        n2_init = _N0 * p0

        p = []  # frequency of strain 2 at end of each cycle

        for cycle in range(ncycles):
            x0 = [n1_init, n2_init, _g0, _a0]
            sol = solve_ivp(ode_crossfeed, [0, _t_end], x0)
            n1_end = sol.y[0, -1]
            n2_end = sol.y[1, -1]
            freq = n2_end / (n1_end + n2_end)
            p.append(freq)
            n1_init = n1_end / F
            n2_init = n2_end / F

        return p ###

    return (growth_cycles,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Reproduce Figure 3B**.""")
    return


@app.cell
def _(growth_cycles, plt):
    # Figure 3B: frequency of cross-feeder over many growth cycles from various p0
    ncycles = 100
    F = 100  # 100-fold daily dilution

    fig3b, ax3b = plt.subplots()

    for p0_val in [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]:
        p_cycles = growth_cycles(p0_val, ncycles, F)
        ax3b.plot(range(1, ncycles + 1), p_cycles, label=f'$p_0={p0_val}$')

    ax3b.set_xlabel('Growth cycle')
    ax3b.set_ylabel('Frequency of cross-feeder (strain 2)')
    ax3b.set_title('Figure 3B: Frequency-dependent selection over growth cycles')
    ax3b.set_ylim(0, 1)
    ax3b.legend(fontsize=8, loc='upper right')
    plt.tight_layout()
    fig3b
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Ex 2: Metastasis of Malignant Tumors

    This exercise follows an example from chapter 7 of Otto and Day (2007).

    We will construct a model for the dynamics of the number of cancer cells lodged in the capillaries of an organ, $C$, and the number of cancer cells that have actually invaded that organ, $I$.

    Suppose that cells are lost from the capillaries by dislodgement or death at a per capita rate $\delta_1$ and that they invade the organ from the capillaries at a per capita rate $\beta$. Once cells are in the organ they die at a per capita rate $\delta_2$, and the cancer cells replicate at a per capita rate $\rho$.

    This gives the following euqations:
    $$
    \frac{dC}{dt} = -\delta_1 C - \beta C $$$$
    \frac{dI}{dt} = \beta C - \delta_2 I + \rho I
    $$

    **Implement the ODE and plot its solution for two sets of parameter values.**

    Use the parameter sets provided below and reproduce the figure.
    """)
    return


@app.cell
def _(np):
    def ode(t, x, δ1, δ2, β, ρ): ###
        C, I = x
        dCdt = -δ1 * C - β * C
        dIdt = β * C - δ2 * I + ρ * I
        return np.array([dCdt, dIdt])

    return (ode,)


@app.cell
def _(np, ode, partial, solve_ivp, plt):
    _δ1, _δ2, _β, _ρ = 0.5, 0.5, 0.8, 0.4 ###
    ode1 = partial(ode, δ1=_δ1, δ2=_δ2, β=_β, ρ=_ρ) ###
    _δ1, _δ2, _β, _ρ = 0.5, 0.5, 0.8, 0.6 ###
    ode2 = partial(ode, δ1=_δ1, δ2=_δ2, β=_β, ρ=_ρ) ###

    # Solve for both parameter sets starting from initial condition: C=100, I=0
    t_span = [0, 10]
    x0_meta = [100, 0]

    sol_meta1 = solve_ivp(ode1, t_span, x0_meta, dense_output=True)
    sol_meta2 = solve_ivp(ode2, t_span, x0_meta, dense_output=True)

    t_meta_plot = np.linspace(0, 10, 300)
    y_meta1 = sol_meta1.sol(t_meta_plot)
    y_meta2 = sol_meta2.sol(t_meta_plot)

    fig_meta, axes_meta = plt.subplots(1, 2, figsize=(12, 4))

    axes_meta[0].plot(t_meta_plot, y_meta1[0], label='$C$ (capillaries)')
    axes_meta[0].plot(t_meta_plot, y_meta1[1], label='$I$ (invaded)')
    axes_meta[0].set_xlabel('Time')
    axes_meta[0].set_ylabel('Cell count')
    axes_meta[0].set_title(r'$\delta_1=0.5,\,\delta_2=0.5,\,\beta=0.8,\,\rho=0.4$')
    axes_meta[0].legend()

    axes_meta[1].plot(t_meta_plot, y_meta2[0], label='$C$ (capillaries)')
    axes_meta[1].plot(t_meta_plot, y_meta2[1], label='$I$ (invaded)')
    axes_meta[1].set_xlabel('Time')
    axes_meta[1].set_ylabel('Cell count')
    axes_meta[1].set_title(r'$\delta_1=0.5,\,\delta_2=0.5,\,\beta=0.8,\,\rho=0.6$')
    axes_meta[1].legend()

    plt.tight_layout()
    fig_meta
    return ode1, ode2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We want to know if a new tumor will be able to take hold and grow or will it disappear?""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Find the only equilibrium** of this system. To do so, you can find the values of $C$ and $I$ that give $\frac{dC}{dt}=\frac{dI}{dt}=0$ (note that all parameters are positive).

    **Test your equilibrium**: choose 1000 random choices of positive model parameters ($\delta_1$, $\delta_2$, $\beta$, and $\rho$) and check that indeed $\frac{dC}{dt}=\frac{dI}{dt}=0$ at the equiblrlium.
    """)
    return


@app.cell
def _(np, ode):
    _δ1, _δ2, _β, _ρ = np.random.uniform(0, 1, size=(4, 1000)) ###
    # Equilibrium: setting dC/dt = -(δ1+β)*C = 0 and dI/dt = β*C + (ρ-δ2)*I = 0
    # Since all parameters are positive, the only solution is C=0 and I=0.
    x_star = np.zeros(2)  # write code here
    np.allclose(ode(0, x_star, _δ1, _δ2, _β, _ρ).T, x_star) ###
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The single equilibrium doesn't provide the whole answer, because clearly for one of the above parameter sets the equilibrium is not reached -- it is unstable.

    **Find and describe the conditions for *local stability* of the equilibrium.**
    Briefly, this requires that the real parts eigenvalues of the Jacobian evaluated at the equilibrium are negative, see a detalied explanation [here](../notebooks/stability.ipynb).

    To solve this exercise, use *SymPy* to find the leading eigenvalue (largest eigenvalue) and print its value.
    The sign of this eigenvalue will determine the stability of the system.

    SymPy notes:
    - `sympy.symbols('x y z')` will create the symbols `x`, `y`, and `z`.
    - `sympy.diff(y, x)` will return the derivative of `y` with respect to `x`.
    - `sympy.Matrix` will take a list of symbolic expression and create a matrix from that list.
    - `A.subs([(x, val1), (y, val2)]` will substitute `val1` and `val2` (numbers) into the symbols `x` and `y` in the expression `A`.
    - `M.eigenvals()` will return the eigenvalues of matrix `M` as a dictionary: the keys are the eigenvalue experssions, the values are the eigenvalue multiplicities (which we can ignore here).
    """)
    return


@app.cell
def _():
    ###
    import sympy
    sympy.init_printing()
    return (sympy,)


@app.cell
def _(sympy):
    # Define sympy symbols for δ1, δ2, β, ρ
    δ1_s, δ2, β_s, ρ = sympy.symbols('delta_1 delta_2 beta rho', positive=True)
    C_s, I_s = sympy.symbols('C I')

    # ODE right-hand sides:
    # dC/dt = -(δ1 + β)*C
    # dI/dt = β*C + (ρ - δ2)*I
    dCdt_sym = -(δ1_s + β_s) * C_s
    dIdt_sym = β_s * C_s + (ρ - δ2) * I_s

    # Jacobian matrix (partial derivatives w.r.t. C and I)
    J = sympy.Matrix([
        [sympy.diff(dCdt_sym, C_s), sympy.diff(dCdt_sym, I_s)],
        [sympy.diff(dIdt_sym, C_s), sympy.diff(dIdt_sym, I_s)],
    ])

    # The Jacobian is constant (linear system), so it's already evaluated at the equilibrium
    J_eq = J.subs([(C_s, 0), (I_s, 0)])

    # Eigenvalues: for a lower-triangular matrix these are the diagonal entries
    # eigenval 1: -(δ1 + β)  [always negative since δ1, β > 0]
    # eigenval 2: ρ - δ2     [sign determines stability]
    eigenvals_dict = J_eq.eigenvals()
    print("Jacobian at equilibrium (C=0, I=0):")
    sympy.pprint(J_eq)
    print("\nEigenvalues:", eigenvals_dict)

    # Leading eigenvalue (largest real part) is ρ - δ2
    λ = ρ - δ2
    print("\nLeading eigenvalue λ =", λ)
    print("Stability condition: λ < 0  ⟺  ρ < δ2")
    return δ2, λ, ρ


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following shows a visualization of the conditions for stability, where stability (and hence the demise of the tumor) occurs in the red region, wheras instability (and hence the growth of the tumor) occurs in the blue region.

    Here, `λ` is a SymPy expression for the leading eigenvalue.

    *You do not need to plot this figure*.
    """)
    return


@app.cell
def _(np, δ2, λ, ρ):
    δ2_ = np.linspace(0, 1, 100)
    ρ_ = np.linspace(0, 1, 100)
    stability = np.array([[λ.subs([(δ2, δ2_[i]), (ρ, ρ_[j])]) for i in range(100)] for j in range(100)]).astype(float)
    return δ2_, ρ_, stability


@app.cell
def _(plt, δ2_, ρ_, stability):
    plt.pcolormesh(δ2_, ρ_, stability, cmap='RdBu')
    plt.plot(δ2_, ρ_, color='k')
    plt.colorbar(label=r'$\lambda$')
    plt.xlabel(r'$\delta_2$')
    plt.ylabel(r'$\rho$')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""__end of assignment__""")
    return


if __name__ == "__main__":
    app.run()
