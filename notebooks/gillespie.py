import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Continuous-time stochastic model: SIR model
    ## [Models in Population Biology](http://modelspopbiol.yoavram.com)
    ## Yoav Ram
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import numba
    from scipy.integrate import solve_ivp
    from scipy.special import lambertw as W
    from functools import partial
    import seaborn as sns
    sns.set_context('talk')
    red, blue, green = sns.color_palette('Set1', 3)
    return W, blue, green, mo, np, numba, partial, plt, red, sns, solve_ivp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SIR model

    A very common model in epidemiology is the compartmental SIR model, which stands for _Susceptible_, _Infectious_, and _Recovered_.

    $$
    \text{Susceptible} \rightarrow \text{Infectious} \rightarrow \text{Recovered}
    $$

    A more quantitative description is:

    - Susceptible individuals contact other individuals with rate $\beta$, and with probability $\frac{I}{N}$ it is an Infectious individual.
    - Infectious individuals recover with rate $\gamma$

    where $N=S+I+R$ is the total population size.

    ![diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/SIR_model_cartoon.png/320px-SIR_model_cartoon.png)

    The model was first introduced as a discrete-time deterministic model in
    > Kermack, W.O., and A.G. McKendrick. 1927. _A Contribution to the Mathematical Theory of Epidemics._ Proceedings of the Royal Society of London, Series A.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Continuous-time deterministic model
    The _deterministic_ equations, which describe the expected dynamics, are

    $$
     \frac{dS}{dt} = -\beta I S , \\
     \frac{dI}{dt} = \beta I S - \gamma I, \\
     \frac{dR}{dt} = \gamma I
    $$

    We assume new $S$ individuals are not produced, that is, the population size $N=S+I+R$ is constant throughout the epidemic.
    This means there is an implicit assumption that the epidemic is shorter than the population generation time.
    So we can assume $S$, $I$, and $R$ are frequencies and $S+I+R=1$.

    This gives the constraint

    $$ \frac{dS}{dt} + \frac{dI}{dt} + \frac{dR}{dt} = 0 , $$


    which reduces the degrees of freedom in the system, just like in the logistic growth model.
    This is different from the predator-prey model, in which new prey constantly entered the system.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analytic solution

    We use the [separation of variables method](https://upload.wikimedia.org/wikipedia/commons/2/21/Sept_proportional_differential_equation.png):

    $$
    \begin{aligned}
    \frac{dS}{dR} &= -\frac{\beta I S}{\gamma I} = -\frac{\beta}{\gamma} S \Rightarrow \\
    \frac{1}{S} dS &= -\frac{\beta}{\gamma} dR \Rightarrow \\
    \int \frac{1}{S} dS &= - \int \frac{\beta}{\gamma} dR \Rightarrow \\
    \log{S} + C_1 &= - \frac{\beta}{\gamma} R + C_2 \Rightarrow \\
    S(t) &= C_3 \cdot e^{- \frac{\beta}{\gamma} R(t)}
    \end{aligned}
    $$


    because $S$, $I$, and $R$ are short for $S(t)$, $I(t)$ and $R(t)$.

    We can add the initial condition now, $S(0)=S_0$, $R(0)=0$,

    $$
    \begin{aligned}
    S(0) &= e^{- \frac{\beta}{\gamma} R(0)} C_3 \Rightarrow \\
    C_3 &= S_0
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So we have

    $$ S(t) = S_0 \cdot e^{- \frac{\beta}{\gamma} R(t)} $$

    Note that $R(t)$ is also a variable, so this is not a closed-form solution.

    A trivial solution occurs if $R(t)\equiv 0$ always, such that $S(t) \equiv S_0$ always--but this can only occur if $I(0) \equiv 0$, because otherwise an infected individual will recover and so $R(t)>0$ for some $t$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What happens after "enough" time has elapesed?
    At the limit $t \to \infty$, we get $S^*=S(\infty) = 1-R(\infty)$, and

    $$
    \begin{aligned}
    S^* &= S_0 e^{-\frac{\beta}{\gamma}(1-S^*)}
      = S_0 e^{-\frac{\beta}{\gamma}}e^{\frac{\beta}{\gamma}S^*} \Rightarrow \\
    S^* e^{-\frac{\beta}{\gamma}S^*} &= S_0 e^{-\frac{\beta}{\gamma}} \Rightarrow \\
    -\frac{\beta}{\gamma} S^* e^{-\frac{\beta}{\gamma}S^*}
      &= -S_0\frac{\beta}{\gamma} e^{-\frac{\beta}{\gamma}}
    \end{aligned}
    $$



    Following [Wang 2010](https://doi.org/10.4169/074683410X480276), This can be solved in terms of a **Lambert W function**.
    Setting $S_0=1$ (as we assume that most of the population is susceptible at the begining), $x=-\beta/\gamma$ and $y=-\beta/\gamma S^*$, we get that

    $$ ye^{y} = xe^{x} $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, using the [identities for the Lambert W function](https://en.wikipedia.org/wiki/Lambert_W_function#Identities), and given that $x<0$ (since the two rates are positive), this has three possible solutions.
    1. $x=y$, that is, $S^*=1$, and the epidemic doesn't occur beyond the initial infectious individuals.
    1. If $x<-1$, that is, $\beta/\gamma>1$, then $y=W_0(xe^{x})$, that is,

    $$ S^* = -\frac{\gamma}{\beta} W_0\left(-\frac{\beta}{\gamma} e^{-\frac{\beta}{\gamma}}\right)
    $$


    1. If $-1<x<0$, that is, $0 < \beta/\gamma < 1$, then $y=W_1(xe^{x})$. However, $W_1(\cdot)<-1$, and therefore $-\frac{\gamma}{\beta} W_1\left(-\frac{\beta}{\gamma} e^{-\frac{\beta}{\gamma}}\right) > 1$, which is not an acceptable solution for $S^*$.

    Therefore, the epidemic will only occur if $\beta>\gamma$, and in that case the number of recovered (hence also the accumulated number of infectious) will be

    $$ R^* = 1-S^*, $$

    $$ S^* = -\frac{\gamma}{\beta} W\left(-S_0 \frac{\beta}{\gamma} e^{-\beta/\gamma}\right). $$


    **Note 1:** The _reproductive number_ of the epidemic is $R_0=\frac{\beta}{\gamma}$. Do not confuse this with $R(t=0)$.

    **Note 2:** We saw the Lambert W function in the population genetics session, see [Lehtonen 2016](https://doi.org/10.1111/2041-210X.12568) for more applications in ecology and evolution.
    """)
    return


@app.cell
def _(W, np):
    def Sstar(S0, β, γ):
        R0 = β/γ # reproductive number
        Sstar_ = -1/R0 * W(-S0 * R0 * np.exp(-R0))
        assert np.allclose(Sstar_.imag, 0), Sstar_.imag
        return Sstar_.real

    return (Sstar,)


@app.cell
def _():
    params = {
        "β": 0.2,
        "γ": 0.1,
        "S0": 1-1/1000,
        "I0": 1/1000,
    }
    return (params,)


@app.cell
def _(Sstar, np, params, plt, sns):
    _S0 = params['S0']
    _γ = params['γ']
    _β = np.logspace(-2, 0, 500)

    plt.plot(_β/_γ, 1-Sstar(S0=_S0, β=_β, γ=_γ))
    plt.axvline(1, ls='--', color='k')
    plt.xlabel(r'Reproductive number, $R_0 = \beta/\gamma$')
    plt.ylabel('Total number of infectious, $R^*$')
    plt.ylim(-0.01, 1)
    plt.xlim(0, 11)
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Numerical solution

    We will solve the ODE numerically just as we did in previous classes.
    """)
    return


@app.cell
def _(blue, green, np, partial, red, solve_ivp):
    def gradient(t, SI, β, γ):
        S, I = SI
        N = S + I
        dSdt = -β * S * I / N
        dIdt = β * S * I - γ * I
        return dSdt, dIdt

    def numerical_solution(β, γ, S0, I0, tmax=250, tsteps=1000):
        N = S0 + I0
        gradient_ = partial(gradient, β=β, γ=γ)
        t = np.linspace(0, tmax, tsteps)
        sol = solve_ivp(gradient_, t_span=(0, t.max()), y0=(S0, I0), t_eval=t)
        S, I = sol.y
        return t, S, I, N - S - I

    def plot_SIR(t, S, I, R, label='', ls='-', ax=None):
        ax.plot(t, S, lw=3, ls=ls, color=green, label='S ' + label)
        ax.plot(t, I, lw=3, ls=ls, color=red, label='I ' + label)
        ax.plot(t, R, lw=3, ls=ls, color=blue, label='R ' + label)
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Frequency')
        return ax

    return numerical_solution, plot_SIR


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now can plot the numerical solution for specific parameters and compare to the analytic solution.

    Note that the rates are given units of events per day.
    """)
    return


@app.cell
def _(mo, params):
    β_ = mo.ui.slider(
        0.05, 1.0, 0.01, value=params["β"], show_value=True, label="β"
    )
    γ_ = mo.ui.slider(
        0.01, 0.5, 0.01, value=params["γ"], show_value=True, label="γ"
    )
    I0_ = mo.ui.slider(
        1/1000, 0.5, 0.01, value=params["I0"], show_value=True, label="I0",
    )
    controls = mo.hstack([β_, γ_, I0_], justify="start")
    controls
    return I0_, controls, β_, γ_


@app.cell
def _(I0_, Sstar, numerical_solution, params, plot_SIR, plt, sns, β_, γ_):
    _fig, _ax = plt.subplots(1, 1, figsize=(7, 4))
    hline_kws = dict(ls='-', alpha=0.5, color='k')

    t, s, i, r = numerical_solution(
        β=β_.value, γ=γ_.value, I0=I0_.value, S0=params['S0'])
    plot_SIR(t, s, i, r, ax=_ax)
    _s_star = Sstar(S0=params['S0'], β=β_.value, γ=γ_.value)
    _ax.axhline(_s_star, **hline_kws)
    _ax.axhline(1 - _s_star, **hline_kws)
    _ax.set_title(f'β={β_.value:.2f}, γ={γ_.value:.2f}, I0={I0_.value:.3f}')
    _ax.legend()
    _fig.tight_layout()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stochastic model

    To deal with stochasticity in this system, we need to describe it using a stochastic model -- using a distribution, rather than just the mean value. That's the difference between a deterministic and a stochastic model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let $f_t(S, I, R)$ be the probability of $S$ susceptibles, $I$ infectious, and $R$ recovered at time $t$.
    It represents a distribution of the number of individuals in each compartment at each time point.

    How does this distribution $f_t(S, I, R)$ change over time? Individuals become infected and then recover. How does it affect the distribution?

    At time $t$, there is probability $f_t(S,I,R)$ that the state is $(S, I, R)$.
    The rates $\beta$ and $\gamma$ are all in 1/days.
    Now, we choose a time interval $dt$ that is so small so that the probability that more then one event (one infection, one recovery) occured during this time interval is negligible.
    So, when we multiply the rates by $dt$ we get the probability for each event to occur:
    - infection of one susceptible , $S \to S-1$ and $I \to I+1$, with probability $\beta S I dt$.
    - recovery of one infectious, $I \to I-1$ and $R \to R+1$, with probability $\gamma I dt$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The change in the distribution from time $t$ to time $t+dt$ can then be described by changes from $S$ to $S+1$, from $S-1$ to $S$, and similarly for $I$ and $R$.

    $$
    \begin{aligned}
    f_{t+dt}(S, I, R) =
        & f_t(S, I, R) \left(1 - \beta S I \,dt  - \gamma I \,dt \right)  + \\
        & f_t(S+1, I-1, R) \, \beta (S+1) (I-1) \,dt + \\
        & f_t(S, I+1, R-1) \, \gamma (I+1) \,dt
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This can be rearranged to:

    \begin{aligned}
    \frac{f_{t+dt}(S, I, R) - f_t(S, I, R)}{dt} =
         & f_t(S, I, R) \left(- \beta S I  - \gamma I \right)  + \\
         & f_t(S+1, I-1, R) \, \beta (S+1) (I-1) + \\
         & f_t(S, I+1, R-1) \, \gamma (I+1)
    \end{aligned}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now if we take the limit $dt \to 0$,

    $$
    \lim_{dt \to 0}{\frac{f_{t+dt}(S,I,R) - f_t(S,I,R)}{dt}} = \frac{d f_t(S,I,R)}{dt}
    $$

    This differential equation that describes the change in $f_t(S,I,R)$ over time is sometimes called the **master equation**:

    \begin{aligned}
    \frac{d f_t(S,I,R)}{dt}
      &= f_t(S, I, R) \left(- \beta S I  - \gamma I \right) \\
      &\quad + f_t(S+1, I-1, R) \, \beta (S+1) (I-1) \\
      &\quad + f_t(S, I+1, R-1) \, \gamma (I+1)
    \end{aligned}

    Note that in this case we assume $S$, $I$, and $R$ are **positive integers**, $t$ is a non-negative real number, and $f_t(S,I,R)$ is a probability so $0 \le f_t(S,I,R) \le 1$ and $\sum_{S,I,R \ge 0}{f_t(S,I,R)} = 1$.

    But how do we integrate this differential equation?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gillespie algorithm

    The master equation described the system fully, but is very hard to work with. We will describe a computational method to integrate a _realization_ of the system; we can think of this as drawing from the distribution $f_t(S,I,R)$ for a time span $0 \le t \le t_{max}$. This can also be thought of as a Monte Carlo method, in which we use simulations to integrate a stochastic differential equation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To implement a stochastic integration method, we first write the master equation as a list of events and their corresponding rates:

    \begin{align}
    \begin{array}{ll}
    \text{event, }r_i & \text{rate, } a_i \\
    S,I \rightarrow S-1, I+1,\;\;\;\; & \beta S I \\
    I,R \rightarrow I-1, R+1 \;\;\;\; & \gamma I
    \end{array}
    \end{align}

    The **Gillespie algorithm** is a method for sampling from the probability distribution $f_t(S,I,R)$.
    It was proven by Dobbs and later implemented by Gillespie ([1976](https://www.sciencedirect.com/science/article/pii/0021999176900413), [1977](https://pubs.acs.org/doi/abs/10.1021/j100540a008?journalCode=jpchax)), see the papers for the technical details.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The idea is that reactions are rare and discrete, and therefore represent separate events that can be modeled by a *Poisson process* with exponentially distributed waiting times.

    Let's plot exponential random variables to recall what their distribution looks like.
    NumPy's exponential random number generator accepts the mean value, or the 1/rate:
    """)
    return


@app.cell
def _(np, plt, sns):
    sample_size = 100000
    wait_exp1 = np.random.exponential(1, size=sample_size)
    wait_exp2 = np.random.exponential(2, size=sample_size)
    wait_exp10 = np.random.exponential(10, size=sample_size)
    _fig, _ax = plt.subplots(1, 1, figsize=(12, 4))
    hist_kws = dict(kde=False, alpha=0.5)
    sns.histplot(wait_exp1, **hist_kws, label='Exp(1)', ax=_ax)
    sns.histplot(wait_exp2, **hist_kws, label='Exp(2)', ax=_ax)
    sns.histplot(wait_exp10, **hist_kws, label='Exp(10)', ax=_ax)
    _ax.set_xlim(-5, 40)
    print(wait_exp1.mean(), 1)
    print(wait_exp2.mean(), 2)
    print(wait_exp10.mean(), 10)
    plt.gcf()
    return hist_kws, wait_exp1, wait_exp10, wait_exp2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Recall from probability theory that the minimum of $n$ exponentially distributed waiting times is exponentioally distributed; the rate of the minimum is the sum of the rates.
    So, if the waiting times for the different reactions are exponentially distributed with rates $a_i$, then the waiting time for the next reaction (whatever it is) is also exponentially distributed with rate $\sum_i{a_i}$.
    """)
    return


@app.cell
def _(hist_kws, np, sns, wait_exp1, wait_exp10, wait_exp2):
    wait_min = np.minimum(wait_exp1, wait_exp2)
    wait_min = np.minimum(wait_min, wait_exp10)
    print(wait_min.mean(), 1 / (1 + 1 / 2 + 1 / 10))
    sns.histplot(wait_min, **hist_kws)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Given that some event occured, the probability that it was event $r_i$ is $\frac{a_i}{\sum_j{a_j}}$.

    So the algorithm works like this, starting with an initial state $x_0 = (S_0, I_0, R_0)$:
    1. Set time $t=0$.
    1. Calculate the event rates $a_i$ using current state $x_t$.
    1. Calculate the sum of rates $\sum_i{a_i}$.
    1. Draw the waiting time for the next event $\Delta t$ from exponential distribution $\mathit{Exp}(\sum_i{a_i})$.
    1. Draw the event type $j$ from multinomial distribution $\mathit{Multinomial}(1, a_i/\sum_j{a_j})$.
    1. Find the state change $\Delta x$ due to event $r_j$.
    1. Update the state $x_{t+\Delta t} = x_t + \Delta x$.
    1. Update the time $t \to t + \Delta t$.
    1. If $t<t_{max}$, go to step 2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Implementation

    First, a function that calculates the event rates.

    [Numba](http://numba.pydata.org) is used here to accelerate the function by passing it through a JIT compiler.
    """)
    return


@app.cell
def _(np, numba):
    @numba.njit
    def get_rates(S, I, R, β, γ):
        N = S + I + R
        return np.array([
            β*S*I/N, # infection
            γ*I, # recovery
        ])

    return (get_rates,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Draw the time for the next event:
    """)
    return


@app.cell
def _(np, numba):
    @numba.njit 
    def draw_time(rates):
        total_rate = rates.sum()
        return np.random.exponential(1/total_rate)

    return (draw_time,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Draw the event type:
    """)
    return


@app.cell
def _(np, numba):
    @numba.njit
    def draw_event(rates):
    #     assert (rates>0).any(), rates # uncomment for debugging, but then turn off for jit
        rates = rates / rates.sum()
        return np.random.multinomial(1, rates).argmax()

    return (draw_event,)


@app.cell
def _(draw_event, get_rates):
    _rates = get_rates(S=100, I=1, R=0, β=0.1, γ=0.05)
    _rates = _rates / _rates.sum()
    draw_event(_rates)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Updates matrix, `updates[i,j]` is the change in type `j` due to event `i`; `j=0` for S, `j=1` for I, `j=2` for R.
    """)
    return


@app.cell
def _(np):
    updates = np.array([
        [-1, 1, 0], # infection
        [0, -1, 1], # recovery
    ])
    return (updates,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One step of the simulation goes through a single update.
    """)
    return


