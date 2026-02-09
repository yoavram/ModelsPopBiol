import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Numerical Python: NumPy

    ## [Scientific Computing with Python](http://scicompy.yoavram.com)
    ## Yoav Ram

    [NumPy](http://www.numpy.org/) is the fundamental package for scientific computing with Python. It contains arrays, math functions, linear algebra, random number capabilities and much more.

    # [![Numpy logo](https://numfocus.org/wp-content/uploads/2016/07/numpy-logo-300.png)](https://matplotlib.org/gallery/mplot3d/voxels_numpy_logo.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Importing NumPy

    The convention is `import numpy as np`. This loads the entire NumPy package once, and uses an alias `np` so that we don't pollute our code with too much `numpy`.

    Some people like to do `from numpy import *`. This is frowned-upon as it pollutes the namespace: it overrides the default `sum` and hides the fact that we are using specific `numpy` functions.

    If you only need specific NumPy objects you can load them using `from numpy import array, ones` etc.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    print("Numpy version:", np.__version__)
    return mo, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Analyzing Patient Data

    We are studying inflammation in patients who have been given a new treatment for arthritis, and need to analyze the first dozen data sets. The data sets are stored in comma-separated values (CSV) format: each row holds information for a single patient, and the columns represent successive days. The first few rows of our data file look like this:

    > 0,0,1,3,1,2,4,7,8,3,3,3,10,5,7,4,7,7,12,18,6,13,11,11,7,7,4,6,8,8,4,4,5,7,3,4,2,3,0,0
    0,1,2,1,2,1,3,2,2,6,10,11,5,9,4,4,7,16,8,6,18,4,12,5,12,7,11,5,11,3,3,5,4,4,5,5,1,1,0,1
    0,1,1,3,3,2,6,2,5,9,5,7,4,5,4,15,5,11,9,10,19,14,12,17,7,12,11,7,4,2,10,5,4,2,2,3,2,2,1,1
    0,0,2,0,4,2,2,1,6,7,10,7,9,13,8,8,15,10,10,7,17,4,4,7,6,15,6,4,9,11,3,5,6,3,3,4,2,3,2,1
    0,1,1,3,3,1,3,5,2,4,4,7,6,5,3,10,8,10,6,17,9,14,9,7,13,9,12,6,7,7,9,6,3,2,2,4,2,0,1,1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Loading data from file

    First let's get the file from the internet using the `urllib` module:
    """)
    return


@app.cell
def _():
    import urllib.request
    import os.path

    return os, urllib


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First thing, we need to copy the file from the web to our local disk. This is done using the `urllib.request.urlretrieve` function:
    """)
    return


@app.cell
def _(os, urllib):
    url = r"https://raw.githubusercontent.com/swcarpentry/python-novice-inflammation/gh-pages/data/inflammation-01.csv"
    fname = "../data/inflammation-01.csv"
    if not os.path.exists(fname):
        urllib.request.urlretrieve(url, fname)
    print("Data file exists:", os.path.exists(fname))
    return (fname,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We saved the file to the local filesystem.
    We can have a look at the file contents from the notebook by calling the notebook magic command `%cat <filename>`, replacing `<filename>` with the name of the file, or with the variable, prepended by `$`.
    """)
    return


@app.cell
def _():
    # %cat $fname
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we read the file into a NumPy array - the new data structure which is the center of all scientific Python.
    """)
    return


