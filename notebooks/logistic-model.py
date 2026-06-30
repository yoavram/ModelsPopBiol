import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import numba
    import scipy.optimize
    from scipy.special import expit
    import pandas as pd
    import seaborn as sns
    blue, green, red = sns.color_palette('muted', 3)
    sns.set_style('ticks')
    sns.set_context('talk')

    import warnings
    warnings.simplefilter('ignore', UserWarning)
    from numba import NumbaDeprecationWarning
    warnings.simplefilter('ignore', NumbaDeprecationWarning)
    return blue, expit, mo, np, pd, plt, red, scipy, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Logistic Model

    ## [Models in Population Biology](http://modelspopbiol.yoavram.com)
    ## Yoav Ram
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the previous section we used one feature with integer values to predict another integer value.
    What if we want to predict a category or class (i.e. classify or categorize) instead of predicting a number?

    There are many ways to classify data (even without a training set), and one of the most common is **logistic regression**.
    But *regression* is usually used for predicting real numbers, how is regression related to classification?
    In logistic regression we are trying to regress (predict a real number) the probability of some data being in a one class and not the other.
    Logistic regression is binomial (two classes, one free variable) but it can easily be expanded to *multinomial logistic regression*, sometimes also known as *softmax regression*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # COVID-19 fatality data

    This dataset includes COVID-19 case details for over 7,500 patients from Singapore, Hong Kong, Philippines, and South Korea.
    Details include age, sex, nationality, status, and dates.

    Data obtained from [dolthub](https://www.dolthub.com/repositories/Liquidata/corona-virus/doc/master/README.md).
    """)
    return


@app.cell
def _(pd):
    df = pd.read_csv("../data/covid-19_case_details.csv")
    df.head()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data formatting
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We convert the place names from a categorical (text) variable to four dummy varaibles that take values 0 or 1. We do this because logistic regression takes numeric values. By having one "boolean" variable per country, we will be able to estimate the effect of each place on probability to die from COVID-19.
    """)
    return


@app.cell
def _(df, pd):
    dummies = pd.get_dummies(df['country_region'])
    dummies = dummies.rename(columns={'China': 'Hong Kong', 'Korea, South': 'South Korea'})
    countries = dummies.columns
    df_1 = pd.concat((df, dummies), axis=1)
    dummies.head()
    return countries, df_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are multiple rows for some cases (i.e. patients), so we take the last row for each case. Also, the case identifiers are unique _per country_.
    """)
    return


@app.cell
def _(df_1):
    df_2 = df_1.groupby(['place_id', 'case_id']).last()
    df_2 = df_2.reset_index()
    return (df_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We filter in only cases that ended with recovery or death, the rest of the cases are undertermined yet.

    We then create a boolean column for recovery.
    """)
    return


@app.cell
def _(df_2):
    dead = df_2['current_status'].isin(['deceased', 'Died', 'Dead', 'deceased', 'Desceased'])
    recovered = df_2['current_status'].isin(['Released', 'released', 'Recovered'])
    df_3 = df_2[dead | recovered]
    df_3['recovered'] = recovered.astype(int)
    return (df_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We convert sex to an integer, and extract only the variables of interest.
    """)
    return


@app.cell
def _(countries, df_3):
    df_3['sex'] = df_3['sex'].map({'F': 0.5, 'M': -0.5})
    var_names = ['recovered', 'sex', 'age'] + countries.tolist()
    df_4 = df_3[var_names].copy()
    df_4 = df_4.dropna()
    df_4.head()
    return df_4, var_names


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We extract the features to `X` and the target to `Y`.
    """)
    return


