import copy
import pandas as pd

from src.palette import palette, graph_custom


def generate_overview_year(data):

    dff = pd.DataFrame({key: data[key] for key in ["AVG", "Year"]})
    dff.index = pd.to_datetime(dff["Year"], format="%Y")
    dff = dff.resample('A').agg({'Year': 'count', 'AVG': 'mean'})

    data = [
        dict(
            type="bar",
            x=dff.index,
            y=dff["Year"],
            name="All years",
            hovertemplate=
            "<b> %{x}: </b> <br> Albums: %{y} <br> Average: %{marker.color:.2f}<extra></extra>",
            marker={
                'color': dff['AVG'],
                'showscale': True,
                'colorbar': {
                    'title': {
                        'text': 'Average'
                    }
                },
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
                'gridcolor': palette['white'],
                'gridwidth': 1,
                'showgrid': True,
            },
            xaxis={
                'title': 'Years',
            },
            dragmode='select',
            selectdirection='h',
        )
    )
    return {'data': data, 'layout': layout}


def generate_overview_year_tbl(data, sel_year, sel_stats):

    dff = pd.DataFrame(data)

    if sel_year is not None:
        start = int(sel_year["range"]['x'][1][0:4])
        end = int(sel_year["range"]['x'][0][0:4])
        dff = dff[dff['Year'].between(start, end)]

    if sel_stats is not None:
        start = sel_stats["range"]['x'][0]
        end = sel_stats["range"]['x'][1]
        dff = dff[dff['AVG'].between(start, end)]

    return dff[["Year", "Artist", "Album", "AVG", "Votes"]].to_dict('records')
