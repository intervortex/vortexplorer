# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import io

# %%

from data.sheets import sheets_list, get_sheet_csv
#
from src.process.clean_data import process_spreadsheet, NONUSER_COLS

# %%
sheets = {}
for sheet in sheets_list:
    resp = requests.get(get_sheet_csv(sheet))
    resp.encoding = 'UTF-8'
    df = process_spreadsheet(pd.read_csv(io.StringIO(resp.text), na_values=[' ']), sheet)
    sheets[sheet] = df

# %%
for sheet in sheets:
    sheets[sheet].to_csv(f"./data/{sheet}.csv")
# %%

users = []

for sheet in sheets.values():
    for col in sheet.columns:
        if (col.lower() not in NONUSER_COLS and col.lower() not in users):
            users.append(col.lower())

print(users)

# %%
users = [
    ('ferday', 'incantacorn', 'goaticorn'),
    ('scuttlegoat', 'scuttlebloodygoat'),
    ('aker', 'akerfeldt', 'akerblogger', 'akergoater'),
    ('dr. verinen', 'dr. death', 'dr. goatinen'),
    ('meri', 'meriyas', 'mericyless', 'goatiyas'),
    ('snyde', 'capryde', 'schuldinyde'),
    ('scoopmeister', 'scoopultura', 'enscooped'),
    ('tarbeaux', 'targeauxt', 'tarborizer'),
    ('ca vimes', 'ca prines', 'slumber of sullen vimes'),
    ('carlos', 'carlcass', 'carlos m.', 'goatickvillian'),
    ('scourge', 'scourgoat'),
    ('dymanic', 'dygoatic', "dy's member"),
    ('mr. samsa', 'scumsa', 'mr.samsa', 'mr. goatse'),
    ('afterthought', 'afterthot', 'aftergoat', 'thanathot'),
    ('patient_ot', 'patientot'),
    ('goldicot', 'goatdicot'),
    ('joshk', 'joatk', 'jorguts', 'jorkhid'),
    ('quillon', ),
    ('planex', ),
    ('nunchuks', ),
    ('gadunka', ),
    ('cherd', ),
    ('absolomb', 'goabsoloat'),
    ('banthas', ),
    ('buckleyan', ),
    ('yeetzah', ),
    ('cerithiel', ),
    ('wickerman', ),
    ('cockman', 'sevenroosters', 'crazygoatman'),
    ('dethjesta', ),
    ('the nerd', 'nonesonerdy', 'the gerd'),
    ('i/0', ),
    ('fugl', ),
    ('whitenoise', ),
    ('hungus', ),
    ('byrath', ),
    ('navybsn', ),
    ('zackflag', ),
    ('markm', ),
    ('johan', ),
    ('thatguy', ),
    ('serjien', ),
    ('surgicalbrute', ),
]

# %% make unique users throughout

for sheet in sheets:
    df = sheets[sheet]
    if "Rank" in df.columns:
        df = df.drop("Rank", axis=1)
    df.columns = map(str.lower, df.columns)
    df["sheet"] = sheet
    sheets[sheet] = df

for user in users:
    if len(user) > 1:
        for sheet in sheets:
            df = sheets[sheet]
            for name in user[1:]:
                if name in df.columns:
                    df.rename(columns={name: user[0]}, inplace=True)
            sheets[sheet] = df

users = [user[0] for user in users]

# %%
complete = pd.concat(sheets.values(), )
todrop = [col for col in complete.columns if col.startswith("unnamed")]
todrop.extend(["day", "yt link", "lists", "rec"])
complete = complete.drop(todrop, axis=1)
complete["artist"] = complete["artist"].apply(str.strip)
complete = complete.sort_values(by="artist")
complete = complete.reset_index(drop=True)
complete = complete[[c for c in complete.columns if c not in users] + users]

# %% write/read
complete.to_csv("./data/complete.csv", index=False)

# %%
pd.read_csv("./data/complete.csv")

# %% Check unique

duplicates = complete.duplicated(subset=['artist', 'album'])
duplicate_names = complete[duplicates][['artist', 'album']].values

# %% Find dupes
dupes = {}
for dupe in duplicate_names:
    name = " - ".join(dupe)
    df_slice = complete[(complete['artist'] == dupe[0]) & (complete['album'] == dupe[1])]
    dupes[name] = df_slice["sheet"].values.tolist()

# %% Bad dupes - to fix
[d for d in dupes.items() if "Reliquary" not in d[1] and "GOAT" not in d[1]]

# %% Interesting dupes - combine

int_dupes = [d for d in dupes.items() if "Reliquary" in d[1] or "GOAT" in d[1]]
int_dupes

# %%

blame_dupes = {}

for dupe in int_dupes:
    artist, album = dupe[0].split(" - ")
    dupe_data = complete[(complete['artist'] == artist) & (complete['album'] == album)]

    ind = dupe_data.index

    for col in dupe_data.columns:
        if all(dupe_data[col].isna()):
            continue

        if all(dupe_data[col].notna()):
            if col not in users:
                continue

            if all(e == dupe_data[col].iloc[0] for e in dupe_data[col]):
                continue

            name = dupe_data['artist'].iloc[0] + " - " + dupe_data['album'].iloc[0]
            if not blame_dupes.get(col):
                blame_dupes[col] = []

            blame_dupes[col].append({name: list(zip(dupe_data['sheet'], dupe_data[col]))})

        # if any(dupe_data[col].isna()):
        #     complete.loc[ind[0], col] = dupe_data[col].dropna()
        #     continue

# %% save dupes

import json
with open("./data/dupes.json", 'w') as f:
    json.dump(blame_dupes, f)

# %% write/read
complete.to_csv("./data/complete.csv", index=False)

# %%
pd.read_csv("./data/complete.csv")
