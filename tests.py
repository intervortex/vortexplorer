# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%

data = pd.read_csv("./data/goat.csv")

# %%
data.head(5)


# %%
data.columns

# %%

users = ['goaticorn',
         'goatiyas', 'Targeauxt', 'Capryde', 'JoatK', 'Dr. Goatinen',
         'crazygoatman', 'aftergoat', 'Ca Prines', 'Goatdicot', 'dygoatic',
         'Goatickvillian']

crossref = np.zeros([len(users), len(users)])

for col1 in users:
    for col2 in users:
        diff = data[col1] - data[col2]
        crossref[
            users.index(col1),
            users.index(col2)
        ] = np.sum(np.abs(diff.dropna())) / len(diff.dropna())

# %%

crossref_adj = crossref / np.average(crossref)


# %%

crossref_pd = pd.DataFrame(data=crossref_adj, index=users, columns=users)


# %%

fig, ax = plt.subplots(figsize=(7, 7))
im = ax.imshow(crossref_adj, cmap="inferno")

# We want to show all ticks...
ax.set_xticks(np.arange(len(users)))
ax.set_yticks(np.arange(len(users)))

# ... and label them with the respective list entries
ax.set_xticklabels(users)
ax.set_yticklabels(users)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(users)):
    for j in range(len(users)):
        text = ax.text(j, i, f"{crossref_adj[i, j]:.1f}",
                       ha="center", va="center", color="k")

ax.set_title("Taste similarity")
fig.tight_layout()
plt.show()

# %%