@app.cell
def _(fname, np):
    data = np.loadtxt(fname, delimiter=',')
    print(data)
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The expression `np.loadtxt(...)` is a function call that asks Python to run the function `loadtxt` that belongs to the `numpy` library. This dotted notation is used everywhere in Python to refer to the parts of things as `thing.component` (see: [namespaces](https://stackoverflow.com/a/3913488/1063612)).

    `numpy.loadtxt` has two arguments: the name of the file we want to read, and the delimiter that separates values on a line. These arguments need to be strings, so we put them in quotes (either `'` or `"`, it doesn't matter).

    We saved the output of `loadtxt` to the variable `data`.
    When we `print(data)`, only a few rows and columns are shown (with `...` to omit elements when displaying big arrays).
    To save space, Python displays numbers as `1.` instead of `1.0` when there's nothing interesting after the decimal point.

    ### Other ways to load data from files

    - `np.load`: Load arrays or [pickled](https://docs.python.org/3/library/pickle.html?highlight=pickle#module-pickle) objects from pickled files, saved using `np.save` with the extension `.npy` or `.npz` (the latter for gzip compressed files).
    - `np.fromstring`: A new 1D array initialized from raw binary (`bytes`).
    - `np.fromregex`: Construct an array from a text file, using regular expression parsing.
    - [`np.genfromtxt`](https://docs.scipy.org/doc/numpy-dev/user/basics.io.genfromtxt.html): provides more sophisticated handling of, e.g. lines with missing values.

    There are some more special I/O functions in [scipy.io](https://docs.scipy.org/doc/scipy/reference/io.html), for example for reading MATLAB data files and audio files, and [imageio](http://imageio.github.io) for reading image files.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Manipulating Data

    Now that our data is in memory, we can start doing things with it. First, let's ask what type of thing data refers to:
    """)
    return


@app.cell
def _(data):
    print(type(data))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The output tells us that data currently refers to an N-dimensional array created by the NumPy library. We can see what its shape is like this:
    """)
    return


@app.cell
def _(data):
    print(data.shape)
    n_patients,n_days = data.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tells us that `data` has 60 rows and 40 columns, which are 60 patients and 40 days. `data.shape` is a member of `data`, i.e. a value that is stored as part of an object.
    We use the same dotted notation for the members of objects that we use for the functions in libraries because they have the same part-and-whole relationship.

    If we want to get a single value from the matrix, we must provide an index in square brackets, just as we do with a `list`, but with as many indices as the number of dimensions in `shape` (two in this case):
    """)
    return


@app.cell
def _(data):
    print("first value in data", data[0,0])
    print("middle value in data:", data[30, 20])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The expression `data[30, 20]` may not surprise you, but `data[0, 0]` might. Programming languages like Fortran and MATLAB start counting at 1, because that's what human beings have done for thousands of years. Languages in the C family (including C++, Java, Perl, and Python) count from 0 because that's simpler for computers to do. Just like with `list` and `str`, if we have an M×N array in Python, its indices go from 0 to M-1 on the first axis and 0 to N-1 on the second. It takes a bit of getting used to, but one way to remember the rule is that the index is how many steps we have to take from the start to get the item we want.

    > **In the Corner.**
    > What may also surprise you is that when Python displays an array, it shows the element with index [0, 0] in the upper left corner rather than the lower left. This is consistent with the way mathematicians draw matrices, but different from the Cartesian coordinates. The indices are (row, column) instead of (column, row) for the same reason, which can be confusing when plotting data.

    An index like `[30, 20]` selects a single element of an array, but we can select whole sections as well. For example, we can select the first ten days (columns) of values for the first four (rows) patients like this:
    """)
    return


@app.cell
def _(data):
    print(data[0:4, 0:10])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The slice `0:4` means, "Start at index 0 and go up to, but not including, index 4." Again, the up-to-but-not-including takes a bit of getting used to, but the rule is that the difference between the upper and lower bounds is the number of values in the slice.

    We don't have to start slices at 0:
    """)
    return


@app.cell
def _(data):
    print(data[5:10, 0:10])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We also don't have to include the upper and lower bound on the slice. If we don't include the lower bound, Python uses 0 by default; if we don't include the upper, the slice runs to the end of the axis, and if we don't include either (i.e. if we just use ':' on its own), the slice includes everything:
    """)
    return


@app.cell
def _(data):
    small = data[:3, 36:]
    print('small is:')
    print(small)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise

    1. Print the last value of the array, that is, the value at the last row and last column.
    1. Print the entire last row.
    1. Print the entire last column.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Operations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also perform common arithmetic operations on arrays: add, subtract, multiply, divide, etc.
    When you perform these operations on arrays, the operation is done on each individual element of the array, i.e. elementwise.
    """)
    return


@app.cell
def _(data):
    doubledata = data * 2.0
    return (doubledata,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    will create a new array `doubledata` whose elements have the value of two times the value of the corresponding elements in `data`.
    """)
    return


@app.cell
def _(data, doubledata):
    print('original:')
    print(data[:3, 36:])
    print('doubledata:')
    print(doubledata[:3, 36:])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is also much faster than doing it with vanilla Python (`%timeit` is a magic command for measuring running time of single lines; use `%%timeit` to measure time of a whole cell).
    """)
    return


@app.cell
def _():
    n = 100000
    # %timeit [x**2 for x in range(n)]
    # %timeit np.arange(n)**2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also use binary (i.e. with two arguments) arithmetic operations like addition:
    """)
    return


@app.cell
def _(data, doubledata):
    tripledata = doubledata + data
    return (tripledata,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    will give you an array where `tripledata[0,0]` will equal `doubledata[0,0]` plus `data[0,0]`, and so on for all other elements of the arrays.
    """)
    return


@app.cell
def _(tripledata):
    print('tripledata:')
    print(tripledata[:3, 36:])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Just another comparison:
    """)
    return


@app.cell
def _():
    # %timeit [x + x**0.5 for x in range(n)]
    # %timeit x = np.arange(n); x + x**0.5
    n_1 = 10000
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise

    Calculate the square root of the data using `numpy`.
    Print the result for the first 5 columns of the first 3 rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Getting help

    You can try:
    """)
    return


@app.cell
def _(np):
    help(np.arange)
    return


@app.cell
def _(np):
    np.lookfor('zeros')
    return


@app.cell
def _(np):
    np.lookfor('concat')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Descriptive statistics

    Often, we want to do more than add, subtract, multiply, and divide values of data.
    We can also do descriptive statistics on arrays.
    If we want to find the average inflammation for all patients on all days, for example, we can just calculate the mean vakue of the array.
    """)
    return


