import dash
import dash_core_components as dcc
import dash_html_components as html
from urllib.parse import urlparse, parse_qsl, urlencode
from dash.dependencies import Input, Output

app = dash.Dash()

app.config.suppress_callback_exceptions = True


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-layout')
])


def apply_default_value(params):
    def wrapper(func):
        def apply_value(*args, **kwargs):
            if 'id' in kwargs and kwargs['id'] in params:
                kwargs['value'] = params[kwargs['id']]
            return func(*args, **kwargs)
        return apply_value
    return wrapper


def build_layout(params):
    layout = [
        html.H2('URL State demo', id='state'),
        apply_default_value(params)(dcc.Dropdown)(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
            value='LA'
        ),
        apply_default_value(params)(dcc.Input)(
            id='input',
            placeholder='Enter a value...',
            value=''
        ),
        apply_default_value(params)(dcc.Slider)(
            id='slider',
            min=0,
            max=9,
            marks={i: 'Label {}'.format(i) for i in range(10)},
            value=5,
        ),
        html.Br(),
    ]

    return layout


def parse_state(url):
    parse_result = urlparse(url)
    params = parse_qsl(parse_result.query)
    state = dict(params)
    return state


@app.callback(Output('page-layout', 'children'),
              inputs=[Input('url', 'href')])
def page_load(href):
    if not href:
        return []
    state = parse_state(href)
    return build_layout(state)


component_ids = [
    'dropdown',
    'input',
    'slider'
]


@app.callback(Output('url', 'search'),
              inputs=[Input(i, 'value') for i in component_ids])
def update_url_state(*values):
    state = urlencode(dict(zip(component_ids, values)))
    return f'?{state}'


if __name__ == '__main__':
    app.run_server(debug=True, port=8070)