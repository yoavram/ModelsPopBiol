import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Continuous-time multivariate deterministic model: Predator-prey model

    ## [Models in Population Biology](http://scicompy.yoavram.com)
    ## Yoav Ram
    """)
    return


@app.cell
def _():
    import marimo as mo
    from functools import partial
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_context('talk')
    sns.set_palette('muted')

    import scipy
    from scipy.integrate import solve_ivp

    return mo, np, partial, plt, scipy, sns, solve_ivp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The [Lotka-Volterra model](https://en.wikipedia.org/wiki/Lotka–Volterra_equations) is a model of species interactions, which can consist of competition, cooperation, or other types of interactions.
    It is commonly reffered to as a _predator-prey_ model, which is what we will focus on today.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Predator-prey model

    ![lynx and hare](http://1.bp.blogspot.com/-ukeoZMEmIkM/VP7psdQO-vI/AAAAAAAACkE/9Togukgl4Yk/s1600/bobby.jpg)
    ![lion and gnu](http://www.differencebetween.info/sites/default/files/images/5/prdators.jpg)
    ![owl and mouse](https://i.ytimg.com/vi/7s0mpZ18Zaw/hqdefault.jpg)


    The predator-prey model is summarized by these ordinary differential equations (ODE):

    $$ \frac{dx}{dt} = b x - h x y $$

    $$ \frac{dy}{dt} = \epsilon h x y - d y $$

    where the parameters are:
    - $x$ is the density of the *prey* (hare, gnu, mouse)
    - $y$ is the density of the *predator* (lynx, lion, owl)
    - $b$ is the *prey* birth rate
    - $d$ is the *predator* death rate
    - $h$ is the rate at which, when *predator* and *prey* meet, predation occurs
    - $\epsilon$ is the rate at which *prey* density is converted to *predator* density when predation occurs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Dynamics

    To implement the model we first write the ODE as a function:
    """)
    return


@app.cell
def _(np):
    def dxydt(t, xy, b, h, ε, d):
        x, y = xy
        dx = b * x - h * x * y
        dy = ε * h * x * y - d * y
        return np.array([dx, dy])

    return (dxydt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Integration

    Now let's integrate the ODE.


    ### Simple integration

    First let's implement an integration method of our own by making a discrete linear approximation of the ODE:

    $$ x_{t} = x_{t-1} + \frac{d x}{d t} \cdot dt $$

    $$ y_{t} = y_{t-1} + \frac{d y}{d t} \cdot dt $$

    This is considered the simplest first-order integration method, called the [Euler method](https://en.wikipedia.org/wiki/Euler_method).
    """)
    return


@app.cell
def _(dxydt, np):
    # model parameters
    b = 1
    h = 0.005
    ε = 0.8
    d = 0.6

    steps = 100000 # number integration steps
    xy = np.empty((2, steps)) # population array
    xy[:,0] = 50, 100 # initial population sizes
    dt = 0.001 # time step for integration

    for t in range(1, steps):
        xy[:, t] = xy[:, t-1] + dxydt(t, xy[:, t-1], b, h, ε, d) * dt

    x = xy[0, :]
    y = xy[1, :]
    t = np.arange(0, dt * steps, dt)
    return b, d, h, t, x, y, ε


@app.cell
def _(plt, sns, t, x, y):
    plt.plot(t, x, alpha=0.75, label='prey')
    plt.plot(t, y, alpha=0.75, label='predator')

    plt.xlabel('Time')
    plt.ylabel('Population size')
    # bbox_to_anchor places the legend at specific position, in this case outside the plot
    plt.legend(bbox_to_anchor=(1, 0.75))
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see the cycles: more prey = more food for predators = more predators = less prey = less food for predators = less predators = more prey ...

    Another way to visualize the dynamics is *orbits* in phase space.
    """)
    return


@app.cell
def _(plt, sns, x, y):
    plt.plot(x, y, linewidth=0.2, color='k')
    plt.xlabel('Prey')
    plt.ylabel('Predator')
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Integration with SciPy

    We are better off using one of SciPy's [`solve_ivp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html) function, which automatically choses `dt` and `steps` to make sure `dx` and `dy` are small so that the linearization is effective.

    Note: `solve_inp` is relatievely new, the previous solver (which you can still use) is called `odeint`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some of the solvers require the Jacobian, or the matrix of 2nd order parital derivatives:

    $$ \mathbf{J}(x, y) = \\(b - h y, -h x),\\ (\epsilon h y, \epsilon h x - d) $$
    """)
    return


@app.cell
def _(np):
    def jac(t, xy, b, h, ε, d):
        x, y = xy
        return np.array([
            [b - h * y, -h * x],
            [ε * h * y, ε * h * x - d]
        ])

    return (jac,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We make a partial version of the `dxydt` and of `jac` which has the model parameters fixed, and use `solve_ivp` with the BDF solver (_backward differentiation formula_).

    We plot the dynamics plots.
    We also add quivers to the phase plot to anotate the direction of the dynamics.
    """)
    return