@app.cell
def _(data):
    data.mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `mean` is a method of the array, i.e. a function that belongs to it in the same way that the member shape does. If variables are nouns, methods are verbs: they describe operations that can be perfomed on the object.
    This is why `data.shape` doesn't need to be called (it's a member, not a method) but `data.mean()` does (it's a method).
    It is also why we need empty parentheses for `data.mean()`: even when we're not passing in any arguments, parentheses are how we tell Python to call a function (what would happen if you just use `data.mean`?).

    NumPy arrays have lots of useful methods:
    """)
    return


@app.cell
def _(data):
    print('maximum inflammation:', data.max())
    print('minimum inflammation:', data.min())
    print('standard deviation:', data.std())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When analyzing data, though, we often want to look at marginal statistics, such as the maximum value per patient or the average value per day.
    One way to do this is to select the data we want to create a new temporary array, then ask it to do the calculation:
    """)
    return


@app.cell
def _(data):
    patient_0 = data[0, :] # 0 on the first axis, everything on the second
    print('maximum inflammation for patient 0:', patient_0.max())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What if we need the maximum inflammation for all patients, or the average for each day? As the diagram below shows, we want to perform the operation across an axis:
    ![axis example](https://github.com/swcarpentry/python-novice-inflammation/raw/gh-pages/fig/python-operations-across-axes.png)
    To support this, most array methods allow us to specify the axis we want to work on.
    If we ask for the average across axis 0, we get:
    """)
    return


@app.cell
def _(data):
    print(data.mean(axis=0))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As a quick check, we can check the shape of the result:
    """)
    return


@app.cell
def _(data):
    print(data.mean(axis=0).shape)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The expression `(40,)` tells us we have an 1D array of length 40, so this is the average inflammation per day for all patients. If we average across axis 1, we get:
    """)
    return


@app.cell
def _(data):
    print(data.mean(axis=1))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    which is the average inflammation per patient across all days.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise

    On which day did each patient had the most inflammation?
    Use `data.argmax` to find out.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Creating arrays

    There are [5 general mechanisms for creating arrays](https://docs.scipy.org/doc/numpy-dev/user/basics.creation.html):

    1. Conversion from other Python structures (e.g., lists, tuples)
    1. Intrinsic numpy array creation objects (e.g., `arange`, `ones`, `zeros`, etc.)
    1. Reading arrays from disk, either from standard or custom formats
    1. Creating arrays from raw bytes through the use of strings or buffers
    1. Use of special library functions (e.g., `numpy.random`)


    Let's start by pecifying a list or list of lists to the `np.array` function:
    """)
    return


