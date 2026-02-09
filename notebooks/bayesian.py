import marimo

__generated_with = "0.19.8"
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
    from numba import NumbaDeprecationWarning
    warnings.simplefilter('ignore', NumbaDeprecationWarning)
    red, blue, green = sns.color_palette('Set1', 3)
    return blue, green, mo, np, plt, red, scipy, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![Py4Eng](img/logo.png)

    # Bayesian inference

    ## Yoav Ram
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the previous lecture we discusses the frequentist approach to statistical inference using maximum likelihood.
    Today we will discuss the Bayesian approach.

    Bayesian inference is a method of statistical inference in which Bayes' theorem is used to update the probability for a hypothesis as more evidence or information becomes available.

    # Bayes' theorem
    Consider the events $A$ and $B$, then Bayes' theorem states that

    $$
    P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}
    $$
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

    Denote the number of leaves by $n$, where the $i^{\rm th}$ measurement $X_i$ reports the observed number of mites on leaf $i$.
    We assume that $X_i$ is Poisson-distributed around the expected number of mites $\mu$,
    $$
    X_i \sim Poi(\mu)
    $$

    So $Poi(\mu)$ is our **model**, and $\{X_i\}$ is the data.

    The question is, given this data $\{X_i\}$, what is our best estimate of $\mu$?
    And the next question would be: does the model provide a good fit to the data?

    Generating this estimate is the objective of **statistical inference**: making conclusions on observable phenomea by applying mathematical methods to data and models.

    ## Synthetic data from Poisson model

    We start by simulating data before using real data.
    """)
    return


@app.cell
def _(np):
    np.random.seed(1)

    # expected number of mites on a leaf
    μ = 10  
    # number of measurements
    n = 50 
    # n measurements of the mites
    X = np.random.poisson(μ, size=n)
    return X, n, μ


@app.cell
def _(X, n, np, plt, red, sns, μ):
    _fig, _axes = plt.subplots(1, 2, figsize=(8, 4))
    _ax = _axes[0]
    _ax.plot(np.arange(n), X, '.k')
    _ax.axhline(μ, linewidth=3, color=red)
    _ax.set_xlabel('Leaf, $i$')
    _ax.set_ylabel('# Mites, $X_i$')
    _ax = _axes[1]
    _ax.hist(X, bins=10, density=True)
    _ax.axvline(μ, linewidth=3, alpha=1, color=red)
    _ax.set_ylabel('Density')
    _ax.set_xlabel('# Mites, $X_i$')
    _fig.tight_layout()
    sns.despine()
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
    We have previously developed the log-likelihood function:
    """)
    return


@app.cell
def _(np, scipy):
    def log_likelihood(μ, X):
         return scipy.stats.poisson(μ).logpmf(X).sum()
    log_likelihood = np.vectorize(log_likelihood, excluded=(1,))
    return (log_likelihood,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And we found that the maximum likelihood estimate $\hat{\mu}$ is the _arithmetic mean_.
    """)
    return


@app.cell
def _(X, green, log_likelihood, np, plt, red, sns, μ):
    μ_mle = X.mean()
    print("μ = {} \nμ_mle = {:.4f}".format(μ, μ_mle))

    X_range = np.linspace(μ_mle-2, μ_mle+2, 1000)
    plt.plot(X_range, log_likelihood(X_range, X), label='LL')
    plt.plot(μ, log_likelihood(μ, X), 'o', color=red, label=r'true $μ$')
    plt.plot(μ_mle, log_likelihood(μ_mle, X), 'o', color=green, label=r'$\hat{μ}_{mle}$')

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
    P(\mu = u) = \begin{cases}
    1, & u > 0 \\
    0, & \text{otherwise}
    \end{cases}
    $$


    Therefore the log-prior is:

    $$
    logP(\mu = x) = \begin{cases}
    0, & x > 0 \\
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
    \sum_{i=1}^{n}{X_i \log{\mu} -\mu -\log{(X_i!)}} + 0
    $$
    where $X_i$ ($1 \le i \le n$) are the data points in $X$ and $\mu>0$.
    """)
    return


