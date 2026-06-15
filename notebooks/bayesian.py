import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.stats
    import scipy.optimize
    import seaborn as sns
    sns.set_context('talk')
    import warnings
    red, blue, green = sns.color_palette('Set1', 3)
    import os
    if os.path.basename(os.getcwd()) != 'notebooks':
        os.chdir('notebooks')
    return blue, green, mo, np, plt, red, scipy, sns


@app.cell
def _(np):
    rng = np.random.default_rng(1202)
    return (rng,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bayesian inference

    ## Yoav Ram
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the previous lecture we discussed the frequentist approach to statistical inference using maximum likelihood estimatio.
    Today we will discuss the Bayesian approach.

    Bayesian inference is a method of statistical inference in which Bayes' theorem is used to update the probability for a hypothesis as more evidence or information becomes available.

    # Bayes' theorem
    Consider the events $A$ and $B$, then Bayes' theorem states that

    $$
    P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}
    $$

    See animation on [Seeing Theory website](https://seeing-theory.brown.edu/bayesian-inference/index.html#section1).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Applied to model-based inference, we define:
    - $\theta$ - the model parameters
    - $X$ - the data

    and we have

    $$
    P(\theta \mid X) = \frac{P(X \mid \theta) P(\theta)}{P(X)}
    $$
    where
    - $P(\theta)$ is called the **prior probability** that formulates our beliefs about the model before seeing any data
    - $P(X \mid \theta)$ is the probability of observing $X$ given $\theta$, what we called the **likelihood** of $\theta$
    - $P(\theta \mid X)$ is called the **posterior probability**, that is, how our beliefs about the model changed due to observing the data
    - $P(X)$ is the probability of observing the data unconditioned on the model; we usually ignore it as it does not depend on the model

    In Bayesian inference we attempt to estimate the posterior distribution over the model parameters; this constrast with classical/frequentist approaches like *maximum likelihood* in which we attempt to estimate a point estimate of the parameters - a single parameter value.
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

    The question is, given this data $\{X_i\}$, what is our best estimate of $\mu$?
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
    _ax.set_ylabel('# Mites, $x_i$')
    _ax = _axes[1]
    _ax.hist(X_poi, bins=10, density=True)
    _ax.axvline(μ, linewidth=3, alpha=1, color=red)
    _ax.set_ylabel('Density')
    _ax.set_xlabel('# Mites, $x_i$')
    _fig.tight_layout()
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this toy example we already know the
    true value of $\mu$, but the question is this: **given our data $X$, what is our best estimate of the true $\mu$?**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We have previously developed the log-likelihood function:
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
    And we found that the maximum likelihood estimate $\hat{\mu}$ is the _arithmetic mean_.
    """)
    return


@app.cell
def _(X_poi, green, log_likelihood_poi, np, plt, red, sns, μ):
    μ_mle = X_poi.mean()
    print("μ = {} \nμ_mle = {:.4f}".format(μ, μ_mle))

    _μ_range_mle = np.linspace(μ_mle-2, μ_mle+2, 1000)
    plt.plot(_μ_range_mle, log_likelihood_poi(_μ_range_mle, X_poi), label='LL')
    plt.plot(μ, log_likelihood_poi(μ, X_poi), 'o', color=red, label=r'true $μ$')
    plt.plot(μ_mle, log_likelihood_poi(μ_mle, X_poi), 'o', color=green, label=r'$\hat{μ}_{mle}$')

    plt.xlabel(r"Expected # mites, $\mu$")
    plt.ylabel("Log-likelihood")
    plt.legend()
    sns.despine()
    return (μ_mle,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bayesian inference with direct computation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the Bayesian approach, we want to compute the  posterior distribution of the model parameter
    $$
    P(\mu \mid X) = \frac{P(X \mid \mu) P(\mu)}{P(X)},
    $$
    which reflects our knowledge or beliefe on the parameter $\mu$.

    This is important: we actually want to form a belief (or opinion) on any value of the $\mu$ parameter (which is expressed by the posterior probability $P(\mu \mid X)$), rather than just choosing the value that fits best to the data (which is what maximum likelihood does)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can't compute $P(X)$, but given a definition of the prior $P(\mu)$ and likelihood $P(X \mid \mu)$ we can compute the posterior $P(\mu \mid X)$ for any $\mu$ up to a constant -- that constant is $P(X)$.
    So if we then normalize we can get the posterior.

    Let's assume the prior is uniform in the positive values:

    $$
    P(\mu) = \begin{cases}
    1, & \mu > 0 \\
    0, & \text{otherwise}
    \end{cases}
    $$


    Therefore the log-prior is:

    $$
    logP(\mu) = \begin{cases}
    0, & \mu > 0 \\
    -\infty, & \text{otherwise}
    \end{cases}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We already have a definition for the log-likelihood in the form of the above `log_likelihood` function, which computes:
    $$
    logP(\mu \mid X) = \log{P(X|\mu)} + \log{P(\mu)} =
    \sum_{i=1}^{n}{x_i \log{\mu} -\mu -\log{(x_i!)}} + 0
    $$
    """)
    return


