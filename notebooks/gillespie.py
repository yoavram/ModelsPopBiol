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
    # '%matplotlib inline' command supported automatically in marimo
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
    \begin{align}
    \text{Susceptible} \rightarrow \text{Infectious} \rightarrow \text{Recovered}
    \end{align}

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

       $$ \frac{dS}{dt} = -\beta I S , $$

       $$ \frac{dI}{dt} = \beta I S - \gamma I, $$

       $$ \frac{dR}{dt} = \gamma I $$



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

       $$ S^* = -\frac{\gamma}{\beta} W_0\left(-\frac{\beta}{\gamma} e^{-\frac{\beta}{\gamma}}\right) $$


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
        assert np.allclose(Sstar_.imag, 0)
        return Sstar_.real

    return (Sstar,)


@app.cell
def _(Sstar, np, plt, sns):
    S0 = 1
    γ = 0.1
    β = np.logspace(-2, 0, 500)
    plt.plot(β/γ, 1-Sstar(S0, β, γ))
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
        dSdt = -β * S * I 
        dIdt = β * S * I - γ * I
        return dSdt, dIdt

    def numerical_solution(β, γ, I0, tmax=250, tsteps=1000):
        gradient_ = partial(gradient, β=β, γ=γ)
        t = np.linspace(0, tmax, tsteps)
        sol = solve_ivp(gradient_, t_span=(0, t.max()), y0=(1-I0, I0), t_eval=t)
        S, I = sol.y
        return t, S, I, 1-S-I

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
def _(Sstar, numerical_solution, plot_SIR, plt, sns):
    _fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    hline_kws = dict(ls='-', alpha=0.5, color='k')
    I0 = 0.001
    S0_1 = 1 - I0
    ax = axes[0]
    β_1, γ_1 = (0.5, 0.1)
    t, S, I, R = numerical_solution(β_1, γ_1, I0)
    plot_SIR(t, S, I, R, ax=ax)
    ax.axhline(Sstar(S0_1, β_1, γ_1), **hline_kws)
    ax.axhline(1 - Sstar(S0_1, β_1, γ_1), **hline_kws)
    ax.set_title('β={}, γ={}'.format(β_1, γ_1))
    ax = axes[1]
    β_1, γ_1 = (0.2, 0.1)
    t, S, I, R = numerical_solution(β_1, γ_1, I0)
    plot_SIR(t, S, I, R, ls='--', ax=ax)
    ax.axhline(Sstar(S0_1, β_1, γ_1), **hline_kws)
    ax.axhline(1 - Sstar(S0_1, β_1, γ_1), **hline_kws)
    ax.set_title('β={}, γ={}'.format(β_1, γ_1))
    ax = axes[2]
    β_1, γ_1 = (0.05, 0.1)
    t, S, I, R = numerical_solution(β_1, γ_1, I0)
    plot_SIR(t, S, I, R, ls='-.', ax=ax)
    ax.axhline(Sstar(S0_1, β_1, γ_1), **hline_kws)
    ax.axhline(1 - Sstar(S0_1, β_1, γ_1), **hline_kws)
    ax.set_title('β={}, γ={}'.format(β_1, γ_1))
    ax.legend()
    _fig.tight_layout()
    sns.despine()
    plt.gcf()
    return β_1, γ_1


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

       $$

    \begin{aligned}
    \frac{f_{t+dt}(S, I, R) - f_t(S, I, R)}{dt} =
         & f_t(S, I, R) \left(- \beta S I  - \gamma I \right)  + \\
         & f_t(S+1, I-1, R) \, \beta (S+1) (I-1) + \\
         & f_t(S, I+1, R-1) \, \gamma (I+1)
    \end{aligned}

       $$
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

    $$
    \begin{aligned}
    \frac{d f_t(S,I,R)}{dt}
      &= f_t(S, I, R) \left(- \beta S I  - \gamma I \right) \\
      &\quad + f_t(S+1, I-1, R) \, \beta (S+1) (I-1) \\
      &\quad + f_t(S, I+1, R-1) \, \gamma (I+1)
    \end{aligned}
    $$



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
    n = 100000
    x1 = np.random.exponential(1, size=n)
    x2 = np.random.exponential(2, size=n)
    x10 = np.random.exponential(10, size=n)
    _fig, ax_1 = plt.subplots(1, 1, figsize=(12, 4))
    kwargs = dict(kde=False, alpha=0.5)
    sns.histplot(x1, **kwargs, label='Exp(1)', ax=ax_1)
    sns.histplot(x2, **kwargs, label='Exp(2)', ax=ax_1)
    sns.histplot(x10, **kwargs, label='Exp(10)', ax=ax_1)
    ax_1.set_xlim(-5, 40)
    print(x1.mean(), 1)
    print(x2.mean(), 2)
    print(x10.mean(), 10)
    plt.gcf()
    return ax_1, kwargs, x1, x10, x2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Recall from probability theory that the minimum of $n$ exponentially distributed waiting times is exponentioally distributed; the rate of the minimum is the sum of the rates.
    So, if the waiting times for the different reactions are exponentially distributed with rates $a_i$, then the waiting time for the next reaction (whatever it is) is also exponentially distributed with rate $\sum_i{a_i}$.
    """)
    return


@app.cell
def _(ax_1, kwargs, np, sns, x1, x10, x2):
    x_min = np.minimum(x1, x2)
    x_min = np.minimum(x_min, x10)
    sns.histplot(x_min, **kwargs)
    ax_1.set_xlim(-5, 40)
    print(x_min.mean(), 1 / (1 + 1 / 2 + 1 / 10))
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
def _(draw_event, get_rates, β_1, γ_1):
    rates = get_rates(100, 1, 0, β_1, γ_1)
    rates = rates / rates.sum()
    draw_event(rates)
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
def _(gillespie_step, np, numba, updates):
    @numba.njit
    def gillespie_ssa(β, γ, S0, I0, t_steps=1000, t0=0, tmax=250):
        times = np.linspace(t0, tmax, t_steps) # recording times: time points in which to record the state
        states = np.empty(shape=(updates.shape[1], t_steps), dtype=np.int32) # recorded states: type x time
        N = S0 + I0
        # init
        t = t0
        S, I, R = S0, I0, 0
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
def _(gillespie_ssa, numerical_solution, plot_SIR, plt, sns):
    β_2, γ_2 = (0.2, 0.1)
    S0_2, I0_1 = (1000, 10)
    N = S0_2 + I0_1
    T, S_1, I_1, R_1 = gillespie_ssa(β_2, γ_2, S0=S0_2, I0=I0_1)
    t_1, s, i, r = numerical_solution(β_2, γ_2, I0=I0_1 / (S0_2 + I0_1))
    _fig, ax_2 = plt.subplots()
    plot_SIR(T, S_1, I_1, R_1, ax=ax_2)
    ax_2.legend(bbox_to_anchor=(1, 0.7))
    plot_SIR(t_1, s * N, i * N, r * N, ls='--', ax=ax_2)
    sns.despine()
    plt.gcf()
    return I0_1, N, S0_2, β_2, γ_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compare stochastic and deterministic
    Run the Gillespie algorithm 100 times and compare it to the deterministic dynamics.

    **Note:** Try to run this with and `numba`; in my tests the version with `numba` is about 6-fold faster.
    """)
    return