@app.cell
def _(b, d, dxydt, h, jac, np, partial, solve_ivp, ε):
    t_1 = np.linspace(0, 50, 50 * 10)
    xy0 = (50, 100)
    dxydt_ = partial(dxydt, b=b, h=h, ε=ε, d=d)
    jac_ = partial(jac, b=b, h=h, ε=ε, d=d)
    sol = solve_ivp(dxydt_, (t_1.min(), t_1.max()), xy0, t_eval=t_1, method='BDF', jac=jac_)
    return (sol,)


@app.cell
def _(plt, sns, sol):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    q_dt = 10

    axes[0].plot(sol.t, sol.y.T)
    axes[1].plot(sol.y[0,:], sol.y[1,:], lw=0.5, color='k')
    axes[1].quiver(sol.y[0,:-1:q_dt], sol.y[1,:-1:q_dt], 
                   sol.y[0,1::q_dt]-sol.y[0,:-1:q_dt], 
                   sol.y[1,1::q_dt]-sol.y[1,:-1:q_dt], 
                   scale_units='xy', angles='xy', scale=1, width=0.005)

    axes[0].set(xlabel='Time', ylabel='Population size', ylim=(0, None))
    axes[1].set(xlabel='Prey', ylabel='Predator', xlim=(0, None))
    axes[0].legend(['Prey', 'Predator'], loc=1)

    fig.tight_layout()
    sns.despine()
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note**: this is an example where the `method` of the ODE solver is important - change the method and you don't get a cycle due to numerical errors.

    The plots look similar, except that maybe the phase plot is more tight.
    We immediately see that we have a cycle, which seems stable!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's wrap this in a function that also plots the dynamics so that we can easily reuse it later.
    """)
    return


@app.cell
def _(dxydt, jac, np, partial, plt, sns, solve_ivp):
    def solve_plot(
        x0,
        y0,
        tmax,
        b,
        h,
        ε,
        d,
        q_dt=10,
        return_value=True,
        method="BDF",
        rtol=1e-6,
        atol=1e-9,
    ):
        t = np.linspace(0, tmax, tmax*10)
        xy0 = (x0, y0)
        dxydt_ = partial(dxydt, b=b, h=h, ε=ε, d=d)
        jac_ = partial(jac, b=b, h=h, ε=ε, d=d)
        solver_kwargs = {"t_eval": t, "method": method, "rtol": rtol, "atol": atol}
        if method in {"BDF", "Radau"}:
            solver_kwargs["jac"] = jac_
        sol = solve_ivp(dxydt_, (t.min(), t.max()), xy0, **solver_kwargs)

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        axes[0].plot(sol.t, sol.y.T)
        axes[1].plot(sol.y[0,:], sol.y[1,:], lw=0.5, color='k')
        axes[1].quiver(sol.y[0,:-1:q_dt], sol.y[1,:-1:q_dt], 
                       sol.y[0,1::q_dt]-sol.y[0,:-1:q_dt], 
                       sol.y[1,1::q_dt]-sol.y[1,:-1:q_dt], 
                       scale_units='xy', angles='xy', scale=1, width=0.005)

        axes[0].set(xlabel='Time', ylabel='Population size', ylim=(0, None))
        axes[1].set(xlabel='Prey', ylabel='Predator')
        axes[0].legend(['Prey', 'Predator'])
        fig.tight_layout()
        sns.despine()
        if return_value:
            return sol.t, sol.y

    return (solve_plot,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can explore the dynamics for different values with marimo sliders.
    """)
    return