@app.cell
def _(draw_event, draw_time, get_rates, numba, updates):
    @numba.njit
    def gillespie_step(S, I, R, β, γ):
        rates = get_rates(S, I, R, β, γ)
        Δt = draw_time(rates)
        ri = draw_event(rates)
        ΔS, ΔI, ΔR = updates[ri]
        return Δt, ΔS, ΔI, ΔR

    return (gillespie_step,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now a full Gillespie stochastic simulation algorithm. We stop when $t \ge t_{max}$.
    """)
    return


@app.cell
def _(gillespie_step, np, updates):
    # @numba.njit
    def gillespie_ssa(β, γ, S0, I0, N=1000, t_steps=1000, t0=0, tmax=250):
        times = np.linspace(t0, tmax, t_steps) # recording times: time points in which to record the state
        states = np.empty(shape=(updates.shape[1], t_steps), dtype=np.int32) # recorded states: type x time        
        # init
        t = t0
        S, I, R = int(S0*N), int(I0*N), 0
        ΔS, ΔI, ΔR = 0, 0, 0
        # loop over recording times
        for i, next_t in enumerate(times):
            # simulate until next recording time
            while t < next_t and I > 0:
                Δt, ΔS, ΔI, ΔR = gillespie_step(S, I, R, β, γ)
                t, S, I, R = t+Δt, S+ΔS, I+ΔI, R+ΔR
            # record the previous state for the time point we just passed
            states[:, i] = S - ΔS, I - ΔI, R - ΔR
        # return array equivalent to [[times, S, I, R] for t in times]
        return np.concatenate((times.reshape(1, -1), states), axis=0)

    return (gillespie_ssa,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Simulation

    Run a single simulation and plot it.
    """)
    return


