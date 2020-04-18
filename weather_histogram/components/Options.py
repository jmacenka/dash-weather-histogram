import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from random import randint

def Options(
    ids:list=['loading','output'],
):
    return html.Div(
        className='container',
        children=[
            dcc.Loading(
                id=f"{ids[0]}-1", 
                type="default",
                children=[
                    html.Div(
                        id=f"{ids[1]}-1"
                    ),
                ], 
            ),
            html.Div(
                [
                    dcc.Loading(
                        id=f"{ids[0]}-2",
                        type="circle",
                        children=[
                            html.Div(
                                children=[
                                    html.Div(
                                        id=f"{ids[1]}-2"
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dcc.Input(id="input-weather-location", placeholder="Input some place to fetch data for... e.G. Munich", debounce=True),
                ]
            ),
        ],
    )