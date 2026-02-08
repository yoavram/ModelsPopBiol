import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Population genetics 2: stochastic discrete-time models

    ## [Models in Population Biology](http://modelspopbiol.yoavram.com)
    ## Yoav Ram
    """)
    return


@app.cell
def _():
    import marimo as mo
    import random

    # '%matplotlib inline' command supported automatically in marimo
    import matplotlib.pyplot as plt
    import numpy as np
    import scipy.stats
    import sympy
    sympy.init_printing()
    import seaborn as sns
    sns.set_context('talk')
    return mo, np, plt, random, sns, sympy


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Today we focus on **discrete-time models**.
    These models can follow, for example:

    - The size of an insect population in year i;
    - The proportion of individuals in a population carrying a particular gene in the i-th generation;
    - The number of cells in a bacterial culture on day i;
    - The concentration of a toxic gas in the lung after the i-th breath;
    - The concentration of drug in the blood after the i-th dose.

    We will model a population with two distinct **types**, focusing on the change in the frequency of individuals in each of these types from one time point to the next.
    These types can model [colored balls](https://en.wikipedia.org/wiki/Polya_urn_model), genes, product, health vs. disease, or even technologies such as USB plug types.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stochastic model: large population

    We mentioned before that the assumption of a _very large population_ may break when either the population is small or when the number of individuals of a certain type is small.

    We'll start with the later case.
    In this case, the population is very large, but most of the individuals are of type $B$, whereas $A$ is initially very rare, so the dynamics of $A$ while rare are stochastic.

    A common model for such dynamics is a **branching process**.

    For simplicity, we assume that the number of offspring per individual is Poisson distributed, with mean $1$ for type $B$ and $1+s$ for type $A$.

    So the probability that an $A$ individual leaves $k$ offspring is

    $$ P(k) = e^{-(1+s)}\frac{(1+s)^k}{k!} $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From Otto and Day 2007 (ch. 14.5):

    > The key insight made by Haldane (1927) was that the probability that a type ultimately leaves no descendants must equal the probability that each offspring produced by this type leaves no descendants.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So we can write the probability to lose type $A$ despite it's advantage over type $B$ as

    $$
    \begin{aligned}
    p_{loss}
      &= \sum_{k=0}^{\infty}{p_{loss}^k P(k)} \\
      &= e^{-(1+s)} \sum_{k=0}^{\infty}{\frac{\left((1+s)p_{loss}\right)^k}{k!}} \\
      &= e^{-(1+s)} e^{p_{loss}(1+s)}
    \end{aligned}
    $$


    where the last equality is due to the Taylor expansion of the exponential function.

    So we get the extinction probability

    $$ p_{loss} = e^{-\left(1-p_{loss}\right)\left(1+s\right)} $$

    and the complement is the fixation probability, $p_{fix} = 1-p_{loss}$.

    The solution to these relationship cannot be expressed using elementary functions, and in fact, the solution is called a [Lambert W function](https://en.wikipedia.org/wiki/Lambert_W_function). A good introduction for the application of Lambert W in population biology can be found in [Lehtonen 2016](https://doi.org/10.1111/2041-210X.12568).

    We can find the specific Lambert W function that solves this relationship with [SymPy](http://sympy.org), a Python framework for symbolic mathematics.
    """)
    return


