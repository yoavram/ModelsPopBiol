import marimo

__generated_with = "0.23.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import os
    import urllib.request
    import zipfile
    from datetime import datetime
    from functools import partial
    from scipy.integrate import solve_ivp
    import scipy.optimize
    import scipy.stats
    return (
        datetime,
        mo,
        np,
        os,
        partial,
        pd,
        plt,
        scipy,
        sns,
        solve_ivp,
        urllib,
        zipfile,
    )


@app.cell
def _(sns):
    sns.set_palette('Set1')
    red, blue, green = sns.color_palette('Set1', 3) ###
    return blue, green, red


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Assignment 5: Statistical inference in dynamic models
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
    # Ex 1: Kleiber's law

    From [Wikipedia](https://en.wikipedia.org/wiki/Kleiber's_law):
    "Kleiber's law, named after Max Kleiber for his biology work in the early 1930s, is the observation that, for the vast majority of animals, an animal's metabolic rate scales to the 3⁄4 power of the animal's mass. Symbolically: if $q_0$ is the animal's metabolic rate, and $M$ is the animal's mass, then Kleiber's law states that

    $$ q_0 \sim M^{3/4}. $$

    Thus, over the same time span, a cat having a mass 100 times that of a mouse will consume only about 32 times the energy the mouse uses."

    The exact value of the exponent in Kleiber's law is unclear, in part because the law currently lacks a single theoretical explanation that is entirely satisfactory.

    Let's use the AnAge dataset to find the exponent and test Kleiber's law.
    """)
    return


@app.cell
def _(os, urllib):
    ###
    url = 'http://genomics.senescence.info/species/dataset.zip'
    fname = '../data/anage_dataset.zip'
    if not os.path.exists(fname):
        urllib.request.urlretrieve(url, fname)
    print("Data file exists:", os.path.exists(fname))
    return (fname,)


@app.cell
def _(fname, pd, zipfile):
    ###
    with zipfile.ZipFile(fname) as _z:
        _f = _z.open('anage_data.txt')
        data_raw = pd.read_table(_f)
    return (data_raw,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will focus on mammals, because they are the most common in this dataset and we don't want to mix classes of organisms.

    **Filter out everything but the mammals**.
    """)
    return


@app.cell
def _(data_raw):
    data = data_raw[data_raw['Class'] == 'Mammalia']
    data.head() ###
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Extract the relevant variables and plot the data**.
    We want the body mass in a variable `M` and the metabolic rate in a variable `Y`.
    Note:

    - some rows have NaN values for these variables so we should remove them.
    - because of the huge differences in body mass, we should use a log-log plot.
    """)
    return


@app.cell
def _(data, np):
    M = data['Body mass (g)'].values
    Y = data['Metabolic rate (W)'].values
    _idx = np.isfinite(M)
    M = M[_idx]
    Y = Y[_idx]
    return M, Y


@app.cell
def _(M, Y, plt):
    plt.plot(M, Y, '.')
    plt.xlabel('Body mass (g)')
    plt.ylabel('Metabolic rate (W)')
    plt.xscale('log')
    plt.yscale('log')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The model we want to fit here is

    $$ Y = Y_0 \cdot M ^ b $$

    which gives

    $$ \log Y = \log Y_0 + b \log M $$

    Let's start with a maximum likelihood estimate, which in this case means we can do a linear regression (unless you don't want to use a normal distribution for the residuals, which is fine).

    **Perform, plot and print the MLE estimation.**
    """)
    return


@app.cell
def _(M, Y, np, scipy):
    logY = np.log(Y)
    logM = np.log(M)
    regress = scipy.stats.linregress(logM, logY)
    logY0, b = regress.intercept, regress.slope
    print("Y0 = {:.4f}, b = {:.4f}".format(np.exp(logY0), b))
    return b, logM, logY, logY0


