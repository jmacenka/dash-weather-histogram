import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from random import randint

def Footer(
    id:str='footer',
    footer_text:str=None,
    className:str='text-muted text-center border-top pt-4',
    children:list=list(),
):
    return  html.Footer(
        id='footer-information',
        className=className,
        children=[
            footer_text,
        ] + children
    )