@app.cell
def _(sympy):
    ploss, s = sympy.symbols('p_{loss} s')
    eq = ploss - sympy.exp(-(1 - ploss) * (1 + s))
    sol = sympy.solve(eq, ploss)[0]

    sol
    return (sol,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's plot the result. We can evaluate SymPy expressions using `evalf` by providing a dictionary of symbol subtitutions.
    """)
    return


@app.cell
def _(np, plt, sol):
    selection_grid = np.logspace(-5, -1)
    pfix = np.array([1 - sol.evalf(subs=dict(s=_s)) for _s in selection_grid])
    plt.plot(selection_grid, pfix)
    plt.xlabel('Selection cofficient, $s$')
    plt.ylabel('Fixation probability, $p_{fix}$')
    plt.gcf()
    return pfix, selection_grid


@app.cell
def _(pfix, plt, selection_grid):
    plt.plot(selection_grid, pfix / selection_grid)
    plt.xlabel('Selection coefficient, $s$')
    plt.ylabel('$p_{fix}/s$')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So for low values of $s$, $p_{fix}\approx 2s$. Let's check this analyticaly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can rewrite the formula in terms of $p_{fix}=1-p_{loss}$:

    $$ p_{fix} = 1-e^{-(1+s)p_{fix}} $$

    If we assume that $s$ and $p_{fix}$ are both *small* (i.e. porportional to some small $\epsilon$), we can use the Taylor expansion for the exponential function (again) to get, up to term of order $o(\epsilon^3)$,

    $$ p_{fix} \approx (1+s)p_{fix} - \frac{1}{2}\big((1+s)p_{fix}\big)^2 $$

    To solve this we do some algebra and assumpe $p_{fix} \ne 0$,

    $$
    \begin{aligned}
    p_{fix} - (1+s)p_{fix} + \frac{1}{2}\big((1+s)p_{fix}\big)^2 &= 0 \Rightarrow \\
    p_{fix} - p_{fix} - s p_{fix} + \frac{1}{2}(1+s)^2 p_{fix}^2 &= 0 \Rightarrow \\
    - s p_{fix} + \frac{1}{2}(1+s)^2 p_{fix}^2 &= 0 \Rightarrow \\
    - s + \frac{1}{2}(1+s)^2 p_{fix} &= 0 \Rightarrow \\
    p_{fix} &= \frac{2s}{(1+s)^2} \Rightarrow \\
    p_{fix} &\approx 2s
    \end{aligned}
    $$

    since $s$ is small.

    Let's compare it to the full result (the Lambert W function).
    """)
    return


