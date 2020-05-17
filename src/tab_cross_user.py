import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

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
                            html.H3(
                                "Keep your friends close and your enemies roasted"),
                            dbc.Card(
                                """Explore taste similarity between users. """
                                """Click on the heatmap to see a detailed breakdown. """
                                """Values closer to 0 mean a better taste agreement. """,
                                body=True, id="intro"),
                        ],
                    ),
                ]
            ),
            className="mt-4",
        ),
        # Similarity Heatmap
        dbc.Row(
            dbc.Col(
                id="user_heatmap_card",
                children=[
                    html.Hr(),
                    html.H3("Tastemap"),
                    html.Hr(),
                    dcc.Graph(
                        id="cross_taste_map",
                        figure={'layout': graph_custom}),
                ],
            )
        ),
        # Crossreference chart
        dbc.Row(
            dbc.Col(
                id="user_crossdetail_card",
                # className="d-flex justify-content-center",
                children=[
                    html.Hr(),
                    html.H3("Tastedetail"),
                    html.Hr(),
                    dcc.Graph(id="taste_detail",
                              figure={'layout': graph_custom}),
                ],
            )
        )]
