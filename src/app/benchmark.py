"""
Benchmark child stats
"""
import pandas as pd

# Words known, by month

# The columns are: age_in_months, and percentiles.
df_wordcount = pd.read_csv('../../data/vocab_norms_english.csv')

PERCENTILES = ['0.1', '0.25', '0.5', '0.75', '0.9']

# Dictionary of list of dictionaries (for d3). Top level key is percentile.
# Each list contains [{ 'month': m, 'count' c }, ...for all months ]
AVERAGE_WORDCOUNT = {
    k: [] for k in PERCENTILES
}

for i in df_wordcount.index:
    row = df_wordcount.loc[i]
    for k in ['0.1', '0.25', '0.5', '0.75', '0.9']:
        AVERAGE_WORDCOUNT[k].append(
            {'month': int(row['age_in_months']), 'count': int(row[k])})


AVERAGE_SYLLABLES = [
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
]


AVERAGE_HEIGHT = [
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
]

AVERAGE_WEIGHT = [
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
]
