import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from random import randint

class Title(id=randint(1000,9999),**kwargs):
    def __init__(self):
        self.id = id
        self.className = kwargs.get('className',None)
        self.custom_style = kwargs.get('custom_style',None)
        self.title_text = kwargs.get('title_text',None)
        self.children = kwargs.get('children',list())
        
    def __repr__(self):
        return f'Component: Title; Id: "{self.id}"'

    def get_component_layout(self):
        f"""
        get_component_layout generates the component layout        
        Returns:
            dash.html -- id = {self.id}
        """
        component_layout = html.Div(
            id=self.id,
            className=self.className,
            custom_style=self.custom_style,
            children=[
                self.title_text,
                
            ],
        )
        
        return component_layout
        