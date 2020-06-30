import copy
import random

import numpy as np
import pandas as pd

import plotly.figure_factory as ff

from src.clean_data import NONUSER_COLS
from src.palette import graph_custom, palette


def generate_album_stats(data, col="AVG"):

    df = pd.DataFrame(data)
    df['std_dev'] = df[[
        col for col in df.columns if col.lower() not in NONUSER_COLS
    ]].apply(
        lambda x: np.std(x) if np.count_nonzero(np.isnan(x)) < 5 else np.nan,
        axis=1
    )

    top = df['std_dev'].idxmax()
    bot = df['std_dev'].idxmin()

    return {
        "agreed": df['Album'].iloc[bot] + " - " + df['Artist'].iloc[bot],
        "disagreed": df['Album'].iloc[top] + " - " + df['Artist'].iloc[top],
    }


def generate_album_breakdown(data, albums):

    hist_data = []
    group_labels = []

    if albums:

        # Have to make sure it's always an array
        albums = [albums] if isinstance(albums, str) else albums
        for album in albums:
            index = data['Album'].index(album)
            hist_data.append([
                data[col][index]
                for col in data
                if col.lower() not in NONUSER_COLS and data[col][index]
            ])
        group_labels = albums  # name of the dataset

    fig = ff.create_distplot(
        hist_data, group_labels, histnorm='probability', show_rug=False
    )

    # format the layout
    fig.update_xaxes(range=[0, 10])
    fig.update_layout(**graph_custom)
    fig.update_layout(
        xaxis_title='Vote',
        yaxis_title='Vote proportion',
        font=dict(family="Open Sans", color=palette['light'], size=18),
        showlegend=True,
    )

    return fig
