import plotly.figure_factory as ff

from src.palette import palette, graph_custom


def generate_overview_stats(data_df):

    dff = data_df

    hist_data = [dff["AVG"]]
    group_labels = ["Average"]

    fig = ff.create_distplot(
        hist_data,
        group_labels,
        colors=[palette['light']],
        bin_size=[0.1],
        show_rug=False
    )

    # format the layout
    fig.update_layout(**graph_custom)
    fig.update_layout(
        title="Average distribution",
        font=dict(family="Open Sans", color=palette['light']),
    )

    return fig
