import plotly.express as px

def make_graph(df, x_axis=None, location_name=None):
    year = df.index[0].year
    if x_axis is None:
        x_axis = df.columns[0]
    graph = px.histogram(df, x=x_axis, title=f'Temperaturverteilung über Stunden für "{location_name}" in {year}',opacity=0.8,)
    return graph