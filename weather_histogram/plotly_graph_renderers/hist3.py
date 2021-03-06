import plotly.graph_objects as go

def make_graph(df, x_data_columns=None):
    """Requires list of tuples with tuple containing (df, list_of_columns_to_display)
    with list_of_columns_to_display as list of df_column_names as strings"""
    fig = go.Figure()
    year = df.index[0].year
    if x_data_columns is None:
        x_data_columns = df.columns[0]
    for col in x_data_columns:
        fig.add_trace(go.Histogram(x=df[col], title=f'{year} - {col}'))               
    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)
    fig.title(f'Temperaturverteilung nach Stunden für {year}')
    return fig
