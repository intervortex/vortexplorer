import copy

from src.palette import palette, graph_custom


def generate_crossuser_corr(data_df, hm_click):

    dff = data_df

    user1 = ""
    user2 = ""
    xdata = ""
    ydata = ""
    zdata = ""
    text = ""

    if hm_click is not None:
        user1 = hm_click["points"][0]["x"]
        user2 = hm_click["points"][0]["y"]
        xdata = dff[user1]
        ydata = dff[user2]
        zdata = dff['AVG']
        text = (
            dff["Artist"]
            + " - "
            + "<i>"
            + dff["Album"]
            + "</i> ("
            + dff["Year"].map(str)
            + ")<br> Average: "
            + dff["AVG"].map(str)
            + " (from "
            + dff["Votes"].map(str)
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
                'showscale':True,
                'colorbar':{'title': {'text': 'Average'}},
            },
            text=text,
        )
    ]
    layout = copy.deepcopy(graph_custom)
    layout.update(
        dict(
            # TODO: do not do like this
            width=800,
            height=800,
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            font=dict(family="Open Sans", color=palette['light'], size=18),
            xaxis={
                'title': user1,
                "range": [0, 10.5],
                "automargin": True,
                "tickmode": 'linear',
                "tick0": 0.0,
                "dtick": 1.0,
            },
            yaxis={
                'title': user2,
                "range": [0, 10.5],
                "automargin": True,
                "tickmode": 'linear',
                "tick0": 0.0,
                "dtick": 1.0,
            },
        )
    )
    return {"data": data, "layout": layout}
