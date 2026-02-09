import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data analysis: Pandas and Seaborn

    ## [Scientific Computing with Python](http://scicompy.yoavram.com)
    ## Yoav Ram

    [![Pandas banner](http://pandas.pydata.org/_static/pandas_logo.png)](http://pandas.pydata.org/)

    _Pandas_ is a very strong library for manipulating large and complex datasets using a new data structure, the **data frame**, which models a table of data.
    Pandas helps to close the gap between Python and R for data analysis and statistical computing.

    Pandas data frames address three deficiencies of NumPy arrays:

    - data frame hold heterogenous data; each column can have its own numpy.dtype,
    - the axes of a data frame are labeled with column names and row indices,
    - and, they account for missing values which this is not directly supported by arrays.

    Data frames are extremely useful for data manipulation.
    They provide a large range of operations such as filter, join, and group-by aggregation, as well as plotting.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    print('Pandas version:', pd.__version__)
    return mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Statistical Analysis of Life History Traits
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will analyze animal life-history data from [AnAge](http://genomics.senescence.info/download.html#anage).
    We will get the data from the download page, but it's compressed with zip so we need to unzip it and then we can read the data using _pandas_ `read_table` function:
    """)
    return


@app.cell
def _():
    import urllib.request
    import zipfile
    import os.path

    return os, urllib, zipfile


@app.cell
def _(os, urllib):
    url = 'http://genomics.senescence.info/species/dataset.zip'
    fname = '../data/anage_dataset.zip'
    if not os.path.exists(fname):
        urllib.request.urlretrieve(url, fname)
    print("Data file exists:", os.path.exists(fname))
    return (fname,)


@app.cell
def _(fname, pd, zipfile):
    with zipfile.ZipFile(fname) as z:
        f = z.open('anage_data.txt')
        data = pd.read_table(f) # lots of other pd.read_... functions
    print(type(data))
    print(data.shape)
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pandas holds data in `DataFrame` (similar to _R_).
    `DataFrame` have a single row per observation (in contrast to the previous exercise in which each table cell was one observation), and each column has a single variable. Variables can be numbers or strings.

    The `head` method gives us the 5 first rows of the data frame.
    """)
    return


@app.cell
def _(data):
    data.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `DataFrame` has many of the features of `numpy.ndarray` - it also has a `shape` and various statistical methods (`max`, `mean` etc.).
    However, `DataFrame` allows richer indexing.
    For example, let's browse our data for species that have body mass greater than 300 kg.
    First we will a create new column (`Series` object) that tells us if a row is a large animal row or not:
    """)
    return


@app.cell
def _(data):
    large_index = data['Body mass (g)'] > 300 * 1000 # 300 kg
    large_index.head()
    return (large_index,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we slice our data with this boolean index.
    The `iterrows` method let's us iterate over the rows of the data.
    For each row we get both the row as a `Series` object (similar to `dict` for our use) and the row number as an `int` (this is similar to the use of `enumerate` on lists and strings).
    """)
    return


@app.cell
def _(data, large_index):
    large_data = data[large_index]
    for _, row in large_data.iterrows(): 
        print(row['Common name'], row['Body mass (g)']/1000, 'kg')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So... a [Dromedary](http://en.wikipedia.org/wiki/Dromedary) is the single-humped camel.

    ![Camel](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Camelus_dromedarius_on_Sinai.jpg/220px-Camelus_dromedarius_on_Sinai.jpg)

    Let's continue with small and medium animals.
    """)
    return


@app.cell
def _(data):
    data_1 = data[data['Body mass (g)'] < 300000.0]
    return (data_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that this statement also removed animals with `NaN` body mass (flies, bees...) as `NaN` is *not* smaller than 300,000.

    Before we continue, I prefer to have mass in kg, let's add a new column:
    """)
    return


@app.cell
def _(data_1):
    data_1['Body mass (kg)'] = data_1['Body mass (g)'] / 1000
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's plot a scatter of body mass vs. metabolic rate.
    Because we work with pandas, we can do that with the `plot` method of `DataFrame`, specifying the columns for `x` and `y` and a plotting style (without the style we would get a line plot which makes no sense here).
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt

    return (plt,)


@app.cell
def _(data_1):
    data_1.plot.scatter(x='Body mass (kg)', y='Metabolic rate (W)', legend=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The points are concentrated at low body mass, let's use a log scale.
    """)
    return


@app.cell
def _(data_1, plt):
    data_1.plot.scatter(x='Body mass (kg)', y='Metabolic rate (W)', legend=False)
    plt.xscale('log')
    plt.yscale('log')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From this plot it seems that
    1. there is a correlation between body mass and metabolic rate, and
    1. there are many small animals (less than 30 kg) and not many medium animals (between 50 and 300 kg) - the body mass seems almost log-uniform distributed, and
    1. it seems there are some animals with a different relationship between body mass and metabolic rate given by the points that are way below the main mass of points.

    What kind of animals do we have here, anyway?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, let's check how many records do we have for each Class (as in the taxonomic unit):
    """)
    return


@app.cell
def _(data_1):
    class_counts = data_1['Class'].value_counts()
    print(class_counts)
    return (class_counts,)


@app.cell
def _(class_counts, plt):
    class_counts.plot.bar()
    plt.ylabel('Num. of species');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So we have lots of mammals and birds, and a few reptiles and amphibians. This is important as amphibian and reptiles could have a different replationship between mass and metabolism because they are cold blooded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise

    1) Check how many reptiles are in this dataset, and how many of them are of the genus `Python`.
    """)
    return


@app.cell
def _(pythons, reptiles):
    print("# of reptiles: ", reptiles)
    print("# of pythons: ", pythons)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2) Plot the number of species in each amphibian genus - use `value_counts` as above.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Seaborn

    Let's do a simple linear regression plot; but let's do it in separate for each Class. We can do this kind of thing with Matplotlib and [SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html), but a very good tool for statistical visualizations is **[Seaborn](http://seaborn.pydata.org)**.

    Seaborn adds on top of Pandas a set of sophisticated statistical visualizations, similar to [ggplot2](http://ggplot2.org) for R.
    """)
    return