@app.cell
def _(log_likelihood_poi, np):
    @np.vectorize
    def log_prior_uniform(μ):
        return 0

    def log_posterior(μ, X):
        return log_prior_uniform(μ) + log_likelihood_poi(μ, X)

    return log_posterior, log_prior_uniform


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a one-dimensional problem, so we can work with a direct approach; that won't work with multi-dimensional problems, and therefore it is common to use sampling methods such as _Markov chain Monte Carlo_, or _MCMC_.

    Let's do it anyway.
    Since we can't compute for every positive $\mu$ lets just do it for $min(X) < \mu < max(X)$, as we can assume the posterior probability is very small for $\mu$ values that outside the range of the data.

    Our point estimate will be the maximum of the posterior (i.e. _MAP_), rather than that of the likelihood (although there is not differene in this case because of the uniform prior).
    """)
    return


@app.cell
def _(
    X_poi,
    log_likelihood_poi,
    log_posterior,
    log_prior_uniform,
    np,
    μ,
    μ_mle,
):
    μ_range_uniform = np.linspace(μ_mle-2, μ_mle+2, 1000)
    pri_uniform = np.exp(log_prior_uniform(μ_range_uniform))
    lik_uniform = np.exp(log_likelihood_poi(μ_range_uniform, X_poi))
    post_uniform = np.exp(log_posterior(μ_range_uniform, X_poi))
    μ_hat_uniform = μ_range_uniform[post_uniform.argmax()] # maximum a posterioi estimate
    print("μ = {} \nμ_hat = {:.4f}".format(μ, μ_hat_uniform))
    return (
        lik_uniform,
        post_uniform,
        pri_uniform,
        μ_hat_uniform,
        μ_range_uniform,
    )


@app.cell
def _(
    X_poi,
    green,
    lik_uniform,
    log_likelihood_poi,
    log_posterior,
    np,
    plt,
    post_uniform,
    pri_uniform,
    red,
    sns,
    μ,
    μ_hat_uniform,
    μ_range_uniform,
):
    plt.plot(μ_range_uniform, pri_uniform/pri_uniform.sum(), label='prior')
    plt.plot(μ_range_uniform, lik_uniform/lik_uniform.sum(), lw=3, label='likelihood')
    plt.plot(μ_range_uniform, post_uniform/post_uniform.sum(), ls='--', label='posterior')
    plt.plot(μ, np.exp(log_posterior(μ, X_poi))/post_uniform.sum(), 'o', color=red, label=r'$\mu$')
    plt.plot(μ_hat_uniform, np.exp(log_likelihood_poi(μ_hat_uniform, X_poi))/lik_uniform.sum(), 'o', color=green, label=r'$\hat{\mu}$')

    plt.xlabel(r"Expected # mites, $\mu$")
    plt.ylabel("Probability")
    plt.legend(bbox_to_anchor=(1, 0.8))
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's change the prior to something more informative: say we think the number of mites on a leaf should be $9 \pm 2$, because of some previous study. We can then use an informative prior distribution,
    $$
    \mu \sim N(9, 2)
    $$
    Now we can plot the prior, likelihood, and posterior again.
    """)
    return


@app.cell
def _(log_likelihood_poi, scipy):
    def log_prior_normal(μ):
        return scipy.stats.norm(loc=9, scale=2).logpdf(μ)

    def log_posterior_normal(μ, X):
        return log_prior_normal(μ) + log_likelihood_poi(μ, X)

    return log_posterior_normal, log_prior_normal


