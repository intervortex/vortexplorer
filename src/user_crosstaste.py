from src.palette import palette, graph_custom


def generate_user_crossdiff(data_df, hm_click):

    filtered_data = data_df

    user1 = ""
    user2 = ""
    xdata = ""
    ydata = ""
    zdata = ""

    if hm_click is not None:
        user1 = hm_click["points"][0]["x"]
        user2 = hm_click["points"][0]["y"]
        xdata = filtered_data[user1]
        ydata = filtered_data[user2]
        zdata = filtered_data['AVG']

    # no worky
    hovertemplate = "<b> %{y} - %{x} <br> Taste similarity: <br> %{text}"

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
            text=zdata,
            text2=zdata,
        )
    ]
    layout = dict(
        xaxis={'title': user1},
        yaxis={'title': user2},
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest',
        showlegend=False,
    )
    layout.update(graph_custom)
    return {"data": data, "layout": layout}
