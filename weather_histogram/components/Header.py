from random import randint
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

BUTTON_STYLE = 'btn btn-secondary text-primary'

def Header(
        id:str='title',
        className:str='text-justify text-center p-2',
        title_text:str=None,
        description_markdown:str=None,
        children:list=list(),
        **kwargs,
    ):    
    """
    Header contains some decription for the App. Also import 
    
    Keyword Arguments:
        id {str} -- Identifyer for the containing element (default: {'title'})
        className {str} -- string of bootstrap classes, separated with spaces (default: {'text-justify text-center p-2'})
        title_text {str} -- Text to be displayed in the Title (default: {None})
        description_markdown {str} -- Text formatted as Markdown to be printed below the Title (default: {None})
        children {list} -- List with Children of this element (default: {list()})
    
    Returns:
        html.H1 -- Returns a dash.html.H1
    """
    return html.Div(
        id=id,
        className=className,
        children=[
            html.H1(
                className='text-bold',
                children=[
                    title_text,
                ],
            ),
            html.Div(
                children=[
                    dbc.Button(
                        id="open-modal-app-information",
                        className=BUTTON_STYLE,
                        children=["App information"], 
                    ),
                    dbc.Modal(
                        id="app-information-modal",
                        size="lg",
                        children=[
                            dbc.ModalHeader(
                                className='lead',
                                children=["App information"],
                            ),
                            dbc.ModalBody(
                                children=[
                                    dcc.Markdown(
                                        className='py-3 px-5 text-justify text-muted',
                                        children=[
                                            description_markdown,
                                        ],
                                    ),
                                ],
                            ),
                            dbc.ModalFooter(
                                children=[
                                    dbc.Button(
                                        id="close-modal-app-information", 
                                        className=BUTTON_STYLE,
                                        children=["Ok"],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ] + children,
    )


Header_callbacks = [
    """
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
    """,
]