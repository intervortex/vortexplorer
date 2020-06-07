palette = {
    'black': '#21252C',
    'white': '#dad7d0',
    'light': '#FFBF00',
}

graph_custom = dict(
    yaxis=dict(
        gridcolor=palette['white'],
        gridwidth=1,
        showgrid=True,
    ),
    font=dict(
        family="Open Sans",
        color=palette['light'],
    ),
    paper_bgcolor=palette['black'],
    plot_bgcolor=palette['black'],
    hovermode='closest',
    autosize=True,
    showlegend=False,
)
