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
    # Assignment 4: Statistical inference
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
    mo.md(r"""# Ex 1: warm vs. cold-blooded animals.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this analysis we will compare the body temperature of animals to check if indeed there is such a thing as [warm-blooded](http://en.wikipedia.org/wiki/Warm-blooded) and [cold-blooded](https://en.wikipedia.org/wiki/Ectotherm) animals.

    ## Data loading and preprocessing

    We start by loading the data.
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
    The temperatures are in Kelvin degrees in the `Temperature (K)` column, and we like Celsius degrees.
    So we transform the temperature to Celsius and save the result in a new column.

    Note: SciPy has a special function for Kelvin to Celsius conversion.
    """)
    return


@app.cell
def _(data_raw):
    ###
    from scipy.constants import convert_temperature
    data_raw['Temperature (C)'] = convert_temperature(data_raw['Temperature (K)'], 'K', 'C')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we clean the data frame from rows with missing values in the temperature column.
    We remove from the data classes with fewer than 10 species -- these are the birds.
    """)
    return


@app.cell
def _(data_raw, np):
    ###
    data = data_raw[np.isfinite(data_raw['Temperature (C)'])]
    data['Class'].value_counts()
    return (data,)


@app.cell
def _(data):
    data_clean = data[data["Class"] != 'Aves'] ###
    return (data_clean,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We are left with mammals, reptiles, and amphibians.

    We collate together the non-mammals (reptiles and amphibians).
    """)
    return


@app.cell
def _(data_clean):
    mammals = data_clean['Class'] == 'Mammalia' ###
    return (mammals,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Plot a histogram of the temperature**: one histogram for mammals, and one histogram for amphibians and reptiles.

    Plot the histograms on the same figure. Use `density=True` so that the histograms will be normalized, since there are many more mammals.
    """)
    return


@app.cell
def _(data_clean, mammals, plt, sns):
    plt.hist(data_clean.loc[mammals, 'Temperature (C)'], density=True, alpha=0.7, label='Mammals')
    plt.hist(data_clean.loc[~mammals, 'Temperature (C)'], density=True, alpha=0.7, label='Others')
    plt.legend()
    plt.xlabel('Temperature (C)')
    plt.ylabel('Density')
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Frequentist approach: t-test

    OK. Now we want to compare these two empirical distribution: do they come from the same distribution? What is the probability that there is no difference between mammals and amphibians/reptiles, and that the difference we see in the dataset is a fluke?

    The standard frequntist approach for this is [Student's t-test](https://en.wikipedia.org/wiki/Student%27s_t-test), which is used _"to determine if the means of two sets of data are significantly different from each other."_

    This test assumes that the data are normally distributed around the mean (the histogram looks OK, I guess), but it also assumes that the variance is equal in the two distibutions, which doesn't seem to be the case.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A more robust test is [Welch's t-test](https://en.wikipedia.org/wiki/Welch%27s_t-test).
    The test statistic is defined as:

    $$ t=\frac{\bar{X}_{1}-\bar{X}_{2}}{\sqrt{\frac{s_{1}^{2}}{N_{1}}+\frac{s_{2}^{2}}{N_{2}}}}, $$

    where $X_i$ is dataset $i$, $\bar{X}_i$ is it's mean, $s_i$ it's standard deviation, and $N_i$ it's size.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The numerator is just the difference in means - we want to test if this is dignificantly different than zero.
    The denominator scales the mean difference using an estimate of the standard errors of the means.

    Welch's test assumes normality, but not equal variance.

    **Compute $t$ and print it.**
    """)
    return


@app.cell
def _(data_clean, mammals):
    X1 = data_clean.loc[mammals, 'Temperature (C)'].values ###
    X2 = data_clean.loc[~mammals, 'Temperature (C)'].values ###
    return X1, X2


