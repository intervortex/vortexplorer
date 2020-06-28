import copy
import numpy as np
import pandas as pd
from src.palette import palette, graph_custom


def generate_crossuser_heatmap(data, users, hm_click, reset, column="AVG"):
    """
    """

    dff = pd.DataFrame(data)

    x_axis = [column] + users
    y_axis = [column] + users

    shapes = []

    if hm_click is not None:
        user1 = hm_click["points"][0]["x"]
        user2 = hm_click["points"][0]["y"]

        # Add shape
        x0 = x_axis.index(user1) / len(x_axis)
        x1 = x0 + 1 / len(x_axis)
        y0 = 1 - (y_axis.index(user2) + 1) / len(y_axis)
        y1 = y0 + 1 / len(y_axis)

        shapes = [
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=x0,
                x1=x1,
                y0=y0,
                y1=y1,
                line=dict(color=palette['black']),
            )
        ]

    # Get z value : sum(number of records) based on x, y,
    crossref = np.zeros([len(x_axis), len(y_axis)])

    annotations = []

    for ind1, col1 in enumerate(x_axis):
        for ind2, col2 in enumerate(y_axis):
            diff = dff[col1] - dff[col2]
            crossref[ind1, ind2] = np.sum(np.abs(diff.dropna())
                                          ) / len(diff.dropna())

            annotation_dict = dict(
                showarrow=False,
                text=f"<b>{crossref[ind1, ind2]:.2f}<b>",
                xref="x",
                yref="y",
                x=col1,
                y=col2,
                font=dict(family="sans-serif", color=palette['black']),
            )

            annotations.append(annotation_dict)

    crossref_adj = crossref / np.average(crossref)

    # Heatmap
    hovertemplate = "<b> %{y} - %{x} <br> Taste similarity: <br> %{z}"

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
                ticktext=['Agree', 'Disagree'],
                tickfont={
                    'size': 13,
                    'color': palette['light']
                },
            ),
            colorscale=[
                (0, palette['black']),
                (0.05, palette['red']),
                (1, palette['lblue']),
            ],
            # reversescale=True,
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
                tickfont=dict(family="sans-serif", color=palette['light']),
                tickcolor=palette['light'],
            ),
            yaxis=dict(
                side="left",
                ticks="",
                ticklen=2,
                tickfont=dict(family="sans-serif", color=palette['light']),
                ticksuffix="",
                tickcolor=palette['light'],
                autorange="reversed"
            ),
        )
    )
    return {"data": data, "layout": layout}
