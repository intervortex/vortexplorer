import io
import pathlib

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from src.crossuser_corr import generate_crossuser_corr
from src.crossuser_heatmap import generate_crossuser_heatmap
from src.overview_stats import generate_overview_stats
from src.overview_year import (
    generate_overview_year, generate_overview_year_tbl
)
from src.tab_cross_user import tab_cross_user
from src.tab_overview import tab_overview
from src.tab_user import tab_user
from src.user_breakdown import generate_user_breakdown
from src.user_overview import generate_user_overview
from src.clean_data import (process_spreadsheet, process_users)

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

OFFLINE = False

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

# Read data
sheets_template = "https://docs.google.com/spreadsheet/ccc?key={0}&output=csv"
spreadsheet_list = {
    'GOAT': "1F_7q1tP7zoy3sJKIAJa2XJ5NbyAGASvmiglSJSneh2U",
    'Reliquary': "13T9MFuhDTuQe_21s58KcX6KiiT2w_HvfiQ9AjEbuzYM",
    'Guts': "18se3f36hUJsTLLoXnYrxKaH_YowWk5HvzqX1jugs72w",
}


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
                    value=next(iter(spreadsheet_list)),
                ),
                style={"width": "200px"},
            ),
            dbc.NavItem(dbc.Button('Halp', id='open')),
            dbc.Modal(
                [
                    dbc.ModalHeader("This is the Vortexplorer."),
                    dbc.ModalBody([
                        html.P(
                            """
                            Welcome to the Vortexplorer. This dashboard is made to get
                            a birds-eye view of the Vortex's spreadsheets, making it
                            simpler to discern what made it into the system, as well
                            as give some insight into each member's tastes and how they
                            compare with one another.
                        """
                        ),
                        html.P(
                            """
                            In order to select one spreadsheet to view, use the drop-down
                            in the top right. The tabs at the top switch between an overview
                            of the music within (Spreadsheet), an overview of the members and
                            their votes (Members) and a cross-grid allowing members to see
                            who they match in taste (CrossTaste).
                        """
                        ),
                        html.Hr(),
                        html.H5("FAQ:"),
                        html.Div("Q: Is this real-time?"),
                        html.Div(
                            "A: Mostly, data is taken from the spreadsheets every time one is selected."
                        ),
                        html.Br(),
                        html.Div("Q: I don't see my name!"),
                        html.Div(
                            "A: Only those who have voted enough times are selected. Get voting."
                        ),
                        html.Br(),
                        html.Div("Q: Something doesn't work!"),
                        html.Div(
                            "A: Let i/0 know and it will be fixed in 1-6 months."
                        ),
                    ]),
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
                label="Members",
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
    if OFFLINE:
        df = pd.read_csv(DATA_PATH / "goat.csv")
    else:
        resp = requests.get(
            sheets_template.format(spreadsheet_list[spreadsheet_name])
        )
        resp.encoding = 'UTF-8'
        df = pd.read_csv(io.StringIO(resp.text))
    return process_spreadsheet(df, spreadsheet_name).to_dict('list')


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

    return generate_user_overview(data, process_users(data))


@app.callback([
    Output("user_breakdown_select", "options"),
    Output("user_breakdown_select", "value"),
], [
    Input("spreadsheet_data", 'modified_timestamp'),
], [State("spreadsheet_data", 'data')])
def update_user_breakdown_value(ts, data):

    if ts is None:
        raise PreventUpdate

    users = process_users(data)

    return [{'label': user, "value": user} for user in users], users[0]


@app.callback(
    Output("user_breakdown", "figure"), [
        Input("spreadsheet_data", 'modified_timestamp'),
        Input("user_breakdown_select", "value"),
    ], [State("spreadsheet_data", 'data')]
)
def update_user_breakdown(ts, sel_users, data):

    if ts is None:
        raise PreventUpdate

    return generate_user_breakdown(data, sel_users)


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

    return generate_crossuser_heatmap(data, process_users(data), click, False)


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