@app.cell
def _(X1, X2, np):
    X1bar = X1.mean()
    X2bar = X2.mean()
    s1 = X1.std(ddof=1)
    s2 = X2.std(ddof=1)
    N1 = X1.size
    N2 = X2.size

    t = (X1bar - X2bar) / np.sqrt(s1 * s1 / N1 + s2 * s2 / N2)

    print('t = {:.3f}'.format(t)) ###
    return N1, N2, s1, s2, t


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Welch showed that that $t$ is approximately t-distributed:

    $$ t \sim \mathbb{t}(\nu) $$

    where the parameter $\nu$ for the distribution of $t$ is

    $$ \nu \approx \frac{\left(\frac{s_{1}^{2}}{N_{1}}+\frac{s_{2}^{2}}{N_{2}}\right)^{2}}{\frac{s_{1}^{4}}{N_{1}^{2} \nu_{1}}+\frac{s_{2}^{4}}{N_{2}^{2} \nu_{2}}} $$

    where $\nu_i = N_i-1$. We won't get into how this is all constructed -- this requires some mathematical abckground.

    However, we will compute the probability to draw from $\mathbb{t}(\nu)$ a value as extreme as $t$.
    We will print this probability, which is commonly called the _p-value_ of the test.

    This p-value tells gives us what we were looking for: the probability that the two distributions actually have the same mean, despite the disparity we see.
    As you will see, the p-value is extremely low, and therefore we can reject the hypothesis (which is usually called the null hypothesis) that there is no difference between the temperature of mammals and amphibians/reptiles.

    _Note:_ we use `scipy.stats.t.sf(x) * 2` (`sf(x) = 1 - cdf(x)`), which returns the probability to get a value as extreme (very large or very small) as `x`. This "very small or very large" is considered a two-sided test: we want to if either mean is much greater than the other one.
    """)
    return


@app.cell
def _(N1, N2, s1, s2, scipy, t):
    ###
    _ν = (s1 * s1 / N1 + s2 * s2 / N2)**2 / (s1**4 / (N1*N1*(N1-1)) + s2**4 / (N2 * N2 * (N2-1)))

    _pvalue = scipy.stats.t.sf(t, _ν) * 2
    print('p-value: {:.2g}'.format(_pvalue))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""By the way, we could have just used `scipy.stats.ttest`. Here's how to do that:""")
    return


@app.cell
def _(X1, X2, scipy):
    ###
    _t, _pvalue = scipy.stats.ttest_ind(X1, X2, equal_var=False)
    print("P-value: {:.2g} (t={:.3f})".format(_pvalue, _t))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bayesian approach: BEST

    Now let's do this using Bayesian statistics, with an approach called BEST ([Bayesian Estimation Supersedes the T-test](https://psycnet.apa.org/fulltext/2012-18082-001.pdf)).

    The nice thing is that once we understand Bayesian inference, we can easily understand BEST; whereas with the t-test, we need to specifically understand t-distributions, which looks very complicated.

    How are we modelling the data?
    Similarly to the t-test, we assume normality:

    $$ X_1 \sim N(\mu_1, \sigma_1^2) $$

    $$ X_2 \sim N(\mu_2, \sigma_2^2) $$

    So the model parameters are $\mu_1$, $\mu_2$, $\sigma_1$, and $\sigma_2$.

    **Start by infering the model parameters** using _PyMC_ (or some other Bayesian inference method if you prefer).

    To have a full description of our model we need to specify the prior for $\theta$.
    We provide wide priors for $\mu_i$ around the sample mean, and some exponential prior for the standard deviation terms:

    $$ \mu_i \sim N(\bar{X}, 50) $$

    $$ \sigma_i \sim Exp(10) $$

    here $\bar{X}$ is the mean of all the samples (including all of $X_1$ and $X_2$), and $Exp(10)$ is an exponential distribution with mean 10 (implemented with `scipy.stats.expon(scale=10)`).
    """)
    return


@app.cell
def _(X1, X2, np):
    X = np.concatenate((X1, X2)) ###
    Xbar = X.mean() ###
    return X, Xbar


@app.cell
def _():
    import pymc as pm
    import arviz as az
    print("PyMC", pm.__version__, "Arviz", az.__version__)
    return az, pm


@app.cell
def _(X1, X2, Xbar, pm):
    with pm.Model() as best_model:
        _μ1 = pm.Normal('μ1', mu=Xbar, sigma=50)
        _μ2 = pm.Normal('μ2', mu=Xbar, sigma=50)

        _σ1 = pm.Exponential('σ1', 10)
        _σ2 = pm.Exponential('σ2', 10)

        _X1_obs = pm.Normal('X1', mu=_μ1, sigma=_σ1, observed=X1)
        _X2_obs = pm.Normal('X2', mu=_μ2, sigma=_σ2, observed=X2)

        idata = pm.sample()
    return best_model, idata


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Plot a trace plot** to make sure the Markov chain has converged.""")
    return


@app.cell
def _(az, idata, plt):
    az.plot_trace(idata)
    plt.tight_layout()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Plot a pair plot** to examine the posterior. It should show nice gaussians, both on and off the diagonal.""")
    return


@app.cell
def _(az, idata, plt):
    az.plot_pair(idata, kind='kde', marginals=True, point_estimate='mean', figsize=(8, 8))
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finally, we can do the Bayesian estimation for the difference between the means $\mu_1$ and $\mu_2$ by computing the posterior of the difference $\Delta\mu = \mu_1 - \mu_2$:

    - **extract the samples** from the inference data.
    - **compute the difference** between the posterior samples of $\mu_1$ and $\mu_2$ to get posterior samples of $\Delta\mu$,
    - **plot the histogram of the posterior** of $\Delta\mu$ (note how far the distribution is from zero!),
    - **print the probability that $\mu_1>\mu_2$** according to the posterior of $\Delta\mu$.
    """)
    return