@app.cell
def _(
    X_poi,
    green,
    log_likelihood_poi,
    log_posterior_normal,
    log_prior_normal,
    np,
    plt,
    red,
    sns,
    μ,
    μ_mle,
):
    μ_range_normal = np.linspace(μ_mle-2, μ_mle+2, 1000)
    pri_normal = np.exp(log_prior_normal(μ_range_normal))
    lik_normal = np.exp(log_likelihood_poi(μ_range_normal, X_poi))
    post_normal = np.exp(log_posterior_normal(μ_range_normal, X_poi))
    μ_hat_normal = μ_range_normal[post_normal.argmax()]  # maximum a posterioi estimate
    print('μ = {} \nμ_hat = {:.4f}'.format(μ, μ_hat_normal))
    plt.plot(μ_range_normal, pri_normal / pri_normal.sum(), label='prior')
    plt.plot(μ_range_normal, lik_normal / lik_normal.sum(), lw=3, label='likelihood')
    plt.plot(μ_range_normal, post_normal / post_normal.sum(), ls='--', label='posterior')
    plt.plot(μ, np.exp(log_posterior_normal(μ, X_poi)) / post_normal.sum(), 'o', color=red, label='$\\mu$')
    plt.plot(μ_hat_normal, np.exp(log_posterior_normal(μ_hat_normal, X_poi)) / post_normal.sum(), 'o', color=green, label='$\\hat{\\mu}$')
    plt.xlabel('Expected # mites, $\\mu$')
    plt.ylabel('Probability')
    plt.legend(bbox_to_anchor=(1, 0.8))
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Monte Carlo: Sampling instead of computing

    For anything that has more than one or two parameters we cannot do the above exhustive method as the complexity increases with the number of parameters (or the dimension of the parameter space).

    A common approach is therefore to use *Monte Carlo* or sampling methods.
    With Monte Carlo, instead of directly computing the posterior distribution, we indirectly sample from the posterior distribution.

    **Note**: this is an important shift in our methodology. **Instead of computing, we sample**. That is, instead of finding the function $P(\mu \mid X)$, we want to find a set of $m$ samples $\{\mu_i\}_{i=1}^{m}$ from the posterior such that $\mu_i \sim P(\mu \mid X)$.

    Monte Carlo methods are used in a variety of applications other then posterior sampling.

    For example, consider the function $f(x) = e^{-2x}$.
    """)
    return


@app.cell
def _(np, plt):
    def f(x):
        return np.exp(-2 * x)
    _x = np.linspace(0, 1)
    plt.plot(_x, f(_x))
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()
    return (f,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we wish to compute the integral $\int_0^1{f(x)}$, we can draw random points in the unit square and compute the fraction of point below the function curve. This would approximate the integral value.
    """)
    return