@app.cell
def _(df_4, var_names):
    X = df_4[var_names[1:]].values.astype(float)
    Y = df_4[var_names[0]].values.astype(float)
    return X, Y


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data visualization

    We can plot the distrubtion of cases.
    """)
    return


@app.cell
def _(df_4, plt, sns):
    _ax = sns.violinplot(data=df_4, x='sex', y='age', hue='recovered', split=True, inner='quart')
    _ax.set_xticklabels(['Male', 'Female'])
    _ax.legend(loc='lower center', title='Recovered')
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From this it seems that age has a strong effect on recovery, whereas the role of sex is less clear.

    How do we continue?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Binary logistic regression
    When there are only two class labels (e.g., 0 and 1; cat and dog), the model is known as **binary logistic regression** (if there are more, it is called multiple/multinomial logistic regression or sometimes softmax regression).

    Let's write the model.
    Denote the number of individuals by $n$.
    We assume that the outcome $y_i \in \{0,1\}$ of individual $i$ is **Bernoulli distributed** with probability $\hat{y}_i$.
    We still have a linear model, but not directly for $\hat{y}_i$, because it is a probability and therefore constrained to be between 0 and 1. Instead, we assume that $z_i=\textit{logit}{(\hat{y}_i)}=\log{\frac{\hat{y}_i}{1-\hat{y}_i}}$ is a linear function of $m$ features, $x_i=(x_{i,1}, \ldots, x_{i,m})$, because $\textit{logit}{(\hat{y}_i)}$ can be any real number.

    Thus,
    $$
    z_i = \sum_{j=1}^{m}{w_j x_{i,j}} + b $$
    $$
    \log{\frac{\hat{y}_i}{1-\hat{y}_i}} = z_i $$
    $$
    y_i \sim \text{Ber}(\hat{y}_i)
    $$
    Here,  $W = (w_1, \ldots, w_m)$ are the model weights (coefficients) and $b$ is the bias (intercept).
    They determine the additive effect of a unit change in the features on the log-odds of the outcome, or the multiplicative effect on the odds of the outcome.

    The inverse of the logit function is called the _expit_ or **logistic function**, and hence the name of the regression method;
    $$
    \hat{y_i} = \frac{1}{1+e^{-z_i}}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Maximum likelihood estimation

    From our model, the likelihood is
    $$
    p(y_i=1 \mid x_i, W, b) \quad= \hat{y}_i $$
    $$
    p(y_i=0 \mid x_i, W, b) = 1-\hat{y}_i
    $$
    where $W=(w_1, \ldots, w_m)$ are the model weights and $b$ is the bias, affecting the likelihood via $\hat{y}_i=1/\left(1+\exp{\left(-\sum_{j=1}^{m}{w_j x_{i,j}}-b\right)}\right)$.

    This can also be written as
    $$
    p(y_i \mid x_{i}, W, b) = \hat{y}_i^{y_i} \cdot (1-\hat{y}_i)^{1-y_i}
    $$
    Assuming $y_i, y_k$ are independent for all $i,k$,
    $$
    p(Y \mid X, W, b) = \prod_{i=1}^{n}{\hat{y}_i^{y_i} \cdot (1-\hat{y}_i)^{1-y_i}}
    $$

    Therefore, the negative log likelihood (which again makes sense because we have a product of exponents) is
    $$
    NLL(W, b) = -\frac{1}{n}\log\left(\prod_{i=1}^{n}{\hat{y}_i^{y_i} \cdot (1-\hat{y}_i)^{1-y_i}}\right) =
    -\frac{1}{n}\sum_{i=1}^{n}y_i \log{\hat{y}_i} + (1-y_i)\log{(1-\hat{y}_i)}
    $$
    where we scale by the dataset size $n$ so that we can compare values between datasets of different sizes.
    This function is called in information theory the [**cross entropy**](https://en.wikipedia.org/wiki/Cross-entropy) function, and in the deep learning context this name has stuck.

    Note that this function can be numerically unstable when $\hat{y}_i$ are close to zero or one.
    A different way to write it is
    $$
    NLL(W, b) = \frac{1}{n}\sum_{i=1}^{n}{z_i (1-y_i) + \log{\left(1+e^{-z_i}\right)}}
    $$

    So here we compute the negative log likelihood or cross entropy function.
    """)
    return


@app.cell
def _(np):
    def logodds(X, W, b):
        return X @ W + b

    def NLL(W, b, X, Y):
        Z = logodds(X, W, b)
        return (Z * (1-Y) + np.log(1 + np.exp(-Z))).mean()

    return NLL, logodds


