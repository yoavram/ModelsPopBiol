import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import numba 
    import seaborn as sns
    import pandas as pd
    from scipy.integrate import solve_ivp
    import scipy.optimize

    import warnings
    warnings.simplefilter('ignore', FutureWarning)
    from numba import NumbaDeprecationWarning
    warnings.simplefilter('ignore', NumbaDeprecationWarning)

    red, blue, green = sns.color_palette('Set1', 3)
    return blue, mo, np, numba, plt, red, scipy, solve_ivp


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bayesian inference in non-linear dynamic models

    ## [Models in Population Biology](http://modelspopbiol.yoavram.com)
    ## Yoav Ram
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The analysis follows an example from the [PyMC docs](https://www.pymc.io/projects/examples/en/latest/ode_models/ODE_Lotka_Volterra_multiple_ways.html#pymc-model-specification-for-gradient-free-bayesian-inference).

    # Predator-prey data

    Here's data from a real predator-prey system -- the hare and lynx system, see for example:
    > Krebs, Boonstra, Boutin, Sinclair (2006). [What drives the 10-year cycle of snowshoe hares?](https://www.bio.fsu.edu/~james/krebs.pdf) _BioScience_

    > Deng (2018). [An Inverse Problem: Trappers Drove Hares to Eat Lynx.](https://doi.org/10.1007/s10441-018-9333-z) _Acta Biotheoretica_
    """)
    return


@app.cell
def _(np):
    t = np.arange(1900., 1921., 1)
    lynx = np.array([4.0, 6.1, 9.8, 35.2, 59.4, 41.7, 19.0, 13.0, 8.3, 9.1, 7.4,
                8.0, 12.3, 19.5, 45.7, 51.1, 29.7, 15.8, 9.7, 10.1, 8.6])
    hare = np.array([30.0, 47.2, 70.2, 77.4, 36.3, 20.6, 18.1, 21.4, 22.0, 25.4, 
                 27.1, 40.3, 57.0, 76.6, 52.3, 19.5, 11.2, 7.6, 14.6, 16.2, 24.7])
    xy = np.array([hare, lynx])
    return hare, lynx, t, xy


@app.cell
def _(blue, hare, lynx, plt, red, t):
    def plot_setup():
        plt.plot(t, hare, 'o--', color=red)
        plt.plot(t, lynx, 'o--', color=blue)
        plt.xlabel('Year')
        plt.ylabel('# Pelts (thousands)')
        plt.legend(['Hare', 'Lynx'])
        plt.ylim(0, None)
        plt.xticks([1900, 1905, 1910, 1915, 1920])
        plt.show()
    
    plot_setup()
    return (plot_setup,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see the cycles that we discussed in the predator-prey class.

    # Predator-prey model

    This is the same model we used earlier in the course.
    I use [Numba]() JIT-compile the functions to improve running time, as we will run these functions many many times.
    """)
    return


@app.cell
def _(np, numba, solve_ivp, t):
    @numba.njit
    def _ode(t, xy, b, h, ε, d):
        x, y = xy
        dx = b * x - h * x * y
        dy = ε * h * x * y - d * y
        return [dx, dy]

    # some ODE solvers need the jacobian, but we don't use Nelder-Mead
    # @njit
    # def jac(t, xy, b, h, ϵ, d):
    #     x, y = xy
    #     return [
    #         [b - h * y, -h * x],
    #         [ϵ * h * y, ϵ * h * x - d]
    #     ]
    def predator_prey_model(θ, t=t):
        θ = np.maximum(θ, 0)
        sol = solve_ivp(_ode, (t.min(), t.max()), θ[-2:], t_eval=t, args=θ[:-2])  # parameters cannot be negative
        return np.array([sol.y[0], sol.y[1]])  # assert sol.success, θ

    return (predator_prey_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's plot some guess for the model parameters and the data. I played a bit with the parameters to get something that looks close enough. You can play with them further.
    """)
    return


@app.cell
def _(blue, np, plot_setup, plt, predator_prey_model, red):
    θ_guess = np.array([0.5, 0.02, 1.2, 1.0, 30.0, 5.0])
    trange = np.arange(1900, 1921, 0.01)
    xhat_guess, yhat_guess = predator_prey_model(θ_guess, trange)
    plt.plot(trange, xhat_guess, color=red)
    plt.plot(trange, yhat_guess, color=blue)
    plot_setup()
    return trange, θ_guess


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Maximum likelihood estimation

    We first assume that observed values are normally distributed around the expected values, which are given by the solution of the ODE.

    Maximizing the log likelihood of the normal distribution reduces down to minimizing the sum of residual squares, so we define a loss function that computes the predicted $x$ and $y$ and then computes the residual mean squares.
    Since we don't have gradeints of the loss with respect to the model paramters $\theta$, we use a minimization algorithm that does not require gradients: the [Nelder-Mead method](https://en.wikipedia.org/wiki/Nelder–Mead_method).
    """)
    return


@app.cell
def _(np, predator_prey_model, scipy, t, xy, θ_guess):
    def loss(θ, t, xy):
        xyhat = predator_prey_model(θ, t)
        return np.mean((xyhat - xy)**2)

    _sol = scipy.optimize.minimize(loss, θ_guess, args=(t, xy), method='Nelder-Mead')
    θ_mle = _sol.x
    print(_sol.message)
    print('loss={:.4f}\nb = {:.4f}\nh = {:.4f}\nϵ = {:.4f}\nd = {:.4f}\nx0 = {:.2f}\ny0 = {:.4f}'.format(_sol.fun, *θ_mle))
    return loss, θ_mle


@app.cell
def _(predator_prey_model, t, xy, θ_mle):
    print(xy)
    print('-'*80)
    xyhat = predator_prey_model(θ_mle, t)
    print(xyhat)
    print('-'*80)
    return


@app.cell
def _(blue, plot_setup, plt, predator_prey_model, red, trange, θ_mle):
    xhat, yhat = predator_prey_model(θ_mle, trange)
    plt.plot(trange, xhat, color=red)
    plt.plot(trange, yhat, color=blue)
    plot_setup();
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This looks pretty good.

    In the following we test the sensitivity of this approach to the guess - it is not sensitive, so that's good!
    """)
    return


@app.cell
def _(loss, np, scipy, t, xy):
    θ_guesses = np.random.uniform(0, 40, size=(10, 6))
    assert (θ_guesses > 0).all()
    for θ_ in θ_guesses:
        _sol = scipy.optimize.minimize(loss, θ_, args=(t, xy), method='Nelder-Mead')
        if not _sol.success:
            print(_sol.message)
        θ_mle_ = _sol.x
        print('loss={:.3f}, b={:.3f}, h={:.3f}, ϵ={:.3f}, d={:.3f}, x0={:.3f}, y0={:.3f}'.format(_sol.fun, *θ_mle_))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Another method that does use the gradients is illustrated at the bottom of the notebook. It uses a more sophisticated approach based on an ODE solver that can compute gradients of the solution with respect to the parameters, and an efficient gradient-descent solver called ADAM.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bayesian inference

    Next, we apply Bayesian inference to the problem using [PyMC](https://pymc.io).
    """)
    return


@app.cell
def _():
    import pytensor
    pytensor.config.linker = 'py' # to avoid error in vs code
    import pymc as pm
    import arviz as az

    import pytensor.tensor as pt
    from pytensor.compile.ops import as_op

    return as_op, az, pm, pt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We need to wrap our ODE model function `predator_prey_model` to a [`pytensor`](http://pytensor.readthedocs.io) function, because `pytensor` is the computational backend of PyMC (since v5), rather than NumPy. This is easily done by the following cell, which just defines the input and output types of the model function: `dvector` and `dmatrix` are a vector and a matrix of doubles, respectively.
    """)
    return


@app.cell
def _(as_op, predator_prey_model, pt):
    @as_op(itypes=[pt.dvector], otypes=[pt.dmatrix])
    def predator_prey_model_op(θ):
        return predator_prey_model(θ)

    return (predator_prey_model_op,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The priors are defined as truncated normal distributions around the MLE; the truncation at zero avoids negative values for the parameters.

    We set the distribution of the observations as Poisson around the expected value, as this is more reasonable than assuming a normal distribution.

    We then sample from the posterior. I used the `Slice` sampler, which does not require gradients of the log-likelihood with respect to the model parameters (we could [do it with gradients](https://www.pymc.io/projects/examples/en/latest/ode_models/ODE_with_manual_gradients.html), but it will complicate the code).
    Each chain took me about 15 mins to run on my laptop. You can [try another sampler if you want](https://www.pymc.io/projects/examples/en/latest/ode_models/ODE_Lotka_Volterra_multiple_ways.html#pymc-model-specification-for-gradient-free-bayesian-inference).
    """)
    return


@app.cell
def _(pm, predator_prey_model_op, xy, θ_mle):
    with pm.Model() as model:   
        b_mle, h_mle, ϵ_mle, d_mle, x0_mle, y0_mle = θ_mle
        b = pm.TruncatedNormal("b", mu=b_mle, sigma=0.1, lower=0, initval=b_mle)
        h = pm.TruncatedNormal("h", mu=h_mle, sigma=0.01, lower=0, initval=h_mle)
        ϵ = pm.TruncatedNormal("ϵ", mu=ϵ_mle, sigma=0.1, lower=0, initval=ϵ_mle)
        d = pm.TruncatedNormal("d", mu=d_mle, sigma=0.01, lower=0, initval=d_mle)
        x0 = pm.TruncatedNormal("x0", mu=x0_mle, sigma=1, lower=0, initval=x0_mle)
        y0 = pm.TruncatedNormal("y0", mu=y0_mle, sigma=1, lower=0, initval=y0_mle)

        ode_solution = predator_prey_model_op(pm.math.stack([b, h, ϵ, d, x0, y0]))
        XY_obs = pm.Poisson("XY_obs", mu=ode_solution, observed=xy)
    return (model,)


@app.cell
def _(az, model, pm):
    with model:
        idata = pm.sample(step=[pm.Slice()], draws=2000, cores=1)
    az.summary(idata)
    return (idata,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following saves and then loads the inference data to and from a file, so that we can continue working on it at a later time.
    """)
    return


@app.cell
def _(idata):
    idata.to_netcdf("idata_hare_lynx.nc")
    return


@app.cell
def _(az):
    idata_1 = az.from_netcdf('idata_hare_lynx.nc')
    return (idata_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next we plot the traces and the marginal posteriors of the two chains to assess for convergence.
    """)
    return


@app.cell
def _(az, idata_1, plt):
    az.plot_trace(idata_1)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It seems that the chains have converged, so we can go ahead and look at the summary of the inference.

    Not the `r_hat` and `ess` are measures for convergence and stability, respectively, read more at [Kruschke (2021) Bayesian Analysis Reporting Guidelines. _Nature Human Behaviour_](https://doi.org/10.1038/s41562-021-01177-7).
    """)
    return


@app.cell
def _(az, idata_1):
    isummary = az.summary(idata_1, round_to=4)
    isummary
    return (isummary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, let's plot predictive plots to check if the estimated parameters can indeed reproduce the dynamics we observe in the data.

    Here, I plot the data as circles, the dynamics using the MAP estimate as black lines, and the dynamics using 100 samples from the posterior as colored transparent lines.
    """)
    return


@app.cell
def _(
    az,
    blue,
    hare,
    idata_1,
    isummary,
    lynx,
    np,
    plot_setup,
    plt,
    predator_prey_model,
    red,
    t,
):
    # plot data
    plt.plot(t, hare, 'o', color=red)
    plt.plot(t, lynx, 'o', color=blue)
    θ_map = isummary['mean'].values
    # plot MAP prediction
    x, y = predator_prey_model(θ_map, t)
    plt.plot(t, x, color='k', lw=3)
    plt.plot(t, y, color='k', lw=3)
    posterior_samples = az.extract(idata_1, num_samples=100).to_dataframe()
    for idx, row in posterior_samples.iterrows():
    # plot posterior predictions 
        θi = row[['b', 'h', 'ϵ', 'd', 'x0', 'y0']].values
        x, y = predator_prey_model(θi, t)
        x = np.random.poisson(x)  # add Poisson noise to the predictions
        y = np.random.poisson(y)  # add Poisson noise to the predictions
        plt.plot(t, x, color=red, alpha=0.05)
        plt.plot(t, y, color=blue, alpha=0.05)
    plot_setup()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This seems pretty good, although some of the highest points in the data (both for hare and lynx) seem to be quite extreme compared to the posterior predictions.

    Next let's look at the joint posterior distribution using a pair plot.
    """)
    return


@app.cell
def _(az, idata_1):
    az.plot_pair(idata_1, kind='kde', figsize=(8, 8), marginals=True, point_estimate='mean')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here we see that the only parameters that seem strongly correlated are $h$ and $\epsilon$, which makes sense, as they appear as a product in the model. Perhaps we should redefine the model with a new parameter $\xi = \epsilon h$. Otherwise the distributions look nice and round.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # MLE using JAX

    [JAX](https://jax.readthedocs.io) is a high-performance array computing library.
    it combines:
    - [Autograd](https://github.com/hips/autograd) for automatic differentiation: automatic computation of gradient functions.
    - [XLA](https://www.tensorflow.org/xla) (Accelerated Linear Algebra), a domain-specific compiler for linear algebra that can accelerate machine learning code.
    It provides a NumPy-like interface so it's easy to learn.
    The major difference is in random number generation, but that's not a concern here.

    Amazingly, JAX has an ODE solver that can be differentiated, that is, given an ODE $$\frac{dy}{dt}=F(y,t,\theta)$$ the solver computes $$\left(y, \frac{dy}{d\theta}\right)= \text{ODESolver}(F, y_0, \theta)$$
    """)
    return