@app.cell
def _(f, np, plt, rng):
    _N = 10000
    _x, _y = rng.random((2, _N))
    _accepted = _y < f(_x)
    print('estimate:\t', _accepted.mean())
    print('real:\t\t', 0.5 - 1 / (2 * np.exp(2)))
    plt.plot(_x, _y, '.', markersize=2)
    plt.plot(_x[_accepted], _y[_accepted], '.', markersize=2)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This method of sampling is called __rejection sampling__ and we can employ if for sampling from the posterior distribution (instead of the area below `f(x)`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rejection sampling

    Given empirical data $X$, a model parameterized by the vector $\theta$, a prior $P(\theta)$, and likelihood $P(X \mid \theta)$, the following describes the *rejection sampling algorithm*:

    1. Generate candidate parameter value from the prior $\theta^* \sim P(\theta)$
    1. Compute the likelihood for the candidate parameter $P(X \mid \theta^*)$
    1. Accept $\theta^*$ with probability proportional to $P(X \mid \theta^*)$.

    This process effectivelty samples from the posterior, as the probability to draw $\theta^*$ proportinal to $P(X \mid \theta^*) P(\theta^*)$.

    Therefore, the collection of accepted $\theta^*$ values _approximates_ the posterior distribution $P(\theta \mid x)$.

    The proportion of accepted values is caleld the __acceptance rate__, and it can be very low if the prior is very different from the posterior (which frequently occurs if we don't know much about the parameter values). For example, if we run the following with a "flat" (uniform) prior, we will get an acceptance rate of about 1:100,000.
    With an informative prior - a Gaussian around the mean of the data - we still only have an acceptance rate of about 1:10,000.

    So we have to take at least 100,000 samples, and the running time is therefore long.
    """)
    return


@app.cell
def _(X_poi, log_likelihood_poi, np, rng, scipy):
    _N = 10000
    prior = scipy.stats.norm(9, 2)
    μs = prior.rvs(_N, random_state=rng)
    log_liks = log_likelihood_poi(μs, X_poi)
    liks = np.exp(log_liks)
    liks = liks / liks.sum()
    liks = liks / prior.pdf(μs)
    randoms = rng.random(_N)
    accepted = randoms < liks
    _accept_rate = accepted.mean()
    print('Acceptance rate: ', _accept_rate)
    return accepted, liks, μs


@app.cell
def _(accepted, μ, μs):
    μ_hat_rejection = μs[accepted].mean()
    print('μ = {} \nμ_hat = {:.4f}'.format(μ, μ_hat_rejection))
    return


@app.cell
def _(accepted, liks, plt, sns, μs):
    plt.plot(μs[~accepted], liks[~accepted], '.', label='rejected')
    plt.plot(μs[accepted], liks[accepted], '.', label='accepted')
    plt.legend(bbox_to_anchor=(1, 0.8))
    plt.xlabel('$\\mu$')
    plt.ylabel('Probability')
    sns.despine()
    plt.show()
    return


@app.cell
def _(accepted, plt, sns, μs):
    plt.hist(μs, bins=50, density=True, label='prior')
    plt.hist(μs[accepted], bins=20, density=True, alpha=0.5, label='posterior')
    plt.legend()
    plt.xlabel('$\\mu$')
    plt.ylabel('Probability')
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The problem with the rejection method is that the acceptance rate can be very low, which requires us to draw many samples from the prior, and compute the log-likelihood many times, and this is very wasteful.

    We deal with the low acceptance rate is in the next section.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Markov chain Monte Carlo: MCMC

    Markov chain Monte Carlo is a family of clever algorithms for sampling with the prior with a much higher acceptance rate by concentrating on the areas of high likelihood.

    We create "chains" of accepted parameter samples of length $N$ using the following algorithm.

    The most well-known, maybe, of these algorithms is the **Metropolis–Hastings** algorithm.

    At iteration $i$, given the previous parameter value $\theta_i$, we
    1. Generate a candidate parameter value $\theta^*$ from a proposal distribution $\theta^* \sim N(\theta_i, \eta)$.
    1. Compute the likelihood $P(X \mid \theta^*)$.
    1. Set the acceptance probability $\alpha = \frac{P(\theta^* \mid X)}{P(\theta_i \mid X)} = \frac{P(X \mid \theta^*)P(\theta^*)}{P(X \mid \theta_i)P(\theta_i)}$ to the ratio of posterior probabilities.
    1. Set $\theta_{i+1} = \theta^*$ with probability $min(1,\alpha)$ (i.e. accept $\theta^*$), otherwise set $\theta_{i+1} = \theta_i$ (i.e. reject $\theta^*$ and keep $\theta_i$ again).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    _Note:_
    in the more general case, we can use a proposal distribution $q(\theta \mid \theta_i)$ and then we set $\alpha = \frac{P(X \mid \theta^*) q(\theta_i \mid \theta^*)}{P(X \mid \theta_i) q(\theta^* \mid \theta_i)}$. If we use the gaussian proposal distribution, then it is symmetric around the mean $q(\theta_i \mid \theta^*) = q(\theta^* \mid \theta_i)$, and $\alpha$ simplifies.

    This sampling algorithm is much more efficient than the rejection sampling, as it is able to "spend more time" in areas of high likelihood.

    However, this algorithm can get stuck on areas of low likelihood.
    """)
    return


@app.cell
def _(X_poi, log_likelihood_poi, log_prior_normal, np, rng):
    η = 0.5
    _N = 10000
    burnin = _N // 2
    _accept = 0
    μ_chain_mcmc = np.empty(_N)
    μ_chain_mcmc[0] = 7
    _logposterior = log_likelihood_poi(μ_chain_mcmc[0], X_poi) + log_prior_normal(μ_chain_mcmc[0])
    _proposals = rng.normal(0, η, size=_N)
    _loguniforms = np.log(rng.random(size=_N))
    logposteriors = np.zeros(_N)
    for _i in range(1, _N):
        _μ_candidate = μ_chain_mcmc[_i - 1] + _proposals[_i]
        _logposterior_candidate = log_likelihood_poi(_μ_candidate, X_poi) + log_prior_normal(_μ_candidate)
        _logα = _logposterior_candidate - _logposterior
        if _loguniforms[_i] < _logα:
            _logposterior = _logposterior_candidate
            μ_chain_mcmc[_i] = _μ_candidate
            _accept = _accept + 1
        else:
            μ_chain_mcmc[_i] = μ_chain_mcmc[_i - 1]
        logposteriors[_i] = _logposterior
    _accept_rate = _accept / _N
    print('Acceptance rate:', _accept_rate)
    return burnin, logposteriors, η, μ_chain_mcmc


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that the acceptance rate is much higher.

    Lets look at the chain using a **trace plot**. It shows the sample values over time, and we would like to make sure that after the burnin time (represented here in shaded area) the chain has "stabilized": it fluctuates, but it no longer has a trend.
    """)
    return


@app.cell
def _(burnin, plt, sns, μ_chain_mcmc):
    plt.plot(μ_chain_mcmc, lw=1)
    plt.axhline(μ_chain_mcmc[burnin:].mean(), color='k')
    plt.fill_betweenx(plt.ylim(), 0, burnin, color='k', alpha=0.25)
    plt.xlabel('Iterations')
    plt.ylabel('Sample')
    plt.xlim(0, None)
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This looks good - the samples fluctuate around their mean (black line), and we can see that the chain seemed to have settled after the burnin time (shaded area).

    Lets get rid of the burnin samples.
    """)
    return


@app.cell
def _(burnin, μ_chain_mcmc):
    μ_samples_mcmc = μ_chain_mcmc[burnin:]
    return (μ_samples_mcmc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How did the MCMC proceed through the likelihood space?

    You can see that most of the time the chain was at high log-likelihood, but occassionaly it traveled through lower likelihood reigons of the $\mu$ range.
    """)
    return


@app.cell
def _(burnin, logposteriors, plt):
    plt.plot(logposteriors[burnin:], lw=1)
    plt.xlabel('Iteration')
    plt.ylabel('Log posterior')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's take the mean of the post-burnin samples as our MAP estimate.

    That makes sense if the posterior is symmetric and unimodal - we can check that.
    """)
    return


