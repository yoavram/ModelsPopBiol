import marimo

__generated_with = "0.23.3"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Continuous-time univariate deterministic model: population growth models

    ## [Models in Population Biology](http://modelspopbiol.yoavram.com)
    ## Yoav Ram
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_context('talk')
    return mo, np, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exponential growth model

    How do we model the growth of a population?

    According to [Malthus](http://en.wikipedia.org/wiki/Thomas_Robert_Malthus), if the rate of births is $b$ per time unit and the rate of deaths is $d$ per time unit, then the change in the number of individuals $N(t)$ is given by

    $$ N(t+\Delta t) = N(t) + N(t) b \Delta t - N(t) d \Delta t \Rightarrow $$

    $$ \frac{N(t+\Delta t) - N(t)}{\Delta t} = b N(t) - d N(t) = r N(t) $$

    where $r = b-d$ is the specific growth rate, and effective parameter (i.e., per capita growth rate).
    If we take $\Delta t \to 0$, then the instantaneous rate of growth (or decline) of the population is

    $$ \frac{dN(t)}{dt} = b N(t) - d N(t) = r N(t) $$

    This is called the Malthusian growth model or more commonly the [exponential growth model](https://en.wikipedia.org/wiki/Exponential_growth).

    This ordinary differential equation, or ODE, can be solved via [logarithmic differentiation](https://en.wikipedia.org/wiki/Logarithmic_differentiation):

    $$ \frac{dN(t)}{dt} = r N(t) $$

    $$ \frac{1}{N(t)} \frac{dN(t)}{dt} = r $$

    $$ \frac{d \log{N(t)}}{dt} = r $$

    $$ \log{N(t)} =  r t + C $$

    $$ N(t) = e^{rt + C} = e^{C} e^{rt} $$

    Now add the boundary condition $N(0) = N_0$ to get

    $$ e^{C} = N_0 $$

    and finally

    $$ N(t) = N_0 e^{rt} $$

    Note that during the integration we found that the **logarithm of the population should be a linear function of time** $\log{N(t)} = \log{N(0)} + rt$.

    Let's implement this model.
    Say we have a bacterial population with initial density $N_0=100$ cells and a specific growth rate of $r=1$ for one cell division per hour (i.e., 60 minutes between cell divisions), and let them grow for 24 hours.
    """)
    return


@app.cell
def _(np):
    N0 = 100
    r = 1
    t = np.linspace(0, 24, 500)
    N = N0 * np.exp(r * t)
    return N, t


@app.cell
def _(N, plt, sns, t):
    plt.plot(t, N)
    plt.xlabel('Time (hr)')
    plt.ylabel('Population size (cells)')
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a problem - the number of cells after one day is $\approx 2.5\cdot10^{12}$, which is just... too much.

    What can limit the growth of the population?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Logistic growth model

    The Malthusian/exponential growth model can't always be correct: many times growth decelerates and effectively stops when reaching a certain size $K$ (carrying capacity, maximum yield, maximum population density etc.).
    This is true for fish body size (Schnute 1981), microbial population size in a constant volume (Zwietering 1990), and natural animal populations.
    In these cases it is common to use the [**logistic growth model**](http://en.wikipedia.org/wiki/Logistic_function#In_ecology:_modeling_population_growth) in which the size of the population inhibits growth, leading to a maximum population size after which growth stops.

    For example, consider a population $N(t)$ which consumes a resource $R(t)$ to grow.

    $$ \frac{dR(t)}{dt} = -h R(t) N(t) $$

    $$ \frac{dN(t)}{dt} = \epsilon h R(t) N(t) $$

    From now on we will omit the $(t)$ after $N$ and $R$, for convenience.

    Set $K = \epsilon R + N$ so that:
    - $\frac{dK}{dt} = \epsilon \frac{dR}{dt} + \frac{dN}{dt} = 0$ and therefore $K$ is constant and we can set $K=\epsilon R(0)+N(0)$.
    - $\epsilon R = K - N$.

    This makes sense - the population consumes a resource to grow, therefore the resource is depleted, which eventually leads to the population growth seizing. It is a law of conservation ($K$ is constant).

    So, we have

    $$ \frac{dN}{dt} = \epsilon h R N $$

    $$ \frac{dN}{dt} = \epsilon h N (K-N) $$

    $$ \frac{dN}{dt} = r N \left(1-\frac{N}{K}\right) $$

    where $r = h / K$.

    This is called the _logistic ordinary differential equation_.

    We can solve this equation by a similar approach to the exponential model, using integration.

    $$ N(t) = \frac{K}{1 - \left( 1 - \frac{K}{N(0)} \right) e^{-r t} } $$
    """)
    return


@app.cell
def _(np):
    def logistic(t, N0, r, K):
        return K / (1 - (1 - K/N0) * np.exp(-r * t))

    return (logistic,)


@app.cell
def _(logistic, np, plt, sns):
    N0_1 = 100
    r_1 = 1
    K = 100000000.0
    t_1 = np.linspace(0, 24, 500)
    N_1 = logistic(t_1, N0_1, r_1, K)
    plt.plot(t_1, N_1)
    plt.xlabel('Time (hr)')
    plt.ylabel('Population size (cells)')
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use sliders to explore logistic-growth parameters:
    """)
    return


@app.cell
def _(mo):
    N0_ui = mo.ui.slider(1, 10000, 1, value=100, show_value=True, label="N0")
    r_ui = mo.ui.slider(0.1, 3.0, 0.1, value=1.0, show_value=True, label="r")
    K_ui = mo.ui.slider(1000, 1000000, 1000, value=100000, show_value=True, label="K")
    tmax_ui = mo.ui.slider(1, 72, 1, value=24, show_value=True, label="tmax")

    controls = mo.hstack([N0_ui, r_ui, K_ui, tmax_ui], justify="start", gap=1.0),
    controls
    return K_ui, N0_ui, r_ui, tmax_ui


@app.cell
def _(K_ui, N0_ui, logistic, np, plt, r_ui, sns, tmax_ui):
    t_ui = np.linspace(0, tmax_ui.value, 500)
    N_ui = logistic(t_ui, N0_ui.value, r_ui.value, K_ui.value)
    plt.plot(t_ui, N_ui, label="N(t)")
    plt.xlabel("Time (hr)")
    plt.ylabel("Population size (cells)")
    plt.legend()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can examine how different parameter values interact:
    """)
    return


@app.cell
def _(logistic, np, plt, sns):
    N0_2 = 100
    t_2 = np.linspace(0, 24, 500)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    for r_2 in [1, 2, 10]:
        for j, K_1 in enumerate([1000000.0, 100000000.0, 10000000000.0]):
            N_2 = logistic(t_2, N0_2, r_2, K_1)
            axes[j].plot(t_2, N_2, label='r={}'.format(r_2))
            axes[j].set_title('K={:.0e}'.format(K_1))
    axes[1].set_xlabel('Time (hr)')
    axes[0].set_ylabel('Population size (cells)')
    axes[2].legend(bbox_to_anchor=(1, 0.9))
    fig.tight_layout()
    sns.despine()
    fig
    return N0_2, t_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's look again at the logistic ODE:

    $$ \frac{dN}{dt} = r N \left(1-\frac{N}{K}\right) = rN - r \frac{N^2}{K} $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can see that $dN/dt$ will reach its minimum zero when $N=0$ and when $N=K$.

    To find its maximum, let's take a derivative with respect to $N$ and solve for zero:

    $$ \frac{d^2N}{dtdN} = r - 2r\frac{N}{K} = 0 $$

    $$ N = \frac{K}{2} $$

    So the maximum of the derivative $dN/dt$ will be reached exactly when $N=K/2$; at this point, growth will stop accelerating and begin to deccelerate until it halts at $N=K$.
    The maximum derivative will be $r K/4$ (just substitue $N=K/2$).
    """)
    return


@app.cell
def _(N0_2, logistic, plt, t_2):
    r_3 = 1
    K_2 = 1000000.0
    N_3 = logistic(t_2, N0_2, r_3, K_2)
    plt.plot(t_2, N_3)
    plt.axhline(N0_2, color='k', ls='--')
    plt.axhline(K_2 / 2, color='k', ls='--')
    plt.axhline(K_2, color='k', ls='--')
    plt.xlabel('Time (hr)')
    plt.ylabel('Population size (cells)')
    plt.gcf()
    return K_2, N_3, r_3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When will $N$ reach $K/2$?
    We can check this in the solution to the ODE:

    $$ N(t) = \frac{K}{1 - \left( 1 - \frac{K}{N(0)} \right) e^{-r t} } = K/2 $$

    $$ \frac{1}{1 - \left( 1 - \frac{K}{N(0)} \right) e^{-r t} } = 1/2 $$

    $$ 1 - \left( 1 - \frac{K}{N(0)} \right) e^{-r t}  = 2 $$

    $$ \left( 1 - \frac{K}{N(0)} \right) e^{-r t}  = -1 $$

    $$ 1 - \frac{K}{N(0)}   = -e^{r t} $$

    $$ \frac{K-N(0)}{N(0)}  = e^{r t} $$

    $$ \log{\frac{K-N(0)}{N(0)}}  = r t $$

    $$ \frac{\log{\left(K-N(0)\right)} - \log{\left(N(0)\right)}}{r}  = t $$
    """)
    return


