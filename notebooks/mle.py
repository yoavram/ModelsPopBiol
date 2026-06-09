# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.3",
# ]
# ///

import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import scipy.stats
    import seaborn as sns
    sns.set(
        style='white',
        context='talk'
    )
    red, blue, green = sns.color_palette('Set1', 3)
    return blue, green, mo, np, plt, red, scipy, sns


@app.cell
def _(np):
    rng = np.random.default_rng(1202)
    return (rng,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Maximum likelihood estimation

    ## [Models in Population Biology](http://modelspopbiol.yoavram.com)
    ## Yoav Ram
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Statistical inference: the frequentist approach

    Statistical inference uses scientific models to explain observable phenomena.

    Statistical inference applies mathematical and computational methods to draw conclusions on _Models_ from the _Theoretical World_ using  _Data_ from the _Real World_.


    The two major approaches to statistical inference (and statistics as a whole) are the **frequentist** and **Bayesian** approaches, but in this course we will use both, in the spirit of [_Statistical pragmatism_](http://www.stat.cmu.edu/~kass/papers/bigpic.pdf).

    Today we will deal with the **frequentist approach**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Poisson model for count data

    This example follows a [blog post by Jake VanDerPlas](http://jakevdp.github.io/blog/2014/03/11/frequentism-and-bayesianism-a-practical-intro/).

    Imagine that we count the number of [European red mites](https://en.wikipedia.org/wiki/Panonychus_ulmi) on apple leaves.

    Denote the number of leaves by $n$, where the $i^{\rm th}$ measurement $x_i$ reports the observed number of mites on leaf $i$.
    We assume that $x_i$ is Poisson-distributed around the expected number of mites $\mu$,
    $$
    x_i \sim Poi(\mu)
    $$

    So $Poi(\mu)$ is our **model**, and $X=\{x_i\}_{i=1}^{n}$ is the data.

    The question is, given this data $X$, **what is our best estimate of $\mu$?**
    And the next question would be: does the model provide a good fit to the data?

    Generating this estimate is the objective of **statistical inference**: making conclusions on observable phenomea by applying mathematical methods to data and models.

    ## Synthetic data from Poisson model

    We start by simulating data before using real data.
    """)
    return


@app.cell
def _(rng):
    μ = 10
    # expected number of mites on a leaf
    n_poi = 150
    # number of measurements
    # n measurements of the mites
    X_poi = rng.poisson(μ, size=n_poi)
    return X_poi, n_poi, μ


@app.cell
def _(X_poi, n_poi, np, plt, red, sns, μ):
    _fig, _axes = plt.subplots(1, 2, figsize=(8, 4))
    _ax = _axes[0]
    _ax.plot(np.arange(n_poi), X_poi, '.k')
    _ax.axhline(μ, linewidth=3, color=red)
    _ax.set_xlabel('Leaf, $i$')
    _ax.set_ylabel('# Mites, $X_i$')
    _ax = _axes[1]
    _ax.hist(X_poi, bins=10, density=True)
    _ax.axvline(μ, linewidth=3, alpha=1, color=red)
    _ax.set_ylabel('Density')
    _ax.set_xlabel('# Mites, $X_i$')
    _fig.tight_layout()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this toy example we already know the
    true value of $\mu$, but the question is this: **given our measurements $\{X_i\}$, what is our best estimate of the true $\mu$?**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Maximum likelihood estimation with Poisson distribution

    Which mathematical method can we use to make conclusions on $\mu$ from $\{X_i\}$?

    Maximum likelihood is a very common and popular approach to statistical inference in which we look for the model that has the maximum probability to generate the observed data.

    Formally, the likelihood $\mathcal{L}$ of the model

    $$
    x_i \sim Poi(\mu)
    $$

    given observed data $X = \{x_i\}_i$ is the probability of seeing data given the model:

    $$
    P(X~|~\mu) =
    \prod_{i=1}^n P(x_i~|~\mu)
    $$

    We assume (or even know) that the distribution of the measurements $x_i$ is Poisson.
    Therefore, the probability to see $x_i$ given $\mu$ is

    $$
    P(x_i~|~\mu) =
    \frac{\mu^{x_i} e^{-\mu}}{x_i!}
    $$

    So the likelihood $P(X~|~\mu)$ is a product of exponents.
    Therefore, we take the log-likelihood $\log{P(X~|~\mu)}$:

    $$
    \log{P(X~|~\mu)} =
    \sum_{i=1}^n \log{P(x_i~|~\mu)}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use `scipy` to implement the `log_likelihood(μ, X)` function, wjocj takes $\mu$, the expected value of a Poisson distribution, and $X$, and array of measurements, and returns $\log\mathcal{L}(\mu~|~X)$, the log-likelihood of $\mu$ given we saw $X$, which equals $\log P(X \mid \mu)$, the log-probability of seeing $X$ if $\mu$ is true.
    """)
    return


@app.cell
def _(np, scipy):
    @np.vectorize(excluded=(1,)) # excluded=(1,) means that the second argument (X) is not vectorized and is passed as is to the function
    def log_likelihood_poi(μ, X):
         return scipy.stats.poisson(μ).logpmf(X).sum()

    return (log_likelihood_poi,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's a plot of the log-likelihood function, with the true value of $\mu$ and a maximum-likelihood estimate.
    """)
    return


@app.cell
def _(X_poi, blue, log_likelihood_poi, np, plt, red, sns, μ):
    _μ_range = np.linspace(X_poi.min(), X_poi.max(), 100)
    _logliks = log_likelihood_poi(_μ_range, X_poi)
    μ_hat_range = _μ_range[_logliks.argmax()]
    print('μ = {} \nμ_hat = {:.4f}'.format(μ, μ_hat_range))
    plt.plot(_μ_range, _logliks, color='k')
    plt.axvline(μ, color=red, label='$\\mu$')
    plt.axvline(μ_hat_range, color=blue, label='$\\hat{\\mu}$')
    plt.xlabel('# Mites, $\\mu$')
    plt.ylabel('Log-likelihood')
    plt.legend()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The estimated value $\mu$ that maximizes the log-likelihood $\log\mathcal{L}$ will be our **maximum likelihood estimate $\hat{\mu}$**.

    We can find this analytically by solving for the root of the derivative of the normal approximation of the log-likelihood:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \frac{d\log\mathcal{L}}{d{\mu}} =
    \frac{d}{d{\mu}} \sum_{i=1}^n{\log{\frac{{\mu}^{x_i} e^{-{\mu}}}{x_i!}}} =
    \\
    \frac{d}{d{\mu}} \sum_{i=1}^n{\log{{\mu}^{x_i}} + \log{e^{-{\mu}}} - \log{(x_i!)}} =
    \\
    \frac{d}{d{\mu}} \sum_{i=1}^n{x_i \log{{\mu}} -{\mu} - \log{(x_i!)}} =
    \\
    \sum_{i=1}^n{\frac{x_i}{{\mu}} - 1} =
    \frac{1}{{\mu}} \sum_{i=1}^n{x_i} - n
    $$

    So

    $$
    \frac{d\log\mathcal{L}}{d{\mu}}(\hat{\mu}) = 0 \Rightarrow
    \hat{\mu} = \frac{1}{n}\sum_{i=1}^n{x_i}
    $$

    So the estimate $\hat{\mu}$ is the **arithmetic mean** $\bar{X}=\frac{1}{n}\sum_{i=1}^n{x_i}$.
    """)
    return


@app.cell
def _(X_poi, blue, log_likelihood_poi, np, plt, red, sns, μ):
    μ_hat_mean = X_poi.mean()
    print('μ = {} \nμ_hat = {:.4f}'.format(μ, μ_hat_mean))
    _μ_range = np.linspace(X_poi.min(), X_poi.max(), 100)
    _logliks = log_likelihood_poi(_μ_range, X_poi)
    plt.plot(_μ_range, _logliks, color='k')
    plt.axvline(μ, color=red, label='$\\mu$')
    plt.axvline(μ_hat_mean, color=blue, label='$\\bar{X}$')
    plt.xlabel('# Mites, $\\mu$')
    plt.ylabel('Log-likelihood')
    plt.legend()
    sns.despine()
    plt.gcf()
    return (μ_hat_mean,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The [Cramér–Rao bound](https://en.wikipedia.org/wiki/Cramér–Rao_bound) provides a lower bound for the precision of this estimate

    $$
    var(\hat{\mu}) \ge \frac{1}{\mathcal{I}}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    where $\mathcal{I}$ is Fisher information, defined as:

    $$
    \mathcal{I} = - \mathbf{E}\Big[\frac{d^2\log P(X~|~\mu)}{d{\mu}^2}(\hat{\mu}) \Big]
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So, we have

    $$
    \frac{d\log P(X~|~\mu)}{d{\mu}} =
    \frac{1}{{\mu}} \sum_{i=1}^n{x_i} - n \Rightarrow \\
    \frac{d^2\log P(X~|~\mu)}{d{\mu}^2}  =
    -\frac{1}{{\mu}^2} \sum_{i=1}^n{x_i} \Rightarrow \\
    \mathcal{I} = - \mathbf{E}\Big[-\frac{1}{\hat{\mu}^2} \sum_{i=1}^n{x_i} \Big] =
    \frac{1}{\hat{\mu}^2} \mathbf{E}\Big[ \sum_{i=1}^n{x_i} \Big] =
    \frac{n}{\hat{\mu}}
    \Rightarrow \\
    var(\hat{\mu}) \ge
    \frac{\hat{\mu}}{n}  \Rightarrow \\
    \sigma_{\hat{\mu}} \ge
    \sqrt{\frac{\hat{\mu}}{n}}
    $$
    """)
    return


@app.cell
def _(
    X_poi,
    blue,
    log_likelihood_poi,
    n_poi,
    np,
    plt,
    red,
    sns,
    μ,
    μ_hat_mean,
):
    _σ_hat = np.sqrt(μ_hat_mean / n_poi)
    print('μ = {} \nμ_hat = {:.4f} +/- {:.4f}'.format(μ, μ_hat_mean, _σ_hat))
    _μ_range = np.linspace(μ_hat_mean - 2, μ_hat_mean + 2, 100)
    _logliks = log_likelihood_poi(_μ_range, X_poi)
    plt.plot(_μ_range, _logliks, color='k')
    plt.axvline(μ, color=red, label='$\\mu$')
    plt.axvline(μ_hat_mean, color=blue, label='$\\bar{X}$')
    _μ_range = np.linspace(μ_hat_mean - _σ_hat, μ_hat_mean + _σ_hat)
    _logliks = log_likelihood_poi(_μ_range, X_poi)
    plt.fill_between(_μ_range, log_likelihood_poi(μ_hat_mean - 2, X_poi), _logliks, alpha=0.5, label='$\\pm \\sigma_{\\hat{\\mu}}$')
    plt.xlabel('# Mites, $\\mu$')
    plt.ylabel('Log-likelihood')
    plt.legend(loc='lower right')
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Goodenss-of-fit to Poisson model

    How good is the fit of the Poisson model to these data?
    In a Poisson model, the variance equals the expected value.
    We estimate the variance (we set `ddof=1` to apply [Bessel's correction](https://en.wikipedia.org/wiki/Bessel%27s_correction)) and compare it to the estimated expected value:
    """)
    return


@app.cell
def _(X_poi, μ_hat):
    print(X_poi.mean(), X_poi.var(ddof=1))
    μ_hat
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Is that close or not? Let's simulate from the model with the estimated parameter and see if we get a ratio close to the empirical result:
    """)
    return


@app.cell
def _(X_poi, n_poi, np, plt, rng, μ_hat_mean):

    _X_syn = rng.poisson(μ_hat_mean, size=(10000, n_poi))
    _ratio = _X_syn.mean(axis=1) / _X_syn.var(axis=1, ddof=1)
    _low, _high = np.percentile(_ratio, [2.5, 97.5])
    plt.hist(_ratio, bins=30, density=True)
    plt.axvline(1, color='k')
    plt.axvline(_low, color='k', linestyle='--')
    plt.axvline(_high, color='k', linestyle='--')
    plt.axvline(X_poi.mean()/X_poi.var(ddof=1), color='r', label='Observed')
    plt.xlabel('Mean/Variance')
    plt.ylabel('Density')
    plt.legend()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Looks good!

    We can also compare the histogram to the inferred Poisson distribution and do a [chi-square test]( https://en.wikipedia.org/wiki/Chi-squared_test) to test the null hypothesis that the data was sampled from a Poisson distribution with the inferred parameter.
    """)
    return


@app.cell
def _(np, scipy):
    def chitest(X, distribution, ddof=0):
        n = X.size
        obser, bins = np.histogram(X, bins=np.arange(0, X.max() * 2))
        bins = bins[:-1]
        expec = distribution.pmf(bins)
        expec = expec / expec.sum()  # normalize (if there is more density outside of bins)
        expec = expec * obser.sum()  # convert from probability to frequency
    ### my implementation
    #     χ2 = ((expec - obser)**2 / expec).sum()
    #     pval = scipy.stats.chi2(n-1-ddof).sf(χ2)
    #     return χ2, pval  
    ### scipy implementation
        return scipy.stats.power_divergence(obser, expec, ddof=ddof)

    return (chitest,)


@app.cell
def _(X_poi, chitest, green, np, plt, scipy, sns, μ_hat_mean):
    def goodness_of_fit_poisson(μ_hat, X):
        poisson = scipy.stats.poisson(μ_hat)
        χ2, pval = chitest(X, poisson, 1)
        print('χ2 = {:.2f}, P-value = {:.2g}'.format(χ2, pval))
        _fig, _ax = plt.subplots()
        _ax.hist(X, bins=10, density=True)
        counts = np.arange(X.max() + 1)
        _ax.plot(counts, poisson.pmf(counts), color='k')
        _ax.axvline(μ_hat, linewidth=3, alpha=1, color=green)
        _ax.set_ylabel('Density')
        _ax.set_xlabel('# Mites, $X_i$')
        _fig.tight_layout()
        sns.despine()
    goodness_of_fit_poisson(μ_hat_mean, X_poi)
    plt.gcf()
    return (goodness_of_fit_poisson,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using a simple chi-square test for goodness-of-fit, we do not reject the hypothesis that this is a Poisson distribution--which makes sense, as we indeed sampled the data from a Poisson.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inference on real data with Poisson model

    We will use data collected by Phillip Garman in 1951 and published by [Bliss and Fisher 1953](https://doi.org/10.2307/3001850) (yes, the same Fisher).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's load the data:
    """)
    return


@app.cell
def _(np, plt):
    X_mites = np.loadtxt('../data/mites.csv', delimiter=',')
    plt.hist(X_mites)
    plt.xlabel('# Mites on leaf')
    plt.ylabel('# leaves')
    plt.gcf()
    return (X_mites,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now perform the Poisson-model inference:
    """)
    return


@app.cell
def _(X_mites, np):
    μ_hat_mites = X_mites.mean()
    _σ_hat = np.sqrt(μ_hat_mites / X_mites.size)
    print('μ_hat = {:.4f} +/- {:.4f}'.format(μ_hat_mites, _σ_hat))
    print('Avg(X)' + '={:.4f}, Var(X)={:.4f}'.format(X_mites.mean(), X_mites.var(ddof=1)))
    return (μ_hat_mites,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We inferred ~1.15 mites per leaf, but the variance seems to be about double the average, which suggests the fit is poor. Let's test it.
    """)
    return


@app.cell
def _(X_mites, n_poi, np, plt, rng, μ_hat_mites):
    _X_syn = rng.poisson(μ_hat_mites, size=(10000, n_poi))
    _ratio = _X_syn.mean(axis=1) / _X_syn.var(axis=1, ddof=1)
    _low, _high = np.percentile(_ratio, [2.5, 97.5])
    plt.hist(_ratio, bins=30, density=True)
    plt.axvline(1, color='k')
    plt.axvline(_low, color='k', linestyle='--')
    plt.axvline(_high, color='k', linestyle='--')
    plt.axvline(X_mites.mean()/X_mites.var(ddof=1), color='r', label='Observed')
    plt.xlabel('Mean/Variance')
    plt.ylabel('Density')
    plt.legend()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The red line is out of the distribution, so this model check does not support using the model for this dataset. What about the goodness of fit test?
    """)
    return


@app.cell
def _(X_mites, goodness_of_fit_poisson, μ_hat_mites):
    goodness_of_fit_poisson(μ_hat_mites, X_mites)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The P-value is very low, such that we reject the Poisson model.
    Indeed, the variance is about twice as large as the mean.

    So what now?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Over-dispersed Poisson model for count data

    Here we assume that the measurements $\{X_i\}$ are still drawn from a Poisson distribution, but the expected values $\mu_i$ changes from leaf to leaf.
    We assume it is drawn from a [Gamma distrubtion](https://en.wikipedia.org/wiki/Gamma_distribution#Related_distributions) with shape $r$ and scale $\phi$ ( with expected value $r\phi$ and variance $r\phi^2$):
    $$
    \mu_i \sim Gamma(r, \phi) \\
    x_i \sim Poi(\mu_i)
    $$

    We note the model parameters as $\theta = (r, \phi)$.

    Our data is still $\{x_i\}$, but the model is now _compound_, as it includes a model for the measurements $Poi(\mu_i)$ and a model for the Poisson parameter $Gamma(r, \phi)$.

    ## Synthetic data from over-dispersed Poisson model
    Let's simulate data according to this compound model.
    """)
    return


@app.cell
def _(rng):
    n_gamma = 150
    θ = r, φ = (5, 2)
    _μi = rng.gamma(r, scale=φ, size=n_gamma)
    X_gamma = rng.poisson(_μi)
    return X_gamma, n_gamma, r, θ, φ


@app.cell
def _(X_gamma, n_gamma, np, plt, r, red, sns, φ):
    _fig, _axes = plt.subplots(1, 2, figsize=(8, 4))
    _ax = _axes[0]
    _ax.plot(np.arange(n_gamma), X_gamma, '.k')
    _ax.axhline(r * φ, linewidth=3, color=red)
    _ax.set_xlabel('Measurement, $i$')
    _ax.set_ylabel('Count, $X_i$')
    _ax = _axes[1]
    _ax.hist(X_gamma, bins=10, density=True)
    _ax.axvline(r * φ, linewidth=3, alpha=1, color=red)
    _ax.set_ylabel('Density')
    _ax.set_xlabel('Count, $X_i$')
    _fig.tight_layout()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Goodness-of-fit to Poisson model

    Let's start by testing how this data fits the Poisson model.
    """)
    return


@app.cell
def _(X_gamma, goodness_of_fit_poisson):
    goodness_of_fit_poisson(X_gamma.mean(), X_gamma)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So this indeed does not fit the Poisson model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Maximum likelihood estimation with negative binomial distribution
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Interestingly, this compound model gives rise to the [Negative Binomial distribution](https://en.wikipedia.org/wiki/Negative_binomial_distribution#Statistical_inference), such that
    $$
    x_i \sim NB(r, p) = Gamma\left(r, \frac{p}{1-p}\right)
    $$
    and $p=\frac{\phi}{\phi+1}$.

    The likelihood function is therefore given by the negative binomial distribution,

    $$
    P(X~|~r, p) =
    \prod_{i=1}^{n}{\binom{x_i +r -1}{x_i} (1-p)^{x_i} p^r}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We therefore implement `log_likelihood(θ, X)`, where $\theta = (r, \phi)$ , $p=\phi/(\phi+1)$, and `X` is the data.
    """)
    return


@app.cell
def _(X_gamma, np, scipy, θ):
    @np.vectorize(signature='(2)->()', excluded=(1,))
    def log_likelihood_negbin(θ, X):
        r, φ = θ
        p = φ / (φ + 1)
        return scipy.stats.nbinom(r, p).logpmf(X).sum()
    print(log_likelihood_negbin(θ, X_gamma))
    return (log_likelihood_negbin,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To find the maximum likelihood we will use a numerical optimization routine from `scipy.optimize`.

    **Note** optimization routines usually _minimize_ rather than _maximize_, so we use the negative log-likelihood.
    """)
    return


@app.cell
def _(X_gamma, log_likelihood_negbin, θ):
    def neg_log_likelihood(θ, X):
        return -log_likelihood_negbin(θ, X)
    print(neg_log_likelihood(θ, X_gamma))
    return (neg_log_likelihood,)


@app.cell
def _(X_gamma, neg_log_likelihood, r, scipy, φ):
    def mle(X, verbose=False, full_path=False):
        r_guess = X.mean()
        φ_guess = r_guess * r_guess / (X.var(ddof=1) - r_guess)  # eq 3 in Bliss and Fisher 1953
        return scipy.optimize.fmin(func=neg_log_likelihood, x0=(r_guess, φ_guess), args=(X,), disp=verbose, retall=full_path)
    θ_hat_gamma = mle(X_gamma, verbose=True)
    r_hat_gamma, φ_hat_gamma = θ_hat_gamma  # function to minimize with respect to first argument
    print('r = {} \tr_hat = {:.4f}\nϕ = {}\tϕ_hat = {:.4f}'.format(r, r_hat_gamma, φ, φ_hat_gamma))  # initial guess  # additional arguments to func  # no prints
    return mle, r_hat_gamma, θ_hat_gamma, φ_hat_gamma


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Computing the log-likelihood for a grid of $r$ and $\phi$ values can take a couple of minutes.
    """)
    return


@app.cell
def _(np):
    r_range_gamma = np.linspace(4, 8, 100)
    φ_range_gamma = np.linspace(0.2, 2.5, 101)
    θ_range_gamma = np.array([[(_r, _φ) for _r in r_range_gamma] for _φ in φ_range_gamma])
    return r_range_gamma, θ_range_gamma, φ_range_gamma


@app.cell
def _(X_gamma, log_likelihood_negbin, θ_range_gamma):
    ll_gamma = log_likelihood_negbin(θ_range_gamma, X_gamma)
    return (ll_gamma,)


@app.cell
def _(
    green,
    ll_gamma,
    plt,
    r,
    r_hat_gamma,
    r_range_gamma,
    red,
    φ,
    φ_hat_gamma,
    φ_range_gamma,
):
    _im = plt.pcolormesh(r_range_gamma, φ_range_gamma, ll_gamma, cmap='viridis')
    plt.colorbar(_im, label='Log-likelihood')
    plt.plot(r, φ, '.', color=red, label='truth')
    plt.plot(r_hat_gamma, φ_hat_gamma, '.', color=green, label='estimate')
    plt.legend()
    plt.xlabel('r')
    plt.ylabel('ϕ')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Goodness-of-fit to overdispersed Poisson model

    Let's see if we got a good fit to the theoretical distribution -- from which we actually sampled.
    """)
    return


@app.cell
def _(X_gamma, chitest, green, np, plt, scipy, sns, θ_hat_gamma):
    def goodness_of_fit_negbin(θ, X):
        r, φ = θ
        p = φ / (φ + 1)
        nbinom = scipy.stats.nbinom(r, p)
        χ2, pval = chitest(X, nbinom, 2)
        print('χ2 = {:.2f}, P-value = {:.2g}'.format(χ2, pval))
        _fig, _ax = plt.subplots()
        _ax.hist(X, bins=10, density=True)
        counts = np.arange(X.max() + 1)
        _ax.plot(counts, nbinom.pmf(counts), color='k')
        _ax.axvline(r * φ, linewidth=3, alpha=1, color=green)
        _ax.set_ylabel('Density')
        _ax.set_xlabel('# Mites, $X_i$')
        _fig.tight_layout()
        sns.despine()
    goodness_of_fit_negbin(θ_hat_gamma, X_gamma)
    plt.gcf()
    return (goodness_of_fit_negbin,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    OK so we can go ahead and try to infer with this over-dispersed model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inference on real data with over-dispersed Poisson model

    Let's try out this over-dispersed Poisson model on our real "mites on leaves" data.

    We reuse the `X_mites` data loaded above and proceed for the maximum likelihood estimation.
    """)
    return


@app.cell
def _(X_mites, mle, scipy):
    θ_hat_mites = mle(X_mites, verbose=True)
    r_hat_mites, φ_hat_mites = θ_hat_mites
    negbin_rv = scipy.stats.nbinom(r_hat_mites, φ_hat_mites / (φ_hat_mites + 1))
    print('r_hat = {:.4f}\nϕ_hat = {:.4f}'.format(r_hat_mites, φ_hat_mites))
    print('Observed mean: {:.4f}, variance: {:.4f}'.format(X_mites.mean(), X_mites.var(ddof=1)))
    print('Expected mean: {:.4f}, variance: {:.4f}'.format(negbin_rv.mean(), negbin_rv.var()))
    return r_hat_mites, θ_hat_mites, φ_hat_mites


@app.cell
def _(X_mites, goodness_of_fit_negbin, θ_hat_mites):
    goodness_of_fit_negbin(θ_hat_mites, X_mites)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So we have inferred the values and got a good fit.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Likelihood surface

    We can plot the log-likelihood surface (since there are only two parameters). We'll also call `fmin` again with `retall=True` to get all the $\theta$ it computed at each iterations and plot them as a path on the log-likelihood surface.
    """)
    return


@app.cell
def _(X_mites, mle, np):
    _θ_hat_mites, θ_path = mle(X_mites, full_path=True)
    θ_path = np.array(θ_path)
    return (θ_path,)


@app.cell
def _(X_mites, log_likelihood_negbin, np):
    r_range_mites = np.linspace(0.5, 2, 100)
    φ_range_mites = np.linspace(0.5, 2, 101)
    θ_range_mites = np.array([[(_r, _φ) for _r in r_range_mites] for _φ in φ_range_mites])
    ll_mites = log_likelihood_negbin(θ_range_mites, X_mites)
    return ll_mites, r_range_mites, φ_range_mites


@app.cell
def _(
    green,
    ll_mites,
    plt,
    r_hat_mites,
    r_range_mites,
    θ_path,
    φ_hat_mites,
    φ_range_mites,
):
    _im = plt.pcolormesh(r_range_mites, φ_range_mites, ll_mites, cmap='viridis')
    plt.colorbar(_im, label='Log-likelihood')
    plt.plot(r_hat_mites, φ_hat_mites, '.', color=green, label='estimate')
    plt.plot(θ_path[:, 0], θ_path[:, 1], '-', color='k', lw=1)
    plt.xlabel('r')
    plt.ylabel('ϕ')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As in many cases, the likelihood function shows a dependence between the model parameters.
    Nevertheless, it seems like we found a good maximum likelihood estimate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bootstrap
    There are several analytic methods to quantify the uncertainty in the parameter estimations.

    However, we will a computational method: the **bootstrap method**, in which we estimate the parameters from many resamples of the data.

    > Bootstrapping is the practice of estimating properties of an estimator (such as its variance) by measuring those properties when sampling from an approximating distribution. One standard choice for an approximating distribution is the empirical distribution function of the observed data. In the case where a set of observations can be assumed to be from an independent and identically distributed population, this can be implemented by constructing a number of resamples with replacement, of the observed data set (and of equal size to the observed data set).

    For efficiency, we parallelize this step using `ThreadPoolExecutor` from Python's standard library.
    """)
    return


@app.cell
def _(X_mites, rng):
    n_resamples = 1000
    resamples = rng.choice(X_mites, size=(n_resamples, X_mites.size))
    return (resamples,)


@app.cell
def _():
    from concurrent.futures import ThreadPoolExecutor

    return (ThreadPoolExecutor,)


@app.cell
def _(ThreadPoolExecutor, mle, resamples):
    # magic command not supported in marimo; please file an issue to add support
    # %%time
    with ThreadPoolExecutor() as exec:
        θ_bootstrap = list(exec.map(mle, resamples))
    return (θ_bootstrap,)


@app.cell
def _(np, θ_bootstrap):
    θ_bootstrap_arr = np.array(θ_bootstrap)
    _r_bootstrap, _φ_bootstrap = θ_bootstrap_arr.T
    return (θ_bootstrap_arr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can inspect the distributions of the estimations to see how far the true and estimated values are compared to all boostrap estimations.

    We do this with a **corner plot** using the [corner](http://corner.readthedocs.io) package.

    The diagonal plots show the histogram of the parameter estimated, and the joint plot (bottom left) shows a joint 2D histogram of the parameters.
    The contours on the joint plot show standard deviations (of a gaussian) to demonstrate confidence regions.
    This demonstrates that the truth (in red) is just on the edge of the confidence region, whereas the estimate (green) is right at the middle.

    You can see that the joint plot is very similar to the likelihood surface.
    """)
    return


@app.cell
def _():
    from corner import corner

    return (corner,)


@app.cell
def _(corner, green, r_hat_mites, θ_bootstrap_arr, φ_hat_mites):
    cor = corner(θ_bootstrap_arr, smooth=True, labels=['r', 'ϕ'], show_titles=True, range=[(0, 2), (0, 2)])
    cor.axes[0].axvline(r_hat_mites, color=green)
    cor.axes[3].axvline(φ_hat_mites, color=green)
    cor.axes[2].plot(r_hat_mites, φ_hat_mites, '.', color=green)
    cor
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In our next meeting we will learn about the Bayesian approach to inference.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # References

    - Jake VanDerPlas's series of [blog posts on Frequentists vs. Bayesian inference](http://jakevdp.github.io/blog/2014/03/11/frequentism-and-bayesianism-a-practical-intro/)
    - Kass, Richard E. 2011. [Statistical inference: The big picture](http://www.stat.cmu.edu/~kass/papers/bigpic.pdf). Stat Sci. doi:10.1214/10-STS337
    - Bliss, C. I., and R. A. Fisher. 1953. [Fitting the Negative Binomial Distribution to Biological Data](https://doi.org/10.2307/3001850).  Biometrics. doi:10.2307/3001850
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
