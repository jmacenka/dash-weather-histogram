import plotly.express as px

def make_graph(df, x_axis=None):
    if x_axis is None:
        x_axis = df.columns[0]
    return px.histogram(df, x=x_axis)