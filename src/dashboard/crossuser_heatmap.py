import copy
import numpy as np
import pandas as pd

from src.palette import palette, graph_custom


def generate_crossuser_heatmap(data_df, users, hm_click, reset, column="AVG"):
    """
    """

    dff = pd.DataFrame(data_df)

    x_axis = [column] + users
    y_axis = [column] + users

    shapes = []

    if hm_click is not None:

        user1 = hm_click["points"][0]["x"]
        user2 = hm_click["points"][0]["y"]

        if user1 in dff.columns and user2 in dff.columns:

            # Add shape
            x0 = x_axis.index(user1) / len(x_axis)
            x1 = x0 + 1 / len(x_axis)
            y0 = 1 - (y_axis.index(user2) + 1) / len(y_axis)
            y1 = y0 + 1 / len(y_axis)

            shapes = [dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=x0,
                x1=x1,
                y0=y0,
                y1=y1,
                line=dict(color=palette['black']),
            )]

    # Get z value : sum(number of records) based on x, y,
    crossref = np.zeros([len(x_axis), len(y_axis)])

    annotations = []

    for ind1, col1 in enumerate(x_axis):
        for ind2, col2 in enumerate(y_axis):
            diff = dff[col1] - dff[col2]
            crossref[ind1, ind2] = np.sum(np.abs(diff.dropna())) / len(diff.dropna())

    crossref_adj = 1 - crossref / np.max(crossref)

    for ind1, col1 in enumerate(x_axis):
        for ind2, col2 in enumerate(y_axis):

            annotations.append(
                dict(
                    showarrow=False,
                    text=f"<b>{crossref_adj[ind1, ind2]:.2f}<b>",
                    xref="x",
                    yref="y",
                    x=col1,
                    y=col2,
                    font=dict(family="sans-serif", color=palette['black']),
                )
            )

    # Heatmap
    hovertemplate = "<b> %{y} - %{x}</b><br> Taste similarity: <br> %{z:.2f}"

    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=crossref_adj,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=True,
            colorbar=dict(
                tickmode='array',
                tickvals=[0, np.max(crossref_adj)],
                ticktext=['Disagree', 'Agree'],
                tickfont={
                    'size': 13,
                    'color': palette['light']
                },
            ),
            colorscale=[
                (0, palette['lblue']),
                (0.95, palette['red']),
                (1, palette['black']),
            ],
        )
    ]

    layout = copy.deepcopy(graph_custom)
    layout.update(
        dict(
            margin=dict(l=100, b=50, t=50, r=50),
            modebar={"orientation": "v"},
            annotations=annotations,
            shapes=shapes,
            xaxis=dict(
                side="top",
                ticks="",
                ticklen=2,
                tickfont=dict(color=palette['light']),
                tickcolor=palette['light'],
            ),
            yaxis=dict(
                side="left",
                ticks="",
                ticklen=2,
                tickfont=dict(color=palette['light']),
                ticksuffix="",
                tickcolor=palette['light'],
                autorange="reversed"
            ),
        )
    )
    return {"data": data, "layout": layout}
