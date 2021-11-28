# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import io

# %%

data = pd.read_csv("./data/goat.csv")

# %%
data.head(5)

# %%
data.columns

# %%

users = [
    'goaticorn', 'goatiyas', 'Targeauxt', 'Capryde', 'JoatK', 'Dr. Goatinen', 'crazygoatman', 'aftergoat', 'Ca Prines', 'Goatdicot', 'dygoatic',
    'Goatickvillian'
]

crossref = np.zeros([len(users), len(users)])

for col1 in users:
    for col2 in users:
        diff = data[col1] - data[col2]
        crossref[users.index(col1), users.index(col2)] = np.sum(np.abs(diff.dropna())) / len(diff.dropna())

# %%

crossref_adj = crossref / np.average(crossref)

# %%

crossref_pd = pd.DataFrame(data=crossref_adj, index=users, columns=users)

# %%
from sheets import sheets_list
from src.clean_data import process_spreadsheet

spreadsheet_name = 'Reliquary'
sheets_template = "https://docs.google.com/spreadsheet/ccc?key={0}&output=csv"

resp = requests.get(sheets_template.format(spreadsheet_list[spreadsheet_name]['url']))
resp.encoding = 'UTF-8'
df = process_spreadsheet(pd.read_csv(io.StringIO(resp.text), na_values=[' ']), spreadsheet_name)

# %%

NONUSER_COLS = ['rank', 'artist', 'album', 'year', 'day', 'lists', 'votes', 'avg', 'wavg', 'released', 'genre', 'label', 'rec', 'yt link']

df = process_spreadsheet(pd.read_csv(io.StringIO(resp.text), na_values=[' ']), spreadsheet_name).reset_index(drop=True)
# df['std_dev'] = df[[
#     col for col in df.columns if col.lower() not in NONUSER_COLS
# ]].std(axis=1)

df['std_dev'] = df[[col for col in df.columns
                    if col.lower() not in NONUSER_COLS]].apply(lambda x: np.std(x) if np.count_nonzero(np.isnan(x)) < 5 else np.nan, axis=1)

top = df['std_dev'].idxmax()
bot = df['std_dev'].idxmin()

# %%