@app.cell
def _(mo):
    x0_ui = mo.ui.slider(1, 100, 1, value=50, show_value=True, label="x0")
    y0_ui = mo.ui.slider(1, 100, 1, value=100, show_value=True, label="y0")
    tmax_ui = mo.ui.slider(1, 1001, 10, value=100, show_value=True, label="tmax")
    b_ui = mo.ui.slider(0, 2, 0.1, value=1.0, show_value=True, label="b")
    h_ui = mo.ui.slider(0, 0.1, 0.001, value=0.005, show_value=True, label="h")
    ε_ui = mo.ui.slider(0, 1, 0.01, value=0.8, show_value=True, label="ε")
    d_ui = mo.ui.slider(0, 2, 0.1, value=0.6, show_value=True, label="d")
    method_ui = mo.ui.dropdown(["BDF", "Radau", "RK45"], value="BDF", label="method")
    rtol_exp_ui = mo.ui.slider(3, 10, 1, value=6, show_value=True, label="rtol: 1e-")
    atol_exp_ui = mo.ui.slider(6, 14, 1, value=9, show_value=True, label="atol: 1e-")

    controls = mo.vstack(
        [
            mo.hstack([x0_ui, y0_ui, tmax_ui], justify="start", gap=1.0),
            mo.hstack([b_ui, h_ui, ε_ui, d_ui], justify="start", gap=1.0),
            mo.hstack([method_ui, rtol_exp_ui, atol_exp_ui], justify="start", gap=1.0),
        ],
        gap=0.5,
    )
    controls
    return atol_exp_ui, b_ui, d_ui, h_ui, method_ui, rtol_exp_ui, tmax_ui, x0_ui, y0_ui, ε_ui


@app.cell
def _(
    atol_exp_ui,
    b_ui,
    d_ui,
    h_ui,
    method_ui,
    plt,
    rtol_exp_ui,
    solve_plot,
    tmax_ui,
    x0_ui,
    y0_ui,
    ε_ui,
):
    rtol = 10.0 ** (-rtol_exp_ui.value)
    atol = 10.0 ** (-atol_exp_ui.value)
    solve_plot(
        x0=x0_ui.value,
        y0=y0_ui.value,
        tmax=tmax_ui.value,
        b=b_ui.value,
        h=h_ui.value,
        ε=ε_ui.value,
        d=d_ui.value,
        method=method_ui.value,
        rtol=rtol,
        atol=atol,
    )
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Equilibrium

    Equilibriums, i.e. steady states or fixed points, are a very important concept in dynamic models.

    Population equilibrium occurs in the model when neither of the populations change, that is, when both of the derivatives are equal to 0:

    $$ bx - hxy = 0 $$

    $$ \epsilon h x y - d y = 0 $$

    $$ x (b - hy) = 0 $$

    $$ y (\epsilon h x - d) = 0 $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The trivial solutions have $x=0$ and/or $y=0$.
    Assuming both are positive,

    $$ x^* = \frac{d}{\epsilon h} $$

    $$ y^* = \frac{b}{h} $$

    - Equilibrium predator density $y^*$ is defined by the ratio of prey birth rate and predation rate.
    - Equilibrium prey density $x^*$ is defined by the ratio of predator death rate and prey-predator conversion rate.

    Interestingly, if something causes predator death $d$ it will increase the density of prey, but not the predator, as the increase of prey density will balance the deaths of the predator.
    Similarly, if something increases the birth rate of the prey $b$, the prey density will not increase - rather, the predator density will increase as nothing balances it.

    Also, the predator equilibrium is not affected by $\epsilon$ the efficiency of converting predator to prey. The more prey is needed to make a predator (think relative masses of predator and prey) the lower the equilibrium rate of the *prey*.

    Perhaps more surprisingly, the higher the predation rate $h$, we have less of both the predator and the prey - the prey population size will decreaes, obviously, but the predator population size will also decrease.
    This presents an interesting "dillema": a highly skilled predator individual will enjoy the benefit of more prey, but will ultimately cause the predator population to decrease in density, unless balanced by increased birth of prey $b$ or increase in prey evasion (which will lower $h$).

    Let's verify our equilibrium solution:
    """)
    return


@app.cell
def _(b, d, dxydt, h, ε):
    xystar = d/(ε*h), b/h
    print(xystar)
    xstar, ystar = xystar
    print(dxydt(0, xystar, b=b, h=h, ε=ε, d=d))
    return xstar, xystar, ystar


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now plot the equilibrium (a _divide by zero_ warning may occur):
    """)
    return


