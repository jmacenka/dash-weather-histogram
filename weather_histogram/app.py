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
import os, io, base64
import pandas as pd
from flask import Flask
from random import randint
from datetime import datetime
from functools import lru_cache

# Import custom modules
from settings import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from weather_api.API import fetch_data, query_location, API_INFO_URL
from plotly_graph_renderers import hist as pgr_hist
from components.Header import Header, Header_callbacks
from components.Options import Options
from components.Results import Results
from components.Footer import Footer

# Server settings
FRAMEWORK_STYLESHEETS = [
    dbc.themes.GRID,
    dbc.themes.SPACELAB,
]

# Server initialization
# loadup local .env if not started from docker
server = Flask(__name__)

server.secret_key = os.environ.get('WEATHER_APP_SECRET_KEY', str(randint(0, 10000000000)))
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
content_children = [        
        Header(
            title_text='App für Temperaturhäufigkeit nach Ort',
            
            description_markdown=f"""
            Mit dieser Applikation kannst du nach den stündlichen Temperaturwerten für einen beliebigen Ort und ein
            beliebiges Jahr suchen.
            Die Daten werden dann von [Wetter-Datenbank]({API_INFO_URL}) geladen und stundengenau nach Häufigkeit aufbereitet.
            Anschließend können die Daten visuell analysiert und in tabellenform heruntergeladen werden.
            
            Als Standard verwendet die App einen kostenfreien API-Key für die Wetter-Datenbank von Jan Macenka, der 500 Wetter-Abfragen pro Tag zulässt.
            Wenn diese Erschöpft sind, muss bis zum nächsten Tag gewartet werden.
            
            Gib zunächst einen Ortsname im Suchfeld links ein, dann überprüfe ob der gefundene Ort korrekt ist. Wenn ja, clicke auf Daten laden.
            """,
            
            repo_link='https://github.com/jmacenka/dash-weather-histogram',
        ),
        
        Options(
            id='options',
            className='container p-2 rounded'
        ),
        
        Results(
            id='results',
        ),
        
        Footer(
            id='footer',
            footer_text='App by Jan Macenka - 2020-04-11',
        ),
    ]

if datetime.now() >= datetime(year=2020, month=6, day=8):
    content_children[1] = html.H1(
        id='outdated-message',
        children=[f'Der Kostenlose Probe-Datenbank-Zugang für die Wetterdaten war begrenzt bis "08 Jun, 2020" und ist abgelaufen. Wenn du die App weiterhin verwenden willst, melde dich bei Jan Macenka.'],        
    )

app.layout = dbc.Jumbotron(
    id='root',
    className='container my-5',
    children=content_children,
)  

# Callback deffinition

# Input to first API Pull
@app.callback(
    [Output('options-search-output','value'),
    Output('options-search-output','disabled'),
    Output('options-search-button','disabled'),
    Output('options-search-button','outline'),
    Output('google-iframe','hidden'),
    Output('google-iframe','src'),],
    [Input('options-search-input','value'),],
)
def search_input_to_location(weather_location_value):
    if weather_location_value is None:
        return [' ', True, True, True, True, None]
    elif len(weather_location_value) < 4:
        return [' ', True, True, True, True, None]
    location, maps_url = query_location(
        api_key=os.environ.get('WEATHER_APP_REMOTE_API_KEY'),
        search_location=str(weather_location_value),
    )
    if location is None:
        return ['Nichts gefunden', True, True, True, True, None]
    else:
        return [location, False, False, False, False, maps_url]

# Update all outputs after request
@lru_cache(maxsize = 4096)
@app.callback(
    [Output('results','children'),], 
    [Input("options-search-button", "n_clicks"),],
    [State("options-search-input", "value"),
    State('options-search-output','value'),]
)
def input_triggers_nested(n_clicks, weather_location_value, found_location):    
    if weather_location_value is None:
        raise PreventUpdate
    
    df_weather_data = fetch_data(
        api_key=os.environ.get('WEATHER_APP_REMOTE_API_KEY'),
        search_location=str(weather_location_value),
        year=2019,
        tp=1,
    )
    
    location, maps_url = query_location(
        api_key=os.environ.get('WEATHER_APP_REMOTE_API_KEY'),
        search_location=str(weather_location_value),
    )
    
    df_metadata = pd.DataFrame(
        {
            'Beschreibung':[f'Die Wetterdaten wurde über folgende API bezogen: {API_INFO_URL}'],
            'Erstelldatum in utc+0':[str(datetime.now().strftime('%d.%m.%Y, %H:%M'))],
            'Suchbegriff':[str(weather_location_value)],
            'Gefundener Ort':[str(found_location)],
        }
    ).T
    
    df_count = df_weather_data[df_weather_data.columns[0]].value_counts().to_frame().reset_index()
    df_count.columns = ['Temperatur °C','Stunden im Jahr']
    
    xlsx_io = io.BytesIO()
    with pd.ExcelWriter(xlsx_io, engine='xlsxwriter') as writer:
        df_weather_data.to_excel(writer, sheet_name=weather_location_value)
        df_count.to_excel(writer, sheet_name='Jahresverteilung')
        df_weather_data.describe().to_excel(writer, sheet_name='Analyse')
        df_metadata.to_excel(writer, sheet_name='Metadaten')
    xlsx_io.seek(0)
    # https://en.wikipedia.org/wiki/Data_URI_scheme
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    data = base64.b64encode(xlsx_io.read()).decode("utf-8")
    href_data_downloadable = f'data:{media_type};base64,{data}'
    
    results =  html.Div(
        id=f'{id}-display',
        className='card py-5 px-2',
        children=[
            # html.H1(
            #     id='headline',
            #     className='text-center text-muted',
            #     children=found_location,
            # ),
            dcc.Graph(
                id='graph',
                figure=pgr_hist.make_graph(df=df_weather_data,location_name=location),
                # figure=pgr_hist.make_graph([df_weather_data])
            ),
            dash_table.DataTable(
                columns=[{'name': i, 'id': i} for i in df_weather_data.describe().reset_index().columns],
                data=df_weather_data.describe().reset_index().to_dict('records'),
            ),
            html.A(
                id='excel-download',
                download=f"{datetime.now().strftime('%Y%m%d%H%m')}_Wetterdaten_{found_location.replace('>','_').replace(' ','')}.xlsx",
                href=href_data_downloadable,
                target="_blank",
                className='centered',
                children=[
                    dbc.Button(
                        id='excel-download-button',
                        className='col-12 shadow-none',
                        color='primary',
                        children=['Als EXCEL-Datenblatt herunterladen']
                    ),
                    
                ],
            ),
            dash_table.DataTable(
                columns=[{'name': i, 'id': i} for i in df_count.reset_index().columns],
                data=df_count.reset_index().to_dict('records'),
            ),
        ],
    )
    
    return [results,]

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
        app.server.run(host='0.0.0.0',debug=False, port=int(os.environ.get('WEATHER_APP_CONTAINER_EXPOSED_PORT',8050)), threaded=True)
