import copy
import pandas as pd

from src.palette import palette, graph_custom


def generate_overview_stats(data_df):

    dff = data_df
    dfy = dff[["AVG", "Year"]]
    dfy.index = pd.to_datetime(dfy["Year"], format="%Y")
    dfy = dfy.resample('A').agg({'Year': 'count', 'AVG': 'mean'})

    data = [
        dict(
            type="bar",
            x=dfy.index,
            y=dfy["Year"],
            name="All years",
            hovertemplate="<b> %{x}: </b> <br> Albums: %{y} <br> Average: %{marker.color:.2f}<extra></extra>",
            marker={
                'color': dfy['AVG'],
                'showscale':True,
                'colorbar':{'title': {'text': 'Average'}},
            },
            colorscale='inferno'
        ),
    ]
    layout = copy.deepcopy(graph_custom)
    layout.update(
        dict(
            title="Albums throughout the years",
            yaxis={
                'title': 'Number of albums',
            },
            dragmode='select',
            selectdirection='h',
        )
    )
    return {'data': data, 'layout': layout}
