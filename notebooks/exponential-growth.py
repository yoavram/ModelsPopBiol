import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import scipy.stats
    import seaborn as sns
    sns.set_context('talk')
    red, blue, green = sns.color_palette('Set1', 3)
    return blue, mo, np, pd, plt, red, scipy, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Generalized linear models 1: Exponential growth

    ## [Models in Population Biology](http://modelspopbiol.yoavram.com)
    ## Yoav Ram

    In this session we will understand:
    - how to build the exponential model for populaton growth and transform it to a linear model
    - how to maximum likelihood inference with linear models using gradient descent
    - how to perform Bayesian inference with linear models using `emcee`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data: World Bank

    Our focus today will be on modeling population growth.
    We will start with human populations and use data from the [World Bank](http://www.worldbank.org/) on the [population size of countries](http://data.worldbank.org/indicator/SP.POP.TOTL) around the world from 1960 until 2021.
    """)
    return


@app.cell
def _(pd):
    df = pd.read_csv('../data/world_growth_2021.csv')
    df.head()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We now want to **tidy our data** - transform the dataset to a **DataFrame** format:

    > Tidy datasets are easy to manipulate, model and visualize, and have a specific structure: each variable is a column, each observation is a row, and each type of observational unit is a table - [Hadley Wickham (2014), _Tidy Data_, J. Stat. Soft.](http://www.jstatsoft.org/v59/i10)


    This means that every row in the table has exactly one measurement - population size - with all the relevant variables - country name and year.
    Read more on [tidy data](http://www.jstatsoft.org/v59/i10).

    We do this using Pandas' `melt` function:
    """)
    return


@app.cell
def _(df, pd):
    print(df.shape)
    df_1 = pd.melt(df, id_vars=('Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'), var_name='Year', value_name='Population')
    print(df_1.shape)
    df_1.head()
    return (df_1,)


@app.cell
def _(df_1):
    df_1.tail()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We get rid of rows that have `NA` values:
    """)
    return


@app.cell
def _(df_1):
    print(df_1.shape)
    df_1.dropna(axis=0, inplace=True)
    print(df_1.shape)
    df_1.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that the `Year` column has a type `O` (object) instead of `int`, so we change that:
    """)
    return


@app.cell
def _(df_1):
    print('Year', df_1['Year'].dtype, 'Population', df_1['Population'].dtype)
    df_1['Year'] = df_1['Year'].astype(int)
    print('Year', df_1['Year'].dtype, 'Population', df_1['Population'].dtype)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To get an idea of how the data looks like, let's start with Israel and some other small developed countries.
    We will plot their population size over time.
    """)
    return


@app.cell
def _(df_1, plt, sns):
    countries = ('Israel', 'Denmark', 'Singapore', 'Ireland')
    countries_mask = df_1['Country Name'].isin(countries)
    _df_countries = df_1[countries_mask]
    _fig, _ax = plt.subplots()
    _df_countries.groupby('Country Name', sort=True).plot('Year', 'Population', ax=_ax)
    _ax.legend(sorted(countries), bbox_to_anchor=(1, 1))
    _ax.set_ylabel('Population size')
    sns.despine()
    plt.gcf()
    return (countries_mask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exponential growth model

    How do we model the growth of a population?

    According to [Malthus](http://en.wikipedia.org/wiki/Thomas_Robert_Malthus), if the instantaneous rate of births is $b$ and the instantaneous rate of deaths is $r$, then the instantaneous rate of growth (or decline) of the population is

    $$
    \frac{dN(t)}{dt} = b N(t) - d N(t) = r N(t)
    $$

    where $N(t)$ is the population size at time $t$ and $r=b-d$ is the specific growth rate (or per capita growth rate).

    This is called the Malthusian growth model or more commonly the [exponential growth model](https://en.wikipedia.org/wiki/Exponential_growth).

    This ODE can be solved via [logarithmic differentiation](https://en.wikipedia.org/wiki/Logarithmic_differentiation):

    $$
    \frac{dN(t)}{dt} = r N(t) \Rightarrow \\
    \frac{1}{N(t)} \frac{dN(t)}{dt} = r \Rightarrow \\
    \frac{d \log{N(t)}}{dt} = r \Rightarrow \\
    \log{N(t)} =  r t + C \Rightarrow \\
    N(t) = e^{rt + C} = e^{rt} e^{C}
    $$

    Now add the initial condition $N(0) = N_0$ to get

    $$
    e^{C} = N_0
    $$

    and finally

    $$
    N(t) = N(0) e^{rt}
    $$

    Note that during the integration we found that the **logarithm of the population should be a linear function of time** $\log{N(t)} = \log{N(0)} + rt$.

    Let's check if the world population growth fits the exponential model.
    First define a new column for the log of the population size:
    """)
    return


