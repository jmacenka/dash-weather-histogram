import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from random import randint

BUTTON_STYLE = 'btn btn-secondary text-primary'

def Options(
        id:str='options',
        className:str='container',
    ):
    """
    Options holds all the possible Options for the UI.

    Keyword Arguments:
        ids {list} -- List of strings with IDs for the enclosed elements (default: {['options','input-weather-location']})

    Returns:
        html.Div -- Returns a dash.html.Div
    """
    return html.Div(
        id=id,
        className=className+' container',
        children=[
            html.Div(
                className='row',
                children=[
                    dbc.FormGroup(
                        className='col-md-4',
                        children=[
                            html.Label(
                                className='mx-5 align-text-bottom text-muted',
                                htmlFor=f'{id}-search-input',
                                children=['Ort-Suche'],
                            ),
                            dbc.Input(
                                id=f'{id}-search-input',
                                type='text',
                                className='text-justify bg-light p-1 border rounded m-2',
                                placeholder="Ortsname eingeben...", 
                                debounce=True,
                            ),
                        ],
                    ),
                    dbc.FormGroup(
                        className='col-md-5',
                        children=[
                            html.Label(
                                className='mx-5 align-text-bottom text-muted',
                                htmlFor=f'{id}-search-output',
                                children=['Gefundener Ort'],
                            ),
                            dbc.Input(
                                id=f'{id}-search-output',
                                type='text',
                                className='p-1 text-dark text-center align-middle border rounded m-2',
                                disabled=True,
                                value='',
                            ),
                        ],
                    ),
                    dbc.FormGroup(
                        className='col-md-2',
                        children=[
                            html.Label(
                                className='mx-5 align-text-bottom text-muted',
                                htmlFor=f'{id}-search-button',
                                children=[' '],
                            ),
                            dbc.Button(
                                id=f'{id}-search-button',
                                className='inline',
                                disabled=True,
                                color='primary',
                                children=['Daten laden'],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )