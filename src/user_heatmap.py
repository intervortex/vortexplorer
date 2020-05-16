import numpy as np
from src.palette import palette, graph_custom


def generate_user_heatmap(data_df, users, spreadsheet, hm_click, reset):
    """
    """

    filtered_data = data_df

    x_axis = users
    y_axis = users

    user1 = ""
    user2 = ""
    shapes = []

    if hm_click is not None:
        user1 = hm_click["points"][0]["x"]
        user2 = hm_click["points"][0]["y"]

        # Add shape
        x0 = x_axis.index(user1) / len(users)
        x1 = x0 + 1 / len(users)
        y0 = y_axis.index(user2) / len(users)
        y1 = y0 + 1 / len(users)

        shapes = [
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=x0,
                x1=x1,
                y0=y0,
                y1=y1,
                line=dict(color="#ff6347"),
            )
        ]

    # Get z value : sum(number of records) based on x, y,
    crossref = np.zeros([len(users), len(users)])

    annotations = []

    for ind1, col1 in enumerate(users):
        for ind2, col2 in enumerate(users):
            diff = filtered_data[col1] - filtered_data[col2]
            crossref[ind1, ind2] = np.sum(
                np.abs(diff.dropna())) / len(diff.dropna())

            annotation_dict = dict(
                showarrow=False,
                text=f"<b>{crossref[ind1, ind2]:.2f}<b>",
                xref="x",
                yref="y",
                x=col1,
                y=col2,
                font=dict(family="sans-serif"),
            )
            # Highlight annotation text by self-click
            if col1 == user1 and col2 == user2:
                if not reset:
                    annotation_dict.update(
                        size=15, font=dict(color=palette['light']))

            annotations.append(annotation_dict)

    crossref_adj = crossref / np.average(crossref)

    # Heatmap
    hovertemplate = "<b> %{y} - %{x} <br> Taste similarity: <br> %{z}"

    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=crossref_adj,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale='inferno',
            reversescale=True,
        )
    ]

    layout = dict(
        margin=dict(l=100, b=50, t=50, r=50),
        modebar={"orientation": "v"},
        font=dict(family="Open Sans"),
        annotations=annotations,
        shapes=shapes,
        xaxis=dict(
            side="top",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif", color=palette['light']),
            tickcolor=palette['light'],
        ),
        yaxis=dict(
            side="left",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif", color=palette['light']),
            ticksuffix="",
            tickcolor=palette['light'],
        ),
        hovermode="closest",
        showlegend=False,
    )
    layout.update(graph_custom)
    return {"data": data, "layout": layout}