@app.cell
def _(np):
    a = np.array([0, 1, 2, 3])
    print(a)
    type(a), a.dtype
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `dtype` attribute gives the data-type.

    We can force a specific data-type:
    """)
    return


@app.cell
def _(np):
    a_1 = np.uint64([0, 1, 2, 3])
    print(a_1)
    (type(a_1), a_1.dtype)
    return


@app.cell
def _(np):
    a_2 = np.float16([0, 1, 2, 3])
    print(a_2)
    (type(a_2), a_2.dtype)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    NumPy has many [data-types](https://docs.scipy.org/doc/numpy-dev/user/basics.types.html), we'll focus on the default `int` and `float` today.

    We can create a 2D array from nested lists - make sure that all nested lists have the same length.
    """)
    return


@app.cell
def _(np):
    b = np.array(
        [
            [0, 1, 2], 
            [3, 4, 5]
        ]
    )
    print(b)
    return


@app.cell
def _(np):
    c = np.array(
        [
            [
                [1], 
                [2]
            ], 
            [
                [3], 
                [4]
            ]
        ]
    )
    print(c)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Arrays are N-dimensional, so you can specify how many dimensions that you would like:
    """)
    return


@app.cell
def _(np):
    d = np.array(
        [
            [
                [1, 2],
                [3, 4],
            ],
            [
                [5, 6],
                [7, 8],
            ],        
        ]
    )
    print(d)
    return (d,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Check the number of dimensions and the shape:
    """)
    return


@app.cell
def _(d):
    print(d.ndim)
    print(d.shape)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use `np.arange`, whish is similar to `range`, but also accepts `float`s:
    """)
    return


@app.cell
def _(np):
    a_3 = np.arange(10)  # end (exclusive)
    print(a_3)
    return


@app.cell
def _(np):
    b_1 = np.arange(-1.5, 9.5, 0.2)  # start, end (exclusive), step
    print(b_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `np.linspace` is similar, but it accepts the required number of points rather than the required step.
    """)
    return


@app.cell
def _(np):
    c_1 = np.linspace(0, 1, 6)  # start, end, num-points
    print(c_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Say we want to produce an array of the squares of numbers from 0 to 99.
    There are a bunch of ways to do it using list comprehensions, `np.arange`, and using different approached for squaring the numbers.

    **Note**: currently NumPy doesn't use generator expressions for creating an array, so `np.array(x**2 for x in range(n))` doesn't work. There is an open [issue](https://github.com/numpy/numpy/pull/5863) on this.

    Let's compare the different approaches in terms of running time:
    """)
    return


@app.cell
def _():
    # %timeit np.array([x**2 for x in range(n)])
    # %timeit np.array([x**2 for x in np.arange(n)])
    # %timeit np.power(np.arange(n), 2)
    # %timeit np.power(range(n), 2)
    # %timeit np.arange(n)**2
    n_2 = 100000
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The fastest way to do it was also the most elegant, `np.arange(n)**2`, which makes us happy because:

    > Beautiful is better than ugly.
    Simple is better than complex.
    Flat is better than nested.
    Readability counts.
    There should be one-- and preferably only one --obvious way to do it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise

    Create an array with the inverse ($1/x$) of the even numbers lower than or equal to 100.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creating arrays - continued
    You can can create an empty array of a certain shape (which is given as a `tuple`) or with the same shape as another array; of course, the array will not actually be empty, but rather will have some arbitrary values as it will not be initialized.
    """)
    return


@app.cell
def _(np):
    d_1 = np.empty((2, 4))
    print(d_1)
    return (d_1,)


@app.cell
def _(d_1, np):
    f = np.empty_like(d_1)
    print(f)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can create an array full of 1s or 0s, or any single number:
    """)
    return


@app.cell
def _(np):
    a_4 = np.ones((3, 3))
    print(a_4)
    return


@app.cell
def _(np):
    a_5 = 5.134 * np.ones((3, 3))
    print(a_5)
    return


@app.cell
def _(np):
    b_2 = np.zeros((2, 2))
    print(b_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Create the identity matrix:
    """)
    return


