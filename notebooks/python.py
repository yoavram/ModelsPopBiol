import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Python tutorial

    ## [Scientific Computing with Python](http://scicompy.yoavram.com)
    ## Yoav Ram
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Hello Jupyter!

    To execute code in Jupyter notebook press `Shift+Enter` (or `Shift+Return`) or press `Control+Enter` (or `Command+Return`). The former will execute and advance, the later will execute and stay.
    You can also use the ▶️ button on the command pallete above.
    """)
    return


@app.cell
def _():
    print("Hello World!")
    return


@app.cell
def _():
    print("Welcome to Python!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `print` is a builtin function, and it can print text along with some execution -- in general `print` accepts as many arguments as we want, and separates them with spaces.
    """)
    return


@app.cell
def _():
    print("The product of 7 and 8 is", 7 * 8)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise: `print`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Print to the screen the following sentences:

    - "I love Python!"
    - "7 + 6 = RESULT", replacing `RESULT` with the computation of 6+7
    - "my name is NAME", replacing `NAME` with your name
    """)
    return


@app.cell
def _():
    # Your code here:
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Variables

    A variable is a _name_ that references a an _object_ in memory.
    An object has a _value_ and a _type_.

    To bind an _object_ to a _variable_, we use the _assignment_ operator `=`.
    """)
    return


@app.cell
def _():
    a = 5
    return (a,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Once a variable has been declared, we can use its name to get its value:
    """)
    return


@app.cell
def _(a):
    print(a)
    return


@app.cell
def _(a):
    a + 7
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Types

    These are the basic Python data types:

    | Type | Description | Range | Use |
    |--------|-----------|-------|--------|
    | `int`  | Integers | -oo to oo | counting, indexing |
    | `float` | Decimal fractions | limited precision, depends on machine | calculations |
    | `complex` | Complex numbers | just two floats | complex calculations  |
    | `str` | Strings | unicode | text, categories |
    | `bool` | Booleans | `True` and `False` | boolean logic |

    We can determine a variable's type using the `type` function.
    """)
    return


@app.cell
def _(a):
    type(a)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `int`
    The **`int`** type is for integers:
    """)
    return


@app.cell
def _(a):
    type(a)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that in Python 3 integers have unlimited precision:
    """)
    return


@app.cell
def _():
    n = 13891783871827487875832758374287348205743285742386738476843768327683467432876284368236487283476847684376843768207185275128758785712853783275137587357138757
    type(n)
    return (n,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    but the larger the number the more memory it requires:
    """)
    return


@app.cell
def _(a, n):
    n.bit_length(), a.bit_length()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `float`

    **`float`** is for decimal point numbers, and is usually implemented using a double in C:
    """)
    return


@app.cell
def _():
    x = 5.12312983
    type(x)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To get info on float precision with this specific Python build, call (we'll learn about `import` in another session):
    """)
    return


@app.cell
def _():
    import marimo as mo
    import sys
    sys.float_info
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `complex`

    **`complex`** is for complex numbers, in which each component is a `float`. Note that the imaginary part is denoted by `j` rather than `i`, probably because `i` is a common name for loop indices.
    """)
    return


@app.cell
def _():
    (1j)**2
    return


@app.cell
def _():
    z = 4.5 + 3j
    type(z)
    return (z,)


@app.cell
def _(z):
    z.real
    return


@app.cell
def _(z):
    type(z.imag)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We saw three numerical types: `int`, `float`, and `complex`.

    The standard library includes additional numeric types. The *fractions* module deals with rational fractions; the *decimal* module deals with floating-point numbers with user-definable precision.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `str`

    **`str`** is for strings, used for both characters and text.
    Will deal with strings later.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `bool`

    Lastly, **`bool`** is for boolean variables that are either `True` or `False`:
    """)
    return


@app.cell
def _():
    value = True # Camelcase
    type(value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Variable names
    * You *can't include spaces*.
    * In principle, you can use any unicode symbol.
    * You can override words that have special meaning in python (for example `print`), but don't do it unless you have a good reason.
    * The convention is to use *lowercase only* and separate words with *underscores*: `num_atoms`, `first_template`.
    * For more details on Python style conventions, see [PEP8](https://www.python.org/dev/peps/pep-0008/), the Python style guide..
    """)
    return


@app.cell
def _():
    שם = 'יואב'
    print(שם)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Comments

    Everything between a hashtag symbol `#` and the end of the line is a comment.
    """)
    return


@app.cell
def _():
    print("This will be printed")
    # print("This will not be printed")
    print("Another example") # of a comment
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Tip:** In the notebook you can comment and uncomment complete lines by selecting them and pressing `Ctrl+/`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Operators

    ## Arithmetic operators

    | Symbol | Operator                    | Use    |
    |--------|-----------------------------|--------|
    | +      | Addition                    | x + y  |
    | -      | Substraction                | x - y  |
    | *      | Multiplication              | x * y  |
    | **     | Power                   | x ** y |
    | /      | Decimal division            | x / y  |
    | //     | Integer division            | x // y |
    | %      | Integer remainder           | x % y  |

    This is fairly straightforward except maybe integer division `//` and power `**`.
    """)
    return


@app.cell
def _():
    a_1 = 5
    b = 2
    return a_1, b


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Add:
    """)
    return


@app.cell
def _(a_1, b):
    a_1 + b
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Substract:
    """)
    return