@app.cell
def _(b, logM, logY, logY0, np, plt, red):
    plt.plot(logM, logY, '.')
    plt.xlabel('log Body mass (g)')
    plt.ylabel('log Metabolic rate (W)')

    _logM_range = np.linspace(1, 14)
    _logYhat = logY0 + b * _logM_range
    plt.plot(_logM_range, _logYhat, '-', color=red, lw=3)
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The next step is to **perform Bayesian inference**. You can use PyMC directly or through Bambi.""")
    return


@app.cell
def _():
    ###
    import pymc as pm
    import arviz as az
    import bambi as bmb

    print("PyMC", pm.__version__)
    print("ArviZ", az.__version__)
    print("Bambi", bmb.__version__)
    return az, bmb, pm


@app.cell
def _(logM, logY, pd):
    df_kleiber = pd.DataFrame(dict(logM=logM, logY=logY))
    df_kleiber.head()
    return (df_kleiber,)


@app.cell
def _(bmb, df_kleiber):
    bmb_model = bmb.Model("logY ~ logM", df_kleiber)
    idata = bmb_model.fit(draws=2000, chains=4, idata_kwargs={"log_likelihood": True}, cores=1)
    return (idata,)


@app.cell
def _(az, idata, plt):
    az.plot_trace(idata)
    plt.tight_layout()
    plt.gcf()
    return


@app.cell
def _(az, idata):
    isummary = az.summary(idata)
    isummary
    return (isummary,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Plot MAP and posterior predictions** compared to the real data.""")
    return


@app.cell
def _(az, idata, isummary, logM, logY, np, plt, red):
    plt.plot(logM, logY, '.')
    plt.xlabel('log Body mass (g)')
    plt.ylabel('log Metabolic rate (W)')

    # MAP prediction
    _logY0, _b, _ = isummary['mean']
    _logM_range = np.linspace(1, 14)
    _logYMAP = _logY0 + _b * _logM_range
    plt.plot(_logM_range, _logYMAP, '-', color=red, lw=2, zorder=100)

    # posterior predictions
    _posterior = az.extract(idata, num_samples=1000).to_dataframe()
    _logY0s, _bs = _posterior[['Intercept', 'logM']].values.T
    _logYpred = _logY0s + _bs * _logM_range.reshape((-1, 1))
    az.plot_hdi(_logM_range, _logYpred.T, color='k')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This looks pretty good. Now we can ask: does $b=3/4$? Or $b=2/3$?

    **Plot the posterior of $b$ and draw lines for both values.**
    Based on this plot, draw your conclusion.
    """)
    return


@app.cell
def _(az, idata, plt, red):
    az.plot_posterior(idata, 'logM')
    plt.axvline(3 / 4, color=red)
    plt.axvline(2 / 3, color=red)
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Ex 2: Fit Lotka-Volterra competition models to experimental data""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this section we will analyse competitions between two strains of bacteria.

    Let's start by loading some data.

    ## Data
    """)
    return