@app.cell
def _(NLL, X, Y, np):
    W = np.linspace(0, 1, X.shape[1])
    b = 0.0
    print(NLL(W, b, X, Y))
    return W, b


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Gradients and the chain rule

    To find the MLE we need to solve $\partial NLL / \partial W = 0$, which can be done using different gradient-based optimization algorithms.
    For that we need to derive the gradient (Prob ML ch. 10.2.3.3).

    We will use the **[chain rule](https://en.wikipedia.org/wiki/Chain_rule)**:
    $$
    \frac{dx}{dy} = \frac{dx}{dz} \cdot \frac{dz}{dy}
    $$

    Remember that $z = w_1 x_1 + \ldots + w_m x_m + b$ and the NLL is a function that we want to minimize.

    Then for a single data example $(x, y)$,
    $$
    \frac{\partial NLL}{\partial w_j} =
    \frac{\partial NLL}{\partial \widehat y} \cdot \frac{\partial \widehat y}{\partial z} \cdot \frac{\partial z}{\partial w_j}
    $$

    So we have three terms.
    The easiest one is:
    $$
    \frac{\partial z}{\partial w_j} = x_j
    $$

    The derivative of the logistic (expit) function is (you can verify this):
    $$
    \frac{\partial \widehat y}{\partial z} = \widehat y ( 1-\widehat y )
    $$

    Next, because $\frac{\partial \log}{\partial x} = \frac{1}{x}$,
    $$
    \frac{\partial NLL}{\partial \widehat y} =
    - \frac{\partial}{\partial \widehat y} \big(y \log{\widehat{y}} + (1-y) \log{(1-\widehat{y})}\big) = $$
    $$
    -y \cdot \frac{1}{\widehat y} + (1-y) \cdot \frac{1}{1-\widehat y} = $$
    $$
    \frac{\widehat y - y}{\widehat y ( 1 - \widehat y)}
    $$

    Putting it all together,
    $$
    \frac{\partial NLL}{\partial w_j} =
    \frac{\partial NLL}{\partial \widehat y} \cdot \frac{\partial \widehat y}{\partial z} \cdot \frac{\partial z}{\partial w_j} = $$
    $$
    \frac{\widehat y - y}{\widehat y ( 1 - \widehat y)} \cdot \widehat y ( 1-\widehat y ) \cdot x_j = $$
    $$
    (\widehat y - y) \cdot x_j
    $$

    This is pretty cool: it is the residual (i.e., difference between the predicted and oberverd probabilities, $\widehat y - y$), so 0 when the model got it right and 1 or -1 when it got it completely wrong, multiplied by the stength of the signal, so that strong signals (large $x_j$) have a stonger gradient and stonger effect on the result.

    Since $\frac{\partial z}{\partial b} = 1$, the gradient with respect to the bias follows the same chain rule but with a simpler last term:
    $$
    \frac{\partial NLL}{\partial b} = (\widehat y - y)
    $$

    This was the gradient for a single sample. We average it over all samples to get a good estimate of the "real gradient" (law of large numbers etc.).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Our implementation of the `gradient_descent` function, similar to the one we had in a previous session, returns updated values for the coefficients `W` and the bias (intercept) `b` based on one iteration of the gradient descent algorithm.
    """)
    return


@app.cell
def _(expit):
    def gradient(W, b, X, Y):
        Z = X @ W + b
        Yhat = expit(Z)
        δ = Yhat - Y
        G_W = X.T @ δ / X.shape[0] # equivalent to G_W = (X * δ).mean(axis=0)
        G_b = δ.mean()
        assert G_W.shape == W.shape
        return G_W, G_b

    return (gradient,)


@app.cell
def _(W, X, Y, b, gradient):
    G_W, G_b = gradient(W, b, X, Y)
    print(G_W, G_b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Gradient descent

    The NLL function is convex (ProbML ch. 10.2.3.4), so all we need to do is follow the negative gradeints that we just calculated towards the global minimum; this is called **gradient descent**.

    This is a simple, effective, and generic iterative algorithm.
    In each step, we calculate that gradient of the NLL function with respect to model parameters $\partial NLL/\partial W$ and $\partial NLL/\partial b$ and update the parameters according to the recursive equations for the parameter values at iteration $t$,
    $$
    W_t = W_{t-1} - \eta \frac{\partial NLL(W, b)}{\partial W}
    $$
    $$
    b_t = b_{t-1} - \eta \frac{\partial NLL(W, b)}{\partial b}
    $$
    Here, $\eta$ is the size of the step we take in the negative gradient in each iteration, also called **learning rate**.
    """)
    return


