from dash import dcc, html
from dash import dash_table as dt
import dash_bootstrap_components as dbc

from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

from src.dashboard.overview_stats import generate_overview_stats
from src.dashboard.overview_year import generate_overview_year
from src.dashboard.overview_tbl import generate_overview_tbl

from src.palette import palette, graph_custom

import pandas as pd


def tab_overview():
    return [
        # Explanation
        dbc.Row(
            dbc.Col(
                children=[
                    html.Div(
                        id="description-card",
                        children=[
                            html.H3("General overview of the spreadsheet"),
                            dbc.Card(
                                """Drag to select on the top graphs, the table will update based on this selection. """
                                """Clicking on the table headers will sort, while typing in the first row will search. """
                                """Searching for numbers and dates takes ranges: ">3" means above average of 3. """,
                                body=True,
                                id="intro"
                            ),
                        ],
                    ),
                ]
            ),
            className="mb-4 mt-4",
        ),
        # Dataset details
        dbc.Row(
            dbc.Col(
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Card title", id="card-album-number", className="card-title"),
                                html.P("Number of albums", className="card-text"),
                            ]),
                        ]),
                    ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Card title", id="card-artist-number", className="card-title"),
                                html.P("Number of artists", className="card-text"),
                            ]),
                        ]),
                    ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Card title", id="card-overall-avg", className="card-title"),
                                html.P(
                                    children=[
                                        "Vote average  ",
                                        dbc.Checklist(
                                            options=[
                                                {
                                                    "label": "Use wAVG?",
                                                    "value": False
                                                },
                                            ],
                                            id="average-select",
                                            switch=True,
                                            inline=True,
                                            style={"display": "inline"}
                                        ),
                                    ],
                                    className="card-text"
                                ),
                            ]),
                        ]),
                    ),
                ]),
            ),
        ),
        # Graphs
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="overview_year", figure={'layout': graph_custom}),
                    md=6,
                ),
                dbc.Col(
                    dcc.Graph(id="overview_stats", figure={'layout': graph_custom}),
                    md=6,
                ),
            ],
            className="mb-4 mt-4",
        ),
        # Table
        dbc.Row(
            [
                dbc.Col(
                    dt.DataTable(
                        id='overview_year_tbl',
                        columns=[
                            {
                                'id': "Released",
                                'name': 'Released',
                                'type': 'datetime',
                            },
                            {
                                'id': "Artist",
                                'name': 'Artist'
                            },
                            {
                                'id': "Album",
                                'name': 'Album'
                            },
                            {
                                'id': "AVG",
                                'name': 'Average',
                                'type': 'numeric',
                            },
                            {
                                'id': "Votes",
                                'name': '#Votes',
                                'type': 'numeric',
                            },
                        ],
                        style_header={'backgroundColor': palette['black']},
                        style_cell={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': palette['white'],
                            'border': '1px solid black'
                        },
                        style_cell_conditional=[
                            {
                                'if': {
                                    'column_id': 'Released'
                                },
                                'width': '20%'
                            },
                            {
                                'if': {
                                    'column_id': 'AVG'
                                },
                                'width': '10%'
                            },
                            {
                                'if': {
                                    'column_id': 'Votes'
                                },
                                'width': '10%'
                            },
                        ],
                        style_filter={
                            'backgroundColor': palette['lblue'],
                            'color': palette['white']
                        },
                        page_size=12,
                        sort_action='native',
                        sort_mode="multi",
                        filter_action='native',
                        cell_selectable=False,
                        style_as_list_view=True,
                    ),
                ),
            ],
            className="mb-4 mt-4",
        )
    ]


# Begin tab callbacks
#
#


@callback([
    Output("card-album-number", "children"),
    Output("card-artist-number", "children"),
    Output("card-overall-avg", "children"),
], [
    Input("average-select", "value"),
    Input("spreadsheet_data", 'modified_timestamp'),
], [State("spreadsheet_data", 'data')])
def update_overview_summary(avg_col, ts, data):

    if ts is None:
        raise PreventUpdate

    col = "AVG"
    if avg_col and "WAVG" in data:
        col = "WAVG"

    df = pd.DataFrame(data)

    return (df['Album'].count(), df['Artist'].nunique(), f"{df[col].mean(): .3f}")


@callback(
    Output("overview_stats", "figure"),
    [
        Input("average-select", "value"),
        Input("spreadsheet_data", 'modified_timestamp'),
    ],
    [State("spreadsheet_data", 'data')],
)
def update_overview_stats(avg_col, ts, data):

    if ts is None:
        raise PreventUpdate

    col = "AVG"
    if avg_col and "WAVG" in data:
        col = "WAVG"

    return generate_overview_stats(data, col)


@callback(
    Output("overview_year", "figure"),
    [
        Input("average-select", "value"),
        Input("spreadsheet_data", 'modified_timestamp'),
    ],
    [State("spreadsheet_data", 'data')],
)
def update_overview_graph(avg_col, ts, data):

    if ts is None:
        raise PreventUpdate

    col = "AVG"
    if avg_col and "WAVG" in data:
        col = "WAVG"

    return generate_overview_year(data, col)


@callback(
    Output("overview_year_tbl", "data"), [
        Input("spreadsheet_data", 'modified_timestamp'),
        Input("overview_year", "selectedData"),
        Input("overview_stats", "selectedData"),
        Input("average-select", "value"),
    ], [State("spreadsheet_data", 'data')]
)
def update_overview_table(ts, sel_year, sel_stats, avg_col, data):

    if ts is None:
        raise PreventUpdate

    col = "AVG"
    if avg_col and "WAVG" in data:
        col = "WAVG"

    return generate_overview_tbl(data, sel_year, sel_stats, col)