@app.cell
def _(green, plt, red, sns, μ, μ_samples_mcmc):
    μ_hat_mcmc = μ_samples_mcmc.mean()
    σ_hat_mcmc = μ_samples_mcmc.std()
    print('μ = {} \nμ_hat = {:.4f} +/- {:.4f}'.format(μ, μ_hat_mcmc, σ_hat_mcmc))
    plt.hist(μ_samples_mcmc, bins=50, alpha=0.75, label='Posterior')
    plt.axvline(μ, color=red, label='$\\mu$')
    plt.axvline(μ_hat_mcmc, color=green, label='$\\hat{\\mu}$')
    plt.axvline(μ_hat_mcmc + σ_hat_mcmc, color='k', ls='--')
    plt.axvline(μ_hat_mcmc - σ_hat_mcmc, color='k', ls='--')
    plt.xlim(8.5, 12)
    plt.xlabel('$\\mu$')
    plt.ylabel('Probability')
    plt.legend()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Other interesting diagnostics we can do are to look at the differences between consecutive samples.
    Their distribution should match the proposal distribution $N(0, \eta)$, ploted below as a black line.
    """)
    return


@app.cell
def _(np, plt, scipy, η, μ_samples_mcmc):
    diff = μ_samples_mcmc[1:] - μ_samples_mcmc[:-1]
    plt.hist(diff, bins=50, density=True)
    diff_range = np.linspace(-η * 5, η * 5)
    plt.plot(diff_range, scipy.stats.norm.pdf(diff_range, 0, η), color='k')
    plt.xlim(-η * 5, η * 5)
    plt.xlabel('$\\mu_{i+1}-\\mu_i$')
    plt.ylabel('Frequency')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is important because it means that our samples are correlated. We want to make sure that they are weakly correlated -- that the correlation is lost after a few iterations

    We can check the [autocorrelation](https://en.wikipedia.org/wiki/Autocorrelation), which is a measure of how much sample $i$ is correlated with sample $i+k$ (with lag $k$). We want to check that the correlation quickly goes down with $k$.

    We can see that here that is the case and that the autocorrelation goes down with the lag $k$.
    """)
    return


@app.cell
def _(np, plt, sns, μ_samples_mcmc):
    autocorr = np.correlate(μ_samples_mcmc, μ_samples_mcmc, mode='full')
    autocorr = autocorr / autocorr.max()
    autocorr = autocorr[autocorr.size // 2:]
    plt.plot(autocorr)
    plt.xlabel('lag $k$')
    plt.ylabel('$cor(\\mu_{i+k}, \\; \\mu_i)$')
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## emcee: The MCMC Hammer

    Now that we understand how sampling could work, we will use a more sophisticated an [affine-invariant ensemble sampler for Markov chain Monte Carlo (MCMC)](https://arxiv.org/abs/1202.3665): the **[emcee](https://emcee.readthedocs.io/)** package.

    To setup the sampler, we generate some random starting guesses for multiple chains of samples.
    """)
    return


@app.cell
def _():
    import emcee

    return (emcee,)


@app.cell
def _(rng):
    ndim = 1  # number of parameters in the model
    nwalkers = 50  # number of MCMC walkers
    nsteps = 10000 // nwalkers  # number of MCMC steps to take
    nburn = nsteps // 2  # "burn-in" period to let chains stabilize

    # we'll start at random locations between 0 and 2000
    guesses = 20 * rng.random((nwalkers, ndim))
    return guesses, nburn, ndim, nsteps, nwalkers


@app.cell
def _(X_poi, emcee, guesses, log_posterior, nburn, ndim, np, nsteps, nwalkers):
    # avoid negative μ values
    def log_posterior_(μ, X):
        if μ < 0: return -np.inf
        return log_posterior(μ, X)

    sampler = emcee.EnsembleSampler(
        nwalkers=nwalkers,
        ndim=ndim,
        log_prob_fn=log_posterior_,
        args=[X_poi]
    )
    sampler.run_mcmc(
        initial_state=guesses,
        nsteps=nsteps
    )

    # sampler.chain.shape = (nwalkers, nsteps, ndim)
    # discard burn-in points and flatten with ravel()
    μ_samples_emcee = sampler.chain[:, nburn:, :].ravel()
    return sampler, μ_samples_emcee


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If this all worked correctly, the array `μ_samples_emcee` should contain a series of 5,000 points drawn from the posterior. Let's plot them and check.
    """)
    return


@app.cell
def _(μ, μ_samples_emcee):
    μ_hat_emcee = μ_samples_emcee.mean()
    σ_hat_emcee = μ_samples_emcee.std()
    print('μ = {} \nμ_hat = {:.4f} +/- {:.4f}'.format(μ, μ_hat_emcee, σ_hat_emcee))
    return μ_hat_emcee, σ_hat_emcee


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before examining the posterior distribution, lets look at the trace plot, which shows:
    1. the posterior distributions for each chain
    1. the samples for each chain -- the $\mu$ sample values across time.
    """)
    return


@app.cell
def _(blue, nburn, plt, sampler, sns):
    _fig, _axes = plt.subplots(1, 2, figsize=(10, 4))
    _axes[0].plot(sampler.chain[:, :, 0].T, alpha=0.25)
    _axes[0].axvline(nburn, color=blue)
    _axes[0].set_ylabel('μ')
    sns.kdeplot(sampler.chain[:, nburn:, 0], alpha=0.25, legend=False, ax=_axes[1])
    _axes[1].set_xlabel('μ')
    _fig.tight_layout()
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can see here why we need to remove the initial `nburn` samples (or maybe less of them).

    Now we can plot the posterior distribution, together with the estimate (green) $\pm$ standard deviation (dashed black lines), the true value (red). We can see that the true value is within the one standard deviation of the estimate, which is pretty good.
    """)
    return


