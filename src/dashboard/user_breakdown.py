import plotly.figure_factory as ff
import plotly.graph_objects as go

from src.palette import palette, graph_custom


def generate_user_breakdown(data_df, sel_users):

    group_labels = []
    hist_data = [[]]

    if sel_users:

        # Have to make sure it's always an array
        sel_users = [sel_users] if isinstance(sel_users, str) else sel_users
        hist_data = [[vote
                      for vote in data_df[user]
                      if vote]
                     for user in sel_users]
        group_labels = sel_users  # name of the dataset

        fig = ff.create_distplot(
            hist_data, group_labels, histnorm='probability', show_rug=False
        )
    else:
        fig = go.Figure()

    # format the layout
    fig.update_xaxes(range=[0, 10])
    fig.update_layout(**graph_custom)
    fig.update_layout(
        xaxis_title='Vote',
        yaxis_title='Vote proportion',
        font=dict(family="Open Sans", color=palette['light'], size=18),
        showlegend=True,
    )

    return fig
