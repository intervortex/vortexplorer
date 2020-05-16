import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from src.palette import palette, graph_custom


def user_description_card():
    return html.Div(
        id="description-card",
        children=[
            html.H3("Keep your friends close and your enemies roasted."),
            html.Div(
                id="intro",
                children="Explore taste similarity between users. Click on the heatmap to see a detailed breakdown.",
            ),
        ],
    )


def tab_users():
    return [
        dbc.Row(
            dbc.Col(
                children=[
                    user_description_card(),
                ]
            )
        ),
        # Similarity Heatmap
        dbc.Row(
            dbc.Col(
                id="user_heatmap_card",
                children=[
                    html.B("Tastemap"),
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
                children=[
                    html.B("Tastedetail"),
                    html.Hr(),
                    dcc.Graph(id="taste_detail",
                              figure={'layout': graph_custom}),
                ],
            )
        )]