@app.cell
def _(datetime, pd):
    ###
    df = pd.read_csv('../data/flow_df_2015-11-18.csv')
    df = df[['Strain', 'date', 'hour', 'freq_mean']]
    df = df.rename(columns=dict(Strain='strain', freq_mean='frequency'))
    # parse date and time, see http://strftime.org
    df['time'] = [
        datetime.strptime(d + '-' + h, '%m/%d/%Y-%H:%M').timestamp()
        for d, h in zip(df['date'], df['hour'])
    ]
    df['time'] = df['time'] - df['time'].min()  # relative time to start of experiment
    df['time'] /= 60 * 60  # to hours
    df.drop(columns=['date', 'hour'], inplace=True)
    df.head()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The data shows results of a competitions between two bacteria strains, one marked as _Green_ and the other as _Red_.
    Approximately every hour, a sample was taken from the tube in which the bacteria were competing. The sample was then processed using flow cytometry to count the number of cells with either a green or a red fluorescent protein (GFP or RFP). Then, the frequencies of the green and red cells were calculated by dividing the number of cells by the total number of cells (i.e. frequency of green = number of green / (number of green + number of red)).

    The frequency of each strain was recored at each time point, but times are encoded as dates and hours.
    The `time` column was created with the number of hours passed since the start of the experiment.

    Next, **plot the frequencies of the two strains over time**.
    Make sure you use the correct colors, labels, etc.

    Tip: try to use `df.groupby` to generate the plot.
    """)
    return


@app.cell
def _(df, green, plt, red):
    _fig, _ax = plt.subplots()
    _colors = dict(Red=red, Green=green)

    for _key, _grp in df.groupby('strain'):
        _grp.plot(x='time', y='frequency', ax=_ax, marker='o', color=_colors[_key])
    plt.legend(df['strain'].unique())
    plt.xlabel('Time (hr)')
    plt.ylabel('Frequency')
    plt.ylim(0, 1)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Model

    To model competitions between two strains (or species) we will use the classical [competitive Lotka–Volterra equations](https://en.wikipedia.org/wiki/Competitive_Lotka–Volterra_equations) (not to be confused with the predator-prey Lotka-Volterra equations).

    This deterministic model describes the change in the expected population sizes of the two strains, $x_1$ and $x_2$.

    $$ \frac{dx_1}{dt} = r_1 x_1 \Big(1 - \bigg(\frac{x_1 + \alpha_2 x_2}{K_1}\bigg)\Big) $$

    $$ \frac{dx_2}{dt} = r_2 x_2 \Big(1 - \bigg(\frac{\alpha_1 x_1 + x_2}{K_2}\bigg)\Big) $$

    where $r_i$ and $K_i$ are the per-capita growth rate and maximum population size of strain $i$, and $\alpha_1$ and $\alpha_2$ are the *competition coefficients*.

    Note the similarity between this model and the single-population logistic growth model; here, the growth-limiting term accounts for both strains, rather than just one.

    The competition coefficients account for the relative effect individuals of strain $i$ have on growth of individuals of strain $j$ compared to other individuals of strain $i$.
    Specifically, different $\alpha_i$ values can be interpreted [competition, parasitism, or even charity](https://en.wikipedia.org/wiki/Biological_interaction#Symbiosis:_long-term_interactions) (see these concepts explained by [Ernie and Bert](https://www.dropbox.com/s/gga4ggpewjus5tq/SesameSt.pptx?dl=0)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the following, we will

    1. fit the above model (LV6) to the data,
    1. fit a nested, simpler, model (LV4) to the data, in which $\alpha_1=\alpha_2=1$; that is, strain $i$ has the same effect on strain $j$ as it does on itself.
    1. select the best model out of the two.

    The names LV6 and LV4 are due to the model name (Lotka-Volterra) and the number of free parameters.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Implementation

    **Write a function called `LV6_ode(t, x, ...)`** that takes the time `t`, an array `x` of populations sizes at time `t`, and the rest of the model parameters, and returns an array of the derivatives of `x` with respect to `t`; $\bigg(\frac{dx_1}{dt}, \frac{dx_2}{dt}\bigg)$.

    **Write another function called `LV4_ode(t, x, ...)`** that performs the same operation, but with the competition parameters set to 1.
    """)
    return


@app.cell
def _():
    def LV6_ode(t, x, *params): ###
        r1, r2, K1, K2, α1, α2 = params
        x1, x2 = x
        return (r1 * x1 * (1 - (x1 + α2 * x2) / K1),
                r2 * x2 * (1 - (α1 * x1 + x2) / K2))

    def LV4_ode(t, x, *params): ###
        r1, r2, K1, K2 = params
        return LV6_ode(t, x, r1, r2, K1, K2, 1, 1)  # α1, α2 = 1, 1
    return LV4_ode, LV6_ode


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now **write a function called `model(ode, t, xinit, ...)`** that takes an ODE function `ode` (such as `LV6_ode` or `LV4_ode`), time points `t`, initial values `xinit` for the population sizes, and any required parameters values.
    The function then integrates the ODE and returns the population <u>*frequencies*</u> at the time points `t`.
    """)
    return


@app.cell
def _(LV4_ode, LV6_ode, np, partial, solve_ivp):
    def model(ode, t, xinit, *params): ###
        result = solve_ivp(lambda t_, x: ode(t_, x, *params),
                           t_span=(0, t.max()), y0=xinit, t_eval=t)
        assert result.success
        x1, x2 = result.y
        xtotal = x1 + x2
        return np.array([x1 / xtotal, x2 / xtotal])

    LV4_model = partial(model, LV4_ode) ###
    LV6_model = partial(model, LV6_ode) ###
    return LV4_model, LV6_model


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Run and plot** an example dynamics for both LV6 and LV4.
    Try to choose parameters values ($r_i, K_i, \alpha_i$) that demonstrate the effect of competition on the dynamics (i.e. such that LV6 and LV4 produce distinct dynamics).
    """)
    return


