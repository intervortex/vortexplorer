from dash import dcc, html
import dash_bootstrap_components as dbc


def build_help():
    return dbc.Modal(
        [
            dbc.ModalHeader([
                dbc.ModalTitle("This is the Vortexplorer."),
            ]),
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
                html.Div("A: Mostly, data is taken from the spreadsheets every time one is selected."),
                html.Br(),
                html.Div("Q: I don't see my name!"),
                html.Div("A: Only those who have voted enough times are selected. Get voting."),
                html.Br(),
                html.Div("Q: Something doesn't work!"),
                html.Div("A: Let i/0 know and it will be fixed in 1-6 months."),
            ]),
            dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto")),
        ],
        id="modal",
        size="lg",
        centered=True,
    )