@app.cell
def _(a_1, b):
    a_1 - b
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Multipy:
    """)
    return


@app.cell
def _(a_1, b):
    a_1 * b
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Power:
    """)
    return


@app.cell
def _(a_1, b):
    a_1 ** b
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Decimal division:
    """)
    return


@app.cell
def _(a_1, b):
    a_1 / b
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Integer division:
    """)
    return


@app.cell
def _(a_1, b):
    a_1 // b
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Remainder (modulo):
    """)
    return


@app.cell
def _(a_1, b):
    a_1 % b
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise: Pythagoras
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Define two variables, `a` and `b`, and give them numeric values of your choice.

    Assume these are the lengths of the edges of a right angle triangle, and use numeric operators to calculate the length of the hypotenuse (יתר).

    Print out the result.

    Reminder: $c^2 = a^2 + b^2$
    """)
    return


@app.cell
def _():
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Hint**: to calculate the squared root of c, use c\*\*0.5
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Comparison operators
    These operators are used to compare values. They always return boolean values: `True` or `False`.

    | Symbol | Operator          | Use    |
    |--------|-------------------|--------|
    | ==     | Equals            | x == y |
    | !=     | Not equals        | x != y |
    | <      | Smaller than      | x < y  |
    | >      | Larger than       | x > y  |
    | <=     | Smaller or equals | x <= y |
    | >=     | Larger or equals  | x >= y |
    """)
    return


@app.cell
def _(a_1, b):
    a_1 == b  # Note: '==', not '='
    return


@app.cell
def _(a_1, b):
    a_1 > b
    return


@app.cell
def _(a_1, b):
    b > a_1
    return


@app.cell
def _(a_1, b):
    a_1 != b
    return


@app.cell
def _(b):
    b < 5
    return


@app.cell
def _(b):
    b <= 5
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For strings, comparison operators are based on **lexicographical order**.
    """)
    return


@app.cell
def _():
    food = 'Noodles'
    drink = 'Ice Tea'
    food == drink
    return drink, food


@app.cell
def _(drink, food):
    food > drink
    return


@app.cell
def _(drink, food):
    food <= drink
    return


@app.cell
def _(food):
    food == 'Noodles'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Logical operators

    | Keyword | Use     |
    |---------|---------|
    | and     | a and b |
    | or      | a or b  |
    | not     | not a   |
    """)
    return


@app.cell
def _(a_1, b):
    a_1 > b and a_1 != b
    return


@app.cell
def _(a_1, b):
    a_1 != b and a_1 < b
    return


@app.cell
def _(a_1, b):
    a_1 != b or a_1 < b
    return


@app.cell
def _(a_1, b):
    boolean = a_1 > b
    type(boolean)
    return (boolean,)


@app.cell
def _(b, boolean):
    boolean and b == 5
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also think of logical operators as 2X2 matrices, or alternatively - Venn diagrams.

    ![logic_venn](https://raw.githubusercontent.com/yoavram/Py4Life/master/lec1_images/logic_venn.jpg)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Conditional statements
    ## `if` statements

    The `if` statement allows us to condition the program flow on its data.
    """)
    return


@app.cell
def _():
    a_2 = 10
    b_1 = 2
    if a_2 > b_1:
        print('Yes')
    return a_2, b_1


@app.cell
def _(a_2, b_1):
    if a_2 < b_1:
        print('Yes')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice the colon and the indented block. The syntax is always:

    ```py
    if condition:
        statement1
        statement2
        statement3
        ...
    ```

    The condition does not need to be surrounded by round brackets `(...)`.

    **Whitespaces mark block code**: Only commands within the indented block are conditional. Other commands will be executed, no matter if the condition is met or not. There is no use of curly brackets or `end` command: unindenting will close the code block.

    Also, the condition does not need to be surrounded by round brackets `(...)`.

    __Note__: the condition expression is always converted to a boolean -- if it's not already a boolean, it will be implicitly converted into one.
    The indented commands only occur if the boolean has a `True` value.
    Therefore, we can use logical operators to create more complex conditions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `if` example: divisibility

    Let's write a program that checks if a number is devisible by 17. Remember the modulo operator.
    """)
    return


@app.cell
def _():
    n_1 = 442
    if n_1 % 17 == 0:
        print(n_1, 'is devisible by 17!')
    print('End of program')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `else` statements

    We can add _else_ statements to perform commands in case the condition is __not__ met, or in other words, if the boolean is False.

    ![if else flow](https://raw.githubusercontent.com/yoavram/Py4Life/master/lec1_images/if_else_flow.jpg)
    """)
    return