@app.cell
def _():
    import seaborn as sns
    sns.set_context("talk")
    return (sns,)


@app.cell
def _(data_1, sns):
    sns.lmplot(x='Body mass (kg)', y='Metabolic rate (W)', hue='Class', data=data_1, ci=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - `hue` means _color_, but it also causes _seaborn_ to fit a different linear model to each of the Classes.
    - `ci` controls the confidence intervals. I chose `False`, but setting it to `True` will show them.

    We can see that mammals and birds have a clear correlation between size and metabolism and that it extends over a nice range of mass, so let's stick to mammals; next up we will see which orders of mammals we have.
    """)
    return


@app.cell
def _(data_1, plt):
    mammalia = data_1[data_1['Class'] == 'Mammalia']
    order_counts = mammalia['Order'].value_counts()
    plt.figure(figsize=(6, 8))
    order_counts.plot.barh()
    plt.xlabel('Num. of species')
    plt.ylabel('Mammalia order')
    return mammalia, order_counts


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You see we have alot of rodents and carnivores, but also a good number of bats (_Chiroptera_) and primates.

    Let's continue with orders that have at least 20 species - this also includes some cool marsupials like Kangaroo, Koala and [Taz](http://upload.wikimedia.org/wikipedia/en/c/c4/Taz-Looney_Tunes.svg) (Diprotodontia and Dasyuromorphia)
    """)
    return


@app.cell
def _(mammalia, order_counts):
    orders = order_counts[order_counts >= 20]
    print(orders)
    abund_mammalia = mammalia[mammalia['Order'].isin(orders.index)]
    return (abund_mammalia,)