@app.cell
def _(K_2, N0_2, N_3, np, plt, r_3, t_2):
    plt.plot(t_2, r_3 * N_3 * (1 - N_3 / K_2))
    plt.axvline((np.log(K_2 - N0_2) - np.log(N0_2)) / r_3, color='k', ls='--')
    plt.axhline(r_3 * K_2 / 4, color='k', ls='--')
    plt.xlabel('Time (hr)')
    plt.ylabel('dN/dt')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That seems a bit too nice--why should the maximum of the population growth rate $dN/dt$ be reached exactly half way to the maximum yeild, $K$?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Generalized logistic model

    The [generalized logistic model](https://en.wikipedia.org/wiki/Generalised_logistic_function) (also called the [Richards model](https://doi.org/10.1093/jxb/10.2.290)) has an additional parameter $\nu$ so that the curve doesn't have to be symmetric, that is, the time to get to $K/2$ can be longer/shorter than the time to get from $K/2$ to $K$.

    $$ \frac{d N}{d t}= r N \left(1 - \left(\frac{N}{K}\right)^{\nu}\right) $$

    The other parameters are the same as the logistic model.

    This model can also be solved:

    $$ N(t) = \frac{K}{\left(1 - \left( 1 - \left(\frac{K}{N(0)}\right)^{\nu} \right) e^{-r \nu t} \right)^{1/\nu}} $$
    """)
    return


@app.cell
def _(np):
    def generalized_logistic(t, N0, r, K, ν):
        return K / (1 - (1 - (K/N0)**ν) * np.exp(-r * ν * t))**(1/ν)

    return (generalized_logistic,)


@app.cell
def _(N0_2, generalized_logistic, logistic, plt, t_2):
    r_4 = 1
    K_3 = 1000000.0
    for ν in [0.1, 1, 10]:
        N_4 = generalized_logistic(t_2, N0_2, r_4, K_3, ν)
        plt.plot(t_2, N_4, ls='-', label='ν={}'.format(ν))
    N_4 = logistic(t_2, N0_2, r_4, K_3)
    plt.plot(t_2, N_4, lw=2, ls='--', color='k', label='logistic')
    plt.legend()
    plt.xlabel('Time (hr)')
    plt.ylabel('Population size (cells)')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # References

    - [Blog post](https://paulromer.net/economic-growth/) by Paul Romer on population and GDP growth
    - Appendices of [Ram et al. 2019](https://doi.org/10.1073/pnas.1902217116) shows how to derive and solve the logistic and generalized logistic.
    - [Hilau et al. 2022](https://doi.org/10.1371/journal.pcbi.1010565) talks about density-dependent effects as the main determinants of variation in bacterial growth dynamics.
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