@app.cell
def _(log_likelihood, np):
    @np.vectorize
    def log_prior(μ):
        return 0

    def log_posterior(μ, X):
        return log_prior(μ) + log_likelihood(μ, X)

    return log_posterior, log_prior


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
def _(X, log_likelihood, log_posterior, log_prior, np, μ, μ_mle):
    μ_range = np.linspace(μ_mle-2, μ_mle+2, 1000)
    pri = np.exp(log_prior(μ_range))
    lik = np.exp(log_likelihood(μ_range, X))
    post = np.exp(log_posterior(μ_range, X))
    μ_hat = μ_range[post.argmax()] # maximum a posterioi estimate
    print("μ = {} \nμ_hat = {:.4f}".format(μ, μ_hat))
    return lik, post, pri, μ_hat, μ_range


@app.cell
def _(
    X,
    green,
    lik,
    log_likelihood,
    log_posterior,
    np,
    plt,
    post,
    pri,
    red,
    sns,
    μ,
    μ_hat,
    μ_range,
):
    plt.plot(μ_range, pri/pri.sum(), label='prior')
    plt.plot(μ_range, lik/lik.sum(), lw=3, label='likelihood')
    plt.plot(μ_range, post/post.sum(), ls='--', label='posterior')
    plt.plot(μ, np.exp(log_posterior(μ, X))/post.sum(), 'o', color=red, label=r'$\mu$')
    plt.plot(μ_hat, np.exp(log_likelihood(μ_hat, X))/lik.sum(), 'o', color=green, label=r'$\hat{\mu}$')

    plt.xlabel(r"Expected # mites, $\mu$")
    plt.ylabel("Probability")
    plt.legend(bbox_to_anchor=(1, 0.8))
    sns.despine()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's change the prior to something more informative: say we think the number of mites on a leaf should be $9 \pm 2$, because of some previous study. We can then use an informative prior distribution,
    $$
    \mu \sim N(\mu=9, \sigma=2)
    $$
    Now we can plot the prior, likelihood, and posterior again.
    """)
    return


@app.cell
def _(scipy):
    def log_prior_1(μ):
        return scipy.stats.norm(loc=9, scale=2).logpdf(μ)

    return (log_prior_1,)


@app.cell
def _(
    X,
    green,
    log_likelihood,
    log_posterior,
    log_prior_1,
    np,
    plt,
    red,
    sns,
    μ,
):
    μ_range_1 = np.linspace(9, 11, 100)
    pri_1 = np.exp(log_prior_1(μ_range_1))
    lik_1 = np.exp(log_likelihood(μ_range_1, X))
    post_1 = np.exp(log_posterior(μ_range_1, X))
    μ_hat_1 = μ_range_1[post_1.argmax()]  # maximum a posterioi estimate
    print('μ = {} \nμ_hat = {:.4f}'.format(μ, μ_hat_1))
    plt.plot(μ_range_1, pri_1 / pri_1.sum(), label='prior')
    plt.plot(μ_range_1, lik_1 / lik_1.sum(), lw=3, label='likelihood')
    plt.plot(μ_range_1, post_1 / post_1.sum(), ls='--', label='posterior')
    plt.plot(μ, np.exp(log_posterior(μ, X)) / post_1.sum(), 'o', color=red, label='$\\mu$')
    plt.plot(μ_hat_1, np.exp(log_posterior(μ_hat_1, X)) / post_1.sum(), 'o', color=green, label='$\\hat{\\mu}$')
    plt.xlabel('Expected # mites, $\\mu$')
    plt.ylabel('Probability')
    plt.legend(bbox_to_anchor=(1, 0.8))
    sns.despine()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Monte Carlo: Sampling instead of computing

    For anything that has more than one or two parameters we cannot do the above exhustive method as the complexity increases with the number of parameters (or the dimension of the parameter space).

    A common approach is therefore to use *Monte Carlo* or sampling methods.
    With Monte Carlo, instead of directly computing the posterior distribution, we indirectly sample from the posterior distribution.

    **Note**: this is an important shift in our methodology. **Instead of computing, we sample**. That is, instead of finding the function $P(\mu \mid X)$, we want to find a set of $m$ samples from the posterior $\{\mu_i\}$ such that $P(\mu_i = u) = P(\mu=u \mid X)$.

    Monte Carlo methods are used in a variety of applications other then posterior sampling.

    For example, consider the function $f(x) = e^{-2x}$.
    """)
    return


