import pandas as pd
import plotly.figure_factory as ff

from src.palette import palette, graph_custom


def generate_user_breakdown(data, sel_users):

    hist_data = []
    group_labels = []

    if sel_users:

        # Have to make sure it's always an array
        sel_users = [sel_users] if isinstance(sel_users, str) else sel_users

        hist_data = [data[user] for user in sel_users]
        group_labels = sel_users  # name of the dataset

    fig = ff.create_distplot(hist_data, group_labels, histnorm='probability')

    # format the layout
    fig.update_layout(**graph_custom)
    fig.update_layout(
        xaxis_title='Vote',
        yaxis_title='Vote count',
        font=dict(family="Open Sans", color=palette['light'], size=18),
        showlegend=True,
    )

    return fig
