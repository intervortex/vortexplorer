from dash import dcc, html
import dash_bootstrap_components as dbc

from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

from src.process.clean_data import process_users

from src.dashboard.crossuser_corr import generate_crossuser_corr
from src.dashboard.crossuser_heatmap import generate_crossuser_heatmap

from src.palette import palette, graph_custom


def tab_cross_user():
    return [
        # Explanation and details
        dbc.Row(
            dbc.Col(
                children=[
                    html.Div(
                        id="description-card",
                        children=[
                            html.H3("Keep your friends close and your enemies roasted"),
                            dbc.Card(
                                """Explore taste similarity between users. """
                                """Click on the heatmap to see a detailed breakdown. """,
                                body=True,
                                id="intro"
                            ),
                        ],
                    ),
                ]
            ),
            className="mt-4",
        ),
        # Similarity Heatmap
        dbc.Row([
            dbc.Col(
                id="user_heatmap_card",
                children=[
                    html.Hr(),
                    html.H3("Tastemap"),
                    html.Hr(),
                    dcc.Graph(id="cross_taste_map", figure={'layout': graph_custom}),
                ],
            )
        ]),
        # Crossreference chart
        dbc.Row(
            dbc.Col(
                id="user_crossdetail_card",
                # className="d-flex justify-content-center",
                children=[
                    html.Hr(),
                    html.H3("Tastedetail"),
                    html.Hr(),
                    dcc.Graph(id="taste_detail", figure={'layout': graph_custom}),
                ],
            )
        )
    ]


# Begin tab callbacks
#
#


@callback(
    Output("cross_taste_map", "figure"),
    [
        Input("spreadsheet_data", 'modified_timestamp'),
        Input("cross_taste_map", "clickData"),
    ],
    [State("spreadsheet_data", 'data')],
)
def update_heatmap(ts, click, data):

    if ts is None:
        raise PreventUpdate

    return generate_crossuser_heatmap(data, process_users(data), click, False)


@callback(
    Output("taste_detail", "figure"),
    [
        Input("spreadsheet_data", 'modified_timestamp'),
        Input("cross_taste_map", "clickData"),
    ],
    [State("spreadsheet_data", 'data')],
)
def update_detail_taste(ts, hm_click, data):

    if ts is None:
        raise PreventUpdate

    return generate_crossuser_corr(data, hm_click)
