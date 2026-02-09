import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Models in Population Biology
    ## Yoav Ram
    ### Tel Aviv University / Spring 2026
    Course website: [modelspopbiol.yoavram.com](https://modelspopbiol.yoavram.com)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tutorials in Marimo

    - [Python](notebooks/python.py)
    - [NumPy](notebooks/numpy-basics.py)
    - [Matplotlib](notebooks/matplotlib-basics.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lectures

    1. [Continuous-time univariate deterministic model: population growth models](notebooks/population-growth.py)
    1. [Continuous-time multivariate deterministic model: Predator-prey model](notebooks/predator-prey.py)
    1. [Discrete-time univariate deterministic model: Haploid selection](notebooks/population-genetics.py)
    1. [Discrete-time univariate stochastic model: Wright-Fisher model](notebooks/wright-fisher.py)
    1. [Continuous-time multivariate stochastic model: SIR model](notebooks/gillespie.py)
    1. [Maximum likelihood estimation](notebooks/mle.py)
    1. [Bayesian inference](notebooks/bayesian.py)
    1. [Generalized linear models 1: Exponential growth](notebooks/exponential-growth.py)
    1. [Generalized linear models 2: COVID-19 survival](notebooks/logistic-model.py)
    1. [Bayesian inference in non-linear dynamic models: Predator-prey model](notebooks/bayesian_ode.py)
    1. [Likelihood-free inference: Animal social networks](notebooks/lfi.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Marimo help

    - Docs: [Marimo documentation](https://docs.marimo.io)
    - Intro tutorial (CLI): run `pixi run marimo tutorial intro`
    - Notebook editing: run `pixi run marimo edit index.py`
    """)
    return


if __name__ == "__main__":
    app.run()
