import pandas as pd
import plotly.figure_factory as ff

from src.palette import palette, graph_custom


def generate_user_breakdown(data, users):

    dff = pd.DataFrame(data)

    hist_data = []
    group_labels = []

    if users:

        # Have to make sure it's always an array
        users = [users] if isinstance(users, str) else users

        hist_data = [dff[user] for user in users]
        group_labels = users  # name of the dataset

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