@app.cell
def _(gradient):
    def gradient_descent(W, b, X, Y, η):
        G_W, G_b = gradient(W, b, X, Y)
        return W - η * G_W, b - η * G_b

    return (gradient_descent,)


@app.cell
def _(W, X, Y, b, gradient_descent):
    import timeit
    _t = timeit.timeit(lambda: gradient_descent(W, b, X, Y, 0.0001), number=1000)
    print(f"{_t/1000*1e3:.3f} ms per call")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Fitting the model

    We are now ready to fit the model.
    We initialize $W$ with all ones, since we know the problem is convex.

    The `fit_logistic` function will do all the hard work.
    """)
    return


@app.cell
def _(NLL, X, Y, gradient_descent, np):
    def fit_logistic(X, Y, η=0.001, niter=100000, verbose=True):
        W = np.ones(X.shape[1])
        b = 0.0
        for t in range(niter+1):
            if t % 5000 == 0 and verbose:
                print("{:6d}: NLL={:.6f}, W={}, b={:.4f}".format(t, NLL(W, b, X, Y), np.array_str(W, precision=4), b))
            W, b = gradient_descent(W, b, X, Y, η)
        return W, b

    logistic_model = fit_logistic
    _W, _b = fit_logistic(X, Y)
    print(_W, _b)
    return (logistic_model,)


@app.cell
def _(X, Y, logistic_model):
    W_2, b_2 = logistic_model(X, Y)
    print(W_2, b_2)
    return W_2, b_2


@app.cell
def _(X, Y, logistic_model):
    # magic command not supported in marimo; please file an issue to add support
    # %%time
    logistic_model(X, Y, verbose=False);
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Of course, there are optimization algorithms that are faster than gradient descent - but they might not be suitable for any problem.
    """)
    return


@app.cell
def _(NLL, W_2, X, Y, gradient, np, scipy):
    min_result = scipy.optimize.minimize(fun=lambda θ: NLL(θ[:W_2.size], θ[-1], X, Y), x0=np.ones(X.shape[1] + 1), jac=lambda θ: np.append(*gradient(θ[:W_2.size], θ[-1], X, Y)), method='TNC')
    assert min_result.success, min_result.message
    print(min_result.x, min_result.fun)  # BFGS 28.7 ms ± 4.71 ms, L-BFGS-B 24.1 ms ± 4.59 ms, TNC 16.1 ms ± 3.71 ms, SLSQP 21.4 ms ± 4.96 ms
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Anyway, let's inspect with the gradient descent results:
    """)
    return


@app.cell
def _(W_2, b_2, np, var_names):
    print('Odds-ratios:')
    print('bias:\t{:.3f}'.format(np.exp(b_2)))
    for _i, _var in enumerate(var_names[1:]):
        print('{}:\t{:.3f}'.format(_var, np.exp(W_2[_i])))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can interpret these results as follows:
    - a baby with no country or sex ($X=0$) will likely survive.
    - Females are 3-fold more likely to survive
    - Every year of age reduces survival by about 8%
    - The Philippines had a much lower survival probability compared to to other countries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Model prediction
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Our model outputs *probabilities*, and we need to convert these to classes.
    We will just decide that if the predicted survival probability is 0.5 then that person survived.

    A good score for a classification problem is the *accuracy*, which tells us the fraction of cases in which our model agrees with the truth.
    """)
    return