@app.cell
def _(b, d, h, np, plt, solve_plot, xstar, xystar, ystar, ε):
    t_2, xy_1 = solve_plot(x0=xstar, y0=ystar, tmax=100, b=b, h=h, ε=ε, d=d)
    assert np.allclose(xy_1[0, :], xystar[0])
    assert np.allclose(xy_1[1, :], xystar[1])
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Local stability

    Stability is another important concept in dynamic modelling.
    We want to know if an equilibrium is locally stable: that is, if we perturbe the system (e.g. nudge it a bit)\, will the system return to the equilibrium?

    ![stability](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn-images-1.medium.com%2Fmax%2F1600%2F0*df4enmd42HaD5Hdl.jpg&f=1&nofb=1)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We concentrate on small perturbations, that is, the concept of **local stability** (see [notebook on stability analysis](stability.py) or ch. 8 in Otto and Day 2007).

    Let's perturbe the equilibrium and check what the values of the ODE are.
    """)
    return


@app.cell
def _(mo):
    perturb_pct_ui = mo.ui.slider(
        0.1, 20.0, 0.1, value=1.0, show_value=True, label="perturbation (%)"
    )
    direction_ui = mo.ui.dropdown(
        [
            "both up",
            "both down",
            "prey up / predator down",
            "prey down / predator up",
        ],
        value="both up",
        label="direction",
    )
    perturb_controls = mo.hstack([perturb_pct_ui, direction_ui], justify="start", gap=1.0)
    perturb_controls
    return direction_ui, perturb_pct_ui


@app.cell
def _(b, d, direction_ui, dxydt, h, perturb_pct_ui, xstar, ystar, ε):
    direction_to_sign = {
        "both up": (1, 1),
        "both down": (-1, -1),
        "prey up / predator down": (1, -1),
        "prey down / predator up": (-1, 1),
    }
    sign_x, sign_y = direction_to_sign[direction_ui.value]
    delta = perturb_pct_ui.value / 100.0
    xypert = xstar * (1 + sign_x * delta), ystar * (1 + sign_y * delta)
    print("perturbation:", direction_ui.value, f"{perturb_pct_ui.value:.1f}%")
    print(xypert)
    print(dxydt(0, xypert, b=b, h=h, ε=ε, d=d))
    return (xypert,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For this perturbation, inspect $\frac{dx}{dt}$ and $\frac{dy}{dt}$ above to see the immediate direction of change.
    """)
    return


@app.cell
def _(b, d, h, plt, solve_plot, xypert, xystar, ε):
    t_3, xy_2 = solve_plot(*xypert, tmax=100, b=b, h=h, ε=ε, d=d)
    plt.plot(*xystar, 'or')
    plt.gcf()
    return (xy_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So we see that the initial equilibirum point (right: time zero; left: red circle) is **unstable**: it "swirls" outwards, but is seems to "swirl" towards some limit cycle; it seems to converge to an orbit.

    Let's continue the dynamics from where we stopped it.
    """)
    return


@app.cell
def _(b, d, h, plt, solve_plot, xy_2, xystar, ε):
    solve_plot(*xy_2[:, -1], tmax=1500, b=b, h=h, ε=ε, d=d)
    plt.plot(*xystar, 'or')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Stability analysis

    We can generalize this observation of a non-stable equilibrium with local stability analysis, by computing the linearization of the (non-linear) model near the equilibrium, and then analyzing the linear system.

    This linearization is given by the the Jacobian at the equiblirum $(x^*, y^*)$.

    **The equilibrium is stable if all eigenvalues of the linear system have negative real parts.** (see [notebook on stability analysis](stability.ipynb) or ch. 8 in Otto and Day 2007).

    For more details see references at the bottom of the page.
    """)
    return


@app.cell
def _(b, d, h, jac, xystar, ε):
    J = jac(0, xystar, b, h, ε, d) # the first argument is time, which doesn't matter in this system
    print(J)
    return (J,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can find the eigenvalues using SciPy:
    """)
    return


@app.cell
def _(J, scipy):
    _eigs = scipy.linalg.eigvals(J)
    print('eigenvalues:', _eigs.real)
    print('real parts are negative:', _eigs.real < 0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The real parts of the eigenvalues are zero, so the equilibrium is unstable.

    Is this the case for any parameter combination?
    """)
    return


@app.cell
def _(jac, np, scipy):
    def is_stable(b, h, eps, d):
        xystar = (d / (eps * h), b / h)
        J = jac(0, xystar, b, h, eps, d)
        _eigs = scipy.linalg.eigvals(J)
        ρ = _eigs.real.max()
        return ρ < 0 and (not np.isclose(ρ, 0))

    return (is_stable,)


