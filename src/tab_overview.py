import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from src.palette import palette, graph_custom


def tab_overview():
    return [
        # Explanation and details
        dbc.Row(
            dbc.Col(
                children=[
                    html.Div(
                        id="description-card",
                        children=[
                            html.H3(
                                "General overview of the spreadsheet"),
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
                                html.H4("Card title",
                                        id="cardText1",
                                        className="card-title"),
                                html.P("Number of albums",
                                       className="card-text"),
                            ]),
                        ]),
                    ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Card title",
                                        id="cardText2",
                                        className="card-title"),
                                html.P("Number of artists",
                                       className="card-text"),
                            ]),
                        ]),
                    ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Card title",
                                        id="cardText3",
                                        className="card-title"),
                                html.P("Vote average",
                                       className="card-text"),
                            ]),
                        ]),
                    ),
                ]),
            ),
        ),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id="overview_year",
                          figure={'layout': graph_custom}),
            ),
            dbc.Col(
                dcc.Graph(id="overview_stats",
                          figure={'layout': graph_custom}),
            ),
        ], className="mb-4 mt-4",),
        dbc.Row([
            dbc.Col(
                dt.DataTable(
                    id='overview_year_tbl',
                    columns=[
                        {'id': "Year", 'name': 'Year'},
                        {'id': "Artist", 'name': 'Artist'},
                        {'id': "Album", 'name': 'Album'},
                        {'id': "AVG", 'name': 'Average'},
                        {'id': "Votes", 'name': 'No. Votes'},
                    ],
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)'
                    },
                    style_cell={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                    },
                    style_filter={
                        'backgroundColor': 'rgb(185, 167, 167)',
                        'color': 'white'
                    },
                    page_size=12,
                    sort_action='native',
                    filter_action='native',
                ),
            ),
        ], className="mb-4 mt-4",)
    ]
