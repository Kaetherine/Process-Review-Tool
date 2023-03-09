from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import json, urllib

app = Dash(__name__)


app.layout = html.Div(className='app-body', children=[
    # Header
    html.Div(className="row", children=[
        html.Div(className='twelve columns', children=[
            html.Div(style={'float': 'left', 'margin-left': '10px'}, children=[
                    html.H1('Hello Kaetherine'),
                    html.H4('Process Review Dashboard')
                ]
            ),
            html.Div(style={'float': 'right'}, children=[
                html.A(
                    html.Img(
                        src=app.get_asset_url("logo.png"),
                        style={'float': 'right', 'height': '75px'}
                    ),
                    href="https://www.hwr-berlin.de/")
            ]),
        ]),
    ]),
    # Controls
    html.Div(className="row", id='control-panel', children=[
        html.Div(className="four columns pretty_container", children=[
            html.Label('Sankey Opacity'),
            dcc.Slider(id='slider', min=0, max=1, value=0.5, step=0.1)

        ]),
        html.Div(className="four columns pretty_container", children=[
            html.Label('Dropdown Placeholder'),
            dcc.Dropdown(id='days',
                         placeholder='Select a value',
                         options=[{'label': 'Val1', 'value': 0},
                                  {'label': 'Val2', 'value': 1},
                                  {'label': 'Val3', 'value': 2},
                                  {'label': 'Val4', 'value': 3},
                                  {'label': 'Val5', 'value': 4},
                                  {'label': 'Val6', 'value': 5},
                                  {'label': 'Val7', 'value': 6}],
                         value=[],
                         multi=True),
        ]),
        html.Div(className="four columns pretty_container", children=[
            html.Label('Placeholder'),
            html.P('Placeholder')
        ]),
    ]),

    # Content
    dcc.Tabs(id='tab', className='tabs', children=[
        dcc.Tab(label='Tab One', children=[
            html.Div(className="row", children=[
                html.Div(className="eight columns pretty_container", children=[
                    html.H6(f'Graph Titel'),
                    dcc.Graph(id="graph")
                ]),
                html.Div(className="four columns pretty_container", children=[
                    html.P('placeholder'),
                ])
            ]),
            html.Div(className="row", children=[
                html.Div(className="fix columns pretty_container", children=[
                    html.P('placeholder')
                ]),
                html.Div(className="fix columns pretty_container", children=[
                    html.P('placeholder')
                ]),
            ]),
        ]),
        dcc.Tab(label='Tab Two', children=[
            html.Div(className="row", children=[
                html.Div(className="seven columns pretty_container", children=[
                    html.P('placeholder')
                ]),
                html.Div(className="five columns pretty_container", children=[
                    html.P('placeholder')
                ])
            ]),
            html.Div(className="row", children=[
                html.Div(className="seven columns pretty_container", children=[
                    html.P('placeholder')
                ]),
                html.Div(className="five columns pretty_container", children=[
                    html.P('placeholder')
                ])
            ]),
        ]),
    ]),
    html.Hr()
])


@app.callback(
    Output("graph", "figure"),
    Input("slider", "value"))
def display_sankey(opacity):
    url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read()) # replace with your own data source

    node = data['data'][0]['node']
    node['color'] = [
        f'rgba(255,0,255,{opacity})'
        if c == "magenta" else c.replace('0.8', str(opacity))
        for c in node['color']]

    link = data['data'][0]['link']
    link['color'] = [
        node['color'][src] for src in link['source']]

    fig = go.Figure(go.Sankey(link=link, node=node))
    fig.update_layout(font_size=10)
    return fig


app.run_server(debug=True)