@app.cell
def _(pfix, plt, selection_grid):
    plt.plot(selection_grid, pfix, label='Lambert W')
    plt.plot(selection_grid, 2 * selection_grid / (1 + selection_grid) ** 2, label='$2s/(1+s)^2$')
    plt.plot(selection_grid, 2 * selection_grid, label='$2s$')
    plt.xlabel('Selection coefficient, $s$')
    plt.ylabel('Fixation probability, $p_{fix}$')
    plt.legend()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So we can use one of the two approximations, depending on the value $s$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stochastic model: small population

    In a small population, random effects can affect the dynamics even when both types are common.

    We will use the **Wright-Fisher model**:
    at each generation the number of offspring of type $A$, which we mark $n$ , is binomially distributed $Bin(N, p)$, where $p$ is the frequency of $A$ parents.

    ![Sewall Wright](https://upload.wikimedia.org/wikipedia/en/8/8d/Sewall_Wright-en.jpg)

    **[Sewall Wright](https://en.wikipedia.org/wiki/Sewall_Wright), 1889 - 1988**

    ![R.A. Fisher](https://upload.wikimedia.org/wikipedia/commons/2/21/RonaldFisher1912.jpg)

    **[R.A. Fisher](https://en.wikipedia.org/wiki/Ronald_Fisher), 1890 - 1972**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conceptual model

    Consider a population of $N$ individuals.
    $p$ of the individuals are of type $A$, and $1-p$ are of type $B$.
    In each reproductive cycle (generation), $A$ and $B$ individuals reproduce at a rate $1+s$ and $1$, where $s>0$ is the selection coefficient of $A$.

    This is similar to an urn with $N$ balls, of which $p$ are blue and $1-p$ are red.
    At each generation we fill a new urn with balls:
    1. we draw a ball from the previous urn, where the odds to draw blue vs red balls is $1+s$.
    1. we put a new ball in the new urn with the color of the drawn ball.
    1. repeat until the new urn has $N$ balls.
    """)
    return


@app.cell
def _(mo):
    mo.Html(
        """
        <iframe
          src="https://speakerdeck.com/player/a82ed8531523453d86f7fc09c857749e"
          width="100%"
          height="420"
          style="border: 0;"
          allowfullscreen
        ></iframe>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pure Python implementation

    First we implement the model using a pure Python function.

    Of course, everytime we run the simulation we will get a different result (yay randomness).
    """)
    return


@app.cell
def _(plt, random):
    def simulation_py(n0, N, s):
        n = [n0]
        while 0 < n[-1] < N:
            p = n[-1] * (1 + s) / (N + n[-1] * s)
            sample = (1 for _ in range(N) if random.random() < p)
            n.append(sum(sample))  # generator expression
        return n
    n0 = 200
    N = 1000
    _selection = 0.001
    _trajectory = simulation_py(n0, N, _selection)
    plt.plot(_trajectory)
    plt.xlabel('Generations')
    plt.ylabel('Number of $A$, $n$')
    plt.ylim(0, N)
    plt.xlim(0, len(_trajectory))
    plt.gcf()
    return (simulation_py,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This becomes slow when $N$ is large, but we don't really care too much because when $N$ is large we can use the deterministic model.

    But still, we can do faster than that using NumPy.

    ## NumPy implementation
    """)
    return


@app.cell
def _(np, plt):
    def simulation_np(n0, N, s, buflen=1000):
        n = np.empty(buflen)
        n[0] = n0
        t = 0
        while 0 < n[t] < N:
            p = n[t] * (1 + s) / (N + n[t] * s)
            t = t + 1
            if t == len(n):
                n = np.append(n, np.empty(buflen))
            n[t] = np.random.binomial(N, p)
        return n[:t + 1].copy()
    wf_initial_count = 200
    wf_pop_size = 1000
    wf_selection = 0.001
    _trajectory = simulation_np(wf_initial_count, wf_pop_size, wf_selection)
    plt.plot(_trajectory)
    plt.xlabel('Generations')
    plt.ylabel('Number of $A$, $n$')
    plt.ylim(0, wf_pop_size)
    plt.xlim(0, len(_trajectory))
    plt.gcf()
    return wf_initial_count, wf_pop_size, wf_selection


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is much faster than the pure Python implementation, and the differences between population sizes is smaller.

    Can we do even faster?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Multiple simulations

    Since the dynamics are random, we will want to run many replications of the simulation and collect some statistics.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pure Python
    """)
    return


@app.cell
def _(wf_initial_count, wf_pop_size, wf_selection, simulation_py):
    def simulations_py(n0, N, s, repetitions=10):
        return [simulation_py(n0, N, s) for _ in range(repetitions)]
    wf_trajectories_py = simulations_py(wf_initial_count, wf_pop_size, wf_selection, 100)
    return (wf_trajectories_py,)


@app.cell
def _(plt, wf_pop_size, wf_trajectories_py):
    for _trajectory in wf_trajectories_py:
        plt.plot(_trajectory, 'k', alpha=0.15)
    plt.xlabel('Generations')
    plt.ylabel('Number of $A$, $n$')
    plt.ylim(0, wf_pop_size)
    plt.xlim(0, max((len(_trajectory) for _trajectory in wf_trajectories_py)))
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NumPy

    We can do fater with NumPy.
    """)
    return


@app.cell
def _(np, plt, wf_initial_count, wf_pop_size, wf_selection):
    def simulations_np(n0, N, s, repetitions=10, buflen=1000):
        n = np.zeros((buflen, repetitions))
        n[0, :] = n0
        t = 0
        update = (n[t] > 0) & (n[t] < N)
        while update.any():
            t = t + 1
            p = n[t - 1] * (1 + s) / (N + n[t - 1] * s)
            if t == n.shape[0]:
                n = np.concatenate((n, np.zeros((buflen, repetitions))))
            n[t, update] = np.random.binomial(N, p[update])
            n[t, ~update] = n[t - 1, ~update]
            update = (n[t] > 0) & (n[t] < N)
        return n[:t].copy()
    wf_trajectories_np = simulations_np(wf_initial_count, wf_pop_size, wf_selection, 100)
    plt.plot(wf_trajectories_np, 'k', alpha=0.15)
    plt.xlabel('Generations')
    plt.ylabel('Number of $A$, $n$')
    plt.ylim(0, wf_pop_size)
    plt.xlim(0, wf_trajectories_np.shape[0])
    plt.gcf()
    return (wf_trajectories_np,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a more sophisticated way to visualize the same result.

    The x-axis is still time; the y-axis represents the repitions (or population), and the color denotes the frequency of type $A$, from dark for zero to bright for 1.

    The repetitions are ordered by the average frequency of type $A$ over the entire simulation duration, so that simulations with quick fixation of $A$ are at the top, simulations with quick extinction of $A$ are at the bottom, and simulations that took a long time to end are at the middle.
    """)
    return


@app.cell
def _(plt, wf_pop_size, wf_trajectories_np):
    _idx = wf_trajectories_np.mean(axis=0).argsort()
    plt.pcolormesh(wf_trajectories_np[:, _idx].T / wf_pop_size)
    plt.colorbar(label='Frequency of $A$')
    plt.xlabel('Generation')
    plt.ylabel('Repetition')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that the NumPy implementation is much faster.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Fixation probability (stochastic model)

    If we want to estimate the fixation probability, we don't actually need to save the entire `n` array.
    """)
    return


@app.cell
def _(np):
    def fix_prob(n0, N, s, repetitions=10):
        N = int(N)
        n = np.repeat(n0, repetitions)
        n[:] = n0 
        update = (n > 0) & (n < N)
        while update.any():
            p = n * (1 + s) / (N + n * s)
            n[update] = np.random.binomial(N, p[update])
            update = (n > 0) & (n < N)

        return (n == N).mean()

    fix_prob(1, 100, 0.1, 100000)
    return (fix_prob,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This saves both memory and CPU.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's plot the fixation probability for different population sizes; we expect it to converge to the deterministic result $2s$ for large populations.
    """)
    return


@app.cell
def _(fix_prob, np):
    Ns = np.logspace(1, 6, 100, dtype=int)
    kimura_selection = 0.001
    kimura_initial_count = 1
    _reps = 1000
    pfix_simulated = np.array([fix_prob(kimura_initial_count, N, kimura_selection, _reps) for N in Ns])
    return Ns, kimura_initial_count, kimura_selection, pfix_simulated


@app.cell
def _(Ns, kimura_selection, pfix_simulated, plt):
    plt.plot(Ns, pfix_simulated, '.', label='simulations')
    plt.axhline(2 * kimura_selection, ls='--', color='k', label='$2s$')
    plt.xlabel('Population size, $N$')
    plt.xscale('log')
    plt.ylabel('Fixation probability, $p_{fix}$')
    plt.legend()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Diffusion equation approximation for fixation probability

    There is a rather good approximation even for small population sizes.
    Using a diffusion equation approximation, [Kimura (1962)](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1210364/) reached his famous equation:

    $$ p_{fix}=\frac{1 - e^{-2 n_0 s}}{1 - e^{-2 N s}} $$

    For large $N$, the denominator is roughly 1, and if $s$ is small than we can approximate this by $2s$.

    For a modern derivation see Durrett's [Probability Models for DNA Sequence Evolution](https://services.math.duke.edu/~rtd/Gbook/Gbook.html), ch. 7 (free online).

    [![Kimura](https://upload.wikimedia.org/wikipedia/en/4/48/Motoo_Kimura.jpg)](https://en.wikipedia.org/wiki/Motoo_Kimura)

    **Motoo Kimura, 1924 - 1994**
    """)
    return


@app.cell
def _(np):
    def fix_kimura(n0, N, s):
        return np.expm1(-2 * n0 * s) / np.expm1(-2 * N * s)

    return (fix_kimura,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note the use of `expm1(x)` which is more precise than `exp(x)-1` for small `x` values.
    """)
    return


@app.cell
def _(Ns, fix_kimura, kimura_initial_count, kimura_selection, pfix_simulated, plt):
    plt.plot(Ns, pfix_simulated, '.', alpha=0.85, label='simulation')
    plt.plot(Ns, fix_kimura(kimura_initial_count, Ns, kimura_selection), '-', label='Kimura')
    plt.axhline(2 * kimura_selection / (1 + kimura_selection), ls='--', color='k', label='$2s$')
    plt.xlabel('N')
    plt.xscale('log')
    plt.ylabel('$p_{fix}$')
    plt.legend()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This approximation does the job very well.

    Behold the power of NumPy's `ufunc`:
    """)
    return


@app.cell
def _(np):
    _population_sizes = np.logspace(1, 6, 5000, dtype=np.int64)
    # %timeit [fix_kimura(n0, N, s) for N in _population_sizes]
    # %timeit fix_kimura(n0, _population_sizes, s)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Numba implementation

    [Numba](http://numba.pydata.org/) is a JIT compiler for Python and NumPy built over LLVM
    """)
    return


@app.cell
def _(fix_kimura, kimura_initial_count, kimura_selection, wf_pop_size):
    import numba
    fix_kimura_nm = numba.jit(fix_kimura)
    fix_kimura_nm(kimura_initial_count, wf_pop_size, kimura_selection)  # burn-in for the jit to work
    return


@app.cell
def _(np):
    # %timeit fix_kimura(n0, Ns, s)
    # %timeit fix_kimura_nm(n0, Ns, s)
    _population_sizes = np.logspace(1, 6, 100, dtype=float)
    return


@app.cell
def _(np):
    # magic command not supported in marimo; please file an issue to add support
    # %timeit fix_kimura(n0, Ns, s)
    # %timeit fix_kimura_nm(n0, Ns, s)
    _population_sizes = np.logspace(1, 6, 10000, dtype=float)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Fixation time (stochastic)

    Now we will focus on the *time* it takes for the fixation of one of the type to occur.
    """)
    return


@app.cell
def _(np):
    def fix_time(n0, N, s, repetitions=10):
        N = int(N)
        n = np.repeat(n0, repetitions)
        T = np.repeat(np.inf, repetitions)
        t = 0
        n[:] = n0
        update = (n > 0) & (n < N)
        while update.any():
            p = n * (1 + s) / (N + n * s)
            n[update] = np.random.binomial(N, p[update])
            update = (n > 0) & (n < N)
            t = t + 1
            T[~update] = np.minimum(T[~update], t)
        return (n == N, T)

    return (fix_time,)


@app.cell
def _(fix_time):
    fixation_initial_count = 10
    fixation_pop_size = 1000
    fixation_selection = 0.01
    fixations, times = fix_time(fixation_initial_count, fixation_pop_size, fixation_selection, 100000)
    return fixation_initial_count, fixation_pop_size, fixation_selection, fixations, times


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We'll plot the distribution of waiting time for fixation of $A$ and for extinction of $A$.
    """)
    return


@app.cell
def _(fixation_initial_count, fixation_pop_size, fixation_selection, fixations, np, plt, sns, times):
    _fig, ax = plt.subplots()
    ax.hist(times[fixations], bins=100, density=True, label='fixations')
    ax.hist(times[~fixations], bins=100, density=True, label='extinctions')
    ax.set(xlim=(0, -4 * np.log(fixation_initial_count / fixation_pop_size) / np.log(1 + fixation_selection)), xlabel='Fixation/extinction time', ylabel='Frequency, $p$')
    ax.legend()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Deterrministic approximation

    We can now compare the expected fixation time to an approximation derived from the deterministic model we studied before.
    """)
    return


@app.cell
def _(fix_time, np):
    def mean_std_fix_time(fixations, times):
        fix_times = times[fixations]
        return (fix_times.mean(), fix_times.std(ddof=1))
    fixation_time_initial_count = 1
    fixation_time_population_sizes = np.logspace(1, 8, 50, dtype=int)
    fixation_time_selection = 0.01
    fixation_time_stats = np.array([
        mean_std_fix_time(*fix_time(fixation_time_initial_count, N, fixation_time_selection, 10000))
        for N in fixation_time_population_sizes
    ])
    return fixation_time_initial_count, fixation_time_population_sizes, fixation_time_selection, fixation_time_stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The deterministic approximation is (see previous lecture)

    $$ t = -2 \frac{log(p_0)}{log{(1+s)}} $$
    """)
    return


@app.cell
def _(np):
    def T_haldane(n0, Ns, s):
        return -2 * np.log(n0/Ns) / np.log(1+s)

    return (T_haldane,)


@app.cell
def _(T_haldane, fixation_time_initial_count, fixation_time_population_sizes, fixation_time_selection, fixation_time_stats, plt, sns):
    plt.errorbar(
        fixation_time_population_sizes,
        fixation_time_stats[:, 0],
        yerr=fixation_time_stats[:, 1],
        capsize=2,
        capthick=1,
        lw=0,
        label='simulations',
        ecolor='k',
        elinewidth=1,
    )
    plt.plot(
        fixation_time_population_sizes,
        T_haldane(fixation_time_initial_count, fixation_time_population_sizes, fixation_time_selection),
        label='deterministic approx.',
    )
    plt.xscale('log')
    plt.xlabel('Population size, $N$')
    plt.ylabel('Fixation time')
    plt.legend()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that the deterministic approximation constantly over estimates the fixation time.

    Can we have a better approximation?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Diffusion equation approximation for fixation time

    Another approximation of the fixation time is based on a diffusion equation and is given in [Kimura and Ohta 1969](http://www.pubmedcentral.nih.gov/articlerender.fcgi?artid=1212239) (eq. 17). It assumes a population size of $2N$ gametes and selection advantage of $s/2$ rather then $N$ and $s$, therefore I'm changing $s=2s$ and $N=N/2$. Also, it has the initial frequency as $x$, so we define $x=n_0/N$.

    $$ I_1(x) = \frac{1 - e^{-2 n_0 s} - e^{-2Ns(1-x)} + e^{-2Ns}}{x(1-x)} $$

    $$ I_2(x) = \frac{(e^{2Nsx} - 1) (1 - e^{-2Ns(1-x)})}{x(1-x)} $$

    $$ J_1 = \frac{1}{s(1-e^{-2Ns})} \int_{x}^{1}{I_1(y) dy} $$

    $$ J_2 = \frac{1}{s(1-e^{-2Ns})} \int_{0}^{x}{I_2(y) dy} $$

    $$ u = \frac{1 - e^{-2Nsx}}{1 - e^{-2Ns}} $$

    $$ T_{fix} = J1 + \frac{1-u}{u} J_2 $$

    For a modern derivation see Durrett's [Probability Models for DNA Sequence Evolution](https://services.math.duke.edu/~rtd/Gbook/Gbook.html), ch. 7 (free online).

    Here we need to integrate some functions, we'll do this using `scipy.integrate.quad`.

    `functools.partial` reduces the number of arguments a function expects, effectively freezing some of them - mathematically, it creates a projection.

    `np.vectorize` is a decorator that converts a scalar function to an array function, giving it the `ufunc` super powers.
    """)
    return