@app.cell
def _(green, plt, red, sns, μ, μ_hat_emcee, μ_samples_emcee, σ_hat_emcee):
    plt.hist(μ_samples_emcee, bins=50, alpha=0.5)
    plt.axvline(μ, color=red, label='$\\mu$')
    plt.axvline(μ_hat_emcee, color=green, label='$\\hat{\\mu}$')
    plt.axvline(μ_hat_emcee + σ_hat_emcee, color='k', ls='--')
    plt.axvline(μ_hat_emcee - σ_hat_emcee, color='k', ls='--')
    plt.xlabel(μ)
    plt.ylabel('Posterior')
    plt.legend()
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For this simple problem, both approaches yield the same result, more or less.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## PyMC: probablistic programming in Python

    [PyMC](http://pymc.io) is a Python library for probabilistic programming, which allows users to define, fit, and analyze Bayesian models using a variety of numerical methods. It is built on top of NumPy and other scientific libraries, and is designed to be easy to use and flexible, while providing advanced features such as Markov chain Monte Carlo (MCMC) sampling and variational inference. PyMC is open-source software and is widely used in a variety of fields, including machine learning, statistics, and bioinformatics.

    [Arviz](http://arviz.org) provides tools for exploratory analysis of Bayesian models. It works well with PyMC, as well as other libraries.
    """)
    return


@app.cell
def _():
    import pymc as pm
    import arviz as az
    print("PyMC", pm.__version__, "Arviz", az.__version__)
    return az, pm


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here we build the model and sample from the posterior using the default sampler, [NUTS](http://www.stat.columbia.edu/~gelman/research/published/nuts.pdf).

    **Note:** this cell fails in VS Code but succeeds in Marimo editor.
    """)
    return


@app.cell
def _(X_poi, pm):
    with pm.Model() as poisson_model:
        _μ_ = pm.Normal('μ', mu=9, sigma=2)  # prior
        _X_obs = pm.Poisson('X_obs', mu=_μ_, observed=X_poi)  # poisson model
        idata_nuts = pm.sample(draws=10000)
    return idata_nuts, poisson_model


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here are the trace plot (on the right) and the posterior of each chain (on the left), to assess convergence. Looking good.
    """)
    return


@app.cell
def _(az, idata_nuts):
    az.plot_trace(idata_nuts);
    return


@app.cell
def _(az, idata_nuts, μ):
    print('μ = {}'.format(μ))
    isummary_nuts = az.summary(idata_nuts, round_to=2)
    μ_hat_nuts = isummary_nuts.loc['μ', 'mean']
    isummary_nuts
    return (μ_hat_nuts,)


@app.cell
def _(az, green, idata_nuts, plt, red, μ, μ_hat_nuts):
    az.plot_posterior(idata_nuts, round_to=4)
    plt.axvline(μ, color=red)
    plt.axvline(μ_hat_nuts, color=green)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Variational inference with ADVI

    PyMC supports various [Variational Inference techniques](https://en.wikipedia.org/wiki/Variational_Bayesian_methods). While these methods are faster than samppling approaches, they are often also less accurate and can lead to biased inference. The main entry point is `pymc.fit()` (see [tutorial](https://www.pymc.io/projects/examples/en/latest/variational_inference/variational_api_quickstart.html)) with uses [Automatic Differentiation Variational Inference](https://arxiv.org/abs/1603.00788).
    """)
    return


