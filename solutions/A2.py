import marimo

__generated_with = "0.23.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    from numba import jit

    return jit, mo, np, plt, sns


@app.cell
def _(sns):
    red, blue, green = sns.color_palette('Set1', 3) ###
    return blue, red


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Assignment 2: Discrete-time deterministic models
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
    # Ex 1: SIS model

    In this exercise we'll model the spread of an infectious disease that spreads through contact with an infected individual.
    Infected individuals remain infected for some time and then become susceptible again (rather than recovering).

    Here, $S$ stands for *susceptible* and $I$ stands for *infected*. The total population size is $N=S+I$.

    Susceptible individuals meet $c$ individuals every day, of which $I/N$ are infected. When meeting an infected individuals, they become infected with probability $b$.
    Thus, on average $\beta S I/N$ susceptible individuals become infected every day, where $\beta=b \cdot c$ is the transmission rate.
    On average, $\gamma I$ infected individuals recover every day, hence $\gamma$ is the recovery rate.

    Therefore, we can write the model as

    $$
    S_{t+1} = S_t - \beta S_t \frac{I_t}{N} + \gamma I_t
    $$
    $$
    I_{t+1} = I_t + \beta S_t \frac{I_t}{N} - \gamma I_t
    $$

    Say that you start with a population of 1000 people, of which only 10 are infected (the rest are susceptible).
    That means your "initial state" is $S=990, I=10$, i.e. 990 are susceptible and 10 are infected.
    """)
    return


@app.cell
def _():
    ###
    SI0 = 990, 10

    β = 1.1
    γ = 0.5
    return SI0, β, γ


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Implement a function called `step_SIS(SI, β, γ)`** that given the current state `SI=(S, I)` and the parameters $\gamma$ and $\beta$, generates the next state.

    Note: you should make sure that $S$ and $I$ don't go below 0 or above $N$.
    """)
    return


@app.cell
def _(SI0, np, β, γ):
    def step_SIS(SI, β, γ): ###
        S, I = SI
        N = S + I
        S2I = β * S * I / N
        I2S = γ * I
        S = S - S2I + I2S
        I = I + S2I - I2S
        S = np.minimum(np.maximum(0, S), N)
        I = np.minimum(np.maximum(0, I), N)
        return S, I

    step_SIS(SI0, β, γ) ###
    return (step_SIS,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Implement a function called `simulation_SIS(SI0, β, γ, days)`** that given an initial state `SI0=(S0, I0)`, parameters $\gamma$ and $\beta$, and the number of days $days$ to run the simulation, simulates the dynamics and returns a vector `SI` in which the value at index `t, j` gives state `j` at day `t` (`j` being 0 for $S$ and 1 for $I$).

    Note that you should call `step_SIS` from `simulation_SIS`.

    Think: What is the type of the returned value? How many dimensions does it have?
    """)
    return


@app.cell
def _(SI0, np, step_SIS, β, γ):
    def simulation_SIS(SI0, β, γ, days): ###
        SI = np.empty((days, len(SI0)))
        SI[0] = SI0
        for t in range(1, days):
            SI[t] = step_SIS(SI[t - 1], β, γ)
        return SI

    print(simulation_SIS(SI0, β, γ, days=10)) ###
    return (simulation_SIS,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Run and plot** the dynamics for 90 days.
    """)
    return


