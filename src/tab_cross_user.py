import dash_core_components as dcc
import dash_html_components as html

from src.palette import palette


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


def user_control_card(spreadsheet_list):
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Spreadsheet"),
            dcc.Dropdown(
                id="spreadsheet-select",
                options=[{"label": i, "value": i} for i in spreadsheet_list],
                value=spreadsheet_list[0],
            ),
        ],
    )


def tab_users(spreadsheet_list):
    return [
        html.Div(
            id="left-column",
            className="four columns",
            children=[
                user_description_card(),
                user_control_card(spreadsheet_list)
            ]
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Similarity Heatmap
                html.Div(
                    id="user_heatmap_card",
                    children=[
                        html.B("Tastemap"),
                        html.Hr(),
                        dcc.Graph(
                            id="cross_taste_map",
                            figure={
                                'layout': {
                                    "paper_bgcolor": palette['black'],
                                    "plot_bgcolor":palette['black'],
                                }}),
                    ],
                ),
                # Crossreference chart
                html.Div(
                    id="user_crossdetail_card",
                    children=[
                        html.B("Tastedetail"),
                        html.Hr(),
                        dcc.Graph(id="taste_detail"),
                    ],
                ),
            ],
        )]