@app.cell
def _(I0_1, S0_2, gillespie_ssa, np, β_2, γ_2):
    # magic command not supported in marimo; please file an issue to add support
    # %%time
    reps = 1000
    TSIR = np.array([gillespie_ssa(β_2, γ_2, S0=S0_2, I0=I0_1) for _ in range(reps)])
    return (TSIR,)


@app.cell
def _(I0_1, S0_2, numerical_solution, β_2, γ_2):
    t_2, s_1, i_1, r_1 = numerical_solution(β_2, γ_2, I0=I0_1 / (S0_2 + I0_1))
    return i_1, r_1, s_1, t_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We plot all the simulated trajectories, but with transparency so we can see them all.

    We also plot the average trajectory (black solid lines) and the ODE solution (black dashed lines).
    """)
    return


@app.cell
def _(N, TSIR, i_1, plot_SIR, plt, r_1, s_1, sns, t_2):
    _fig, ax_3 = plt.subplots()
    T_1 = TSIR[0, 0, :]
    S_2 = TSIR[:, 1, :]
    I_2 = TSIR[:, 2, :]
    R_2 = TSIR[:, 3, :]
    plot_SIR(T_1, S_2.T, I_2.T, R_2.T, ax=ax_3)
    for line in ax_3.get_lines():
        line.set_alpha(0.01)
    plot_SIR(T_1, S_2.mean(axis=0), I_2.mean(axis=0), R_2.mean(axis=0), ax=ax_3)
    for line in ax_3.get_lines()[-3:]:
        line.set_color('k')
    plot_SIR(t_2, s_1 * N, i_1 * N, r_1 * N, ax=ax_3)
    for line in ax_3.get_lines()[-3:]:
        line.set_ls('--')
        line.set_color('k')
        line.set_alpha(0.5)
    ax_3.legend().set_visible(False)
    sns.despine()
    plt.gcf()
    return I_2, R_2, S_2, T_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that indeed the mean of the stochastic dynamics is very close to the ODE solution, even with just 100 replicates.

    Instead of plotting all the trajectories, we can just plot the mean with a 95% confidence interval.
    """)
    return


@app.cell
def _(I_2, R_2, S_2, T_1, blue, green, np, plot_SIR, plt, red, sns, t_2):
    _fig, ax_4 = plt.subplots()
    plot_SIR(T_1, S_2.mean(axis=0), I_2.mean(axis=0), R_2.mean(axis=0), ax=ax_4)
    S_low, S_high = (np.quantile(S_2, 0.025, axis=0), np.quantile(S_2, 0.975, axis=0))
    I_low, I_high = (np.quantile(I_2, 0.025, axis=0), np.quantile(I_2, 0.975, axis=0))
    R_low, R_high = (np.quantile(R_2, 0.025, axis=0), np.quantile(R_2, 0.975, axis=0))
    ax_4.fill_between(t_2, S_low, S_high, alpha=0.5, color=green)
    ax_4.fill_between(t_2, I_low, I_high, alpha=0.5, color=red)
    ax_4.fill_between(t_2, R_low, R_high, alpha=0.5, color=blue)
    ax_4.legend(bbox_to_anchor=(1, 0.75))
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