@app.cell
def _():
    n_2 = 586
    if n_2 % 17 == 0:
        print(n_2, 'is devisible by 17!')
    else:
        print(n_2, 'is not devisible by 17!')
    print('End of program')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `elif` statements

    When using _elif_ statements, multiple conditions are tested one by one. Once a condition is met, the corresponding indented commands are performed. If none of the conditions is `True`, the `else` block (if exists) is executed.
    """)
    return


@app.cell
def _():
    n_3 = 586
    if n_3 % 17 == 0:
        print(n_3, 'is devisible by 17!')
    elif n_3 % 2 == 0:
        print(n_3, 'is not devisible by 17, but it is even!')
    else:
        print(n_3, 'is not devisible by 17, and it is odd!')
    print('End of program')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise: leap year
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A leap year is a year that has 366 days (adding February 29th). A year is a leap year if it is divisible by 400, or divisible by 4 but not by 100.

    For example, 2012 and 2000 are leap years, but 1900 isn't.

    Test a year of your choice by  using an appropriate `if` statement and print the result.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `while` loop
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use `while` loops to do something again and again, as long as a condition is met.

    ![while](http://www.tutorialspoint.com/images/python_while_loop.jpg)

    The syntax is very similar to that of `if` statement.

    Let's count how many times it takes to get a random number greater than 90.
    """)
    return


@app.cell
def _():
    from random import randint # we will get back to import later on

    trials = 1
    random_num = randint(1, 100)

    while random_num <= 90:        # condition
        print(random_num)           # indented block
        random_num = randint(1,100) # indented block
        trials = trials + 1
    print ('Found a number greater than 90 (', random_num, ') after ', trials, 'trials.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise: Collatz Conjecture
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Collatz Conjecture (also known as the 3n+1 conjecture) is the conjecture that the following process is finite for every natural number:

    > If the number n is even divide it by two, if it is odd multiply it by 3 and add 1. Repeat this process until you get the number 1.

    Write a program to check if the Collatz conjecture is true for a number of your choice. Print every step of the process.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![CollatzXKCD](http://imgs.xkcd.com/comics/collatz_conjecture.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Sequences
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Strings

    Strings are ordered collections of _characters_.

    _Ordered collections_ means that elements are numbered with _indexes_: 0, 1, 2, 3, 4...
    Note that the first index is 0, __not__ 1!

    We can create new string usings single- or double-quotes: `'` or `"`.
    """)
    return


@app.cell
def _():
    x_1 = 'Jupyter'
    y = 'I love Python'
    print(x_1)
    print(y)
    return (x_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Strings are objects of type `str`:
    """)
    return


@app.cell
def _(x_1):
    type(x_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Multiline strings

    Multiline strings can be defined using `\"\"\"`:
    """)
    return


@app.cell
def _():
    cheeseshop_dialog ="""Customer: 'Not much of a cheese shop really, is it?'
    Shopkeeper: 'Finest in the district, sir.'
    Customer: 'And what leads you to that conclusion?'
    Shopkeeper: 'Well, it's so clean.'
    Customer: 'It's certainly uncontaminated by cheese.'
    """
    print(cheeseshop_dialog)
    type(cheeseshop_dialog)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Concatenation
    We can concatenate strings using the addition operator `+`.
    """)
    return


@app.cell
def _(x_1):
    print(x_1 + '2018')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Conversion
    We can convert string to numbers and vice versa (if it is appropriate).
    """)
    return


@app.cell
def _():
    x_2 = '4'
    y_1 = int(x_2)
    print('y + 1 =', y_1 + 1)
    return x_2, y_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Otherwise, we get an error message...
    """)
    return


@app.cell
def _(x_2):
    print('x + 1 =', x_2 + 1)
    return


@app.cell
def _(y_1):
    x_3 = str(y_1)
    print('x =', x_3)
    return


@app.cell
def _():
    x_4 = '3.14'
    y_2 = float(x_4)
    print('y*2 =', y_2 * 2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Strings as sequences

    Strings are text but can represent other things, too. For example, DNA sequences.

    Again we can concat strings:
    """)
    return


@app.cell
def _():
    upstream = "AAA"
    downstream = "GGG"
    dna = upstream + "ATG" + downstream
    print(dna)
    return (dna,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can find the length of a string using the command `len`:
    """)
    return


@app.cell
def _(dna):
    n_4 = len(dna)
    print('The length of the DNA variable is', n_4)
    dna_1 = dna + 'AGCTGA'
    print('Now it is', len(dna_1))
    return (dna_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Augmented assignment

    We can use augmented assignment to make `dna = dna + x` into `dna += x`:
    """)
    return


@app.cell
def _(dna_1):
    print(dna_1)
    dna_2 = dna_1 + 'AGCTGA'
    print(dna_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Augmented assignment also work with numbers and other operators:
    """)
    return


@app.cell
def _():
    x_5 = 10
    x_5 = x_5 * 7
    print(x_5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Access: Indexing

    We can acces specific characters (sequence items) in a string using square brackets `[i]`:
    """)
    return


@app.cell
def _():
    text = "A musician wakes from a terrible nightmare."
    return (text,)


@app.cell
def _(text):
    print(text[0])
    print(text[5])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Python uses **zero-count** indexing: the first element has index 0.

    In addition, there is also support for **reverse indexing** using negative numbers:
    """)
    return


@app.cell
def _(text):
    print(text[-1])
    print(text[-4])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here, the last element is accessed using -1 index, and so on.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Access: Slicing
    We can extract subsets of a string by using _slicing_, with the corresponding indexes.
    Remember: indexes start from **0**!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can access specific indexes of the list (_starting from 0_)
    """)
    return


@app.cell
def _(text):
    # get the 1st and 6th letters
    print(text[0])
    print(text[5])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Indexes work from the tail as well, using negative indices:
    """)
    return


