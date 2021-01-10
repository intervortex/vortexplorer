palette = {
    'black': '#21252C',
    'white': '#dad7d0',
    'light': '#FF7D00',
    'red': '#d7263d',
    'dblue': '#02182B',
    'blue': '#087E8B',
    'lblue': '#0197F6',
}

graph_custom = dict(
    yaxis=dict(
        gridcolor=palette['white'],
        gridwidth=1,
        showgrid=True,
    ),
    font=dict(
        family=
        "Lato, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol",
        color=palette['white'],
    ),
    paper_bgcolor=palette['black'],
    plot_bgcolor=palette['black'],
    hovermode='closest',
    autosize=True,
    showlegend=False,
)
