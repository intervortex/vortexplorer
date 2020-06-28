import copy
from datetime import datetime
import pandas as pd

from src.palette import palette, graph_custom


def generate_overview_year(data, column="AVG"):

    dff = pd.DataFrame({key: data[key] for key in [column, "Released"]})
    try:
        dff.index = pd.to_datetime(dff["Released"], format="%Y")
        dff = dff.resample('A').agg({'Released': 'count', column: 'mean'})
    except:
        dff.index = pd.to_datetime(dff["Released"], format="%b-%d-%Y")
        dff = dff.resample('M', label='left').agg({
            'Released': 'count',
            column: 'mean'
        })

    data = [
        dict(
            type="bar",
            x=dff.index,
            y=dff["Released"],
            name="All years",
            hovertemplate=
            "<b> %{x}: </b> <br> Albums: %{y} <br> Average: %{marker.color:.2f}<extra></extra>",
            marker={
                'color':
                dff[column],
                'showscale':
                True,
                'colorbar': {
                    'title': {
                        'text': 'Average'
                    }
                },
                'colorscale': [
                    (0, palette['lblue']),
                    (0.5, palette['light']),
                    (1, palette['red']),
                ],
            }
        ),
    ]
    layout = copy.deepcopy(graph_custom)
    layout.update(
        dict(
            title="Albums throughout time",
            yaxis={
                'title': 'Number of albums',
                'gridcolor': palette['white'],
                'gridwidth': 1,
                'showgrid': True,
            },
            xaxis={
                'title': 'Time',
            },
            dragmode='select',
            selectdirection='h',
        )
    )
    return {'data': data, 'layout': layout}