@app.cell
def _(pm, poisson_model):
    with poisson_model:
        approx = pm.fit(n=50000)
    return (approx,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result here is *not* a sample from the posterior, but rather an [approximation](https://www.pymc.io/projects/docs/en/latest/api/generated/pymc.Approximation.html) of the posterior.

    We can check for convergence by looking at the history of the loss function.
    """)
    return


@app.cell
def _(approx, np, plt):
    elbo = np.log(approx.hist)

    plt.plot(elbo, lw=0.5)
    plt.ylabel('Loss function (log-ELBO)');
    return (elbo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It's very noisy so it's hard to say. Let's take a sliding average over it to smooth it a bit.
    We also focus on the last 10,000 iterations of the fitting.
    """)
    return


@app.cell
def _(elbo, np, plt):
    sliding_avg = np.lib.stride_tricks.sliding_window_view(elbo, 100).mean(axis=-1)
    _fig, _axes = plt.subplots(1, 2, figsize=(10, 4))
    _axes[0].plot(sliding_avg, lw=0.5)
    _axes[0].set_ylabel('Loss function (log-ELBO)')
    _axes[0].set_ylim(4.91, 4.96)
    _axes[1].plot(np.arange(elbo.size - 10000, elbo.size), sliding_avg[-10000:], lw=0.5)
    _axes[1].set_ylim(4.914, 4.918)
    _fig.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To examine the posterior distribution we now need to sample from the approximation, at which point we can use the returned `InferenceData` just as we did with the sampling approach.
    """)
    return


@app.cell
def _(approx, az, μ):
    idata_advi = approx.sample(5000)
    az.plot_posterior(idata_advi)
    az.summary(idata_advi)
    μ_samples_advi = idata_advi.posterior['μ'].to_numpy()
    μ_hat_advi = μ_samples_advi.mean()
    σ_hat_advi = μ_samples_advi.std()
    print('μ = {} \nμ_hat = {:.2f} +/- {:.2f}'.format(μ, μ_hat_advi, σ_hat_advi))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We got similar results to the NUTS results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Over-dispersed Poisson model for count data

    Here we assume that the measurements $\{x_i\}$ are still drawn from a Poisson distribution, but the expected values $\mu_i$ changes from leaf to leaf.
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
def _(np):
    _rng = np.random.default_rng(87)
    n_gamma = 150
    θ = r, φ = (5, 2)
    _μi = _rng.gamma(r, scale=φ, size=n_gamma)
    X_gamma = _rng.poisson(_μi)
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
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Again, we have already written the log-likelihood function:
    """)
    return


@app.cell
def _(X_gamma, np, scipy, θ):
    @np.vectorize(signature='(2)->()', excluded=(1,))
    def log_likelihood_negbin(θ, X):
        r, φ = θ
        p = 1 / (φ + 1)
        return scipy.stats.nbinom(r, p).logpmf(X).sum()
    print(log_likelihood_negbin(θ, X_gamma))

    def neg_log_likelihood_negbin(θ, X):
        return -log_likelihood_negbin(θ, X)
    print(neg_log_likelihood_negbin(θ, X_gamma))
    return (neg_log_likelihood_negbin,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We used SciPy's optimization routines to find the maximum likelihood (and then bootstrap to find confidence intervals).
    """)
    return


@app.cell
def _(X_gamma, neg_log_likelihood_negbin, r, scipy, φ):
    def mle(X, verbose=False, full_path=False):
        r_guess = X.mean() ** 2 / (X.var(ddof=1) - X.mean())  # eq 3 in Bliss and Fisher 1953
        φ_guess = X.mean() / r_guess
        return scipy.optimize.fmin(func=neg_log_likelihood_negbin, x0=(r_guess, φ_guess), args=(X,), disp=verbose, retall=full_path)
    θ_hat_mle = mle(X_gamma, verbose=True)
    r_hat_mle, φ_hat_mle = θ_hat_mle  # function to minimize with respect to first argument
    print('r = {} \tr_hat = {:.4f}\nϕ = {}\tϕ_hat = {:.4f}'.format(r, r_hat_mle, φ, φ_hat_mle))  # initial guess  # additional arguments to func  # no prints
    return r_hat_mle, φ_hat_mle


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inference on synthetic data

    This is very similar to the previous case, with minor modifications for the compound model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use uninformative priors:
    $$
    r \sim U(0, 10) \\
    \phi \sim U(0, 5)
    $$

    Note that here we need to sample a separate $\mu_i$ for each data point $i$, so we need to add a new "lead" dimension to the Poisson distribution.
    We do this by specifying a `coords` for the `Model` constructor, and then specifiying `dims=leaf` to the `Poisson` distribution.
    """)
    return


@app.cell
def _(X_gamma, n_gamma, pm):
    with pm.Model(coords={'leaf': range(n_gamma)}) as gamma_poisson_model:
        _r = pm.Uniform('r', lower=0, upper=10)
        _φ = pm.Uniform('ϕ', lower=0, upper=5)
        _μ = pm.Gamma('μ', alpha=_r, beta=1/_φ, dims='leaf')
        _X_obs = pm.Poisson('X_obs', mu=_μ, observed=X_gamma)
        idata_gamma_poisson = pm.sample(draws=10000)
    return (idata_gamma_poisson,)


@app.cell
def _(az, idata_gamma_poisson, plt):
    az.plot_trace(idata_gamma_poisson, var_names=['r', 'ϕ'])
    plt.tight_layout()
    return


