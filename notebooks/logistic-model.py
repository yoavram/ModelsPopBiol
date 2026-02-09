import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import numba
    import scipy.optimize
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_curve
    import pandas as pd
    import seaborn as sns
    blue, green, red = sns.color_palette('muted', 3)
    sns.set_style('ticks')
    sns.set_context('talk')

    import warnings
    warnings.simplefilter('ignore', UserWarning)
    from numba import NumbaDeprecationWarning
    warnings.simplefilter('ignore', NumbaDeprecationWarning)
    return (
        LogisticRegression,
        blue,
        mo,
        np,
        numba,
        pd,
        plt,
        red,
        roc_curve,
        scipy,
        sns,
    )


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
    _female = df_3['sex'] == 'F'
    df_3.loc[_female, 'sex'] = 0.5
    df_3.loc[~_female, 'sex'] = -0.5
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
    # Logistic regression

    Let's try and use logistic regression to clear this up (if we can).
    How does it work?

    We briefly mentioned that when predicting integer values the normal distribution, and hence the *normal linear model*, is not be the best model, and demonstrated that a [GLM](https://en.wikipedia.org/wiki/Generalized_linear_model) with a Poisson distribution and an log link function intead of a normal distribution performed better.
    We will do a similar trick here.

    We first use a linear model (as we did before) to predict the **log-odds** for survival.

    Odds here is actually short for odds-ratio (OR), which is just the ratio of the probability that something happens and the probability that it does not happen:
    $$
    OR =
    \frac{P(\text{Survived})}{P(\text{Died})}
    $$
    so when the odds-ratio is 1, both events are as likley, and when it is >1 (<1) survival (death) is more likely.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the odds-ratio instead of the probability itself, because it is a value between $-\infty$ and $\infty$, rather then between 0 and 1, which is important both for mathematical formality, as the linear model is unbounded, and for interpretation - the odds can be doubles again and again (2:1 becoming 4:1 becomnig 8:1...) whereas the probability cannot (what is the double of 75%?).

    The log-odds, which we mark as $z$, is the natural logarithm of the odds ratio.
    $$
    z =
    \log{\frac{P(\text{Survived})}{P(\text{Died})}}
    $$
    Why use the log-odds? Because (i) it is more mathematically convinient, as log-odds is symmetric in the probability, whereas odds is not, and (ii) it is easier to interpret, as we will see below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So to use a linear model for predicting the log-odds, we have $m$ features, $x_1, x_2, \ldots, x_m$, and we try to estimate coefficients $\mathbf{W} = (b, a_1, \ldots, a_m)$ such that
    $$
    z = b + a_1 x_1 + \ldots + a_m x_m
    $$
    or
    $$
    z = \mathbf{X} \cdot \mathbf{W}
    $$
    gives us a good prediction of the true log-odds.

    From the log-odds we can find the probability for the event to occur using the *logisitic* (hence the name of the method!) or the *expit* function (same function, different name):
    $$
    P(\text{Survived}) = expit(z) = \frac{1}{1+e^{-z}}
    $$
    """)
    return


@app.cell
def _(numba):
    @numba.njit
    def logodds(X, W, b):
        Z = X @ W + b
        return Z

    return (logodds,)


@app.cell
def _(X, logodds, np):
    W = np.ones(X.shape[1])
    b = 1
    print(logodds(X, W, b)[:5])
    return W, b


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Maximum likelihood

    Now we want to find suitable $a_i$ such that we make a good prediction.
    We'll use *maximum likelihood* again.

    Given data $(x, y)$ where $x = (x_1, \ldots, x_m)$ are some numbers and $y$ is either 0 or 1, the logistic model provides us an estimate $\widehat y$

    $$
    \widehat{y} = P(y=1)=\frac{1}{1+e^{-z}} = \frac{1}{1+e^{-b -a_1 x_1 - \ldots -a_m x_m}}
    $$

    The likelihood of this model is

    $$
    \mathcal{L}(b, a_1, \ldots, a_m \mid x_1, \ldots, x_m, y) =
    P(y \mid b, a_1, \ldots, a_m, x_1, \ldots, x_m) =
    \cases{
        \widehat{y}, & y=1 \\
        1-\widehat{y}, & y=0
    }
    $$

    If we have many $(x,y)$ pairs, and we will **assume that each pair is independent** (which maybe we can't always do, and specifically in the Titanic case we probably shouldn't do, but ok) then the joint likelihood of all the pairs is just the product of all the pair likelihoods: the product is used because the joint probability of independent events occuring is the product of their occurence probabilities.
    Writing the set of $x$s as $X$ and the corresponding set of $y$s as $Y$, and because $y$ are either 0 or 1,

    $$
    \mathcal{L}(b, a_1, \ldots, a_m \mid X, Y) =
    \prod_{i} {(\widehat{y}_i)^{y_i} \; (1-\widehat{y}_i) ^{1-y_i}}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We'll use the log-likelihood because otherwise we will have to deal with a product of really small numbers; so we take the sum of the log of the likelihood $\mathbf{L}$ of the the $(x, y)$ pairs (sum because the log of products is the sum of logs). The use of log here is not "magic", it's a mathematical convenience. It just happens that "log-likelihood" sounds very impressive.

    $$
    \log{\mathcal{L}(b, a_1, \ldots, a_m \mid X, Y)} =
    \sum_{i} {y_i \log{\widehat{y}_i} + (1-y_i) \log{(1-\widehat{y}_i)}}
    $$

    This is very similar to the negative of an information theory function called [*cross entropy*](https://en.wikipedia.org/wiki/Cross_entropy), and we usually average it over all the samples so that we can compare cross entropies between datasets of different size:

    $$
    \mathbf{J}(b. a_1, \ldots, a_m, X, Y) = -\frac{1}{n} \log{\mathcal{L}(b, a_1, \ldots, a_m \mid X, Y)}
    $$

    where $n$ is the number of samples in $X,Y$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Numerical stability

    Due to numerical issues when using very small or very large numbers, we should play around with the definition a little bit to find an expression that we can calculate with good numerical stability.

    Note that
    $$
    \log{\widehat{y}} = -\log{\Big(1 + e^{-z}\Big)}  = -\log{\Big(1 + e^{-z}\Big)} \\
    \log{(1-\widehat{y})} = -z - \log{\Big(1 + e^{-z}\Big)}
    $$
    and therefore
    $$
    y \log{\widehat{y}} + (1-y) \log{(1-\widehat{y})} = \\
    -y \log{\Big(1 + e^{-z}\Big)} + (1-y)\Big(-z - \log{\Big(1 + e^{-z}\Big)}\Big) = \\
    (1-y)z - \log{\Big(1 + e^{-z}\Big)}
    $$

    Finally,
    $$
    \log{\mathcal{L}(b, a_1, \ldots, a_m \mid X, Y)} =
    \sum_{(x,y) \in (X,Y)} {-z (1-y) - \log{\Big(1 + e^{-z}\Big)}},
    $$
    where $z=\text{log-odds} = a_1 x_1 + \ldots + a_n x_n$.
    """)
    return