@app.cell
def _(np):
    c_2 = np.eye(3)
    print(c_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Create matrices by specifying the digonals:
    """)
    return


@app.cell
def _(np):
    d_2 = np.diag([1, 2, 3, 4])
    print(d_2)
    return


@app.cell
def _(np):
    d_3 = np.diag([1, 2, 3], 1) + np.diag([4, 5, 6], -1)
    print(d_3)
    return (d_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Create matrices by reshaping another matrix or array:
    """)
    return


@app.cell
def _(d_3):
    f_1 = d_3.reshape((2, 8))
    print(f_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise

    Skim through the documentation for `np.ravel`, and use this function to construct the array:
    ```py
    [1. 0. 0. 0. 1. 0. 0. 0. 1.]
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Random arrays

    We'll set the random seed for reproducability (i.e. to get the same result every time), but in real-life application you should think if you want to set the seed.
    """)
    return


@app.cell
def _(np):
    np.random.seed(1231410)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Start with drawing a single random number uniformly between 0 and 1:
    """)
    return


@app.cell
def _(np):
    np.random.random()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    An array of four random numbers between 0 and 1:
    """)
    return


@app.cell
def _(np):
    a_6 = np.random.random(size=4)
    print(a_6)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A 3x3 matrix or random numbers drawn from a normal distribution with mean 1 and standard deviation 0.5:
    """)
    return


@app.cell
def _(np):
    b_3 = np.random.normal(1, 0.5, size=(3, 3))
    print(b_3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now draw a 3x2x4 array from a Poisson distribution with mean 5:
    """)
    return


@app.cell
def _(np):
    c_3 = np.random.poisson(5, size=(3, 2, 4))
    print(c_3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise

    1) Create a 4x5x6 array with numbers drawn from a geometric distribution with `p=0.1` (the number of trails until success, where the probability of success is `p`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2) Normalize a 5x5 random matrix - that is, first subsctract by the minimum and then divide by the new maximum.
    """)
    return


@app.cell
def _(np):
    Z = np.random.random((5, 5))
    print(Z)
    return (Z,)


@app.cell
def _(Z):
    # your code here
    print(Z)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Broadcasting

    A very powerful mechanism of NumPy arrays is [broadcasting](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html).
    Broadcasting is used when an operation is used on two arrays of different shapes.
    The rules are:

    1. If arrays dimension differ, left-pad the smaller array's shape with 1s.
    1. If the shapes differ, change any dimension of size 1 to match the dimension of the other array.
    1. If shapes still differ, raise an error.

    Some exmaples:
    ![broadcasting examples](http://www.astroml.org/_images/fig_broadcast_visual_1.png)
    """)
    return


@app.cell
def _(np):
    np.arange(3) + 5
    return


@app.cell
def _(np):
    np.ones((3,3)) + np.arange(3)
    return


@app.cell
def _(np):
    np.arange(3).reshape((3, 1)) + np.arange(3)
    return


@app.cell
def _(np):
    np.ones((3,3)) + np.ones((3,2))
    return


@app.cell
def _(np):
    np.ones((3,3,1)) + np.ones((3,1,3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise

    Given a 1D array `X`, calculate the differences between each two elements of `X` using broadcasting and save it to array `D`.
    """)
    return


@app.cell
def _(np):
    X = np.linspace(0, 1, 50)
    return


@app.cell
def _():
    # your code here
    return


@app.cell
def _(D):
    assert D.shape == (50, 50)
    assert (D.diagonal() == 0).all()
    assert (D[5,5] == D[-5,-5])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Indexing and slicing

    [Indexing and slicing](https://docs.scipy.org/doc/numpy-dev/user/basics.indexing.html) on 1D arrays is similar to Python lists:
    """)
    return


@app.cell
def _(np):
    a_7 = np.arange(1, 10)
    print(a_7)
    print(a_7[3])
    print(a_7[2:5])
    print(a_7[-2:-5:-1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    However, inconsistent with lists, array slicing returns a **view** rather then a copy, so **changing a slices changes the original array**:
    """)
    return


@app.cell
def _():
    print('Lists:')
    a_8 = [1, 2, 3, 4, 5, 6]
    b_4 = a_8[2:5]
    print('a is b?', a_8 is b_4)
    print(a_8)
    b_4[0] = 0
    print(a_8)
    return


@app.cell
def _(np):
    print('Arrays:')
    a_9 = np.arange(1, 7)
    b_5 = a_9[2:5]
    print('a is b?', a_9 is b_5)
    print(a_9)
    b_5[0] = 0
    print(a_9)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is useful if you want to save space and the CPU required by copying arrays, but it can also be dangerous.
    If you explicitly want a **copy** rather than a **view**, call the `copy` method.
    """)
    return


@app.cell
def _(np):
    print('Arrays:')
    a_10 = np.arange(1, 7)
    b_6 = a_10[2:5].copy()
    print('a is b?', a_10 is b_6)
    print(a_10)
    b_6[0] = 0
    print(a_10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Arrays support multidimensional indexing and slicing:
    """)
    return


@app.cell
def _(np):
    a_11 = np.diag([1, 2, 3])
    print(a_11)
    print()
    print(a_11[:2, 1:])
    return


@app.cell
def _(np):
    y = np.arange(35).reshape(5,7)
    print(y)
    return (y,)


@app.cell
def _(y):
    print(y[0])
    print(y[0,:])
    return


@app.cell
def _(y):
    print(y[:,1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Arrays can also be indexed using an array or list of indices, this is called **fancy indexing**:
    """)
    return


@app.cell
def _(np):
    a_12 = np.arange(10, 30, 1)
    print(a_12)
    b_7 = a_12[[1, 6, 9]]
    print(b_7)
    b_7 = a_12[[1, 6, 9, 9, 9, 9, 9, 9]]
    print(b_7)
    return


@app.cell
def _(y):
    print(y[[1,2,3]])
    return


@app.cell
def _(y):
    print(y)
    print(y[ [0, 2], [1, 2] ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If one of the indexing lists is smaller than the other, NumPy will attempt broadcasting:
    """)
    return


@app.cell
def _(y):
    print(y[ [0, 2], [1] ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But broadcasting isn't always possible:
    """)
    return


@app.cell
def _(y):
    y[[0,2,4], [0,1]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The broadcasting mechanism permits index arrays to be combined with scalars for other indices. The effect is that the scalar value is used for all the corresponding values of the index arrays:
    """)
    return


@app.cell
def _(y):
    print(y[[0,2,4], 1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Boolean or mask arrays

    You can create boolean arrays by using the comparison operators:
    """)
    return


@app.cell
def _(np):
    a_13 = np.random.random(size=(4, 4))
    print(a_13)
    b_8 = a_13 < 0.5
    print(b_8)
    return (a_13,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    These boolean arrays can be used for indexing:
    """)
    return


@app.cell
def _(a_13, np):
    c_4 = np.arange(16).reshape((4, 4))
    print(c_4)
    print(c_4[a_13 < 0.5])
    print(c_4[c_4 > 2])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise

    Given a 1D array, negate (i.e. turn to negative) all elements which are between 3 and 8, in place (i.e. without creating a new array).
    """)
    return


@app.cell
def _(np):
    Z_1 = np.arange(11)
    print(Z_1)
    return (Z_1,)


@app.cell
def _(Z_1):
    # Your code here
    print(Z_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # "Losing Your Loops": Fast Numerical Computing with NumPy

    From the PyCon 2015 conferece, a [presentation](https://speakerdeck.com/jakevdp/losing-your-loops-fast-numerical-computing-with-numpy-pycon-2015) by [Jake VanderPlas](http://vanderplas.com).

    Also available on [YouTube](https://www.youtube.com/watch?v=EEUXKG97YRw).
    """)
    return


@app.cell
def _(mo):
    mo.Html(
        """
        <iframe
          src="https://speakerdeck.com/player/a5d2540d0d4c452d91f8045ede6ca130"
          width="100%"
          height="420"
          style="border: 0;"
          allowfullscreen
        ></iframe>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # References

    - [NumPy MedKit](http://mentat.za.net/numpy/numpy_advanced_slides/) for much more on indexing, slicing, and other advanced NumPy tricks.
    - [NumPy tutorial](https://github.com/rougier/numpy-tutorial) with some exercises.
    - [NumPy basics](https://docs.scipy.org/doc/numpy-dev/user/basics.html)
    - [NumPy for MATLAB users](https://docs.scipy.org/doc/numpy-dev/user/numpy-for-matlab-users.html)
    - [100 NumPy exercise](https://github.com/rougier/numpy-100)
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
