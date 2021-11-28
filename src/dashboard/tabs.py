from dash import dcc


def build_tabs():
    return dcc.Tabs(
        id="app-tabs",
        value="tab1",
        className="custom-tabs",
        persistence=True,
        persistence_type="local",
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
            dcc.Tab(
                id="album-tab",
                label="Albumator",
                value="tab4",
                className="custom-tab bg-dark",
                selected_className="custom-tab--selected",
            ),
        ],
    )