@app.cell
def _(text):
    # get the last letter
    print(text[-1])
    # get 5th letter from the end
    print(text[-5])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can get a range of indexes using _\[start:end\]_
    """)
    return


@app.cell
def _(text):
    # get the 3rd to 8th letters
    print(text[2:8])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice that the _start_ position is included, but not the _end_ position. We actually take the characters with indexes 2,3,4,5,6,7.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are shortcuts for taking the first and last characters:
    """)
    return


@app.cell
def _(text):
    # get the first 5 letters
    print(text[0:5])
    # or simply:
    print(text[:5])

    # get 3rd to last letters:
    print(text[3:])

    # last 3 letters
    print(text[-3:])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise: String access
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The sequence below (named _seq_) consists of 20 characters.

    1. Print the 2nd and 7th characters.
    2. Print the 2nd character from the end.
    3. Slice the first half of the sequence.
    4. Slice the second half of the sequence.
    5. Slice the middle 10 characters
    """)
    return


@app.cell
def _():
    seq = "CAAGTAATGGCAGCCATTAA"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### String formatting

    There are three ways to do this:
    1. Using `%` (the old way)
    2. Using the `format` method (the new way)
    3. Using [f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) (the very new way)

    We'll mostly use the `format` method

    The `format` method works on a string template, with placeholders marked by curly brackets (who said Python doesn't like curly brackets?).
    The method arguments are parsed to be the values for the placeholders, by order:
    """)
    return


@app.cell
def _():
    _message = 'Hello {}, would you like {} or {} apples?'
    _message = _message.format('Adam Price', 1, 2)
    print(_message)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also specify placeholder's replacement using indices:
    """)
    return


@app.cell
def _():
    _message = 'Hello {0}, my name is {1}, if your name is not {0}, please let me know'
    _message = _message.format('Adam', 'Wendy')
    print(_message)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finally, we can also use named placeholders and specify the values as keyword arguments:
    """)
    return


@app.cell
def _():
    _message = 'Hello {guest}, my name is {host}, if your name is not {guest}, please let me know'
    _message = _message.format(guest='Adam', host='Wendy')
    print(_message)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Format automatically handles numbers and other string conversions:
    """)
    return


@app.cell
def _():
    print("Snowhite and the {} dwarfs".format(7))
    print("Snowhite and the {} dwarfs".format(7.0))
    print("Snowhite and the {} dwarfs".format(7+0j))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But we can specify how to convert numbers, if we want; for example, we can specify the number of decimal digits we want:
    """)
    return