@app.cell
def _():
    import numpy.random as npr
    import jax.numpy as jnp
    from jax import jit, grad
    from jax.experimental.ode import odeint

    return grad, jit, jnp, odeint


@app.cell
def _(jit, jnp, odeint):
    @jit
    def _ode(xy, t, b, h, ε, d):
        x, y = xy
        dx = b * x - h * x * y
        dy = ε * h * x * y - d * y
        return jnp.array([dx, dy])

    @jit
    def predator_prey_model_1(θ, t):
        θ = jnp.maximum(θ, 0)
        xy = odeint(_ode, θ[-2:], t, *θ[:-2]).T
        return xy

    return (predator_prey_model_1,)


@app.cell
def _(blue, hare, jnp, lynx, plot_setup, plt, predator_prey_model_1, red, t):
    t_1 = jnp.array(t)
    xy_1 = jnp.array([hare, lynx])
    θ_guess_1 = jnp.array([0.5, 0.02, 1.2, 1, 30, 5])
    trange_1 = jnp.arange(1900, 1921, 0.01)
    xhat_1, yhat_1 = predator_prey_model_1(θ_guess_1, trange_1)
    plt.plot(trange_1, xhat_1, color=red)
    plt.plot(trange_1, yhat_1, color=blue)
    plot_setup()
    return t_1, xy_1, θ_guess_1