@app.cell
def _(logodds, np, numba):
    @numba.njit
    def cross_entropy(X, Y, W, b):
        Z = logodds(X, W, b)
        logliks = -Z * (1 - Y) - np.log(1 + np.exp(-Z))
        return -logliks.mean()

    return (cross_entropy,)


@app.cell
def _(W, X, Y, b, cross_entropy):
    cross_entropy(X, Y, W, b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Gradient descent and the chain rule

    Now we can minimize the cross entropy using gradient descent.
    We need to calculate the derivative of the cross entropy with regards to $a_i$.
    We will use the [chain rule](https://en.wikipedia.org/wiki/Chain_rule):

    $$
    f(g(x))' = f'(g(x)) \cdot g'(x),
    $$

    which is easier to write as

    $$
    \frac{dx}{dy} = \frac{dx}{dz} \cdot \frac{dz}{dy}
    $$

    because then we can eliminate fractions as if these were fractions and not [infinitesimals](https://en.wikipedia.org/wiki/Infinitesimal).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Remember that $z=\text{log-odds} = a_0 + a_1 x_1 + \ldots + a_m x_m$ and $\mathbf{J}$ is the cross entropy function which we want to minimize.

    Then
    $$
    \frac{\partial \mathbf{J}}{\partial a_k} =
    \frac{\partial \mathbf{J}}{\partial \widehat y} \cdot \frac{\partial \widehat y}{\partial z} \cdot \frac{\partial z}{\partial a_k}
    $$

    The easiest one is:

    $$
    \frac{\partial z}{\partial a_k} = x_k
    $$

    The derivative of the logistic function is (you can verify later):

    $$
    \frac{\partial \widehat y}{\partial z} = \widehat y ( 1-\widehat y )
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, because $\frac{d}{dx} log(x) = \frac{1}{x}$ (again, you can verify this),

    $$
    \frac{\partial \mathbf{J}}{\partial \widehat y} =
    - \frac{\partial}{\partial \widehat y} \big(y \log{\widehat{y}} + (1-y) \log{(1-\widehat{y})}\big) = \\
    -y \cdot \frac{1}{\widehat y} + (1-y) \cdot \frac{1}{1-\widehat y} = \\
    \frac{\widehat y - y}{\widehat y ( 1 - \widehat y)}
    $$

    Putting it all together,
    $$
    \frac{\partial \mathbf{J}}{\partial a_k} =
    \frac{\partial \mathbf{J}}{\partial \widehat y} \cdot \frac{\partial \widehat y}{\partial z} \cdot \frac{\partial z}{\partial a_k} = \\
    \frac{\widehat y - y}{\widehat y ( 1 - \widehat y)} \cdot \widehat y ( 1-\widehat y ) \cdot x_k = \\
    (\widehat y - y) \cdot x_k
    $$

    which you have to admit is pretty cool: this is the residual (i.e. difference between the predicted and oberverd probabilities, $\widehat y - y$), so 0 when you got it right and 1 or -1 when you got it completely wrong, multiplied by the stength of the signal, so that strong signals (large $x_k$) have a stonger gradient and stonger effect on the result.

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
def _(logodds, np, numba):
    @numba.njit
    def gradient(X, Y, W, b):
        Z = logodds(X, W, b)
        _Yhat = 1 / (1 + np.exp(-Z))
        δ = _Yhat - Y
        dW = X.T @ δ / δ.shape[0]
        db = δ.mean()
        assert dW.shape == W.shape
        return (dW, db)

    @numba.njit
    def gradient_descent(X, Y, W, b, η=0.01):
        dW, db = gradient(X, Y, W, b)
        return (W - η * dW, b - η * db)

    return gradient, gradient_descent


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When your solution is ready, comment out the first line of the next cell and run it.
    """)
    return


@app.cell
def _(W, X, Y, b, gradient_descent):
    W_1, b_1 = gradient_descent(X, Y, W, b)
    print(W_1)
    print(b_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Fitting the logistic model
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Fitting the model is done in much the same way as we did with the linear model - just have to choose initial coefficeints, different stopping condition, and adjust to the API of the new `gradient_descent` function.

    This time we stop when the difference in cross entropy between two iterations is smaller than some value ($10^{-4}$).
    """)
    return


@app.cell
def _(cross_entropy, gradient_descent, np, numba):
    @numba.njit 
    def logistic_model(X, Y, W=None, b=1, iters=100000, verbose=True):
        if W is None:
            W = np.zeros(X.shape[1])    
        for t in range(iters+1):
            W, b = gradient_descent(X, Y, W, b)
            if verbose and t % (iters//10) == 0:
                J = cross_entropy(X, Y, W, b)
                print(t, "- J =", round(J, 6), "W =", np.round(W, 4), "b =", round(b, 4))
        return W, b

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
def _(W_2, X, Y, cross_entropy, gradient, np, scipy):
    # magic command not supported in marimo; please file an issue to add support
    # %%time
    min_result = scipy.optimize.minimize(fun=lambda θ: cross_entropy(X, Y, θ[:W_2.size], θ[-1]), x0=np.ones(X.shape[1] + 1), jac=lambda θ: np.append(*gradient(X, Y, θ[:W_2.size], θ[-1])), method='TNC')
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
def _(LogisticRegression, X, Y):
    model = LogisticRegression(penalty=None, fit_intercept=True) # by default, scikit-learn uses l2 penalty
    model.fit(X, Y)
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

    Let's suppose that a positive answer is "person survived" that is $y=1$ or `truth==1` and use *scikit-learn*'s utility to calculate and plot the [Receiver operating characteristic](https://en.wikipedia.org/wiki/Receiver_operating_characteristic) curve.

    An "ideal" model will shoot directly to the top, that is, have maximum TPR for any FPR.
    A "random" or "naive" model can be expected to follow the dashed line.

    Indeed if we look at the ROC curve, the threshold we choose is right on the "knee" of the curve.
    """)
    return


@app.cell
def _(X, Y, model, plt, roc_curve):
    _Yhat = model.predict_proba(X)[:, 1]
    fpr, tpr, thresholds = roc_curve(Y, _Yhat)
    plt.plot(fpr, tpr)
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    idx = (thresholds < 1 - 0.06).argmax()
    plt.plot(fpr[idx], tpr[idx], 'ok')
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
    import pymc as pm
    import arviz as az
    import bambi as bmb

    return az, bmb


@app.cell
def _(df_4):
    # create columns without spaces
    df_4['HongKong'] = df_4['Hong Kong']
    df_4['SouthKorea'] = df_4['South Korea']
    return


@app.cell
def _(bmb, df_4):
    logistic_model_1 = bmb.Model('recovered ~ sex + age + HongKong + SouthKorea + Philippines + Singapore', df_4, family='bernoulli')
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
            predictions = pred_idata.posterior['recovered_mean']
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