@app.cell
def _(is_stable, np):
    εs = np.linspace(1e-6, 1, 51)
    ds = np.linspace(0, 1, 50)

    ρs = [is_stable(2/3, 4/3, ε_, d) for ε_ in εs for d in ds]
    ρs = np.array(ρs).reshape(51, 50)
    return (ρs,)


@app.cell
def _(ρs):
    print('Unstable across range?', not ρs.any())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## SymPy

    Can we find an analytic solution for the stability question?

    Let's use SymPy, a Python package for symbolic mathematics.
    """)
    return


@app.cell
def _():
    import sympy
    sympy.init_printing()
    return (sympy,)


@app.cell
def _(sympy):
    x_, y_, b_, h_, ε_, d_ = sympy.symbols(r'x y b h \epsilon d')
    dxdt = b_ * x_ - h_ * x_ * y_
    dydt = ε_ * h_ * x_ * y_ - d_ * y_
    J_ = sympy.Matrix(
        [[sympy.diff(dxdt, x_), sympy.diff(dxdt, y_)], 
         [sympy.diff(dydt, x_), sympy.diff(dydt, y_)]])
    J_
    return J_, b_, d_, h_, x_, y_, ε_


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, the case of the trivial equilibrium $x=0, y=0$:
    """)
    return


@app.cell
def _(J_, x_, y_):
    J_.subs({x_: 0, y_: 0}).eigenvals()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first eigenvalue is equal to $b>0$, so extinctions are not stable to perturbations.
    This makes sense: if you add some prey, they will flourish in the absence of a predator.

    Second, the more interesting case, the Jacobian at the equilibrium.
    """)
    return


@app.cell
def _(J_, b_, d_, h_, x_, y_, ε_):
    eigs = J_.subs({x_: d_ / (ε_ * h_), y_: b_ / h_}).eigenvals()
    eigs
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since $b>0$ and $d>0$, then $bd>0$ and both eigenvalues are complex with a zero real part, so the equilibrium is "neutral".

    In a [two-equation system](https://en.wikipedia.org/wiki/Linear_dynamical_system#Classification_in_two_dimensions) we can learn more about the stability by looking at the product and sum of the eigenvalues, $\Delta=\lambda_1 \lambda_2 = -bd < 0$ and $\tau=\lambda_1 + \lambda_2=0$.

    So the equilibrium point is a _center_ of a stable cycle: there is a stable "orbit" around the fixed point, which was what we kindof suspected.
    """)
    return


@app.cell
def _(b, d, h, plt, solve_plot, ε):
    solve_plot(76, 211, tmax=100, b=b, h=h, ε=ε, d=d)
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stochastic effects

    The problem is that both prey and predator come very close to zero many times,  and therefore their populations will be subject to random extinctions, which cannot be reflected in a deterministic model.
    This is sometimes called the "atto-fox problem", an atto-fox being a notional $10^{−18}$ of a fox.

    If the prey goes extinct, so will the predator:
    """)
    return


@app.cell
def _(b, d, h, plt, solve_plot, ystar, ε):
    solve_plot(0, ystar, 10, b, h, ε, d);
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    and if the predator goes extinct, the prey population explodes:
    """)
    return


@app.cell
def _(b, d, h, plt, solve_plot, xstar, ε):
    solve_plot(xstar, 0, 10, b, h, ε, d);
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So clearly the model is not biologically reasonable - but it can still give us insight on species interactions.

    Furthermore, we will come back to this problem and use a stochastic model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Further reading

    - [Discussion of predation with some biological data](https://globalchange.umich.edu/globalchange1/current/lectures/predation/predation.html)
    - [Evolution towards oscillation or stability in a predator–prey system](http://rspb.royalsocietypublishing.org/content/277/1697/3163)
    - A Biologist's Guide to Mathematical Modeling in Ecology and Evolution by Otto and Day 2007 (available online via the [library](https://idc-primo.hosted.exlibrisgroup.com/primo-explore/fulldisplay?docid=972IDC_INST_ALMA2152572240003105&context=L&vid=972IDC_INST_V1&search_scope=IDC)):
     - Chapter 5 for equilibria and stability with one variable.
     - Chapter 7 for equilibria and stability with multiple variables.
     - Chapter 8 for equilibria and stability with multiple variables in non-linear models.
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