@app.cell
def _(np, plt):
    def f(x):
        return np.exp(-2 * _x)
    _x = np.linspace(0, 1)
    plt.plot(_x, f(_x))
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    return (f,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we wish to compute the integral $\int_0^1{f(x)}$, we can draw random points in the unit square and compute the fraction of point below the function curve. This would approximate the integral value.
    """)
    return


@app.cell
def _(f, np, plt):
    _N = 10000
    _x, y = np.random.random((2, _N))
    accepted = y < f(_x)
    print('estimate:\t', accepted.mean())
    print('real:\t\t', 0.5 - 1 / (2 * np.exp(2)))
    plt.plot(_x, y, '.')
    plt.plot(_x[accepted], y[accepted], '.')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
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
def _(X, log_likelihood, np, scipy):
    _N = 10000
    prior = scipy.stats.norm(9, 2)
    μs = prior.rvs(_N)
    log_liks = log_likelihood(μs, X)
    liks = np.exp(log_liks)
    liks = liks / liks.sum()
    liks = liks / prior.pdf(μs)
    randoms = np.random.random(_N)
    accepted_1 = randoms < liks
    _accept_rate = accepted_1.mean()
    print('Acceptance rate: ', _accept_rate)
    return accepted_1, liks, μs


@app.cell
def _(accepted_1, μ, μs):
    μ_hat_2 = μs[accepted_1].mean()
    print('μ = {} \nμ_hat = {:.4f}'.format(μ, μ_hat_2))
    return


@app.cell
def _(accepted_1, liks, plt, sns, μs):
    plt.plot(μs[~accepted_1], liks[~accepted_1], '.', label='rejected')
    plt.plot(μs[accepted_1], liks[accepted_1], '.', label='accepted')
    plt.legend(bbox_to_anchor=(1, 0.8))
    plt.xlabel('$\\mu$')
    plt.ylabel('Probability')
    sns.despine()
    return


@app.cell
def _(accepted_1, plt, sns, μs):
    plt.hist(μs, bins=50, density=True, label='prior')
    plt.hist(μs[accepted_1], bins=20, density=True, alpha=0.5, label='posterior')
    plt.legend()
    plt.xlabel('$\\mu$')
    plt.ylabel('Probability')
    sns.despine()
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
def _(X, log_likelihood, log_prior_1, np):
    η = 0.5
    _N = 10000
    burnin = _N // 2
    accept = 0
    μ_samples = np.empty(_N)
    μ_samples[0] = 7
    logposterior = log_likelihood(μ_samples[0], X) + log_prior_1(μ_samples[0])
    proposals = np.random.normal(0, η, size=_N)
    loguniforms = np.log(np.random.random(size=_N))
    logposteriors = np.zeros(_N)
    for i in range(1, _N):
        μ_candidate = μ_samples[i - 1] + proposals[i]
        logposterior_candidate = log_likelihood(μ_candidate, X) + log_prior_1(μ_candidate)
        logα = logposterior_candidate - logposterior
        if loguniforms[i] < logα:
            logposterior = logposterior_candidate
            μ_samples[i] = μ_candidate
            accept = accept + 1
        else:
            μ_samples[i] = μ_samples[i - 1]
        logposteriors[i] = logposterior
    _accept_rate = accept / _N
    print('Acceptance rate:', _accept_rate)
    return burnin, logposteriors, η, μ_samples


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that the acceptance rate is much higher.

    Lets look at the chain using a **trace plot**. It shows the sample values over time, and we would like to make sure that after the burnin time (represented here in shaded area) the chain has "stabilized": it fluctuates, but it no longer has a trend.
    """)
    return


@app.cell
def _(burnin, plt, sns, μ_samples):
    plt.plot(μ_samples, lw=1)
    plt.axhline(μ_samples[burnin:].mean(), color='k')
    plt.fill_betweenx(plt.ylim(), 0, burnin, color='k', alpha=0.25)
    plt.xlabel('Iterations')
    plt.ylabel('Sample')
    plt.xlim(0, None)
    sns.despine()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This looks good - the samples fluctuate around their mean (black line), and we can see that the chain seemed to have settled after the burnin time (shaded area).

    Lets get rid of the burnin samples.
    """)
    return


@app.cell
def _(burnin, μ_samples):
    μ_samples_1 = μ_samples[burnin:]
    return (μ_samples_1,)


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
    plt.ylabel('Log posterior');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's take the mean of the post-burnin samples as our MAP estimate.

    That makes sense if the posterior is symmetric and unimodal - we can check that.
    """)
    return


