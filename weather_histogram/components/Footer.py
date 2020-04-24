import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from random import randint

def Footer(
    id:str='footer',
    footer_text:str=None,
    footer_repo_link:str=None,
    className:str='text-muted text-center border-top pt-4',
    children:list=list(),
    **kwargs,
):
    
    footer_children = [footer_text,]
    if not footer_repo_link is None:
        footer_children.append(
            dcc.Link(
                id='github-repo-link',
                href=footer_repo_link,
                children=[
                    'App source code',
                    ],
                )
        )
    footer_children.append(children)
    
    return  html.Footer(
        id='footer-information',
        className=className,
        children=footer_children,
    )
