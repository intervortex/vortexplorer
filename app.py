import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ClientsideFunction

import numpy as np
import pandas as pd
import pathlib

from src.tab_cross_user import tab_users
from src.user_heatmap import generate_user_heatmap
from src.user_crosstaste import generate_user_crossdiff

# Create application
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.CYBORG],
)

server = app.server
app.title = "Vortexplorer"
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = False

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

# Read data
spreadsheet_list = ['GOAT']
data_df = pd.read_csv(DATA_PATH / "goat.csv")
users = ['goaticorn',
         'goatiyas', 'Targeauxt', 'Capryde', 'JoatK', 'Dr. Goatinen',
         'crazygoatman', 'aftergoat', 'Ca Prines', 'Goatdicot', 'dygoatic',
         'Goatickvillian']


def header():
    return dbc.NavbarSimple(
        children=[
            html.P("Select Spreadsheet"),
            dcc.Dropdown(
                id="spreadsheet-select",
                options=[{"label": i, "value": i} for i in spreadsheet_list],
                value=spreadsheet_list[0],
            )
        ],
        brand="Vortexplorer",
        brand_href="#",
        color="warning",
        dark=True,
    )


def build_tabs():
    return dcc.Tabs(
        id="app-tabs",
        value="tab2",
        className="custom-tabs",
        children=[
            dcc.Tab(
                id="general-tab",
                label="General Overview",
                value="tab1",
                className="custom-tab",
                selected_className="custom-tab--selected",
            ),
            dcc.Tab(
                id="user-tab",
                label="CrossTaste",
                value="tab2",
                className="custom-tab",
                selected_className="custom-tab--selected",
            ),
        ],
    )


app.layout = html.Div(
    id="outer-wrapper",
    children=[
        dcc.Store(id="spreadsheet"),
        header(),
        dbc.Container(
            id="app-container",
            children=[
                dbc.Row(
                    dbc.Col(
                        build_tabs(),
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        id="app-content"
                    )
                )
            ],
        ),
        # generate_modal(),
    ],
)

# Data


@app.callback(
    Output("spreadsheet", "data"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
)
# Tabs
@app.callback(Output('app-content', 'children'),
              [Input('app-tabs', 'value')])
def render_content(tab):
    if tab == 'tab1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab2':
        return html.Div(tab_users())


@app.callback(
    Output("cross_taste_map", "figure"),
    [
        # Input("spreadsheet", "value"),
        Input("spreadsheet-select", "value"),
        Input("cross_taste_map", "clickData"),
    ],
)
def update_heatmap(spreadsheet, hm_click):

    reset = False
    # Find which one has been triggered
    # ctx = dash.callback_context

    # if ctx.triggered:
    #     prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
    #     if prop_id == "reset-btn":
    #         reset = True

    # Return to original hm(no colored annotation) by resetting
    return generate_user_heatmap(data_df, users, spreadsheet, hm_click, reset)


@app.callback(
    Output("taste_detail", "figure"),
    [Input("cross_taste_map", "clickData")],
)
def update_detail_taste(hm_click):

    # Return to original hm(no colored annotation) by resetting
    return generate_user_crossdiff(data_df, hm_click)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