@app.cell
def _(jit, jnp, predator_prey_model_1):
    @jit
    def loss_1(θ, t, xy):
        xyhat = predator_prey_model_1(θ, t)
        return jnp.mean((xyhat - xy) ** 2)

    return (loss_1,)


@app.cell
def _(loss_1, t_1, xy_1, θ_guess_1):
    print('Loss at i=0:', loss_1(θ_guess_1, t_1, xy_1))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We now use the ADAM optimizer, implemented in [Optax](https://github.com/deepmind/optax/blob/master/examples/quick_start.ipynb), a JAX optimizers library.
    ADAM is a very efficient and generic gradient descent optimizer, used commonly in many deep learning:
    > <div class="csl-entry">Kingma, D. P., &#38; Ba, J. L. (2015). Adam: A method for stochastic optimization. <i>3rd International Conference on Learning Representations, ICLR 2015 - Conference Track Proceedings</i>, 1–15.</div>
    """)
    return


@app.cell
def _():
    import optax

    return (optax,)


@app.cell
def _(grad, loss_1, optax, t_1, xy_1, θ_guess_1):
    optimizer = optax.adam(0.01)
    opt_state = optimizer.init(θ_guess_1)
    grad_loss = grad(loss_1)
    grad_loss(θ_guess_1, t_1, xy_1)
    return grad_loss, opt_state, optimizer


@app.cell
def _(grad_loss, loss_1, opt_state, optax, optimizer, t_1, xy_1, θ_guess_1):
    θ_hat = θ_guess_1.copy()
    for i in range(1500):
        grads = grad_loss(θ_hat, t_1, xy_1)
        Δθ, opt_state_1 = optimizer.update(grads, opt_state, θ_hat)
        θ_hat = optax.apply_updates(θ_hat, Δθ)
        if i % 100 == 0:
            print('Loss at i={}: {}'.format(i, loss_1(θ_hat, t_1, xy_1)))
    return (θ_hat,)


@app.cell
def _(isummary, θ_hat):
    for param, pymc_val, jax_val in zip(isummary.index, isummary['mean'], θ_hat.tolist()):
        print("{}\t{:.4f}\t{:.4f}".format(param, pymc_val, jax_val))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can see that our JAX-based approach works very well and finds a point estimate that is similar to that of the Bayesian approach.
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