@app.cell
def _(W_2, X, Y, b_2, logodds, np):
    Z = logodds(X, W_2, b_2)
    _Yhat = 1 / (1 + np.exp(-Z))
    accuracy = ((_Yhat > 0.5) == Y).mean()
    print('Accuracy: {:.2%}'.format(accuracy))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Scikit-learn

    Now we fit a logistic model to the data.
    We will use **Scikit-learn** this time: specifically, the `sklearn.linear_model.LogisticRegression` model.
    """)
    return


@app.cell
def _():
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import precision_recall_curve

    return LogisticRegression, precision_recall_curve


@app.cell
def _(LogisticRegression, X, Y):
    model = LogisticRegression(penalty=None, fit_intercept=True) # by default, scikit-learn uses l2 penalty
    model.fit(X, Y);
    return (model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here are the effects of the features, using the model coefficients.
    """)
    return


@app.cell
def _(model, np, var_names):
    print('{:<10}\t{:>11.4f}'.format('intercept', np.exp(model.intercept_)[0]))
    for _var, coef in zip(var_names[1:], np.exp(model.coef_).ravel()):
        print('{:<10}\t{:>11.4f}'.format(_var, coef))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We see that:
    - intercept: for a baby with indeterminate sex and country, the death rate is 1 to 2.2 million
    - females are about 4.3 times more likely to survive,
    - age reduces survival by ~10% per year
    - Hong Kong and Singapore are much safer, but this may be due to the effect that we have no data about deceased there.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Classification threshold

    To find a good threshold for classification, lets look at the historgram of probability for death, applied to recovered (blue) and deceased (red) cases.
    """)
    return


@app.cell
def _(X, Y, model, np, plt, sns):
    logPdeceased = model.predict_log_proba(X)[:,0] # probabilities are pretty low so we use log-probabilities

    bins = np.linspace(-10, 0, 50)
    plt.hist(logPdeceased[Y==1], bins=bins,density=True, alpha=0.7, label='Recovered');
    plt.hist(logPdeceased[Y==0], bins=bins,density=True, alpha=0.7, label='Deceased')
    plt.xlabel(r'Probability to die, $\hat{y}$')
    plt.ylabel('Frequency')
    xticks = plt.xticks()[0]
    plt.xticks(xticks, np.round(np.exp(xticks), 4))
    plt.xlim(bins.min(), bins.max())
    plt.axvline(-2.75, color='k')
    print("Threshold: {:.2f}".format(np.exp(-2.75)))
    plt.legend()
    sns.despine()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The threshold we pick (i.e. 0.06) can balance between the probability to give an incorrect positive answer and the probability to give a correct positive answer.
    These are called the false-positive rate and true-positive rates.

    You might consider that it is preferable to sometimes tell someone they are not going to survive and should remain under care, when they are actually going to survive without care, rather than sometimes telling people they are healthy enough to leave the hospital when they are actually not going to make it and they should remain under supervision.

    Let's suppose that a positive answer is "person survived" that is $y=1$ or `truth==1` and use *scikit-learn*'s utility to calculate and plot the [Precision-Recall curve](https://en.wikipedia.org/wiki/Precision_and_recall).

    **Precision** is the fraction of predicted survivors that truly survived; **recall** is the fraction of actual survivors that were correctly predicted.
    An "ideal" model reaches the top-right corner (precision=1, recall=1).
    A "random" classifier follows a horizontal line at the class prevalence.

    The marked point corresponds to the 0.06 death-probability threshold we chose above.
    """)
    return