@app.cell
def _(LV4_model, LV6_model, green, np, plt, red):
    _t = np.linspace(0, 6, 100)

    _x1, _x2 = LV4_model(_t, [0.1, 0.1], 1, 1.1, 1.1, 1)
    plt.plot(_t, _x1, label='Green LV4', color=green, ls='--')
    plt.plot(_t, _x2, label='Red LV4', color=red, ls='--')

    _x1, _x2 = LV6_model(_t, [0.1, 0.1], 1, 1.1, 1.1, 1, 0.9, 1.1)
    plt.plot(_t, _x1, label='Green LV6', color=green)
    plt.plot(_t, _x2, label='Red LV6', color=red)

    plt.xlabel('Time (hr)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Model fit

    We assume that the real frequencies $X_i$ are normally distributed around the model expected value $x_i$ ($i=1,2$):

    $$ X_i \sim N(x_i, \sigma_i^2) $$

    where $x_i$ are the solutions to the ODEs.

    If we are not interested in estimating $\sigma_i$, then the negative log likelihood (NLL) reduces to the sum of squared errors:

    $$ NLL = \sum_t{(X_1 - x_1)^2} $$

    Note that because $X_1+X_2=1$, it's enough to fit just one strain.

    **Fit both models to the data**.

    - implement the NLL as the loss function
    - minimize the NLL loss function using `scipy.optimize`.
    - what should be the value of `xinit` and `t`?

    After fitting the two models, **print and plot a summary** of the fitting for each model:

    - print the maximum likelihood estimated parameter values,
    - plot the data together with the fitted model.

    Make sure the print messages and the plots are as clear and illustrative as possible.
    """)
    return


@app.cell
def _(LV4_model, LV6_model, df, partial):
    X1 = df.loc[df['strain'] == 'Green', 'frequency'].values ###
    X2 = df.loc[df['strain'] == 'Red', 'frequency'].values ###
    xinit = df.loc[df['time'] == 0, 'frequency'].values
    t = df['time'].unique()

    def loss(params, model): ###
        x1, x2 = model(t, xinit, *params)
        return ((x1 - X1)**2).sum()

    loss_LV4 = partial(loss, model=LV4_model) ###
    loss_LV6 = partial(loss, model=LV6_model) ###
    return X1, X2, loss_LV4, loss_LV6, t, xinit


@app.cell
def _(loss_LV4, loss_LV6, scipy):
    result_LV4 = scipy.optimize.minimize(loss_LV4, [1, 1, 1, 1])
    assert result_LV4.success
    print('LV4 loss: {:.2g}'.format(result_LV4.fun))
    print('r={:.2f}, {:.2f}; K={:.2f}, {:.2f}'.format(*result_LV4.x))
    print()
    result_LV6 = scipy.optimize.minimize(loss_LV6, [1, 1, 1, 1, 1, 1])
    print('LV6 loss: {:.2g}'.format(result_LV6.fun))
    print('r={:.2f}, {:.2f}; K={:.2f}, {:.2f}; α={:.2f}, {:.2f}'.format(*result_LV6.x))
    return result_LV4, result_LV6


@app.cell
def _(
    LV4_model,
    LV6_model,
    X1,
    X2,
    green,
    np,
    plt,
    red,
    result_LV4,
    result_LV6,
    t,
    xinit,
):
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4))
    _t_range = np.linspace(t.min(), t.max(), 100)

    _x1, _x2 = LV6_model(_t_range, xinit, *result_LV6.x)
    _ax = _axes[0]
    _ax.plot(t, X1, 'o', color=green, label='Observed green')
    _ax.plot(t, X2, 'o', color=red, label='Observed red')
    _ax.plot(_t_range, _x1, '--', color=green, label='Predicted green')
    _ax.plot(_t_range, _x2, '--', color=red, label='Predicted red')
    _ax.set_xlabel('Time (hr)')
    _ax.set_ylabel('Frequency')
    _ax.set_ylim(0, 1)
    _ax.set_title('LV6 dynamics')

    _x1b, _x2b = LV4_model(_t_range, xinit, *result_LV4.x)
    _ax = _axes[1]
    _ax.plot(t, X1, 'o', color=green, label='Observed green')
    _ax.plot(t, X2, 'o', color=red, label='Observed red')
    _ax.plot(_t_range, _x1b, '--', color=green, label='Predicted green')
    _ax.plot(_t_range, _x2b, '--', color=red, label='Predicted red')
    _ax.set_xlabel('Time (hr)')
    _ax.set_ylabel('Frequency')
    _ax.set_ylim(0, 1)
    _ax.set_title('LV4 dynamics')

    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bayesian inference

    Now **perform Bayesian inference** for both the LV4 and the LV6 models.
    Sample, plot the traces and the marginal distributions, and summarize the results.
    """)
    return


