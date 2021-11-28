from dash import dcc, html
import dash_bootstrap_components as dbc

from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

from src.dashboard.albumator_stats import generate_album_breakdown
from src.dashboard.albumator_stats import generate_album_stats

from src.palette import palette, graph_custom


def tab_albumator():
    return [
        # Explanation
        dbc.Row(
            dbc.Col(
                children=[
                    html.Div(
                        id="description-card",
                        children=[
                            html.H3("Explore albums and artists. Find the gems."),
                            dbc.Card("""Coming soon.""", body=True, id="intro"),
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
                                html.H4("Card title", id="cardText1", className="card-title"),
                                html.P("Most agreed on", className="card-text"),
                            ]),
                        ]),
                    ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Card title", id="cardText2", className="card-title"),
                                html.P("Most disagreed on", className="card-text"),
                            ]),
                        ]),
                    ),
                ]),
            ),
            className="mb-4 mt-4",
        ),
        # Album breakdown
        dbc.Row(
            [
                dbc.Col([html.H3("Individual breakdown"),
                         html.Hr(), dcc.Dropdown(
                             id="album_breakdown_select",
                             multi=True,
                         )], md=4),
                dbc.Col([
                    dcc.Graph(id="album_breakdown", figure={'layout': graph_custom}),
                ], md=8),
            ],
            className="mb-4",
        ),
    ]


@callback(
    [
        Output("cardText1", "children"),
        Output("cardText2", "children"),
    ],
    [
        Input("spreadsheet_data", 'modified_timestamp'),
    ],
    [State("spreadsheet_data", 'data')],
)
def update_text(ts, data):

    if ts is None:
        raise PreventUpdate

    stats = generate_album_stats(data)

    return (
        stats['agreed'],
        stats['disagreed'],
    )


@callback(
    [
        Output("album_breakdown_select", "options"),
        Output("album_breakdown_select", "value"),
    ],
    [Input("spreadsheet_data", 'modified_timestamp')],
    [State("spreadsheet_data", 'data')],
)
def update_album_breakdown_value(ts, data):

    if ts is None:
        raise PreventUpdate

    albums = data['Album']

    return [{'label': album, "value": album} for album in albums], albums[0]


@callback(
    Output("album_breakdown", "figure"),
    [
        Input("spreadsheet_data", 'modified_timestamp'),
        Input("album_breakdown_select", "value"),
    ],
    [State("spreadsheet_data", 'data')],
)
def update_album_breakdown(ts, albums, data):

    if ts is None:
        raise PreventUpdate

    return generate_album_breakdown(data, albums)