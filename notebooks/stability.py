import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    # Local stability analysis

    ## [Models in Population Biology](http://scicompy.yoavram.com)
    ## Yoav Ram

    This is an appendix that provides the mathematical background to local stability analysis as used in the [predator-prey model](predator-prey.ipynb) and the [SIR model](gillespie.ipynb) notebooks.
    """)
    return


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    ## Single-valued ODE

    Consider the ODE

    $$ \frac{d x}{d t} = f(t, x). $$

    The equilibrium $x^*$ is the solution to

    $$ f(t, x^*) = 0. $$
    """)
    return


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    $x^*$ is **locally stable** if there exists $\delta > 0$ such that if $|x(0) - x^*| < \delta$ then $x(t) \to x^*$.
    """)
    return


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    Denote $\epsilon(t) = x(t) - x^*$, then by definition of $x^*$,

    $$ \frac{d \epsilon}{d t} = \frac{d}{d t} \big(x(t) - x^*\big). $$

    $$ \frac{d \epsilon}{d t} = \frac{d x}{d t} = f(t, x). $$

    We use a linear approximation (i.e. Taylor expansion) of $f(t, x)$ around $x^*$ such that

    $$ f(t, x) \approx f(t, x^*) + (x-x^*) \cdot \frac{d f}{d x} \mid_{x=x^*}. $$

    Therefore,

    $$ \frac{d \epsilon}{d t} = \frac{d^2 x}{d t d x}\mid_{x=x^*} \cdot \epsilon(t), $$

    up to terms of order $\epsilon(t)^2$.
    """)
    return


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    Denoting $\lambda = \frac{d^2 x}{d t d x}(x^*)$ and integrating, we now have

    $$ \epsilon(t) = x(0) e^{\lambda t}. $$

    Therefore, if $\lambda < 0$ then $\epsilon(t) \to 0$.

    See also Otto and Day, Recipe 5.3 Case C (cases A and B are for discrete time dynamics).
    """)
    return


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    ## Multi-valued ODE

    Now $x$ is multivariate (multidimensional), $\bar x(t) = (x_1(t), x_2(t), \ldots, x_n(t)) \in \mathbb{R}^n$ (a bar represents vectors).

    The ODE is given by

    $$ \frac{d \bar x}{d t} = F(t, \bar x), $$

    where $F_n(t, \bar x) = \frac{d x_n}{d t}$.

    The equilibrium $\bar x^*$ is a solution to

    $$ F(t, \bar x^*) = 0. $$
    """)
    return


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    Given a small perturbation $\bar \epsilon(t) = \bar x(t) - \bar x^*$, we again have

    $$ \frac{d \bar \epsilon}{d t} = \ldots = F(t, \bar x). $$
    """)
    return


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    We again do a linearization of $F(t, \bar x)$ around $\bar x^*$.
    For that we use the Jacobian.

    $$ J_{ij}(\bar x) = \frac{\partial F_i}{\partial x_j}. $$

    $$ J(\bar x) = [J_{ij}(\bar x)]_{i,j=1}^{n}. $$

    where $F_n(t, \bar x) = \frac{d x_n}{d t}$.

    Then $J^* = J(\bar x^*)$, and using a linear approximation around $\bar x^*$ we have

    $$ \frac{d \bar \epsilon}{d t} = F(t, \bar x^*) + J^* \cdot \bar \epsilon = J^* \cdot \bar \epsilon, $$

    by definition of $\bar x^*$.
    """)
    return


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    Note that this ODE is solved by

    $$ \bar \epsilon(t) = c_1 \bar v_1 e^{\lambda_1 t} + \ldots + c_n \bar v_n e^{\lambda_n t}, $$

    if $\lambda_k$ and $\bar v_k$ are eigenvalues and eigenvectors of $J^*$, and $c_k$ are constants,
    because

    $$ c_k \bar v_k \frac{d e^{\lambda_k t}}{d t} = \lambda_k c_k \bar v_k e^{\lambda_k t} = J^* c_k \bar v_k e^{\lambda_k t}. $$
    """)
    return


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    The eigenvalues can be complex, for example $\lambda_k = a + bi$.
    However,

    $$ e^{at+bti} = e^{at} \cdot e^{bti} = e^{at} \cdot (\cos(bt) + i\sin(bt)), $$

    due to Euler's formula, and therefore only the real part $a$ affects the distance of $\epsilon(t)$ from the origin, i.e. the size of the perturbation.

    Therefore, if the real parts of all the eigenvalues are negative then

    $$ \bar \epsilon(t) = c_1 \bar v_1 e^{\lambda_1 t} + \ldots + c_n \bar v_n e^{\lambda_n t} \to 0, $$

    and $\bar x^*$ is locally stable.
    """)
    return


@app.cell(hide_code=True)
def _():
    marimo.md(r"""
    # Colophon

    This notebook was written by [Yoav Ram](http://www.yoavram.com) and is part of the [Models in Population Biology](http://modelspopbiol.yoavram.com) course at Tel Aviv University.

    This work is licensed under a CC BY-NC-SA 4.0 International License.
    """)
    return


if __name__ == "__main__":
    app.run()