@app.cell
def _(az, idata_gamma_poisson, r, r_hat_mle, φ, φ_hat_mle):
    print('True: r={}, ϕ={}'.format(r, φ))
    print('MLE: r_mle={:.3f}, ϕ_mle={:.3f}'.format(r_hat_mle, φ_hat_mle))
    isummary_gamma = az.summary(idata_gamma_poisson, var_names=['r', 'ϕ'], round_to=4)
    r_hat_gamma = isummary_gamma.loc['r', 'mean']
    φ_hat_gamma = isummary_gamma.loc['ϕ', 'mean']
    isummary_gamma
    return


@app.cell
def _(az, green, idata_gamma_poisson, plt, r, red, φ):
    _grid = az.plot_pair(idata_gamma_poisson, kind='kde', var_names=['r', 'ϕ'], marginals=True, point_estimate='mean', point_estimate_kwargs=dict(lw=1), point_estimate_marker_kwargs=dict(color=green, marker='o', zorder=100, ec='k'), reference_values={'r': r, 'ϕ': φ}, reference_values_kwargs=dict(color=red))
    _grid[0, 0].set_xlim(2, 8)
    _grid[1, 1].set_ylim(1, 3.5)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's look at the posteriors of the different $\mu$.
    """)
    return


@app.cell
def _(az, idata_gamma_poisson, plt, r, red, φ):
    az.plot_forest(idata_gamma_poisson, var_names=['μ'], kind='forestplot', combined=True);
    plt.axvline(r * φ, color=red);
    plt.axvline(r * φ + (r * φ * φ)**0.5, color=red, ls='dashed')
    plt.axvline(r * φ - (r * φ * φ)**0.5, color=red, ls='dashed')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inference on mites data

    Let's try out this over-dispersed Poisson model on our real "mites on leaves" data.

    We reload our data.
    """)
    return


@app.cell
def _(np, plt):
    X_mites = np.loadtxt('../data/mites.csv', delimiter=',')
    plt.hist(X_mites, range(8))
    plt.axvline(X_mites.mean(), color='k')
    plt.xlabel('# Mites on leaf')
    plt.ylabel('# leaves')
    return (X_mites,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The MLE estimate was $\hat r \approx 1.02$ and $\hat \phi \approx 0.9$, so we can set the priors a bit narrower.
    """)
    return


@app.cell
def _(X_mites, pm):
    with pm.Model(coords={'leaf': range(X_mites.size)}) as mites_model:
        _r_ = pm.Uniform('r', lower=0, upper=3)
        _φ_ = pm.Uniform('ϕ', lower=0, upper=2)
        _μ_ = pm.Gamma('μ', alpha=_r_, beta=1 / _φ_, dims='leaf')
        _X_obs = pm.Poisson('X_obs', mu=_μ_, observed=X_mites)
        idata_mites = pm.sample(draws=50000)
    return (idata_mites,)


@app.cell
def _(az, idata_mites, plt):
    az.plot_trace(idata_mites, var_names=['r', 'ϕ'])
    plt.tight_layout();
    return


@app.cell
def _(az, idata_mites):
    isummary_mites = az.summary(idata_mites, var_names=['r', 'ϕ'], round_to=4)
    isummary_mites
    return (isummary_mites,)


@app.cell
def _(isummary_mites):
    r_hat_mites = isummary_mites.loc['r', 'mean']
    φ_hat_mites = isummary_mites.loc['ϕ', 'mean']
    return r_hat_mites, φ_hat_mites


@app.cell
def _(az, green, idata_mites, plt):
    _grid = az.plot_pair(idata_mites, kind='kde', var_names=['r', 'ϕ'], marginals=True, point_estimate='mean', point_estimate_kwargs=dict(lw=1), point_estimate_marker_kwargs=dict(color=green, marker='o', zorder=100, ec='k'))
    plt.show()
    return


@app.cell
def _(X_mites, green, plt, r_hat_mites, φ_hat_mites):
    plt.hist(X_mites, range(8))
    plt.axvline(X_mites.mean(), color='k')
    plt.axvline(r_hat_mites * φ_hat_mites, color=green)
    plt.xlabel('# Mites on leaf')
    plt.ylabel('# leaves')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # References

    - Jake VanDerPlas's series of [blog posts on Bayesian inference](http://jakevdp.github.io/blog/2014/03/11/frequentism-and-bayesianism-a-practical-intro/)
    - Cam Davidson-Pilon's book [Bayesian Methods for Hackers](http://camdavidsonpilon.github.io/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/)
    - [emcee](https://emcee.readthedocs.io/): the MCMC Hammer
    - [PyMC](https://www.pymc.io): probabilistic programming for Python
    - [corner](http://corner.readthedocs.io/): plotting joint and marginal density plots
    - [ArviZ](https://arviz-devs.github.io/arviz): plotting MCMC results
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Colophon
    This notebook was written by [Yoav Ram](http://www.yoavram.com).

    This work is licensed under a CC BY-NC-SA 4.0 International License.
    """)
    return


if __name__ == "__main__":
    app.run()