@app.cell
def _(df_1, np):
    df_1['LogPopulation'] = np.log10(df_1['Population'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we write $y(t) = \log N(t)$, we can model the log of the population size as
    $$
    \widehat{y} = rt + y_0
    $$
    where here $t$ is the number of year since the first year in the dataset, 1960.

    Remember, the model parameters can be interpreted as follows:
    - the "intercept" $y_0$ is the estimate for log size in year zero,
    - the "slope" $r$ is the estimate for the specific growth rate,

    Let's get the time and log population for Israel as an example.
    We change $t$ to start at zero rather than 1960, and we get the NumPy array from the Pandas dataframe.
    """)
    return


@app.cell
def _(df_1):
    idx = df_1['Country Name'] == 'Israel'
    t = df_1.loc[idx, 'Year']
    t = t - t.min()
    t = t.values
    y = df_1.loc[idx, 'LogPopulation'].values
    return t, y


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can then calculate the expected outcome $\widehat{y}$ and the [residuals](https://en.wikipedia.org/wiki/Errors_and_residuals), $y - \widehat{y}$, which are the differences between the observations and the expectations.

    A reasonalbe first guess is to set $y_0$ to the minimal observed value, and $r$ to the average difference between consecutive observations, $y(t+1)-y(t)$.
    """)
    return


@app.cell
def _(plt, sns, t, y):
    y0 = y.min()
    r = (y[1:] - y[:-1]).mean()
    print('y0 = {:.2f}, r = {:.2f}'.format(y0, r))
    _yhat = r * t + y0
    residuals = y - _yhat
    _fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    _ax = axes[0]
    _ax.plot(t, y, '.k')
    _ax.plot(t, _yhat, color='k')
    _ax.set_xlabel('Years since 1960')
    _ax.set_ylabel('Log population size,\n Israel')
    _ax = axes[1]
    sns.histplot(residuals, bins=20, ax=_ax)
    _ax.set(xlabel='Residuals', ylabel='Frequency')
    _fig.tight_layout()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For this first-guess model we see that most all of the markers are above the line, and the residuals are all positive, which means that our model predictions $\widehat{y}$ are lower than the observed values $y$: that is, our model is an under-estimation.

    How do we proceed to find suitable model parameters $r$ and $y_0$?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Maximum likelihood estimation and least squares

    The exponential growth model above means that the log population size is a linear function of time.
    In the simplest form of linear model, we assume that the data ($y$) has a [normal (or Gaussian) distribution](https://en.wikipedia.org/wiki/Normal_distribution) around the linear estimator ($\widehat{y})$.

    Note that this assumption is often invalid, and the framework of _generalized linear models_ allow us to replace the normal distribution with other distributions.
    We'll talk about it again later.

    Usually, when we speak about probabilities, we ask **"what is the probability to see this data given this model"** - when I say "model" I mean something like
    $$
    \widehat{y}_i = rt_i+y_0
    $$
    with given values for $r$ and $y_0$, such as $r=1$ and $y_0=0$, and a normal distribution of observed values around the expected value,
    $$
    y_i \sim \mathit{Normal}(\widehat{y}_i, \sigma^2)
    $$
    where $\sigma^2$ is the variance of the normal distribution.

    That is, we want to say something about how the observed data is expected to be dispersed given a specific model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In general, the probability density function for an observed value $y$ is defined by the normal distribution as
    $$
    p(y_i~|~t_i,r, y_0, \sigma) = \frac{1}{\sqrt{2 \pi \sigma^2}} exp\bigg(-\frac{(y_i-\widehat{y}_i)^2}{2\sigma^2}\bigg).
    $$

    When viewed as a function of the parameters $r, y_0, \sigma$, this is the **likelihood function**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we have mutliple data points (we do!) we can just multiply all of them under the assumption that each data point is *independent*. In this case, we assume that the measurement errors $y_i - \widehat{y}_i$ are independent. Thus, the likelihood is
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    p(Y~|~T,r,y_0,\sigma) = (2 \pi \sigma^2)^{-n/2} \prod_{i=1}^{n}{ exp\left(-\frac{(y_i-rt_i-y_0)^2}{2\sigma^2}\right)}
    $$
    where $Y=(y_1,\ldots,y_n)$ and $T=(t_1,\ldots,t_n)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After establishing what likelihood is, we can ask _"what are the parameters $r$ and $y_0$ that maximize the model likelihood"_.
    This is akin to asking what are the $r$ and $y_0$ values for which the probability of seeing the data we saw is maximized.
    This approach is called **maximum likelihood**.

    Now, our likelihood $\mathcal{L}$ is a product of exponents, so we can take the log-likelihood (literally the log of the likelihood) to get a simpler expression
    $$
    \log p = \\
    \log (2 \pi \sigma^2)^{-n/2} + \log{\prod_{i=1}^{n}{ exp\bigg(-\frac{(y_i-rt_i-y_0)^2}{2\sigma^2}\bigg)}} = \\
    -\frac{n}{2}\log{(2 \pi \sigma^2)} + \sum_{i=1}^{n}{-\frac{(y_i-rt_i-y_0)^2}{2\sigma^2}} = \\
    -\frac{n}{2}\log{(2 \pi \sigma^2)} - \frac{1}{2\sigma^2} \sum_{i=1}^{n}{(y_i-rt_i-y_0)^2} \Rightarrow \\
    \textit{argmax}_{r,y_0}{\left(-\log p\right)} = \textit{argmax}_{r,y_0}{\sum_{i=1}^{n}{(y_i-rt_i-y_0)^2}}
    $$

    Note that
    - $\log{p}$ is an increasing function of $p$ so maximizing the log-likelihood is equivalent to maximizing the likelihood
    - $a$ and $b$ only appear in the sum-of-squares, which is prepended by a negative sign, so minimizing the sum-of-squares is equivalent to maximizing the log-likelihood
    - if we only care about the best estimate of $r$ and $y_0$ then we don't really care about the variance $\sigma^2$ (we would care if we wanted to have some statistical measure of precision or confidence)

    This is where the **least squares** approach comes from -- when assuming a model with normal distribution of residuals, maximizing the likelihood is equivalent to minimizing the sum-of-squares of the residuals, or the differences between the model expected values $\widehat{y}$ and the observed values $y$.
    Note that this works with non-linear models just the same, as long as the residuals are normally and independently distributed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this case of a linear model, there is an **analytical formula** for the maximum likelihood estimates of $r$ and $y_0$.
    Taking derivatives of the RSS with respect to $r$ and $y_0$ and setting them to zero,
    $$
    \frac{\partial RSS}{\partial r} = \sum_{i=1}^{n}{rt_i^2 + t_i y_0 - t_i y_i} = 0 \\
    \frac{\partial RSS}{\partial y_0} = \sum_{i=1}^{n}{rt_i + y_0 - y_i} = 0
    $$
    Solving these equations gives the maximum likelihood estimates:
    $$
    \hat r = \frac{\sum_{i=1}^{n}{(t_i - \bar{t})(y_i - \bar{y})}}{\sum_{i=1}^{n}{(t_i - \bar{t})^2}} \\
    \hat y_0 = \bar{y} - \hat{r} \bar{t}
    $$
    """)
    return


@app.cell
def _(t, y):
    def mle(t, y):
        r_hat = ((t - t.mean()) * (y - y.mean())).sum() / ((t - t.mean())**2).sum()
        y0_hat = y.mean() - r_hat * t.mean()
        return r_hat, y0_hat

    θhat_mle = mle(t, y)
    print('r={:.4f}, y0={:.4f}'.format(*θhat_mle))
    return (θhat_mle,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plot and interpret a linear model
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's plot the results.
    We plot a straight line over the scatterplot.
    Note that we sort the x values first otherwise the straight line will zigzag over the plot.
    """)
    return


@app.cell
def _(plt, red, sns, t, y, θhat_mle):
    def plot_model(θ, t, y, color=red):
        r, y0 = θ
        yhat = r * t + y0
        plt.plot(t, 10 ** y, 'o')
        plt.plot(t, 10 ** yhat, '-', color=color)
        plt.xlabel('Years since 1960')
        plt.ylabel('Population size')
        sns.despine()
        print('r={:.3f}, y0={:.3f}'.format(r, y0))
    plot_model(θhat_mle, t, y)
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The results can be interpreted as follows
    - in year 1960, the population size was $10^6.638$.
    - in every year, the population sizes multiplies by $exp(0.01) \approx 1.01$, that is, increases by 1%.

    This model will probably do a good job at *interpolation*, that is estimating $\widehat{y}$ for $x$ values that are within the original $x$ values, but not at *extrapolation*: indeed you can see that it over-estimates both at time zero and at the last time point.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Plot with Seaborn

    Seaborn has a function, `lmplot`, to automatically generate linear model plots.
    """)
    return


@app.cell
def _(countries_mask, df_1, sns):
    _df_countries = df_1[countries_mask]
    _grid = sns.lmplot(x='Year', y='LogPopulation', hue='Country Name', data=_df_countries, height=4, aspect=1.5, line_kws=dict(ls='--'), scatter_kws=dict(s=20))
    _grid
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What about the G7 countries?
    """)
    return


