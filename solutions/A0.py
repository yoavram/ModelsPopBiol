import marimo

__generated_with = "0.19.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from datetime import date
    import string
    import pickle
    return date, mo, np, pickle, plt, string


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Assignment 0: Python, NumPy, Matplotlib
    ## [Scientific Computing with Python](https://scicompy.yoavram.com/)
    ## Yoav Ram
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # General instructions

    1. Questions regarding the exercises should be posted to the course forum at the designated group (i.e. "assignment 0"). You can post questions anonymously. You can also visit the Office Hours, but please do not email the course staff with questions about the exercise.
    1. This is assignment should **not** be submitted and will **not** be graded.
    1. Lines that end with `###`, as well as cells that start with `###`, are unitests for your solutions, don't change them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Exercise 1""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following cell loads a dictionary called **presidents_by_party** (taken from https://github.com/inglesp/python-data-structure-exercises)

    The keys of the dictionaries are US political party names, and the values are lists of presidents from each party.
    Each president is represented by a dictionary in which the keys are properties, e.g. `name` and `born`, and the values are the property values, e.g. `George Washington` and `date(1732, 2, 22)`. Dates are given using the Python `datetime.date` type.
    """)
    return


@app.cell
def _(pickle):
    with open('../data/presidents.obj', 'rb') as f:
        presidents_by_party_data = pickle.load(f)
    presidents_by_party_data['Independent']
    return (presidents_by_party_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Add Donald Trump to the correct party**.""")
    return


@app.cell
def _(presidents_by_party_data, date):
    presidents_by_party = presidents_by_party_data
    presidents_by_party['Republican'].append(dict(
        name='Donald Trump',
        born=date(1946, 6, 14),
        took_office=date(2017, 1, 20)
    ))
    return (presidents_by_party,)


@app.cell
def _(presidents_by_party):
    len(presidents_by_party['Republican']) ###
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Create dictionary called `parties`** with `party_name` as a key and a tuple `(number_of_presidents, last_president_name)` as a value.

    Bonus: use a [dictionary comprehension](https://dbader.org/blog/list-dict-set-comprehensions-in-python).
    """)
    return


@app.cell
def _(presidents_by_party):
    parties = {
        party: (len(pres_list), pres_list[-1]['name'])
        for party, pres_list in presidents_by_party.items()
    }
    return (parties,)


@app.cell
def _(parties):
    parties['Democratic'] ###
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Create a list called `presidents`** that contains all the president dictionaries.

    Then **sort the presidents list** by ascending date of taking office.
    """)
    return


@app.cell
def _(presidents_by_party):
    # Create list:
    presidents = []
    for _party_presidents in presidents_by_party.values():
        presidents.extend(_party_presidents)

    # Sort by ascending date of taking office:
    presidents.sort(key=lambda p: p['took_office'])
    return (presidents,)


@app.cell
def _(presidents):
    len(presidents)
    return


@app.cell
def _(presidents):
    presidents[-1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Print all the presidents that took office on Jan 20**.""")
    return


@app.cell
def _(presidents):
    for _pres in presidents:
        if _pres['took_office'].month == 1 and _pres['took_office'].day == 20:
            print(_pres['name'], _pres['took_office'].strftime('%m/%d/%y'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exercise 2

    The following cell defines frequencies arrays for the characters of English, Deutch, and French texts.

    For example, `en[0]` gives the frequency of `a` in English texts, whereas `de[10]` gives the frequency of `k`.

    We only consider lowercase letters a-z.
    """)
    return