@app.cell
def _(green, plt, red, sns, μ, μ_samples_1):
    μ_hat_3 = μ_samples_1.mean()
    σ_hat = μ_samples_1.std()
    print('μ = {} \nμ_hat = {:.4f} +/- {:.4f}'.format(μ, μ_hat_3, σ_hat))
    plt.hist(μ_samples_1, bins=50, alpha=0.75, label='Posterior')
    plt.axvline(μ, color=red, label='$\\mu$')
    plt.axvline(μ_hat_3, color=green, label='$\\hat{\\mu}$')
    plt.axvline(μ_hat_3 + σ_hat, color='k', ls='--')
    plt.axvline(μ_hat_3 - σ_hat, color='k', ls='--')
    plt.xlim(8.5, 12)
    plt.xlabel('$\\mu$')
    plt.ylabel('Probability')
    plt.legend()
    sns.despine()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Other interesting diagnostics we can do are to look at the differences between consecutive samples.
    Their distribution should match the proposal distribution $N(0, \eta)$, ploted below as a black line.
    """)
    return


@app.cell
def _(np, plt, scipy, η, μ_samples_1):
    diff = μ_samples_1[1:] - μ_samples_1[:-1]
    plt.hist(diff, bins=50, density=True)
    diff_range = np.linspace(-η * 5, η * 5)
    plt.plot(diff_range, scipy.stats.norm.pdf(diff_range, 0, η), color='k')
    plt.xlim(-η * 5, η * 5)
    plt.xlabel('$\\mu_{i+1}-\\mu_i$')
    plt.ylabel('Frequency')
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
def _(np, plt, sns, μ_samples_1):
    autocorr = np.correlate(μ_samples_1, μ_samples_1, mode='full')
    autocorr = autocorr / autocorr.max()
    autocorr = autocorr[autocorr.size // 2:]
    plt.plot(autocorr)
    plt.xlabel('lag $k$')
    plt.ylabel('$cor(\\mu_{i+k}, \\; \\mu_i)$')
    sns.despine()
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
    import emcee # python -m pip install emcee

    return (emcee,)


@app.cell
def _(np):
    ndim = 1  # number of parameters in the model
    nwalkers = 50  # number of MCMC walkers
    nsteps = 10000 // nwalkers  # number of MCMC steps to take
    nburn = nsteps // 2  # "burn-in" period to let chains stabilize

    # we'll start at random locations between 0 and 2000
    guesses = 20 * np.random.rand(nwalkers, ndim)
    return guesses, nburn, ndim, nsteps, nwalkers


@app.cell
def _(X, emcee, guesses, log_posterior, nburn, ndim, np, nsteps, nwalkers):
    # avoid negative μ values
    def log_posterior_(μ, X):
        if μ < 0: return -np.inf
        return log_posterior(μ, X)

    sampler = emcee.EnsembleSampler(
        nwalkers=nwalkers, 
        ndim=ndim,
        log_prob_fn=log_posterior_,
        args=[X]
    )
    sampler.run_mcmc(
        initial_state=guesses,
        nsteps=nsteps
    )

    # sampler.chain.shape = (nwalkers, nsteps, ndim)
    # discard burn-in points and flatten with ravel()
    sample = sampler.chain[:, nburn:, :].ravel()
    return sample, sampler


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If this all worked correctly, the array `sample` should contain a series of 5,000 points drawn from the posterior. Let's plot them and check.
    """)
    return


@app.cell
def _(sample, μ):
    μ_hat_4 = sample.mean()
    std_hat = sample.std()
    print('μ = {} \nμ_hat = {:.4f} +/- {:.4f}'.format(μ, μ_hat_4, std_hat))
    return std_hat, μ_hat_4


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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can see here why we need to remove the initial `nburn` samples (or maybe less of them).

    Now we can plot the posterior distribution, together with the estimate (green) $\pm$ standard deviation (dashed black lines), the true value (red). We can see that the true value is within the one standard deviation of the estimate, which is pretty good.
    """)
    return


@app.cell
def _(green, plt, red, sample, sns, std_hat, μ, μ_hat_4):
    plt.hist(sample, bins=50, alpha=0.5)
    plt.axvline(μ, color=red, label='$\\mu$')
    plt.axvline(μ_hat_4, color=green, label='$\\hat{\\mu}$')
    plt.axvline(μ_hat_4 + std_hat, color='k', ls='--')
    plt.axvline(μ_hat_4 - std_hat, color='k', ls='--')
    plt.xlabel(μ)
    plt.ylabel('Posterior')
    plt.legend()
    sns.despine()
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
    """)
    return