@app.cell
def _(df_1, sns):
    G7_countries = ('Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States')
    G7_mask = df_1['Country Name'].isin(G7_countries)
    G7 = df_1[G7_mask]
    G7_max = G7.groupby('Country Name')['Population'].max()
    G7_max.sort_values(ascending=False, inplace=True)
    _grid = sns.lmplot(x='Year', y='LogPopulation', hue='Country Name', data=G7, height=7, aspect=1.5, line_kws=dict(ls='--'), scatter_kws=dict(s=20), hue_order=G7_max.index)  # split-apply-combine
    _grid
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is interesting. While some countries fit the exponential growth model very well (United States, France, United Kingdom), some countries don't fit as well: Japan seems to have stopped growing during the 1980s, and, Germany, Italy and Canada also seem to decelerate their growth.
    For an interesting evolutionary perspective see [this paper](http::/doi.org/10.1016/j.tpb.2003.07.003):
    > Ihara Y, Feldman MW (2004) Cultural niche construction and the evolution of small family size. Theor Popul Biol 65(1):105–111.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## SciPy
    SciPy's statistics package has its own linear regression method that also calculates some statistics of the resgression.
    """)
    return


@app.cell
def _(scipy, t, y):
    regress = scipy.stats.linregress(t, y)
    print(regress.slope, regress.intercept)
    return (regress,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The P-value gives the probability to get this data if the null hypothesis is right; in this case, the null hypothesis is $r=0$: that the growth rate is zero.
    """)
    return


