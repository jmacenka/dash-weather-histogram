import pandas as pd
import plotly.graph_objects as go

def make_graph(list_of_display_data:list=[(pd.DataFrame(), x_data_columns=[None]),]:
    """Requires list of tuples with tuple containing (df, list_of_columns_to_display)
    with list_of_columns_to_display as list of df_column_names as strings"""
    fig = go.Figure()
    for df, x_data_columns in list_of_display_data:
        year = df.index[0].year
        if x_data_columns is None:
            x_data_columns = df.columns[0]
        for col in x_data_columns:
            fig.add_trace(go.Histogram(x=df[col], title=f'{year} - {col}')               
    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)
    return fig