@app.cell
def _(X, pm):
    with pm.Model() as poisson_model:
        _μ_ = pm.Normal('μ', mu=9, sigma=2)  # prior
        _X_obs = pm.Poisson('X_obs', mu=_μ_, observed=X)  # poisson model
        idata = pm.sample(draws=10000)
    return idata, poisson_model


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here are the trace plot (on the right) and the posterior of each chain (on the left), to assess convergence. Looking good.
    """)
    return


@app.cell
def _(az, idata):
    az.plot_trace(idata);
    return


@app.cell
def _(az, idata, μ):
    print('μ = {}'.format(μ))
    isummary = az.summary(idata, round_to=2)
    μ_hat_5 = isummary.loc['μ', 'mean']
    isummary
    return (μ_hat_5,)


@app.cell
def _(az, green, idata, plt, red, μ, μ_hat_5):
    az.plot_posterior(idata, round_to=4)
    plt.axvline(μ, color=red)
    plt.axvline(μ_hat_5, color=green)
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
    idata_1 = approx.sample(5000)
    az.plot_posterior(idata_1)
    az.summary(idata_1)
    μ_samples_2 = idata_1.posterior['μ'].to_numpy()
    μ_hat_6 = μ_samples_2.mean()
    μ_std = μ_samples_2.std()
    print('μ = {} \nμ_hat = {:.2f} +/- {:.2f}'.format(μ, μ_hat_6, μ_std))
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

    Here we assume that the measurements $\{X_i\}$ are still drawn from a Poisson distribution, but the expected values $\mu_i$ changes from leaf to leaf.
    We assume it is drawn from a [Gamma distrubtion](https://en.wikipedia.org/wiki/Gamma_distribution#Related_distributions) with shape $r$ and scale $\phi$ ( with expected value $r\phi$ and variance $r\phi^2$):
    $$
    \mu_i \sim Gamma(r, \phi) \\
    X_i \sim Poi(\mu_i)
    $$

    We note the model parameters as $\theta = (r, \phi)$.

    Our data is still $\{X_i\}$, but the model is now _compound_, as it includes a model for the measurements $Poi(\mu_i)$ and a model for the Poisson parameter $Gamma(r, \phi)$.

    ## Synthetic data from over-dispersed Poisson model

    Let's simulate data according to this compound model.
    """)
    return


@app.cell
def _(np):
    # for reproducibility
    np.random.seed(42)
    n_1 = 150
    θ = r, φ = (5, 2)
    μi = np.random.gamma(r, scale=φ, size=n_1)
    X_1 = np.random.poisson(μi)
    return X_1, n_1, r, θ, φ


@app.cell
def _(X_1, n_1, np, plt, r, red, sns, φ):
    _fig, _axes = plt.subplots(1, 2, figsize=(8, 4))
    _ax = _axes[0]
    _ax.plot(np.arange(n_1), X_1, '.k')
    _ax.axhline(r * φ, linewidth=3, color=red)
    _ax.set_xlabel('Measurement, $i$')
    _ax.set_ylabel('# Mites, $X_i$')
    _ax = _axes[1]
    _ax.hist(X_1, bins=10, density=True)
    _ax.axvline(r * φ, linewidth=3, alpha=1, color=red)
    _ax.set_ylabel('Density')
    _ax.set_xlabel('Count, $X_i$')
    _fig.tight_layout()
    sns.despine()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Again, we have already written the log-likelihood function:
    """)
    return


@app.cell
def _(X_1, scipy, θ):
    def log_likelihood_1(θ, X):
        r, φ = θ
        p = φ / (φ + 1)
        return scipy.stats.nbinom(r, p).logpmf(X).sum()
    log_likelihood_1(θ, X_1)
    return (log_likelihood_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We used SciPy's optimization routines to find the maximum likelihood (and then bootstrap to find confidence intervals).
    """)
    return