@app.cell
def _(SI0, blue, plt, red, simulation_SIS, sns, β, γ):
    SI = simulation_SIS(SI0, β, γ, days=90)
    plt.plot(SI[:, 0], '.-', label='S', color=blue)
    plt.plot(SI[:, 1], '.-', label='I', color=red)
    plt.xlabel('Days')
    plt.ylabel('# of individuals')
    plt.legend()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For every $\beta, \gamma$ combination there is an expected equilibrium number of infected individuals $I^*$.

    **Plot $I^*$ as a function of $\beta$**.

    **Add a vertical line** for $\beta=\gamma$: epidemiological theory suggest that $R_0=\beta/\gamma$ is the reproductive number of an infectious disease. When $R_0<1$, the disease will die without infecting much of the population, whereas when $R_0>0$ the disease will become an epidemic, or even a pandemic, and will infect a significant fraction of the population.
    """)
    return


@app.cell
def _(SI0, simulation_SIS):
    def find_I_star(β, γ, days): ###
        SI = simulation_SIS(SI0, β, γ, days)
        return SI[-1, 1]

    return (find_I_star,)


@app.cell
def _(find_I_star, np, plt, γ):
    βs = np.linspace(0, 1, 100)
    I_star = [find_I_star(_β, γ, days=90) for _β in βs]

    plt.plot(βs, I_star, '-')
    plt.axvline(γ, color='k', ls='--')
    plt.xlabel(r'$\beta$')
    plt.ylabel(r'$I^*$')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## SEIS model

    An possible extension is the SEIS model, in which suscptibles (S) become "exposed" (E) during contact with infected (I), exposed then become infected after an incubation time of $\Delta$ days, and then infected recover to become susceptible again.

    When $\Delta=0$, we get the SIS model again.

    **Implement this model and plot the dynamics for a range of $\Delta$ values.**

    **UPDATE**: note that previously the plot I had here was incorrect.
    """)
    return


@app.cell
def _(np, simulation_SIS):
    def step_SEIS(SEI, β, γ, Δ): ###
        S, E, I = SEI
        N = S + E + I
        S2E = β * S * I / N
        E2I = E / Δ
        I2S = γ * I
        S = S - S2E + I2S
        E = E + S2E - E2I
        I = I + E2I - I2S
        S = np.minimum(np.maximum(0, S), N)
        E = np.minimum(np.maximum(0, E), N)
        I = np.minimum(np.maximum(0, I), N)
        return S, E, I

    def simulation_SEIS(SEI0, β, γ, Δ, days): ###
        SEI = np.zeros((days, len(SEI0)))
        if Δ == 0:
            SI = simulation_SIS((SEI0[0], SEI0[1] + SEI0[2]), β, γ, days)
            SEI[:, 0] = SI[:, 0]
            SEI[:, 2] = SI[:, 1]
        else:
            SEI[0] = SEI0
            for t in range(1, days):
                SEI[t] = step_SEIS(SEI[t - 1], β, γ, Δ)
        return SEI

    return (simulation_SEIS,)