@app.cell
def _(LV4_model, LV6_model, t, xinit):
    import pytensor.tensor as pt
    from pytensor.compile.ops import as_op

    @as_op(itypes=[pt.dvector], otypes=[pt.dmatrix])
    def LV4_model_op(θ):
        return LV4_model(t, xinit, *θ)

    @as_op(itypes=[pt.dvector], otypes=[pt.dmatrix])
    def LV6_model_op(θ):
        return LV6_model(t, xinit, *θ)
    return LV4_model_op, LV6_model_op


@app.cell
def _(LV4_model_op, X1, X2, pm, result_LV4):
    with pm.Model() as LV4_model_pm: ###
        _r1_mle, _r2_mle, _K1_mle, _K2_mle = result_LV4.x
        _r1 = pm.TruncatedNormal("r1", mu=_r1_mle, sigma=1, lower=0, initval=_r1_mle)
        _r2 = pm.TruncatedNormal("r2", mu=_r2_mle, sigma=1, lower=0, initval=_r2_mle)
        _K1 = pm.TruncatedNormal("K1", mu=_K1_mle, sigma=1, lower=0, initval=_K1_mle)
        _K2 = pm.TruncatedNormal("K2", mu=_K2_mle, sigma=1, lower=0, initval=_K2_mle)
        _σ = pm.HalfCauchy("σ", 1)

        _ode_solution = LV4_model_op(pm.math.stack([_r1, _r2, _K1, _K2]))
        _X12_obs = pm.Normal("X12_obs", mu=_ode_solution, sigma=_σ, observed=[X1, X2])
    return (LV4_model_pm,)


@app.cell
def _(LV4_model_pm, az, pm):
    with LV4_model_pm:
        idata_LV4 = pm.sample(draws=10000, chains=4, cores=1)
    az.summary(idata_LV4)
    return (idata_LV4,)


@app.cell
def _(az, idata_LV4, plt):
    az.plot_trace(idata_LV4)
    plt.tight_layout()
    plt.gcf()
    return


@app.cell
def _(az, idata_LV4):
    isummary_LV4 = az.summary(idata_LV4, round_to=4)
    isummary_LV4
    return


