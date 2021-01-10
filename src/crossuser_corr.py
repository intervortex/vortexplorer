import copy

import pandas as pd
import random

from src.palette import palette, graph_custom


def generate_crossuser_corr(data_df, hm_click, column="AVG"):

    dff = pd.DataFrame(data_df)

    user1 = column
    user2 = column

    if hm_click is not None:

        user1 = hm_click["points"][0]["x"]
        user2 = hm_click["points"][0]["y"]

        if user1 not in dff.columns or user2 not in dff.columns:
            user1 = column
            user2 = column

    xdata = dff[user1].apply(lambda x: x + (random.random() - 0.5) / 3)
    ydata = dff[user2].apply(lambda x: x + (random.random() - 0.5) / 3)
    zdata = dff[column]
    text = (
        dff["Artist"] + " - " + "<i>" + dff["Album"] + "</i> (" +
        dff["Released"].map(str) + ")<br> Average: " + dff[column].map(str) +
        " (from " + dff["Votes"].map(str) + " votes)"
    )

    hovertemplate = "%{x:.1f} VS %{y:.1f}<br><b> Album: </b> <br> %{text}<extra></extra>"

    data = [
        dict(
            x=xdata,
            y=ydata,
            mode='markers',
            opacity=0.7,
            hovertemplate=hovertemplate,
            marker={
                'symbol':
                'square',
                'size':
                10,
                'line': {
                    'width': 0.5,
                    'color': palette['black']
                },
                'color':
                zdata,
                'colorscale': [
                    (0, palette['lblue']),
                    (0.5, palette['light']),
                    (1, palette['red']),
                ],
                'showscale':
                True,
                'colorbar': {
                    'title': {
                        'text': 'Average'
                    }
                },
            },
            text=text,
        ),
    ]
    layout = copy.deepcopy(graph_custom)
    layout.update(
        dict(
            margin={
                'l': 40,
                'b': 40,
                't': 10,
                'r': 10
            },
            font=dict(family="Open Sans", color=palette['light'], size=18),
            xaxis={
                'title': user1,
                "range": [0, 10.5],
                "automargin": True,
                "tickmode": 'linear',
                "tick0": 0.0,
                "dtick": 1.0,
                "constrain": "domain",
            },
            yaxis={
                'title': user2,
                "range": [0, 10.5],
                "automargin": True,
                "tickmode": 'linear',
                "tick0": 0.0,
                "dtick": 1.0,
                "scaleanchor": "x",
                "scaleratio": 1,
                "constrain": "domain",
            },
            shapes=[{
                # extra x=y line
                'type': 'line',
                'xref': 'x',
                'yref': 'y',
                'x0': 0,
                'y0': 0,
                'x1': 10,
                'y1': 10,
                'line': {
                    'color': 'rgb(255, 255, 255)',
                    "dash": 'dash',
                    'width': 1,
                }
            }],
            height=800,
        )
    )
    return {"data": data, "layout": layout}