@app.cell
def _(X, Y, model, plt, precision_recall_curve):
    _Yhat = model.predict_proba(X)[:, 1]
    precision, recall, thresholds = precision_recall_curve(Y, _Yhat)
    plt.plot(recall, precision)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    idx = (thresholds < 1 - 0.06).argmax()
    plt.plot(recall[idx], precision[idx], 'ok')
    plt.ylim(0.9,1)
    plt.xlim(0.9,1)
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We plot the probability to die for each age in each country, separated by sex.
    """)
    return


@app.cell
def _(blue, countries, df_4, model, plt, red, var_names):
    fig, axes = plt.subplots(2, 2, figsize=(8, 6), sharex=True, sharey='col')
    for _country, _ax in zip(sorted(countries), axes.flat):
        df_ = df_4[df_4[_country] == 1]
        df_ = df_.sort_values('age')
        X_ = df_[var_names[1:]]
        Y_ = df_[var_names[0]]
        Pdie_ = model.predict_proba(X_)[:, 0]
        _female = df_['sex'] > 0
        _ax.plot(X_.loc[_female, 'age'], Pdie_[_female], '-', color=red, label='Female')
        _ax.plot(X_.loc[~_female, 'age'], Pdie_[~_female], '-', color=blue, label='Male')
        _ax.set(title=_country)
    axes[0, 0].legend(loc='upper left')
    axes[0, 0].set(ylabel='Probability to die')
    axes[1, 0].set(xlabel='Age', ylabel='Probability to die', xticks=[0, 20, 40, 60, 80, 100])
    axes[1, 1].set(xlabel='Age', xticks=[0, 20, 40, 60, 80, 100])
    fig.tight_layout()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bayesian logistic model

    This time we will use [bambi](https://bambinos.github.io/bambi/), a high-level Bayesian model-building interface written in Python. It works with the probabilistic programming frameworks PyMC and is designed to make it extremely easy to fit Bayesian mixed-effects models common in biology, social sciences and other disciplines.

    This will save us some work in setting up the model.
    """)
    return


@app.cell
def _():
    import pytensor
    pytensor.config.linker = 'py' # to avoid error in vs code
    import pymc as pm
    import arviz as az
    import bambi as bmb

    return az, bmb


@app.cell
def _(df_4):
    df_5 = df_4.copy()
    df_5['HongKong'] = df_5['Hong Kong']
    df_5['SouthKorea'] = df_5['South Korea']
    return (df_5,)


@app.cell
def _(bmb, df_5):
    logistic_model_1 = bmb.Model('recovered ~ sex + age + HongKong + SouthKorea + Philippines + Singapore', df_5, family='bernoulli')
    idata = logistic_model_1.fit(draws=1000, idata_kwargs={'log_likelihood': True})
    return idata, logistic_model_1


@app.cell
def _(az, idata):
    az.to_netcdf(idata, 'idata_logistic_covid.nc')
    return


@app.cell
def _(az):
    idata_1 = az.from_netcdf('idata_logistic_covid.nc')
    return (idata_1,)


@app.cell
def _(az, idata_1, plt):
    az.plot_trace(idata_1)
    plt.tight_layout()
    az.summary(idata_1)
    plt.gcf()
    return


@app.cell
def _(az, idata_1, logistic_model_1, np, pd, plt, sns):
    countries_1 = ['HongKong', 'SouthKorea', 'Philippines', 'Singapore']
    sexes = [' Male', ' Female']
    colors = sns.color_palette('Paired', 2 * len(countries_1))
    age = np.arange(0, 100)
    plt.figure(figsize=(12, 4))
    for _i, sex in enumerate([-0.5, 0.5]):
        base_pred_data = pd.DataFrame({'age': age, 'sex': [sex] * len(age), 'HongKong': 0, 'SouthKorea': 0, 'Philippines': 0, 'Singapore': 0})
        for j, _country in enumerate(countries_1):
            pred_data = base_pred_data.copy()
            pred_data[_country] = 1
            pred_idata = logistic_model_1.predict(idata_1, data=pred_data, inplace=False)
            predictions = pred_idata.posterior['p']
            plt.plot(age, predictions.mean(['chain', 'draw']), color=colors[2 * j + _i], lw=2, label=_country + sexes[_i])
            az.plot_hdi(age, predictions, color=colors[2 * j + _i])
    plt.xlabel('Age')
    plt.ylabel('Recovery probability')
    plt.legend(loc='lower left', ncol=2, fontsize=14)
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # References

    - Pawitan Y, 2001. *In all likelihood: statistical modelling and inference using likelihood*. **Ch. 6.2**.
    - Scikit-learn documentation has a [tutorial](http://scikit-learn.org/stable/tutorial/statistical_inference/supervised_learning.html#classification) using the classical Iris dataset, with examples for other classification methods other than logistic regression.
    - [bambi](https://bambinos.github.io/bambi/notebooks/model_comparison.html) logistic regression example including model comparison.
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