@app.cell
def _(np):
    en = np.array([0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
                0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
                0.00978, 0.0236 , 0.0015 , 0.01974, 0.00074])
    de = np.array([0.06516, 0.01886, 0.02732, 0.05076, 0.16396, 0.01656, 0.03009,
                0.04577, 0.0655 , 0.00268, 0.01417, 0.03437, 0.02534, 0.09776,
                0.02594, 0.0067 , 0.00018, 0.07003, 0.0727 , 0.06154, 0.04166,
                0.00846, 0.01921, 0.00034, 0.00039, 0.01134])
    fr = np.array([0.07636, 0.00901, 0.0326 , 0.03669, 0.14715, 0.01066, 0.00866,
                0.00737, 0.07529, 0.00613, 0.00074, 0.05456, 0.02968, 0.07095,
                0.05796, 0.02521, 0.01362, 0.06693, 0.07948, 0.07244, 0.06311,
                0.01838, 0.00049, 0.00427, 0.00128, 0.00326])
    return de, en, fr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We want to use these frequency arrays to determine the language of a text of our choice.

    First, **write a function called `frequencies(text)`** that takes a string and returns the frequency of each letter in the text in a NumPy array, similar to those above. Disregard casing (`A` is the same as `a`) and punctuation.

    Apply the function on `../data/Gulliver.txt`, an English book by Jonathan Swift.

    **Tip**: use the function `ord`.
    """)
    return


@app.cell
def _(np, string):
    def frequencies(text):
        freq = np.zeros(26)
        for char in text:
            if char in string.ascii_lowercase:
                freq[ord(char) - ord('a')] += 1
            elif char in string.ascii_uppercase:
                freq[ord(char) - ord('A')] += 1
        freq /= freq.sum()
        return freq
    return (frequencies,)


@app.cell
def _(frequencies):
    ###
    with open('../data/Gulliver.txt') as f:
        gulliver = f.read()

    gulliver_freq = frequencies(gulliver)
    print(gulliver_freq)
    return gulliver, gulliver_freq


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Implement a function called `relative_entropy(p, q)`** to compute the relative entropy of a text frequencies array `q` and a language frequencies array `p` according to the following formula:
    $$
    re(p, q) = \sum_{i=1}^{n}{p_i \log{\Big(\frac{p_i}{q_i}\Big)}}
    $$
    where $i=1$ for `a` and $i=n$ for `z`.

    Relative entropy is a measure of similarity between two distributions or frequencies: the lower the relative entropy of `p` and `q`, the more similar `p` and `q`.

    Reminder: frequency array values are between 0 and 1 and sum to 1.
    """)
    return


@app.cell
def _(np):
    def relative_entropy(p, q):
        q = q.copy()
        q[q == 0] = 1e-8
        return (p * np.log(p / q)).sum()
    return (relative_entropy,)


@app.cell
def _(de, en, fr, gulliver_freq, relative_entropy):
    ###
    print('en', relative_entropy(en, gulliver_freq))
    print('fr', relative_entropy(fr, gulliver_freq))
    print('de', relative_entropy(de, gulliver_freq))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Finally, **write a function called `detect_language(text)`** that takes a text and returns the name of the language most likely for that text, e.g. `en`, `fr`, or `de`.""")
    return


@app.cell
def _(de, en, fr, frequencies, relative_entropy):
    _language_frequencies = {'en': en, 'fr': fr, 'de': de}

    def detect_language(text):
        text_freq = frequencies(text)
        language_rel_ent = [
            (lang, relative_entropy(freq, text_freq))
            for lang, freq in _language_frequencies.items()
        ]
        return min(language_rel_ent, key=lambda t: t[1])[0]
    return (detect_language,)


@app.cell
def _(detect_language, gulliver):
    print(detect_language(gulliver)) ###
    return


@app.cell
def _(detect_language):
    ###
    ne_me_quitte_pas = """Ne me quitte pas
Il faut oublier
Tout peut s'oublier
Qui s'enfuit déjà
Oublier le temps
Des malentendus
Et le temps perdu
A savoir comment
Oublier ces heures
Qui tuaient parfois
A coups de pourquoi
Le coeur du bonheurNe me quitte pas
Ne me quitte pas
Ne me quitte pas
Ne me quitte pas"""

    print(detect_language(ne_me_quitte_pas))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Exercise 3""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The file `../data/stocks.csv` contains a table with 1967 rows and 4 columns that represent the quotes (stock prices) for four corporations -- Amazon, Apple, Facebook, and Microsoft -- over 1,967 days starting from 2012-05-18 and ending at 2020-03-13.

    **Load the data using NumPy**.
    """)
    return


@app.cell
def _(np):
    data = np.loadtxt('../data/stocks.csv', delimiter=',')
    return (data,)


@app.cell
def _(data):
    data ###
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Re-create the plot** with all four companies on the same axis.""")
    return


@app.cell
def _(data, np, plt):
    _companies = sorted(['apple', 'facebook', 'amazon', 'microsoft'])

    _fig, _ax = plt.subplots(1, 1, figsize=(4, 2))
    for _quote, _company in zip(data.T, _companies):
        _ax.plot(_quote, label=_company)
    _ax.set(xlabel='Time', ylabel='Quote')
    _ax.legend()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Re-create the plot** with each company on a different axis.""")
    return


@app.cell
def _(data, np, plt):
    _companies = sorted(['apple', 'facebook', 'amazon', 'microsoft'])
    _rows = len(_companies)

    _fig, _axes = plt.subplots(_rows, 1, figsize=(4, 2 * _rows), sharex=True, sharey=False)
    for _quote, _company, _ax in zip(data.T, _companies, _axes):
        _ax.plot(_quote, color='k')
        _ax.set_title(_company)
        _ax.set_axis_off()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**End of assignment**""")
    return


if __name__ == "__main__":
    app.run()
