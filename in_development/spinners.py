# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
import time

from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H3("Edit text input to see loading state"),
        dcc.Input(
            id="loading-input", 
            value='Input triggers local spinner'
        ),
        dcc.Loading(
            id="loading",
            type="default",
            children=[
                html.Div(
                    id="loading-output"
                ),
            ],
        ),
    ],
)

@app.callback(
    Output("loading-output", "children"), 
    [Input("loading-input", "value"),]
)
def input_triggers_spinner(value):
    time.sleep(1)
    return value


if __name__ == "__main__":
    app.run_server(debug=False)