@app.cell
def _():
    from scipy.integrate import quad 
    from functools import partial

    def integral(f, N, s, a, b):
        f = partial(f, N, s)    
        return quad(f, a, b)[0] # quad returns the integral value and an error estimate

    return (integral,)


@app.cell
def _(integral, np):
    def I1(N, s, x):
        if x == 1:
            return 0
        return (1 - np.exp(-2*N*s*x) - np.exp(-2 * N * s * (1 - x)) + np.exp(-2 * N *s)) / (x*(1-x))

    def I2(N, s, x):
        if x == 0:
            return 0
        return -np.expm1(2 * N * s * x) * np.expm1(-2 * N * s * x) / (x * (1 - x))

    @np.vectorize
    def T_kimura(n0, N, s):
        x = n0 / N
        J1 = -1.0 / (s * np.expm1(-2 * N * s)) * integral(I1, N, s, x, 1)
        u = np.expm1(-2 * N * s * x) / np.expm1(-2 * N * s)
        J2 = -1.0 / (s * np.expm1(-2 * N *s)) * integral(I2, N, s, 0, x)
        return J1 + ((1 - u) / u) * J2

    assert 254 < T_kimura(1, 1e6, 0.1) < 255
    return (T_kimura,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Behold the power of `np.vectorize`.
    """)
    return


@app.cell
def _(np):
    # %timeit np.array([T_kimura(n0, N, s) for N in Ns])
    # %timeit T_kimura(n0, Ns, s)
    _population_sizes = np.logspace(1, 6, 100)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's compare the simulation results with the two approximations:
    """)
    return


@app.cell
def _(T_haldane, T_kimura, np):
    comparison_initial_count = 1
    comparison_population_sizes = np.logspace(1, 8, 50, dtype=int)
    comparison_selection = 0.01
    fix_time_kimura = T_kimura(comparison_initial_count, comparison_population_sizes, comparison_selection)
    fix_time_haldane = T_haldane(comparison_initial_count, comparison_population_sizes, comparison_selection)
    return comparison_population_sizes, fix_time_haldane, fix_time_kimura


@app.cell
def _(comparison_population_sizes, fix_time_haldane, fix_time_kimura, fixation_time_stats, plt, sns):
    plt.errorbar(
        comparison_population_sizes,
        fixation_time_stats[:, 0],
        yerr=fixation_time_stats[:, 1],
        capsize=2,
        capthick=1,
        lw=0,
        label='simulation',
        ecolor='k',
        elinewidth=1,
    )
    plt.plot(comparison_population_sizes, fix_time_haldane, label='Haldane')
    plt.plot(comparison_population_sizes, fix_time_kimura, label='Kimura')
    plt.xscale('log')
    plt.xlabel('Population time, $N$')
    plt.ylabel('Fixation time')
    plt.legend()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Kimura's diffusion approximation is fantastic.
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
