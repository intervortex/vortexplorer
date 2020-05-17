import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

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
                            html.H3(
                                "User voting details"),
                        ],
                    ),
                ]
            ),
            className="mb-4 mt-4",
        ),
        dbc.Row([
            dbc.Col([
                html.H3("Overview"),
                html.Hr(),
                dcc.Graph(id="user_overview",
                          figure={'layout': graph_custom}),
            ]),
        ], className="mb-4",),
        dbc.Row([
            dbc.Col([
                html.H3("Individual breakdown"),
                html.Hr(),
                dcc.Dropdown(
                    id="user_breakdown_select",
                    multi=True,
                )
            ], width=4),
            dbc.Col([
                dcc.Graph(id="user_breakdown",
                          figure={'layout': graph_custom}),
            ]),
        ], className="mb-4",),
    ]