@app.cell
def _(controls):
    controls
    return


@app.cell
def _(
    I0_,
    gillespie_ssa,
    numerical_solution,
    params,
    plot_SIR,
    plt,
    sns,
    β_,
    γ_,
):
    _fig, _ax = plt.subplots()

    _stoch = gillespie_ssa(
        S0=params['S0'], I0=I0_.value, β=β_.value, γ=γ_.value)
    plot_SIR(*_stoch, ax=_ax)
    _ax.legend(bbox_to_anchor=(1, 0.7))

    _det = numerical_solution(
        S0=params['S0'], I0=I0_.value, β=β_.value, γ=γ_.value)
    plot_SIR(*_det, ls='--', ax=_ax,)

    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compare stochastic and deterministic
    Run the Gillespie algorithm 100 times and compare it to the deterministic dynamics.

    **Note:** Try to run this with and `numba`; in my tests the version with `numba` is about 6-fold faster.
    """)
    return


@app.cell
def _(I0_, gillespie_ssa, np, numerical_solution, params, β_, γ_):
    reps = 1000
    sir_trajectories = np.array([
        gillespie_ssa(S0=params['S0'], I0=I0_.value, β=β_.value, γ=γ_.value)
        for _ in range(reps)
    ])
    t_det, s_det, i_det, r_det = numerical_solution(
        S0=params['S0'], I0=I0_.value, β=β_.value, γ=γ_.value)
    return i_det, r_det, s_det, sir_trajectories, t_det


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We plot all the simulated trajectories, but with transparency so we can see them all.

    We also plot the average trajectory (black solid lines) and the ODE solution (black dashed lines).
    """)
    return


