from dash import dcc, html
import dash_bootstrap_components as dbc

from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

from src.process.clean_data import process_users

from src.dashboard.user_breakdown import generate_user_breakdown
from src.dashboard.user_overview import generate_user_overview

from src.palette import palette, graph_custom


def tab_user():
    return [
        # Explanation and details
        dbc.Row(
            dbc.Col(
                children=[
                    html.Div(
                        id="description-card",
                        children=[
                            html.H3("Member voting details"),
                            dbc.Card(
                                """The way each member voted for their albums. """
                                """First graph shows an overview of all voters. """
                                """Second graph can be customised to show the vote distribution on a person-by-person basis. """,
                                body=True,
                                id="intro"
                            ),
                        ],
                    ),
                ]
            ),
            className="mb-4 mt-4",
        ),
        # Overview
        dbc.Row(
            [
                dbc.Col([
                    html.H3("Overview"),
                    html.Hr(),
                    dcc.Graph(id="user_overview", figure={'layout': graph_custom}),
                ]),
            ],
            className="mb-4",
        ),
        # Breakdown
        dbc.Row(
            [
                dbc.Col([html.H3("Individual breakdown"),
                         html.Hr(), dcc.Dropdown(
                             id="user_breakdown_select",
                             multi=True,
                         )], md=4),
                dbc.Col([
                    dcc.Graph(id="user_breakdown", figure={'layout': graph_custom}),
                ], md=8),
            ],
            className="mb-4",
        ),
    ]


# Begin tab callbacks
#
#


@callback(Output("user_overview", "figure"), [
    Input("spreadsheet_data", 'modified_timestamp'),
], [State("spreadsheet_data", 'data')])
def update_user_overview(ts, data):

    if ts is None:
        raise PreventUpdate

    return generate_user_overview(data, process_users(data))


@callback(
    [
        Output("user_breakdown_select", "options"),
        Output("user_breakdown_select", "value"),
    ],
    [Input("spreadsheet_data", 'modified_timestamp')],
    [State("spreadsheet_data", 'data')],
)
def update_user_breakdown_value(ts, data):

    if ts is None:
        raise PreventUpdate

    users = process_users(data)

    return [{'label': user, "value": user} for user in users], users[0]


@callback(
    Output("user_breakdown", "figure"),
    [
        Input("spreadsheet_data", 'modified_timestamp'),
        Input("user_breakdown_select", "value"),
    ],
    [State("spreadsheet_data", 'data')],
)
def update_user_breakdown(ts, sel_users, data):

    if ts is None:
        raise PreventUpdate

    return generate_user_breakdown(data, sel_users)
