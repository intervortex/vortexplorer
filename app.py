import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import numpy as np
import pandas as pd
import pathlib

from src.tab_overview import tab_overview
from src.overview_year import generate_overview_year
from src.overview_year import generate_overview_year_tbl
from src.overview_stats import generate_overview_stats

from src.tab_cross_user import tab_cross_user
from src.crossuser_heatmap import generate_crossuser_heatmap
from src.crossuser_corr import generate_crossuser_corr

from src.tab_user import tab_user
from src.user_overview import generate_user_overview
from src.user_breakdown import generate_user_breakdown

# Create application
app = dash.Dash(
    __name__,
    meta_tags=[{
        "name": "viewport",
        "content": "width=device-width, initial-scale=1"
    }],
    external_stylesheets=[dbc.themes.DARKLY],
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
users = [
    'goaticorn', 'goatiyas', 'Targeauxt', 'Capryde', 'JoatK', 'Dr. Goatinen',
    'crazygoatman', 'aftergoat', 'Ca Prines', 'Goatdicot', 'dygoatic',
    'Goatickvillian'
]


def header():
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Select Spreadsheet", href="#")),
            dbc.NavItem(
                dcc.Dropdown(
                    id="spreadsheet-select",
                    options=[{
                        "label": i,
                        "value": i
                    } for i in spreadsheet_list],
                    value=spreadsheet_list[0],
                ),
                style={"width": "200px"},
            ),
            dbc.NavItem(dbc.Button('Halp', id='open')),
            dbc.Modal(
                [
                    dbc.ModalHeader("Help"),
                    dbc.ModalBody("This is the content of the modal"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="ml-auto")
                    ),
                ],
                id="modal",
                size="lg",
                centered=True,
            ),
        ],
        brand=app.title,
        brand_href="#",
        color="primary",
        dark=True,
        fixed='top',
        sticky='sticky',
    )


def build_tabs():
    return dcc.Tabs(
        id="app-tabs",
        value="tab1",
        className="custom-tabs",
        children=[
            dcc.Tab(
                id="general-tab",
                label="Spreadsheet",
                value="tab1",
                className="custom-tab bg-dark",
                selected_className="custom-tab--selected",
            ),
            dcc.Tab(
                id="user-tab",
                label="Users",
                value="tab2",
                className="custom-tab bg-dark",
                selected_className="custom-tab--selected",
            ),
            dcc.Tab(
                id="cross-tab",
                label="CrossTaste™",
                value="tab3",
                className="custom-tab bg-dark",
                selected_className="custom-tab--selected",
            ),
        ],
    )


app.layout = html.Div(
    id="outer-wrapper",
    children=[
        dcc.Store(id="spreadsheet_data"),
        header(),
        dbc.Container(
            id="app-container",
            children=[
                dbc.Row(dbc.Col(build_tabs(), )),
                dbc.Row(dbc.Col(id="app-content"))
            ],
            style={'margin-top': "100px"}
        ),
    ],
)


# Modal
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"),
     Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Tabs
@app.callback(Output('app-content', 'children'), [Input('app-tabs', 'value')])
def render_content(tab):
    if tab == 'tab1':
        return tab_overview()
    elif tab == 'tab2':
        return tab_user()
    elif tab == 'tab3':
        return tab_cross_user()


# Data
@app.callback(
    Output("spreadsheet_data", "data"),
    [
        Input("spreadsheet-select", "value"),
    ],
)
def get_spreadsheet_data(spreadsheet_name):
    return data_df.to_dict('records')


# Data tab 1
@app.callback([
    Output("cardText1", "children"),
    Output("cardText2", "children"),
    Output("cardText3", "children"),
], [Input("spreadsheet_data", 'modified_timestamp')],
              [State("spreadsheet_data", 'data')])
def update_text(ts, data):

    if ts is None:
        raise PreventUpdate

    df = pd.DataFrame(data)

    return (
        df['Album'].count(), df['Artist'].nunique(), f"{df['AVG'].mean(): .3f}"
    )


@app.callback(
    Output("overview_year",
           "figure"), [Input("spreadsheet_data", 'modified_timestamp')],
    [State("spreadsheet_data", 'data')]
)
def update_overview_year(ts, data):

    if ts is None:
        raise PreventUpdate

    return generate_overview_year(data)


@app.callback(
    Output("overview_stats",
           "figure"), [Input("spreadsheet_data", 'modified_timestamp')],
    [State("spreadsheet_data", 'data')]
)
def update_overview_stats(ts, data):

    if ts is None:
        raise PreventUpdate

    return generate_overview_stats(data)


@app.callback(
    Output("overview_year_tbl", "data"), [
        Input("spreadsheet_data", 'modified_timestamp'),
        Input("overview_year", "selectedData"),
        Input("overview_stats", "selectedData"),
    ], [State("spreadsheet_data", 'data')]
)
def update_overview_year_tbl(ts, sel_year, sel_stats, data):

    if ts is None:
        raise PreventUpdate

    return generate_overview_year_tbl(data, sel_year, sel_stats)


# Data tab 2
@app.callback(
    Output("user_overview", "figure"), [
        Input("spreadsheet_data", 'modified_timestamp'),
    ], [State("spreadsheet_data", 'data')]
)
def update_user_overview(ts, data):

    if ts is None:
        raise PreventUpdate

    return generate_user_overview(data, users)


@app.callback([
    Output("user_breakdown_select", "options"),
    Output("user_breakdown_select", "value"),
], [
    Input("spreadsheet_data", 'modified_timestamp'),
], [State("spreadsheet_data", 'data')])
def update_user_breakdown_value(ts, data):

    if ts is None:
        raise PreventUpdate

    return [{'label': user, "value": user} for user in users], users[0]


@app.callback(
    Output("user_breakdown", "figure"), [
        Input("spreadsheet_data", 'modified_timestamp'),
        Input("user_breakdown_select", "value"),
    ], [State("spreadsheet_data", 'data')]
)
def update_user_breakdown(ts, users, data):

    if ts is None:
        raise PreventUpdate

    return generate_user_breakdown(data, users)


# Data tab 3
@app.callback(
    Output("cross_taste_map", "figure"), [
        Input("spreadsheet_data", 'modified_timestamp'),
        Input("cross_taste_map", "clickData"),
    ], [State("spreadsheet_data", 'data')]
)
def update_heatmap(ts, click, data):

    if ts is None:
        raise PreventUpdate

    return generate_crossuser_heatmap(data, users, click, False)


@app.callback(
    Output("taste_detail", "figure"), [
        Input("spreadsheet_data", 'modified_timestamp'),
        Input("cross_taste_map", "clickData"),
    ], [State("spreadsheet_data", 'data')]
)
def update_detail_taste(ts, hm_click, data):

    if ts is None:
        raise PreventUpdate

    return generate_crossuser_corr(data, hm_click)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
