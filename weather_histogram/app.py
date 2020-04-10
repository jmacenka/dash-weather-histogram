# -*- coding: utf-8 -*-
import os

from flask import Flask

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.exceptions import PreventUpdate

from dash.dependencies import Input, Output, State

# loadup .env
server = Flask(__name__)
if not os.environ.get('LAUNCHED_FROM_DOCKER_COMPOSE',False):
    from dotenv import load_dotenv
    load_dotenv(os.path.join(server.root_path,'..'))

from weather_api.API import fetch_data
from plotly_graph_renderers import hist as pgr_hist


app = dash.Dash(server=server)

app.scripts.config.serve_locally = True

app.layout = html.Div(
    className='container',
    children=[
        dcc.Loading(id="loading-1", children=[html.Div(id="output-1")], type="default"),
        html.Div(
            [
                dcc.Loading(
                    id="loading-2",
                    children=[html.Div([html.Div(id="output-2")])],
                    type="circle",
                ),
                dcc.Input(id="input-weather-location", placeholder="Input some place to fetch data for... e.G. Munich", debounce=True),
            ]
        ),
        html.Div(
            id='results',
        ),
    ],
)

@app.callback([Output("output-2", "children"),Output('results','children')], [Input("input-weather-location", "value")])
def input_triggers_nested(weather_location_value):
    
    if weather_location_value is None:
        raise PreventUpdate
    
    df_weather_data, response_city = fetch_data(
        api_key=os.environ.get('WEATHER_APP_REMOTE_API_KEY'),
        search_location=str(weather_location_value),
        year=2019,
        tp=24,
    )
    
    #fig_weather = pgr_hist.make_graph(df=df_weather_data, x='avgtempC')
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

    #sumary_df = df_weather_data.groupby(['avgtempC', 'maxtempC','mintempC']).size().to_frame(name='counts')
    sumary_df = df_weather_data['avgtempC'].value_counts(dropna=False).to_frame().reset_index().rename(columns={"index": "°C", "avgtempC": "Anzahl Tage"})
    #sumary_df = sumary_df['°C'].astype(int).to_dict().sort_values(by=['°C']) # Funktioniert so noch nicht!

    sumary_table = dash_table.DataTable(
        columns=[{'name': i, 'id': i} for i in sumary_df.columns],
        data=sumary_df.to_dict('records'),
    )
    
    return (response_text, [graph, sumary_table, data_table])


if __name__ == "__main__":
    app.run_server(debug=False)