@app.cell
def _(X_1, log_likelihood_1, r, scipy, φ):
    def neg_log_likelihood(θ, X):
        return -log_likelihood_1(θ, X)

    def mle(X, verbose=False, full_path=False):
        r_guess = X.mean()
        φ_guess = r_guess * r_guess / (X.var(ddof=1) - r_guess)  # eq 3 in Bliss and Fisher 1953
        return scipy.optimize.fmin(func=neg_log_likelihood, x0=(r_guess, φ_guess), args=(X,), disp=verbose, retall=full_path)
    θ_hat = mle(X_1, verbose=True)
    r_hat, φ_hat = θ_hat  # function to minimize with respect to first argument
    print('r = {} \tr_hat = {:.4f}\nϕ = {}\tϕ_hat = {:.4f}'.format(r, r_hat, φ, φ_hat))  # initial guess  # additional arguments to func  # no prints
    return


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
def _(X_1, n_1, pm):
    with pm.Model(coords={'leaf': range(n_1)}) as gamma_poisson_model:
        _r_ = pm.Uniform('r', lower=0, upper=10)
        _φ_ = pm.Uniform('ϕ', lower=0, upper=5)
        _μ_ = pm.Gamma('μ', alpha=_r_, beta=1 / _φ_, dims='leaf')
        _X_obs = pm.Poisson('X_obs', mu=_μ_, observed=X_1)
        idata_gamma_poisson = pm.sample(draws=10000)
    return (idata_gamma_poisson,)


@app.cell
def _(az, idata_gamma_poisson, plt):
    az.plot_trace(idata_gamma_poisson, var_names=['r', 'ϕ'])
    plt.tight_layout()
    return


@app.cell
def _(az, idata_gamma_poisson, r, φ):
    print('r={}, ϕ={}'.format(r, φ))
    isummary_1 = az.summary(idata_gamma_poisson, var_names=['r', 'ϕ'], round_to=4)
    r_hat_1 = isummary_1.loc['r', 'mean']
    φ_hat_1 = isummary_1.loc['ϕ', 'mean']
    isummary_1
    return


@app.cell
def _(az, green, idata_gamma_poisson, r, red, φ):
    _grid = az.plot_pair(idata_gamma_poisson, kind='kde', var_names=['r', 'ϕ'], marginals=True, point_estimate='mean', point_estimate_kwargs=dict(lw=1), point_estimate_marker_kwargs=dict(color=green, marker='o', zorder=100, ec='k'), reference_values={'r': r, 'ϕ': φ}, reference_values_kwargs=dict(color=red))
    _grid[0, 0].set_xlim(4, 8)
    _grid[1, 1].set_ylim(1, 3)
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
    plt.axvline(r * ϕ, color=red);
    plt.axvline(r * ϕ + (r * ϕ * ϕ)**0.5, color=red, ls='dashed');
    plt.axvline(r * ϕ - (r * ϕ * ϕ)**0.5, color=red, ls='dashed');
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
    X_2 = np.loadtxt('../data/mites.csv', delimiter=',')
    plt.hist(X_2, range(8))
    plt.axvline(X_2.mean(), color='k')
    plt.xlabel('# Mites on leaf')
    plt.ylabel('# leaves')
    return (X_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The MLE estimate was $\hat r \approx 1.02$ and $\hat \phi \approx 0.9$, so we can set the priors a bit narrower.
    """)
    return


@app.cell
def _(X_2, n_1, pm):
    with pm.Model(coords={'leaf': range(n_1)}) as mites_model:
        _r_ = pm.Uniform('r', lower=0, upper=3)
        _φ_ = pm.Uniform('ϕ', lower=0, upper=2)
        _μ_ = pm.Gamma('μ', alpha=_r_, beta=1 / _φ_, dims='leaf')
        _X_obs = pm.Poisson('X_obs', mu=_μ_, observed=X_2)
        idata_mites = pm.sample(draws=50000)
    return (idata_mites,)


@app.cell
def _(az, idata_mites, plt):
    az.plot_trace(idata_mites, var_names=['r', 'ϕ'])
    plt.tight_layout();
    return


@app.cell
def _(az, idata_mites):
    isummary_2 = az.summary(idata_mites, var_names=['r', 'ϕ'], round_to=4)
    isummary_2
    return (isummary_2,)


@app.cell
def _(isummary_2):
    r_hat_2 = isummary_2.loc['r', 'mean']
    φ_hat_2 = isummary_2.loc['ϕ', 'mean']
    return r_hat_2, φ_hat_2


@app.cell
def _(az, green, idata_mites):
    _grid = az.plot_pair(idata_mites, kind='kde', var_names=['r', 'ϕ'], marginals=True, point_estimate='mean', point_estimate_kwargs=dict(lw=1), point_estimate_marker_kwargs=dict(color=green, marker='o', zorder=100, ec='k'))
    _grid[0, 0].set_xlim(0.5, 2)
    return


@app.cell
def _(X_2, green, plt, r_hat_2, φ_hat_2):
    plt.hist(X_2, range(8))
    plt.axvline(X_2.mean(), color='k')
    plt.axvline(r_hat_2 * φ_hat_2, color=green)
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