@app.cell
def _():
    x_6 = 7.0554332
    print('Snowhite and the {:.0f} dwarfs'.format(x_6))
    print('Snowhite and the {:.4f} dwarfs'.format(x_6))
    print('Snowhite and the {:.6f} dwarfs'.format(x_6))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    See all formatting options in the [docs](https://docs.python.org/3.6/library/string.html#format-string-syntax).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise: bottles of beer

    Write a template and fill it with values using `format` to produce the following text:

    ```
    3 bottles of beer on the wall, 3 bottles of beer.
    Take one down, pass it around, 2 bottles of beer on the wall...
    2 bottles of beer on the wall, 2 bottles of beer.
    Take one down, pass it around, 1 bottles of beer on the wall...
    1 bottles of beer on the wall, 1 bottles of beer.
    Take one down, pass it around, 0 bottles of beer on the wall...
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### String methods

    Strings have many methods for text processing.

    We can change a string to lowercase:
    """)
    return


@app.cell
def _(text):
    text_1 = text.lower()
    print(text_1)
    return (text_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    and back to uppercase:
    """)
    return


@app.cell
def _(text_1):
    text_2 = text_1.upper()
    print(text_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can replace characters:
    """)
    return


@app.cell
def _():
    dna_3 = 'AAAATGGGGAGCTGAAGCTGA'
    rna = dna_3.replace('T', 'U')
    print(rna)
    return (dna_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Count
    We can count characters.

    For example, let's count the number of histidine (`H`) and proline (`P`) in the [amino-acid](http://upload.wikimedia.org/wikipedia/commons/a/a9/Amino_Acids.svg) sequence of the [Human Insulin](http://www.uniprot.org/blast/?about=P01308) enzyme:
    """)
    return


@app.cell
def _():
    insulin = 'MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN'
    print("# of histidine:", insulin.count('H'))
    print("# of proline:", insulin.count('P'))
    return (insulin,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Find substrings
    We can find a substring within a string.
    For example, we can look for the character `D` in the insulin sequence.
    """)
    return


@app.cell
def _(insulin):
    pos = insulin.index('D')
    print(pos)
    return (pos,)


@app.cell
def _(pos):
    type(pos)
    return


@app.cell
def _(insulin, pos):
    print(insulin[pos])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is the index (position) of the first `D` found in the sequence.

    We can also look for longer substrings, representing motiffs. For example, let's find the position of the Insulin [B-chain](http://www.uniprot.org/blast/?about=P01308[25-54]) - a specific subsequence - in the entire protein sequence:
    """)
    return


@app.cell
def _(insulin):
    b_chain = "FVNQHLCGSHLVEALYLVCGERGFFYTPKT"
    position = insulin.index(b_chain)
    print("Position:", position)
    return b_chain, position


@app.cell
def _(b_chain):
    print(len(b_chain))
    return


@app.cell
def _(b_chain, insulin, position):
    found = insulin[position : position + len(b_chain)] # slicing (notice the ':')
    print(b_chain == found)
    print("Original:", b_chain)
    print("Found:   ", found)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Split

    We can split a string on every occurence of a separator character:
    """)
    return


@app.cell
def _():
    names = "banana,ananas,potato,tomato"
    foods = names.split(",")
    print(foods)
    return (foods,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What do we get?
    """)
    return


@app.cell
def _(foods):
    type(foods)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lists

    Lists are similar to strings in being sequential, only they can contain **any type of data**, not just characters. They are also mutable (we'll get back to that distinction).

    Lists could even include mixed variable types.

    We define a list just like any other variable, but use `[ ]` to surround the list elements and `,` to separate the elements.
    """)
    return


@app.cell
def _():
    # a list of strings
    apes = ["Human", "Gorilla", "Chimpanzee"]
    print(apes)
    return (apes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![Gorila](http://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Western_Lowland_Gorilla_at_Bronx_Zoo_2_cropped.jpg/338px-Western_Lowland_Gorilla_at_Bronx_Zoo_2_cropped.jpg)
    """)
    return


@app.cell
def _():
    # a list of numbers
    nums = [7, 13, 2, 400]
    print(nums)
    return


@app.cell
def _():
    # a mixed list
    _mixed = [12, 'Mouse', True]
    print(_mixed)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Access

    You can access list elements just like strings, using indexes (starting from 0):
    """)
    return


@app.cell
def _(apes):
    print(apes[0])
    print(apes[-1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lists are dynamic and mutable - you can append, remove and insert into them. This is done using _list methods_.

    We can access and change list elements:
    """)
    return


@app.cell
def _(apes):
    new_apes = apes.copy() # make a copy of the apes list
    new_apes[2] = 'Bonobo'
    print(new_apes)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This __does NOT__ work with strings though...
    """)
    return


@app.cell
def _(dna_3):
    print(dna_3)
    dna_3[5] = 'G'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is because strings are **immutable** whereas lists are **mutable**. We'll get back to this notion soon.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### List methods

    Lists also have many methods.
    The most useful ones we'll see here make use of the fact that lists are **mutable**.

    `append` adds an element to the end of the list:
    """)
    return


@app.cell
def _(apes):
    apes.append("Macaco")
    print(apes)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `insert` adds an element at a given index:
    """)
    return


@app.cell
def _(apes):
    apes.insert(2, "Kofiko")
    print(apes)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `remove` finds and deletes an element from list:
    """)
    return


@app.cell
def _(apes):
    apes.remove("Human")
    print(apes)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `pop` deletes an elements from a list by its index:
    """)
    return


@app.cell
def _(apes):
    print(apes.pop(3))
    print(apes)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can concatenate lists, just like strings, using the addition operator:
    """)
    return


@app.cell
def _(apes):
    print(apes + ["Orangutan", "Baboon"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![Organutan](http://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Orang_Utan%2C_Semenggok_Forest_Reserve%2C_Sarawak%2C_Borneo%2C_Malaysia.JPG/220px-Orang_Utan%2C_Semenggok_Forest_Reserve%2C_Sarawak%2C_Borneo%2C_Malaysia.JPG)

    Searching in lists is done using `index`:
    """)
    return


@app.cell
def _(apes):
    _i = apes.index('Kofiko')
    print(_i, apes[_i])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### EAFP vs. LBYL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If the value is not found a `ValueError` is raised.
    We can catch the error with a try-except block.
    This idiom is called *EAFP* - easier to ask for forgiveness than permission.
    It is a based on a quote of [Admiral Grace Hopper](https://en.wikiquote.org/wiki/Grace_Hopper), the famous computer scientists.

    ![Grace Hopper](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Commodore_Grace_M._Hopper%2C_USN_%28covered%29.jpg/192px-Commodore_Grace_M._Hopper%2C_USN_%28covered%29.jpg)
    """)
    return


@app.cell
def _(apes):
    try:
        _i = apes.index('Panda')
    except ValueError:
        print('Panda not in apes list')
    else:
        print('Panda in index', _i)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can also check if something is in a list before accesing it; this is called *LBYL* - look before you leap.
    """)
    return


@app.cell
def _(apes):
    if 'Panda' in apes:
        _i = apes.index('Panda')
        print('Panda in index', _i)
    else:
        print('Panda not in apes list')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Although exceptions are somewhat less efficient than `if` in terms of performance, in the former example we do only a single lookup (just `index`, no `in` test) and moreover, it is stable in multi-threaded applications.
    In the latter example a different thread could in principle change the dictionary between the test (`in`) and the lookup (`index`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sorting lists

    We can sort lists using the `sorted` method.
    If the list is made __entirely__ of strings, then sorting is straightforward -- it will be sorted lexicographically (think about the way '<' and '>' work on strings).
    """)
    return


@app.cell
def _(apes):
    sorted_apes = sorted(apes)
    print(sorted_apes)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But beware of mixed lists!
    """)
    return


@app.cell
def _(apes):
    _mixed = apes + [1, 2, 3]
    print(_mixed)
    print(sorted(_mixed))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Access: Slicing

    We can slice lists just like we did with strings, to get partial lists.
    For example:
    """)
    return


@app.cell
def _(measurements):
    # get the first 10 measurements
    print(measurements[:10])
    # get the last 3 measurements
    print(measurements[-3:])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise: Lists

    - Use the lists `birds` and `snakes` to create a single list of strings with the animal names.
    - Add the string `Mus musculus` to the list.
    - Remove the `Corvus corone` from the list.
    - Print the 2nd to 5th elements of the resulting list, sorted alphabetically.
    """)
    return


@app.cell
def _():
    birds = ['Gallus gallus', 'Corvus corone', 'Passer domesticus']
    snakes = ['Ophiophagus hannah', 'Vipera palaestinae', 'Python bivittatus']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `for` loops

    Say we want to print each element of our list:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Python’s `for` loop syntax allows us to iterate over the elements of a `list`, or any `iterable` value. Python's `for` is similar to the `foreach` statement in other languages, rather than `for(i=0; i<n; i++)`:

    ```py
    for loop_variable in iterable:
        statement1
        statement2
        statement3
        ...
    ```
    """)
    return


@app.cell
def _(apes):
    for _ape in apes:
        print(_ape, 'is an ape')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![Python loop](http://2.bp.blogspot.com/-7lXe1_Gou3k/UX92PWche3I/AAAAAAAAAFA/JxD4u8St-9g/s1600/python+loop.jpg)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Looping over strings

    Let's go over the Insulin AA sequnce and count the number of prolines manualy. Reminder: `insulin` is a `str`, not `list`.
    """)
    return


@app.cell
def _(insulin):
    count = 0
    for aa in insulin:
        count = count + (aa == 'P')  # the next line is equivalent to
    print('# of prolines:', count)  # if aa == "P": count = count + 1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Do you remember another way of doing this?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise: string loop
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Complete the code below to count the _ratio_ of electrically-charged amino acids in the Insulin sequence.
    """)
    return


@app.cell
def _(charged_ratio):
    charged = ['R', 'H', 'K', 'D', 'E']
    insulin_1 = 'MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN'
    # Your code here
    print('Ratio of charged amino acids is:', charged_ratio)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `range`

    Sometimes we want to loop over consecutive numbers.

    This is accomplished using the `range` function.

    `range` accepts one, two, or three arguments: the bottom and upper limits and the step size.
    The bottom limit can be omitted - the default is zero - and the step can be omitted, too - the default is one.
    The upper limit is __not__ included.
    """)
    return


@app.cell
def _():
    for _i in range(10):  # == range(0, 10, 1)
        print(_i)
    return


@app.cell
def _():
    for _i in range(100, 1000, 10):
        print(_i, end=' ')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can turn the range into a list -- so what is `range`?
    """)
    return


@app.cell
def _():
    list(range(10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also use `range` to loop on the indices of a list instead of the elements themselves.
    This is useful in some cases.
    """)
    return


@app.cell
def _(apes):
    for _i in range(len(apes)):
        print(apes[_i])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `enumerate`

    Another elegant way to iterate over lists is with the `enumerate` function. `enumerate` provides two loop variables for every item in the list -- the index and the element:
    """)
    return


@app.cell
def _(apes):
    for _i, _ape in enumerate(apes):
        print('The ape at index', _i, 'is', _ape)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise: primality check

    Implement a simple primality check for the variable `n=97` (or some other value of your choice).

    For each number `k` between 2 and `n` (or some other range if you prefer), check if `k` is a divider of `n` (using the modulo operation, right?).
    If `k` is a divider you can break the loop using `break`.

    **Note** `for` can have an `else` clause that will be executed if we exited the `for` normally, without a `break` or an exception.
    """)
    return


@app.cell
def _():
    n_5 = 97  # try other numbers
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tuples

    [Tuples](https://docs.python.org/3.5/tutorial/datastructures.html#tuples-and-sequences) are another data structure for sequential data. They, too, can contain any type and mixed types. The main difference between tuples and lists is that tuples are **immutable**.

    Tuples are denoted by round brackets `()`:
    """)
    return


@app.cell
def _():
    t = (15, 76, 'a')
    print(t)
    type(t)
    return (t,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Tuples are commonly packed and unpacked in Python:
    """)
    return


@app.cell
def _(t):
    a_3, b_2, c = t  # unpacking
    print('a:', a_3, 'b:', b_2, 'c:', c)
    t_1 = (a_3, b_2)  # packing
    print(t_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can also create empty and singleton tuples:
    """)
    return


@app.cell
def _():
    t0 = ()
    type(t0)
    return


@app.cell
def _():
    t1 = (5,) # notice the comma
    type(t1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Dictionaries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Dictionaries** are hashtables or maps: a data structure used to store collections of elements to be accessed with a _key_.
    Keys can be of any _immutable_ type - strings, integers, floats, etc.
    Each key refers to a single _value_.
    """)
    return


@app.cell
def _():
    taxonomy = {
        'Pan troglodytes': 'Mammalia', 
        'Gallus gallus': 'Aves', 
        'Xenopus laevis': 'Amphibia', 
        'Vipera palaestinae': 'Reptilia'
    }
    return (taxonomy,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this dictionary, the _keys_ are the organisms and the _values_ are the taxonomic classification of each organism. Both are of type `str`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Access
    Accessing a dictionary record is similar to what we did with lists, only this time we'll use a _key_ instead of an _index_:
    """)
    return


@app.cell
def _(taxonomy):
    print(taxonomy['Pan troglodytes'])
    print(taxonomy['Gallus gallus'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Changing and adding records
    We can change the dictionary by simply assigning a new value to a key.
    """)
    return


@app.cell
def _(taxonomy):
    taxonomy['Pan troglodytes'] = 'Mammals'
    print(taxonomy['Pan troglodytes'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Similarly, we can use this syntax to add new records:
    """)
    return


@app.cell
def _(taxonomy):
    taxonomy['Danio rerio'] = 'Actinopterygii'
    print(taxonomy['Danio rerio'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    __Note 1__: The fact that we can change elements of the dictionary and dynamically add more elements suggests that `dict` is a **mutable** type.

    __Note 2__: A dictionary may not contain multiple records with the same _key_, but it may contain many keys with the same _value_.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Looping over dictionaries

    By default, `for` loops over the dictionary keys:
    """)
    return


@app.cell
def _(taxonomy):
    for organism in taxonomy:
        print('{} is of class {}'.format(organism, taxonomy[organism]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note**: the order of the keys in the dictionary items is **arbitrary** in Python <=3.5, and **ordered** in Python 3.6, but the fact it is ordered is an implelemtation detail rather than part of the specification, so we should not rely on this order. If you need a **explicitly ordered** dictionary, use [OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict).

    We can even change values while looping, as this doesn't affect the keys collection (changing what you loop over is dangerous!)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dictionaries as containers
    We can check if a dictionary contains a *key* using the `in` operator:
    """)
    return


@app.cell
def _(taxonomy):
    'Vipera palaestinae' in taxonomy
    return


@app.cell
def _(taxonomy):
    'Bos taurus' in taxonomy
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise: secret

    Given in the code below is a dictionary (named `code`) where the keys represent encrypted characters and the values are the corresponding decrypted characters. Use the dictionary to decrypt an ecnrypted message (named `secret`) and print out the resulting cleartext message.
    """)
    return


@app.cell
def _():
    secret = """Mq osakk le eh ue usq qhp, mq osakk xzlsu zh Xcahgq,
    mq osakk xzlsu eh usq oqao ahp egqaho,
    mq osakk xzlsu mzus lcemzhl gehxzpqhgq ahp lcemzhl oucqhlus zh usq azc, mq osakk pqxqhp ebc Zokahp, msauqjqc usq geou dat rq,
    mq osakk xzlsu eh usq rqagsqo,
    mq osakk xzlsu eh usq kahpzhl lcebhpo,
    mq osakk xzlsu zh usq xzqkpo ahp zh usq oucqquo,
    mq osakk xzlsu zh usq szkko;
    mq osakk hqjqc obccqhpqc, ahp qjqh zx, mszgs Z pe heu xec a dedqhu rqkzqjq, uszo Zokahp ec a kaclq iacu ex zu mqcq obrfblauqp ahp ouacjzhl, usqh ebc Qdizcq rqtehp usq oqao, acdqp ahp lbacpqp rt usq Rczuzos Xkqqu, mebkp gacct eh usq oucbllkq, bhuzk, zh Lep’o leep uzdq, usq Hqm Meckp, mzus akk zuo iemqc ahp dzlsu, ouqio xecus ue usq cqogbq ahp usq kzrqcauzeh ex usq ekp."""

    code = {'w': 'x', 'L': 'G', 'c': 'r', 'x': 'f', 'G': 'C', 'E': 'O', 'h': 'n', 'O': 'S', 'y': 'q', 'R': 'B', 'd': 'm', 'f': 'j', 'i': 'p', 'o': 's', 'g': 'c', 'a': 'a', 'u': 't', 'k': 'l', 'q': 'e', 'r': 'b', 'V': 'Z', 'X': 'F', 'N': 'K', 'B': 'U', 'T': 'Y', 'M': 'W', 'U': 'T', 'm': 'w', 'C': 'R', 'J': 'V', 't': 'y', 'S': 'H', 'v': 'z', 'e': 'o', 'D': 'M', 'p': 'd', 'K': 'L', 'A': 'A', 'P': 'D', 'l': 'g', 's': 'h', 'W': 'X', 'H': 'N', 'j': 'v', 'z': 'i', 'I': 'P', 'b': 'u', 'Z': 'I', 'F': 'J', 'Y': 'Q', 'Q': 'E', 'n': 'k'}
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Sets

    A [set](https://docs.python.org/3.5/tutorial/datastructures.html#sets) is an **unordered collection** with **unique elements**, similar to the mathematical concept of a [set](https://en.wikipedia.org/wiki/Set_%28mathematics%29) (קבוצה).

    Curly braces (`{}`) or the `set()` function can be used to create sets.
    """)
    return


@app.cell
def _():
    basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
    print(basket) # duplicates have been removed
    type(basket)
    return (basket,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Basic uses include eliminating duplicate entries (as above, one apple and one orange were eliminated), and fast membership testing:
    """)
    return


@app.cell
def _(basket):
    print('orange' in basket)
    print('crabgrass' in basket)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Set objects also support set-theoretical operations like union, intersection, difference, and symmetric difference.
    """)
    return


@app.cell
def _():
    a_4 = set('abracadabra')
    b_3 = set('alacazam')
    print(a_4)
    print(b_3)
    type(b_3)
    return a_4, b_3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Letters in `a` but not in `b`:
    """)
    return


@app.cell
def _(a_4, b_3):
    a_4 - b_3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Letters in either `a` or `b`:
    """)
    return


@app.cell
def _(a_4, b_3):
    a_4 | b_3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Letters in both `a` and `b`:
    """)
    return


@app.cell
def _(a_4, b_3):
    a_4 & b_3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Letters in `a` or `b` but not both:
    """)
    return


@app.cell
def _(a_4, b_3):
    a_4 ^ b_3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To create an empty set you have to use `set()`, not `{}`; the latter creates an empty dictionary.
    """)
    return


@app.cell
def _():
    Ø = set()
    print(Ø)
    type(Ø)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that a `set` is mutable:
    """)
    return


@app.cell
def _(a_4):
    print(a_4)
    a_4.add('z')
    print(a_4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `frozenset`

    There is also a immutable set, called `frozenset`:
    """)
    return


@app.cell
def _():
    a_5 = frozenset('abracadabra')
    print(type(a_5), a_5)
    a_5.add('z')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Functions

    We _define_ functions with the __def__ command.
    The general syntax is:

    ```py
    def function_name(input1, input2, input3,...):
        # some processes
        .
        .
        .
        return output1, output2, ...
    ```

    For example:
    """)
    return


@app.function
def multiply(x, y):
    z = x * y
    return z


@app.cell
def _():
    x_7 = 3
    y_3 = multiply(x_7, 2)
    print(y_3)
    return


@app.cell
def _():
    z_1 = multiply(7, 5)
    print(z_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise: secret (2)

    Let's turn the code from the last exercise into a function.
    Write a function called `decrypt` that takes two arguments, `secret` and `code`, and returns a string which is the cleartext (decrypted) message. Then call the function to decrypt the secret from above.
    """)
    return


@app.cell
def _():
    secret_1 = 'Mq osakk le eh ue usq qhp, mq osakk xzlsu zh Xcahgq,\nmq osakk xzlsu eh usq oqao ahp egqaho,\nmq osakk xzlsu mzus lcemzhl gehxzpqhgq ahp lcemzhl oucqhlus zh usq azc, mq osakk pqxqhp ebc Zokahp, msauqjqc usq geou dat rq,\nmq osakk xzlsu eh usq rqagsqo,\nmq osakk xzlsu eh usq kahpzhl lcebhpo,\nmq osakk xzlsu zh usq xzqkpo ahp zh usq oucqquo,\nmq osakk xzlsu zh usq szkko;\nmq osakk hqjqc obccqhpqc, ahp qjqh zx, mszgs Z pe heu xec a dedqhu rqkzqjq, uszo Zokahp ec a kaclq iacu ex zu mqcq obrfblauqp ahp ouacjzhl, usqh ebc Qdizcq rqtehp usq oqao, acdqp ahp lbacpqp rt usq Rczuzos Xkqqu, mebkp gacct eh usq oucbllkq, bhuzk, zh Lep’o leep uzdq, usq Hqm Meckp, mzus akk zuo iemqc ahp dzlsu, ouqio xecus ue usq cqogbq ahp usq kzrqcauzeh ex usq ekp.'
    code_1 = {'w': 'x', 'L': 'G', 'c': 'r', 'x': 'f', 'G': 'C', 'E': 'O', 'h': 'n', 'O': 'S', 'y': 'q', 'R': 'B', 'd': 'm', 'f': 'j', 'i': 'p', 'o': 's', 'g': 'c', 'a': 'a', 'u': 't', 'k': 'l', 'q': 'e', 'r': 'b', 'V': 'Z', 'X': 'F', 'N': 'K', 'B': 'U', 'T': 'Y', 'M': 'W', 'U': 'T', 'm': 'w', 'C': 'R', 'J': 'V', 't': 'y', 'S': 'H', 'v': 'z', 'e': 'o', 'D': 'M', 'p': 'd', 'K': 'L', 'A': 'A', 'P': 'D', 'l': 'g', 's': 'h', 'W': 'X', 'H': 'N', 'j': 'v', 'z': 'i', 'I': 'P', 'b': 'u', 'Z': 'I', 'F': 'J', 'Y': 'Q', 'Q': 'E', 'n': 'k'}
    return code_1, secret_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Documenting your functions

    Documenting functions is done by adding a *docstring* element below the function definition. Docstrings are enclosed by `\"\"\"`. For example:
    """)
    return


@app.cell
def _(code_1, secret_1):
    def decrypt(secret, code):
        """Decrypt a message using a substitution code.
    
        The function only decrypts characters that appear in `code`; other characters remain as they appear in `secret`.
    
        Parameters
        ----------
        secret : str
            an encrypted message
        code : dict
            a substitution code, where the keys are encrypted characters and the values are the cleartext characters.
    
        Returns
        -------
        str
            the decrypted cleartext message.
        """
        return ''.join((code.get(c, c) for c in secret))  # this is advanced python code
    print(decrypt(secret_1, code_1))
    return (decrypt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can easily access the documentation of a function using the `help()` command.
    """)
    return


@app.cell
def _(decrypt):
    help(decrypt)
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