@app.cell
def _(LV6_model_op, X1, X2, pm, result_LV6):
    with pm.Model() as LV6_model_pm: ###
        _r1_mle, _r2_mle, _K1_mle, _K2_mle, _α1_mle, _α2_mle = result_LV6.x
        _r1 = pm.TruncatedNormal("r1", mu=_r1_mle, sigma=1, lower=0, initval=_r1_mle)
        _r2 = pm.TruncatedNormal("r2", mu=_r2_mle, sigma=1, lower=0, initval=_r2_mle)
        _K1 = pm.TruncatedNormal("K1", mu=_K1_mle, sigma=1, lower=0, initval=_K1_mle)
        _K2 = pm.TruncatedNormal("K2", mu=_K2_mle, sigma=1, lower=0, initval=_K2_mle)
        _α1 = pm.TruncatedNormal("α1", mu=_α1_mle, sigma=1, lower=0, initval=_α1_mle)
        _α2 = pm.TruncatedNormal("α2", mu=_α2_mle, sigma=1, lower=0, initval=_α2_mle)
        _σ = pm.HalfCauchy("σ", 1)

        _ode_solution = LV6_model_op(pm.math.stack([_r1, _r2, _K1, _K2, _α1, _α2]))
        _X12_obs = pm.Normal("X12_obs", mu=_ode_solution, sigma=_σ, observed=[X1, X2])
    return (LV6_model_pm,)


@app.cell
def _(LV6_model_pm, az, pm):
    with LV6_model_pm:
        idata_LV6 = pm.sample(draws=10000, chains=4, cores=1)
    az.summary(idata_LV6)
    return (idata_LV6,)


@app.cell
def _(az, idata_LV6, plt):
    az.plot_trace(idata_LV6)
    plt.tight_layout()
    plt.gcf()
    return


@app.cell
def _(az, idata_LV6):
    isummary_LV6 = az.summary(idata_LV6, round_to=4)
    isummary_LV6
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Model comparison

    Next we will do model comparison to decide which model is a better fit to our data.

    We start by computing the log-likelihoods to be used for model comparison.
    """)
    return


@app.cell
def _(LV4_model_pm, idata_LV4, pm):
    ###
    with LV4_model_pm:
        idata_LV4_ll = pm.compute_log_likelihood(idata_LV4)
    return (idata_LV4_ll,)


@app.cell
def _(LV6_model_pm, idata_LV6, pm):
    ###
    with LV6_model_pm:
        idata_LV6_ll = pm.compute_log_likelihood(idata_LV6)
    return (idata_LV6_ll,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Use ArviZ's `az.compare` function** to compare between models.
    The function takes a dictionary where keys are model names (i.e. `LV4` and `LV6`) and values are the inference data objects.

    This is done by computing LOO ELPD: leave-one-out expected log-predictive density (ELPD),
    which is a widely-applied, general-purpose metric to measure out-of-sample posterior predictive performance.
    For more, see

    > Vehtari, A., Gelman, A., & Gabry, J. 2017. _Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC_. Statistics and Computing.
    > Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A. and Rubin, D. B. 2013, _Bayesian Data Analysis_.

    The output of `az.compare` has a ranking to specify which is the best model (rank 0); the LOO ELPD (higher is better); the model weights, which are roughly the probability assigned for each model being the correct model (assuming any of them are correct!); the standard error of the ELPD.

    Another way to show this is to **plot the comparison using `az.plot_compare`**, which takes the result of `az.compare` as input.

    You can also use `ic='waic'` in `az.compare` to use the WAIC instead of LOO. WAIC is the widely-applicable information criterion, which is a Bayesian extension of AIC that takes the entire posterior into account rather than just the point estimate (e.g. the MAP estimate).
    """)
    return


@app.cell
def _(az, idata_LV4_ll, idata_LV6_ll):
    df_compare = az.compare(dict(LV4=idata_LV4_ll, LV6=idata_LV6_ll))
    df_compare
    return (df_compare,)


@app.cell
def _(az, df_compare, plt):
    az.plot_compare(df_compare)
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This comparison suggests that LV6 is better supported by this data set compared to LV4.
    This may be surprising because in a previous assignment we used the likelihood ratio test on the maximum likelihood estimates of each model and found that the data does not support rejecting the nested model, LV4. However, now that we have performed Bayesian analysis, and we do not a-priori assume LV4 is better (that is, we do not test the null hypothesis that LV4 is the correct model), we have found support for LV6.

    That being said, a difference in ELPD this small is usually considered "not worth mentioning" (anything below 2), see

    > Kass, R. E. and Raftery, A. E. 1995. _Bayes factors_, J. Am. Stat. Assoc. 90(430), 773.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""__end of assignment__""")
    return


if __name__ == "__main__":
    app.run()
