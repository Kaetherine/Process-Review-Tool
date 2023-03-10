import base64
import datetime
import io
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import pandas as pd
import plotly.graph_objs as go
from controller import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = {}
options = []
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Div([
            html.Label('Select columns'),
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': opt, 'value': opt} for opt in options],
                value=options[0],
                multi=True
            ),
            ],style={'width': '20%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Checklist(
                id='selection',
                options=[{'label': opt, 'value': opt} for opt in options],
                value=options
            ),
            ]),

        html.Button('Submit', id='submit', n_clicks=0),
        html.Div(dcc.Input(id='input-on-submit', type='text')),
        dcc.Graph(id="MyGraph")
    ]
)


@app.callback(
    Output("selection", "options"),
    [Input("upload-data", "contents"),
     Input("upload-data", "filename")]
)
def update_df(contents, filename):
    global df
    global options
    opts = [' ']
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        options = list(df.columns)
        print(options)
        opts = [{'label': opt, 'value': opt} for opt in options]
    return opts

@app.callback(
    Output('MyGraph', 'figure'),
    Input('submit', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_graph(a, b):
    global df
    if len(df) > 0:
        fig = gen_sankey(df, cols=['CPU', 'GPU', 'RAM', 'gb memory'], value_cols='Price')
        return fig
    fig = go.Figure()
    return fig


def parse_data(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if "xlsx" in filename:
            return pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return None


"""
@app.callback(
    Output("MyGraph", "figure"),
    [Input("submit-selection", "contents")]
)
def update_graph():
    global df
    if len(df) > 0:
        fig = gen_sankey(df, cols=['CPU', 'GPU', 'RAM', 'gb memory'], value_cols='Price')
        return fig
    fig = go.Figure()
    return fig
"""


if __name__ == '__main__':
    app.run_server(debug=True)
