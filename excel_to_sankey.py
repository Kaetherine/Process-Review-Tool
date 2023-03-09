import base64
import io

from dash import Dash, dcc, html, Input, Output, dash_table
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__)

app.layout = html.Div([
    html.H2(
        'mäander',
        style={
            'color': '#757575',
            'margin-left': '5%',
            'margin-top': '3%',
            # 'font-family': 'Arial',
        }
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '90%',
            'height': '5%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin-left': '5%'
                },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    dcc.Dropdown(
        value='Borough',
        id='demo-dropdown',
        style = {
        'margin-top': '1.8%',
        'margin-left': '2.5%',
        'width': '95%',
        },
        multi=True,
        placeholder='Select the columns you want to visualize'
    ),
    html.Div(id='dd-output-container'),
    dcc.Graph(
        id="graph",
        # set the initial figure to an empty Sankey diagram
        figure={'data': [], 'layout': {'title': 'Sankey Diagram'}}
    ),
])

@app.callback(
    Output('graph', 'figure'),
    Input('demo-dropdown', 'value'),
    State('output-data-upload', 'children'),
    State('output-data-upload', 'filename'),
    State('output-data-upload', 'last_modified')
)
def update_figure(selected_cols, list_of_contents, list_of_names, list_of_dates):
    df = pd.DataFrame()
    if list_of_contents:
        for c, n in zip(list_of_contents, list_of_names):
            content_type, content_string = c.split(',')
            decoded = base64.b64decode(content_string)
            try:
                if 'csv' in n:
                    # Assume that the user uploaded a CSV file
                    df_file = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                elif 'xls' in n:
                    # Assume that the user uploaded an excel file
                    df_file = pd.read_excel(io.BytesIO(decoded))
                df = pd.concat([df, df_file])
            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error processing this file.'
                ])
    # generate the Sankey diagram using the selected columns
    data = generate_sankey(df, selected_cols)
    # create a plotly figure object
    fig = {'data': [data], 'layout': {'title': 'Sankey Diagram'}}
    return fig


def generate_sankey(df, cols):
    nodes = []
    link_sources = []
    link_targets = []
    link_values = []
    for col in cols:
        nodes.extend(df[col].unique())
        for i in range(len(df[col])-1):
            link_sources.append(df[col][i])
            link_targets.append(df[col][i+1])
            link_values.append(1)
    nodes = list(set(nodes))
    data = dict(
        type='sankey',
        node=dict(
          pad=15,
          thickness=20,
          line=dict(color="black", width=0.5),
          label=nodes
        ),
        link=dict(
          source=link_sources,
          target=link_targets,
          value=link_values
        ),
    )
    return data

# def parse_contents(contents, filename, date):
#     content_type, content_string = contents.split(',')

#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])
    
#     dropdown_options = [
#         {'label': col, 'value': col} for col in df.columns
#         ]
#     return html.Div([
#         dcc.Dropdown(
#             value='Borough',
#             # disabled = 'False',
#             search_value = '',
#             clearable = True,
#             id='demo-dropdown',
#             style = {
#             'margin-top': '1.8%',
#             'margin-left': '2.5%',
#             'width': '95%',
#             },
#             options=dropdown_options,
#             multi=True,
#             placeholder='Select the columns you want to visualize'
#         ),
#         html.Div(id='dd-output-container'),
#         dcc.Graph(
#             id="graph",
#             # set the initial figure to an empty Sankey diagram
#             figure={'data': [], 'layout': {'title': 'Sankey Diagram'}}
#         ),
#     ])

# @app.callback(
#     Output('graph', 'figure'),
#     Input('demo-dropdown', 'value'),
# )
# def update_figure(selected_cols):
#     # generate the Sankey diagram using the selected columns
#     data = generate_sankey(df, selected_cols)
#     # create a plotly figure object
#     fig = {'data': [data], 'layout': {'title': 'Sankey Diagram'}}
#     return fig

if __name__ == '__main__':
    app.run_server(debug=True)

# app.run_server(debug=True)