@app.cell
def _(abund_mammalia, sns):
    sns.lmplot(
        x='Body mass (kg)', 
        y='Metabolic rate (W)', 
        hue='Order',
        data=abund_mammalia, 
        ci=False
    );
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This plot ain't very good: part of the problem is that some orders are large (e.g. primates) and some are small (e.g. rodents).

    Let's plot a separate regression plot for each order.
    We do this using the `col` and `row` arguments of `lmplot`, but in general this can be done for any plot using [seaborn's `FacetGrid` function](http://stanford.edu/~mwaskom/software/seaborn/tutorial/axis_grids.html).
    """)
    return


@app.cell
def _(abund_mammalia, sns):
    sns.lmplot(
        x='Body mass (kg)', 
        y='Metabolic rate (W)', 
        data=abund_mammalia, 
        hue='Order',
        col='Order', 
        col_wrap=3, 
        ci=None, 
        sharex=False, 
        sharey=False
    );
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We used the `sharex=False` and `sharey=False` arguments so that each Order will have a different axis range and so the data is will spread nicely.

    Last but not least, let's have a closer look at the corelation between mass and metabolism in primates.
    """)
    return


@app.cell
def _(mammalia, sns):
    primates = mammalia[mammalia['Order'] == 'Primates']
    print(' | '. join(sorted(primates["Common name"])))
    sns.lmplot(
        x='Body mass (kg)', 
        y='Metabolic rate (W)', 
        data=primates
    );
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Linear model with SciPy

    Now that we believe there is a linear relationship, let's calculate it with SciPy.
    """)
    return


@app.cell
def _():
    import numpy as np
    from scipy.stats import linregress

    return linregress, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Reminder, the model is:
    $$
    y = a x + b
    $$
    """)
    return


@app.cell
def _(linregress, mammalia):
    x, y = mammalia['Body mass (kg)'].values, mammalia['Metabolic rate (W)'].values
    model = linregress(x, y)
    print(model)
    return model, x, y


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The p-value is surprisingly low, while the r-value is very high, so that's good.

    Let's plot it.
    """)
    return


@app.cell
def _(model, plt, x, y):
    _a, _b = (model.slope, model.intercept)
    _idx = x.argsort()
    x_1 = x[_idx]
    y_1 = y[_idx]
    plt.plot(x_1, y_1, '.k')
    plt.plot(x_1, _a * x_1 + _b)
    plt.xlabel('Body mass')
    plt.ylabel('Metabolic rate')
    return x_1, y_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The points for small animals are very concentrated, let's try a log-scale.
    We'll also take the linear model in the log-scale, that is:
    $$
    \log{y} = a \log{x} + b
    $$
    """)
    return


@app.cell
def _(linregress, np, plt, x_1, y_1):
    model_1 = linregress(np.log10(x_1), np.log10(y_1))
    print(model_1)
    _a, _b = (model_1.slope, model_1.intercept)
    _idx = x_1.argsort()
    x_2 = x_1[_idx]
    y_2 = y_1[_idx]
    plt.plot(x_2, y_2, '.k')
    plt.plot(x_2, 10 ** (_a * np.log10(x_2) + _b))
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Body mass')
    plt.ylabel('Metabolic rate')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Which model is better? How can we determine?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # References

    - Examples: [Seaborn example gallery](http://seaborn.pydata.org/examples/index.html)
    - Slides: [Statistical inference with Python](https://docs.google.com/presentation/d/1imQAEmNg4GB3bCAblauMOOLlAC95-XvkTSKB1_dB3Tg/pub?slide=id.p) by Allen Downey
    - Book: [Think Stats](greenteapress.com/thinkstats2/html/index.html) by Allen Downey - statistics with Python. Free Ebook.
    - Blog post: [A modern guide to getting started with Data Science and Python](http://twiecki.github.io/blog/2014/11/18/python-for-data-science/)
    - Tutorial: [An Introduction to Pandas](http://www.synesthesiam.com/posts/an-introduction-to-pandas.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Colophon
    This notebook was written by [Yoav Ram](http://python.yoavram.com) and is part of the [_Scientific Computing with Python_](https://scicompy.yoavram.com/) course at IDC Herzliya.

    The notebook was written using [Python](http://python.org/) 3.6.5.
    Dependencies listed in [environment.yml](../environment.yml).

    This work is licensed under a CC BY-NC-SA 4.0 International License.

    ![Python logo](https://www.python.org/static/community_logos/python-logo.png)
    """)
    return


if __name__ == "__main__":
    app.run()
