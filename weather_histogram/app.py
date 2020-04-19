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
from settings import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from weather_api.API import fetch_data, query_location, API_INFO_URL
from plotly_graph_renderers import hist as pgr_hist
from components.Header import Header, Header_callbacks
from components.Options import Options
from components.Results import Results

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

server.secret_key = os.environ.get('WEATHER_APP_SECRET_KEY', str(randint(0, 100000000000)))
app = dash.Dash(
    __name__, 
    external_scripts=EXTERNAL_SCRIPTS,
    external_stylesheets=FRAMEWORK_STYLESHEETS+EXTERNAL_STYLESHEETS,
    include_assets_files=True, 
    server=server
)
app.title = 'Temperaturhäufigkeit'
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# Helper functions

# Application layout
app.layout = dbc.Jumbotron(
    id='root',
    className='container my-5',
    children=[
        
        Header(
            title_text='App für Temperaturhäufigkeit nach Ort',
            
            description_markdown=f"""
            Mit dieser Applikation kannst du nach den stündlichen Temperaturwerten für einen beliebigen Ort und ein
            beliebiges Jahr suchen.
            Die Daten werden dann von [Wetter-Datenbank]({API_INFO_URL}) geladen und in stündliche Werte aufbereitet.
            Anschließend können die Daten visuell analysiert und in tabellenform heruntergeladen werden.
            
            Als Standard verwendet die App einen kostenfreien API-Key für die Wetter-Datenbank von Jan Macenka, der 500 Wetter-Abfragen pro Tag zulässt.
            Wenn diese Erschöpft sind, muss bis zum nächsten Tag gewartet werden.
            
            Gib zunächst einen Ortsname im Suchfeld links ein, dann überprüfe ob der gefundene Ort korrekt ist. Wenn ja, clicke auf Daten laden.
            """,
        ),
        
        Options(
            id='options',
            className='container p-2 rounded'
        ),
        
        Results(
            id='results',
        ),
        
    ],
)

# Callback deffinition

# Input to first API Pull
@app.callback(
    [Output('options-search-output','value'),
    Output('options-search-button','disabled')],
    [Input('options-search-input','value'),],
)
def search_input_to_location(weather_location_value):
    if weather_location_value is None:
        return [' ', True]
    elif len(weather_location_value) < 4:
        return [' ', True]
    location = query_location(
        api_key=os.environ.get('WEATHER_APP_REMOTE_API_KEY'),
        search_location=str(weather_location_value),
    )
    if location is None:
        return [' ', True]
    else:
        return [location, False]

# Update all outputs after request
@lru_cache(maxsize = 4096)
@app.callback(
    [Output('results','children'),], 
    [Input("options-search-button", "n_clicks"),],
    [State("options-search-input", "value")]
)
def input_triggers_nested(n_clicks, weather_location_value):    
    if weather_location_value is None:
        raise PreventUpdate
    
    df_weather_data = fetch_data(
        api_key=os.environ.get('WEATHER_APP_REMOTE_API_KEY'),
        search_location=str(weather_location_value),
        year=2019,
        tp=1,
    )
        
    result_tabs =   dbc.Tabs(
        className='justify-content',
        children=[
            dbc.Tab(
                className='card py-5 px-2',
                id=f'{id}-tab-graph',
                label='Graph',
                children=[
                    dcc.Graph(
                        id='graph',
                        figure=pgr_hist.make_graph(df=df_weather_data),
                    ),
                ],
            ),
            dbc.Tab(
                className='card py-5 px-2',
                id=f'{id}-tab-analysis',
                label='Analysis',
                children=[
                    dash_table.DataTable(
                        columns=[{'name': i, 'id': i} for i in df_weather_data.describe().reset_index().columns],
                        data=df_weather_data.describe().reset_index().to_dict('records'),
                    ),
                ],
            ),
            dbc.Tab(
                className='card py-5 px-2',
                id=f'{id}-tab-data',
                label='Data',
                children=[
                    dash_table.DataTable(
                        columns=[{'name': i, 'id': i} for i in df_weather_data.reset_index().columns],
                        data=df_weather_data.reset_index().to_dict('records'),
                    ),
                ],
            ),
        ],
    ),
    
    
    return result_tabs

# Toogle app-information-modal
@app.callback(
    Output("app-information-modal", "is_open"),
    [Input("open-modal-app-information", "n_clicks"), 
    Input("close-modal-app-information", "n_clicks"),],
    [State("app-information-modal", "is_open"),],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# App launcher
if __name__ == '__main__':
    if not os.environ.get('LAUNCHED_FROM_DOCKER_COMPOSE',False):
        app.run_server(debug=True, port=8055)
    else:
        app.server.run(host='0.0.0.0',debug=True, port=int(os.environ.get('WEATHER_APP_CONTAINER_EXPOSED_PORT',8050)), threaded=True)