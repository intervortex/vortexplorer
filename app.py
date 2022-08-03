import io
import os
import pathlib

import requests
import pandas as pd

from dash import Dash
from dash import dcc, html
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# Connect to redis if possible
REDIS = None
try:
    import redis
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    REDIS = redis.from_url(redis_url)
    REDIS.ping()
except:
    REDIS = None
    pass

# Offline mode (no G Sheets) and paths of offline data, for testing
OFFLINE = False

# Main app component imports

from data.sheets import sheets_list, get_sheet_csv
#
from src.process.clean_data import process_spreadsheet
#
from src.dashboard.help import build_help
from src.dashboard.tabs import build_tabs
from src.dashboard.tab_albumator import tab_albumator
from src.dashboard.tab_cross_user import tab_cross_user
from src.dashboard.tab_overview import tab_overview
from src.dashboard.tab_user import tab_user

# Create application
app = Dash(
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
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
         <link href="https://fonts.googleapis.com/css?family=B612:400,700" rel="stylesheet">
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Begin app layout
#
#

app.layout = html.Div(
    id="outer-wrapper",
    children=[
        dcc.Store(id="spreadsheet_data"),
        dbc.Container(
            id="app-container",
            children=[
                # The header
                dbc.Row(
                    justify="center",
                    align="center",
                    style={
                        "height": "100px",
                        "margin-top": "50px",
                    },
                    children=[
                        dbc.Col(
                            dbc.Label("Select Spreadsheet"),
                            className="col-4",
                            style={'text-align': 'right'},
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="spreadsheet-select",
                                options=[{
                                    "label": i,
                                    "value": i
                                } for i in sheets_list],
                                value=next(iter(sheets_list)),
                                persistence=True,
                                persistence_type="local",
                            ),
                            className="col-4"
                        ),
                        dbc.Col(dbc.Button('Halp', id='open'), className="col-4"),
                        build_help(),
                    ],
                ),
                # The tabs
                dbc.Row(dbc.Col(build_tabs(), )),
                # The content
                dbc.Row(dbc.Col(id="app-content")),
                # The error modal
                dbc.Modal(id="error-modal"),
                # Some extra space
                dbc.Row(style={"height": "50px"}),
            ],
        ),
    ],
)

# Begin app callbacks
#
#


# Help Modal
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
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
    if tab == 'tab2':
        return tab_user()
    if tab == 'tab3':
        return tab_cross_user()
    if tab == 'tab4':
        return tab_albumator()


# Data
@app.callback(
    [
        Output("spreadsheet_data", "data"),
        Output("error-modal", "is_open"),
        Output("error-modal", "children"),
    ],
    [Input("spreadsheet-select", "value")],
    [State("error-modal", "is_open")],
)
def get_spreadsheet_data(spreadsheet_name, err_modal):
    if OFFLINE:
        BASE_PATH = pathlib.Path(__file__).parent.resolve()
        DATA_PATH = BASE_PATH.joinpath("data").resolve()
        df = pd.read_csv(DATA_PATH / "goat.csv")
    else:
        try:
            resp = requests.get(get_sheet_csv(spreadsheet_name))
            resp.encoding = 'UTF-8'
            df = process_spreadsheet(
                pd.read_csv(io.StringIO(resp.text), na_values=[' ']), spreadsheet_name
            )
        except Exception as ex:
            from src.notifications import notify
            notify(str(ex))
            return {}, True, str(ex)

    return df.to_dict('list'), False, None


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
