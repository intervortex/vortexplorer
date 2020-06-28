palette = {
    'black': '#21252C',
    'white': '#dad7d0',
    'light': '#FF7D00',
    'red': '#d7263d',  # High
    'blue': '#087E8B',  # Low
    'dblue': '#02182B',  # Toned
    'lblue': '#0197F6',  # Toned
}

graph_custom = dict(
    yaxis=dict(
        gridcolor=palette['white'],
        gridwidth=1,
        showgrid=True,
    ),
    font=dict(
        family="Open Sans",
        color="white",
    ),
    paper_bgcolor=palette['black'],
    plot_bgcolor=palette['black'],
    hovermode='closest',
    autosize=True,
    showlegend=False,
)
