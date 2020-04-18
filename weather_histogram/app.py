# -*- coding: utf-8 -*-
# Import main framework modules
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

# Import helper modules
import os
from flask import Flask
from functools import lru_cache

# Import custom modules
from settings import EXTERNAL_STYLESHEETS
from weather_api.API import fetch_data
from plotly_graph_renderers import hist as pgr_hist
from components.Title import Title
from components.Options import Options

# Server settings
FRAMEWORK_STYLESHEETS = [
    dbc.themes.GRID,
    dbc.themes.MATERIA,
]

# Server initialization
# loadup local .env if not started from docker
server = Flask(__name__)
if not os.environ.get('LAUNCHED_FROM_DOCKER_COMPOSE',False):
    from random import randint
    from dotenv import load_dotenv
    load_dotenv(server.root_path)

server.secret_key = os.environ.get('COVID_APP_SECRET_KEY', str(randint(0, 100000000000)))
app = dash.Dash(
    __name__, 
    external_stylesheets=FRAMEWORK_STYLESHEETS+EXTERNAL_STYLESHEETS,
    include_assets_files=True, 
    server=server
)
app.title = 'Historic weather App'
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# Application layout
app.layout = dbc.Jumbotron(
    id='root',
    children=[
        Title(id='title',title_text='Test'),
        Options(),
        html.Div(id='results'),
    ],
)

# Callback deffinition
@lru_cache(maxsize = 4096)
@app.callback(
    [Output("output-2", "children"),
    Output('results','children')], 
    [Input("input-weather-location", "value")],
)
def input_triggers_nested(weather_location_value):
    
    if weather_location_value is None:
        raise PreventUpdate
    
    df_weather_data, response_city = fetch_data(
        api_key=os.environ.get('WEATHER_APP_REMOTE_API_KEY'),
        search_location=str(weather_location_value),
        year=2019,
        tp=1,
    )
    fig_weather = pgr_hist.make_graph(df=df_weather_data)
    response_text = f'Displaying Data for: {response_city}'

    graph = dcc.Graph(
        id='graph',
        figure=fig_weather,
    )
    
    data_table = dash_table.DataTable(
        columns=[{'name': i, 'id': i} for i in df_weather_data.reset_index().columns],
        data=df_weather_data.reset_index().to_dict('records'),
    )
    
    return (response_text, [graph, data_table])

# App launcher
if __name__ == '__main__':
    if not os.environ.get('LAUNCHED_FROM_DOCKER_COMPOSE',False):
        app.run_server(debug=True, port=8055)
    else:
        app.server.run(host='0.0.0.0',debug=True, port=int(os.environ.get('WEATHER_APP_CONTAINER_EXPOSED_PORT',8050)), threaded=True)