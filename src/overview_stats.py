import copy
import pandas as pd
import numpy as np
import scipy.stats as sps

from src.palette import palette, graph_custom


def generate_overview_stats(data, column="AVG"):

    dff = pd.DataFrame({key: data[key] for key in [column, "Votes"]})
    hist, bins = np.histogram(dff[column], bins='auto', density=False)
    color = dff['Votes'].groupby(pd.cut(dff[column], bins)).mean()

    data = [
        dict(
            type="bar",
            x=bins,
            y=hist,
            name="All years",
            hovertemplate=
            "<b> Mean: %{x:.2f} </b> <br> Albums: %{y} <br> Average votes: %{marker.color:.2f}<extra></extra>",
            marker={
                'color':
                color,
                'showscale':
                True,
                'colorbar': {
                    'title': {
                        'text': '#Votes'
                    }
                },
                'colorscale': [
                    (0, palette['lblue']),
                    (0.5, palette['light']),
                    (1, palette['red']),
                ],
            },
        ),
    ]
    layout = copy.deepcopy(graph_custom)
    layout.update(
        dict(
            title="Average distribution",
            yaxis={
                'title': 'Number of albums',
                'gridcolor': palette['white'],
                'gridwidth': 1,
                'showgrid': True,
            },
            xaxis={
                'title': 'Average',
            },
            dragmode='select',
            selectdirection='h',
        )
    )
    return {'data': data, 'layout': layout}
