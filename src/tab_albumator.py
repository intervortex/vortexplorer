import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from src.palette import palette, graph_custom


def tab_albumator():
    return [
        # Explanation and details
        dbc.Row(
            dbc.Col(
                children=[
                    html.Div(
                        id="description-card",
                        children=[
                            html
                            .H3("Explore albums and artists. Find the gems."),
                            dbc
                            .Card("""Coming soon.""", body=True, id="intro"),
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
                                html.H4(
                                    "Card title",
                                    id="cardText1",
                                    className="card-title"
                                ),
                                html.P("Most agreed", className="card-text"),
                            ]),
                        ]),
                    ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody([
                                html.H4(
                                    "Card title",
                                    id="cardText2",
                                    className="card-title"
                                ),
                                html.P(
                                    "Most disagreed", className="card-text"
                                ),
                            ]),
                        ]),
                    ),
                ]),
            ),
        ),
    ]