@app.cell
def _(regress):
    print('P = {:.2g}'.format(regress.pvalue))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This hypothesis test is not very intereting, as we know that $r>0$ because clearly the population grows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Statsmodels

    This package focuses on statistical modeling, and as such, provides a full statistical analysis of the linear model:

    $$
    \widehat{y} = a x + b \\
    y \sim N(\widehat{y}, \sigma)
    $$
    """)
    return


@app.cell
def _():
    import statsmodels.api as sm

    return (sm,)


@app.cell
def _(np, pd, sm, t, y):
    T = pd.DataFrame({'r': t, 'y0': np.ones(len(t))})
    results = sm.OLS(y, T).fit()
    return (results,)


@app.cell
def _(results):
    results.summary()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bayesian linear models

    To perform Bayesian inference with linear models, we just need to decide on a prior distribution for the model parameters $a$ and $b$, and run the MCMC sampler.

    The model is
    $$
    \hat{y} = r t_i + y_0 \\
    y \sim N(\hat{y}, \sigma)
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Prior elicitation

    How can we choose a prior distribution?
    Let's start with $r$. According to [Wikipedia](https://en.wikipedia.org/wiki/World_population): "the highest global population growth rates, with increases of over 1.8% per year, occurred between 1955 and 1975, peaking at 2.1% between 1965 and 1970. The growth rate declined to 1.1% between 2015 and 2020..."
    So we should set the prior distribution for the growth rate to somewhere between 0.011 and 0.021. But how do we do that? We can use [PreliZ](https://preliz.readthedocs.io/en/latest/index.html), a package for prior distribution elicitation.

    Let's import PreliZ and ask it for a log-normal distribution that gives 95% probability to the range between 0.11 and 0.021.
    """)
    return


