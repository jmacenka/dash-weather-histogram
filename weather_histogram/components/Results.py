import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from random import randint

def Results(
        id:str='results',
        className:str=None,
        loading_icon_type:str='default',
        children:list=list(),
        **kwargs,
    ):
    return dcc.Loading(
        id=f'{id}-loading',
        className='m-5',
        type=loading_icon_type,
        children=[
            html.Div(
                id=id,
                className=className,
                children=children,
            ),
        ],
    )


# html.Div(
#     children=[
#         dcc.Loading(
#             id=f"{id}-loading", 
#             type="default",
#             children=[
#                 html.Div(
#                     id=f"{ids[1]}-1"
#                 ),
#             ], 
#         ),
#         html.Div(
#             id=id,
#             className=className,
#             children=children,
#         )
#     ],
# )