@app.cell
def _(i_det, plot_SIR, plt, r_det, s_det, sir_trajectories, sns, t_det):
    _fig, _ax = plt.subplots()
    t_stoch = sir_trajectories[0, 0, :]
    s_stoch = sir_trajectories[:, 1, :]
    i_stoch = sir_trajectories[:, 2, :]
    r_stoch = sir_trajectories[:, 3, :]
    plot_SIR(t_stoch, s_stoch.T, i_stoch.T, r_stoch.T, ax=_ax)
    for line in _ax.get_lines():
        line.set_alpha(0.01)
    plot_SIR(t_stoch, s_stoch.mean(axis=0), i_stoch.mean(axis=0), r_stoch.mean(axis=0), ax=_ax)
    for line in _ax.get_lines()[-3:]:
        line.set_color('k')
    plot_SIR(t_det, s_det, i_det, r_det, ax=_ax)
    for line in _ax.get_lines()[-3:]:
        line.set_ls('--')
        line.set_color('k')
        line.set_alpha(0.5)
    _ax.legend().set_visible(False)
    sns.despine()
    plt.gcf()
    return i_stoch, r_stoch, s_stoch, t_stoch


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that indeed the mean of the stochastic dynamics is very close to the ODE solution, even with just 100 replicates.

    Instead of plotting all the trajectories, we can just plot the mean with a 95% confidence interval.
    """)
    return


@app.cell
def _(
    blue,
    green,
    i_stoch,
    np,
    plot_SIR,
    plt,
    r_stoch,
    red,
    s_stoch,
    sns,
    t_stoch,
):
    _fig, _ax = plt.subplots()
    plot_SIR(t_stoch, s_stoch.mean(axis=0), i_stoch.mean(axis=0), r_stoch.mean(axis=0), ax=_ax)
    s_low, s_high = (np.quantile(s_stoch, 0.025, axis=0), np.quantile(s_stoch, 0.975, axis=0))
    i_low, i_high = (np.quantile(i_stoch, 0.025, axis=0), np.quantile(i_stoch, 0.975, axis=0))
    r_low, r_high = (np.quantile(r_stoch, 0.025, axis=0), np.quantile(r_stoch, 0.975, axis=0))
    _ax.fill_between(t_stoch, s_low, s_high, alpha=0.5, color=green)
    _ax.fill_between(t_stoch, i_low, i_high, alpha=0.5, color=red)
    _ax.fill_between(t_stoch, r_low, r_high, alpha=0.5, color=blue)
    _ax.legend(bbox_to_anchor=(1, 0.75))
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # References
    - Some of this session follows Justin Bois notes (Caltech BE150 2017), which are not available online anymore.
    - [Python code and original papers](https://github.com/karinsasaki/gillespie-algorithm-python) by Karin Sasaki
    - [Mechanisms of noise-resistance in genetic oscillators](http://www.pnas.org/content/99/9/5988.full) - paper by Vilar, Kueh, Barkai, Leibler that uses Gillespie algorithm.
    - [Paper](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0095150) comparing Gillespie simulation with agent-based simulation in cancer modelling.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Colophon
    This notebook was written by [Yoav Ram](http://www.yoavram.com) and is part of the [Models in Population Biology](http://modelspopbiol.yoavram.com) course at Tel Aviv University.

    This work is licensed under a CC BY-NC-SA 4.0 International License.
    """)
    return


if __name__ == "__main__":
    app.run()