@app.cell
def _():
    import preliz as pz
    print("Preliz", pz.__version__)
    return (pz,)


@app.cell
def _(plt, pz):
    pz.maxent(pz.LogNormal(), 0.011, 0.021, 0.95)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The initial population size we can set to a log-normal distribution such that 95% of the distribution is within half or double of the real initial value.
    """)
    return


@app.cell
def _(plt, pz, y):
    pz.maxent(pz.LogNormal(), y[0]/2, y[0]*2, 0.95)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lastly, at the log scale the data does not seem very noisy, so we can use an exponential distribution, say with parameter 0.1; PreliZ can be used to visualize this prior and test different options.
    """)
    return


@app.cell
def _(plt, pz):
    pz.Exponential(0.1).plot_pdf(pointinterval=True)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So overall our priors are:
    $$
    r \sim LogNormal(\mu=-4.16, \sigma=0.16) \\
    log(y_0) \sim LogNormal(\mu=1.96, \sigma=0.33) \\
    \sigma \sim \mathit{Exp}(0.1)
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## PyMC

    We can infer linear models with PyMC, but there is also a high-level library for this (i.e., like statsmodels), called [bambi](https://bambinos.github.io/bambi/main/index.html).
    """)
    return


@app.cell
def _():
    import pytensor
    pytensor.config.linker = 'py' # to avoid error in vs code
    import pymc as pm
    import arviz as az

    return az, pm


@app.cell
def _(pm, t, y):
    model = pm.Model()
    with model:
        _r = pm.LogNormal('r', mu=-4.16, sigma=0.16)
        _y0 = pm.LogNormal('y0', mu=1.96, sigma=0.33)
        _σ = pm.Exponential('σ', lam=0.1)
        y_obs = pm.Normal('y', mu=_r * t + _y0, sigma=_σ, observed=y)
        idata = pm.sample(cores=1)
    return (idata,)


@app.cell
def _(az, idata):
    az.to_netcdf(idata, 'idata_exponential_growth.nc')
    return


@app.cell
def _(az):
    idata_1 = az.from_netcdf('idata_exponential_growth.nc')
    return (idata_1,)


@app.cell
def _(az, idata_1, plt):
    az.plot_trace(idata_1)
    plt.tight_layout()
    plt.gcf()
    return


@app.cell
def _(az, idata_1):
    isummary = az.summary(idata_1)
    θ_bayes = isummary['mean'].values
    isummary
    return


@app.cell
def _(az, idata_1, plt):
    az.plot_pair(idata_1, kind='kde', marginals=True, point_estimate='median', figsize=(10, 10))
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Posterior predictive plots

    One advantage of sampling from the poterior is that we can use these samples to plot a posterior predictive plot.

    Here, we plot the Bayesian estimate in red, but also add lines for 100 samples from the posterior distribution of the model parameters, to plot the dispersion of prediction lines.
    """)
    return


@app.cell
def _(az, blue, idata_1, plt, sns, t, y):
    samples = az.extract(idata_1, num_samples=100, rng=0).to_dataframe()
    _r = samples['r'].values
    _y0 = samples['y0'].values
    t_ = t.reshape((-1, 1))
    _yhat = _r * t_ + _y0
    plt.plot(t, 10 ** _yhat, '-k', alpha=0.1)
    plt.plot(t, 10 ** y, '.', color=blue)
    plt.xlabel('Years since 1960')
    plt.ylabel('Population size')
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # References

    - Pawitan Y, 2001. *In all likelihood: statistical modelling and inference using likelihood*. **Ch. 6.1**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Colophon
    This notebook was written by [Yoav Ram](http://www.yoavram.com) and is part of the [_Models in Population Biology_](https://modelpopbiol.yoavram.com/) course at Tel Aviv University.

    This work is licensed under a CC BY-NC-SA 4.0 International License.
    """)
    return


if __name__ == "__main__":
    app.run()
