import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from random import randint

def Title(
        id:str=str(randint(1000,9999)),
        className:str=None,
        title_text:str=None,
        children:list=list(),
        **kwargs,
    ):
    return html.Div(
        id=id,
        className=className,
        children=[
            title_text,
        ] + children,
    )