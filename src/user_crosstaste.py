from src.palette import palette, graph_custom


def generate_user_crossdiff(data_df, hm_click):

    filtered_data = data_df

    user1 = ""
    user2 = ""
    xdata = ""
    ydata = ""
    zdata = ""
    text = ""

    if hm_click is not None:
        user1 = hm_click["points"][0]["x"]
        user2 = hm_click["points"][0]["y"]
        xdata = filtered_data[user1]
        ydata = filtered_data[user2]
        zdata = filtered_data['AVG']
        text = (
            filtered_data["Artist"]
            + " - "
            + "<i>"
            + filtered_data["Album"]
            + "</i> ("
            + filtered_data["Year"].map(str)
            + ")<br> Average: "
            + filtered_data["AVG"].map(str)
            + " (from "
            + filtered_data["Votes"].map(str)
            + " votes)"
        )

    hovertemplate = "<b> Album: </b> <br> %{text}<extra></extra>"

    data = [
        dict(
            x=xdata,
            y=ydata,
            mode='markers',
            opacity=0.7,
            hovertemplate=hovertemplate,
            marker={
                'symbol': 'square',
                'size': 17,
                'line': {'width': 0.5, 'color': palette['light']},
                'color': zdata,
                'colorscale': 'inferno',
            },
            text=text,
        )
    ]
    layout = dict(
        # TODO: do not do like this
        width=800,
        height=800,
        font=dict(family="Open Sans", color=palette['light'], size=18),
        xaxis={
            'title': user1,
            "range": [0, 10.5],
            "automargin": True,
            "tickmode": 'linear',
            "tick0": 0.0,
            "dtick": 1.0,
            "tickfont": dict(family="sans-serif", color=palette['light']),
            'tickcolor': palette['light'],
        },
        yaxis={
            'title': user2,
            "range": [0, 10.5],
            "automargin": True,
            "tickmode": 'linear',
            "tick0": 0.0,
            "dtick": 1.0,
            "tickfont": dict(family="sans-serif", color=palette['light']),
            'tickcolor': palette['light'],
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest',
        showlegend=False,
    )
    layout.update(graph_custom)
    return {"data": data, "layout": layout}