@app.cell
def _(plt, simulation_SEIS, sns, β, γ):
    SEI0 = 990, 10, 0

    for Δ in [0, 1, 2, 3, 4, 5, 10, 20]:
        SEI = simulation_SEIS(SEI0, β, γ, Δ, days=250)
        plt.plot(SEI[:, 2], '.-', label=Δ)
    plt.ylim(0, sum(SEI0))
    plt.legend(title='Δ', ncol=2)
    plt.xlabel('Days')
    plt.ylabel('# of individuals')
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Ex 2: Logistic model

    The discrete-time logistc model is given by:

    $$
    N_{t+1} = r N_t \left(1 - N_t\right)
    $$

    This model is notoriously strange for some values of $r$.

    A similar model is the Ricker model, which have a somewhat nicer behaviour:

    $$
    N_{t+1} = N_t e^{r \left(1 - N_t\right)}
    $$

    **Implement both models and plot their dynamics for a set of $r$ values**.
    """)
    return


@app.cell
def _(jit, np):
    @jit ###
    def logistic(N0, r, tmax): ###
        N = np.empty(tmax)
        N[0] = N0
        for t in range(1, tmax):
            N[t] = N[t - 1] * r * (1 - N[t - 1])
        return N

    return (logistic,)


@app.cell
def _(jit, np):
    @jit ###
    def ricker(N0, r, tmax): ###
        N = np.empty(tmax)
        N[0] = N0
        for t in range(1, tmax):
            N[t] = N[t - 1] * np.exp(r * (1 - N[t - 1]))
        return N

    return (ricker,)


@app.cell
def _(logistic, plt, ricker):
    rs = [0.1, 1, 2, 3, 4] ###
    N0 = 0.1
    fig, axes = plt.subplots(len(rs), 2, figsize=(8, 8), sharex=True, sharey=False)
    for i, r in enumerate(rs):
        N = logistic(N0, r, 100)
        axes[i, 0].plot(N, '-')
        N = ricker(N0, r, 100)
        axes[i, 1].plot(N, '-')
        axes[i, 0].set_title('Logistic, r={}'.format(r))
        axes[i, 1].set_title('Ricker, r={}'.format(r))
        axes[i, 0].set_ylabel('N')
    axes[-1, 0].set_xlabel('t')
    axes[-1, 1].set_xlabel('t')
    fig.tight_layout()
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A bifurcation plot shows how the equilbrlium values of a model change when one of its parameters change.

    The Bifurcation plot of the logistic model, which shows $N^*$ as a function of $r$, is very well known, so we will reproduce it here.
    For every value of $r$, it shows the values reached by the model after it ran for many steps.
    If the model reaches a stable equilibrium, there will be a single value; otherwise there could be several values if the model reaches a stable cycle, of very many if the model reaches an unstable cycle or becomes chaotic (!!!).

    **Plot a *bifurcation plot* for both models:**
    - choose a set of $r$ values
    - for each $r_i$ value, run the model for $n$ , to get $N_1, \ldots, N_n$
    - plot the last $m<n$ values as a function of $r_i$: $(r_i, N_{n-m}), \dots (r_i, N_{n})$.
    """)
    return


@app.cell
def _(np, plt):
    def bifurcation(model, npts=200): ###
        rs = np.arange(0.1, 4, 0.001)
        for r in rs:
            N = model(0.1, r, npts * 3)
            plt.plot([r] * npts, N[-npts:], '.k', markersize=0.2)
        plt.xlabel('$r$')
        plt.ylabel('$N^*$')

    return (bifurcation,)


@app.cell
def _(bifurcation, logistic, plt):
    bifurcation(logistic)
    plt.title('Logistic model')
    plt.gcf()
    return


@app.cell
def _(bifurcation, plt, ricker):
    bifurcation(ricker)
    plt.title('Ricker model')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bonus: Interactive exploration of the logistic map

    The static plots above show only 5 values of $r$. The really interesting behavior — period-doubling and the route to chaos — happens at very specific values, so to *see* the transition it's much more illuminating to drag a slider through the range and watch the dynamics update.

    **Build an interactive plot using marimo widgets:**

    1. In the first cell below, create an `mo.ui.slider` for $r$ over the range $[0.1, 4.0]$ with a small step (e.g. `0.01`). Assign it to `r_ui` and display it.
    1. In the second cell, use `r_ui.value` to call `logistic(0.1, r_ui.value, 100)` and plot $N_t$ vs $t$.

    Drag the slider through the range. Around what value of $r$ does the fixed point become unstable? Where does a 2-cycle appear? When does chaos set in?

    See the slider examples in `notebooks/predator-prey.py`.
    """)
    return


@app.cell
def _(mo):
    r_ui = mo.ui.slider(0.1, 4.0, 0.01, value=3.2, show_value=True, label="r")
    r_ui
    return (r_ui,)


@app.cell
def _(logistic, plt, r_ui):
    N_traj = logistic(0.1, r_ui.value, 100)
    fig_slider, ax_slider = plt.subplots()
    ax_slider.plot(N_traj, '.-')
    ax_slider.set_xlabel('t')
    ax_slider.set_ylabel('N')
    ax_slider.set_title(f'Logistic map, r={r_ui.value:.2f}')
    ax_slider.set_ylim(0, max(1.0, float(N_traj.max()) * 1.1))
    fig_slider
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    __end of assignment__
    """)
    return


if __name__ == "__main__":
    app.run()