@app.cell
def _(az, idata, plt):
    posterior_df = az.extract(idata, var_names=['μ1', 'μ2']).to_dataframe()
    posterior_df['Δμ'] = posterior_df['μ1'] - posterior_df['μ2']

    posterior_df['Δμ'].plot.hist(bins=100, density=True)
    plt.xlabel(r'$\Delta\mu$')
    plt.ylabel('Density')

    print('P(μ1 > μ2) =', (posterior_df['Δμ'] > 0).mean())
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
def _(LV4_ode, LV6_ode, partial, solve_ivp):
    def model(ode, t, xinit, *params): ###
        result = solve_ivp(lambda t_, x: ode(t_, x, *params),
                           t_span=(0, t.max()), y0=xinit, t_eval=t)
        assert result.success
        x1, x2 = result.y
        xtotal = x1 + x2
        return x1 / xtotal, x2 / xtotal

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

    Note: in this assignment we use `X1_freq`, `X2_freq`, and `times` for the strain data (instead of `X1`, `X2`, `t`) because `X1`, `X2`, and `t` are already used in Ex 1.
    """)
    return


@app.cell
def _(LV4_model, LV6_model, df, partial):
    X1_freq = df.loc[df['strain'] == 'Green', 'frequency'].values ###
    X2_freq = df.loc[df['strain'] == 'Red', 'frequency'].values ###
    xinit = df.loc[df['time'] == 0, 'frequency'].values
    times = df['time'].unique()

    def loss(params, model): ###
        x1, x2 = model(times, xinit, *params)
        return ((x1 - X1_freq)**2).sum()

    loss_LV4 = partial(loss, model=LV4_model) ###
    loss_LV6 = partial(loss, model=LV6_model) ###
    return X1_freq, X2_freq, loss_LV4, loss_LV6, times, xinit


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
    X1_freq,
    X2_freq,
    green,
    np,
    plt,
    red,
    result_LV4,
    result_LV6,
    times,
    xinit,
):
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4))
    _t_range = np.linspace(times.min(), times.max(), 100)

    _x1, _x2 = LV6_model(_t_range, xinit, *result_LV6.x)
    _ax = _axes[0]
    _ax.plot(times, X1_freq, 'o', color=green, label='Observed green')
    _ax.plot(times, X2_freq, 'o', color=red, label='Observed red')
    _ax.plot(_t_range, _x1, '--', color=green, label='Predicted green')
    _ax.plot(_t_range, _x2, '--', color=red, label='Predicted red')
    _ax.set_xlabel('Time (hr)')
    _ax.set_ylabel('Frequency')
    _ax.set_ylim(0, 1)
    _ax.set_title('LV6 dynamics')

    _x1_, _x2_ = LV4_model(_t_range, xinit, *result_LV4.x)
    _ax = _axes[1]
    _ax.plot(times, X1_freq, 'o', color=green, label='Observed green')
    _ax.plot(times, X2_freq, 'o', color=red, label='Observed red')
    _ax.plot(_t_range, _x1_, '--', color=green, label='Predicted green')
    _ax.plot(_t_range, _x2_, '--', color=red, label='Predicted red')
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
    ## Model selection

    Since it may be difficult to decide which model is better based on the summaries above, **perform model selection** to select one of the models and answer the question:  _can the nested model LV4 be rejected in favor of the full model LV6?_

    Print and plot any required steps to support your decision, and finish with a clear statement answering the question above.

    If you are not sure how to perform model selection, I would recommend the [likelihood ratio test](https://en.wikipedia.org/wiki/F-test#Regression_problems).
    """)
    return


@app.cell
def _(result_LV4, result_LV6, scipy, times):
    _n = times.size  # number of samples
    _p0 = 4  # number of parameters in null model
    _p1 = 6  # number of parameters in alternative model
    # F-statistic, see https://en.wikipedia.org/wiki/F-test#Regression_problems
    _F = ((result_LV4.fun - result_LV6.fun) / (_p1 - _p0)) / (result_LV6.fun / (_n - _p1))
    _pvalue = scipy.stats.f(_p1 - _p0, _n - _p1).sf(_F)  # sf = 1 - cdf
    print("F-statistic: {:.2g}".format(_F))
    print("Likelihood-ratio test p-value = {:.2g}".format(_pvalue))
    print("The nested model is rejected:", _pvalue < 0.05)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""__end of assignment__""")
    return


if __name__ == "__main__":
    app.run()
