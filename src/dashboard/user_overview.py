import numpy as np
import plotly.graph_objects as go

from src.palette import palette, graph_custom


def generate_user_overview(data, users):

    # generate an array of rainbow colors by fixing the saturation and lightness of the HSL
    # representation of colour and marching around the hue.
    # Plotly accepts any CSS color format, see e.g. http://www.w3schools.com/cssref/css_colors_legal.asp.
    c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, len(users))]

    # Each box is represented by a dict that contains the data, the type, and the colour.
    # Use list comprehension to describe N boxes, each with a different colour and with different randomly generated data:
    fig = go.Figure(data=[go.Box(y=data[user], name=user, marker_color=c[ind]) for ind, user in enumerate(users)])

    # format the layout
    fig.update_layout(**graph_custom)
    fig.update_layout(
        yaxis_title='Vote',
        font=dict(family="Open Sans", color=palette['light'], size=18),
        margin=dict(l=50, b=50, t=20, r=50),
    )

    return fig
