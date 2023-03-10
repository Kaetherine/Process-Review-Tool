import base64
import io

from dash import Dash, dcc, html, Input, Output, dash_table, State
#from dash.dependencies import Input, Output, State
#from dash import dcc, html, dash_table
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
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    dropdown_options = [{'label': col, 'value': col} for col in df.columns]
    return html.Div([
        dcc.Dropdown(
            id='demo-dropdown',
            style = {
            'margin-top': '1.8%',
            'margin-left': '2.5%',
            'width': '95%',
            },
            options=dropdown_options,
            multi=True,
            placeholder='Select the columns you want to visualize'
        ),
        html.Div(id='dd-output-container'),
        dcc.Graph(id="graph"),
        
  ])
@app.callback(Output('output-data-upload', 'children'),
              # Output('dd-output-container', 'children'),
              Input('upload-data', 'contents'),
              # Input('demo-dropdown', 'value'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

def display_sankey(value, linear=True):
    df = pd.DataFrame[value] # nur die ausgewählten Spalten des DataFrames verwenden
    
    df['count_col'] = [f'count_{x}' for x in range(len(df))]
    columns = list(df.columns)

    if linear:
        for col in df.columns:
            for index, value in enumerate(df[col]):
                df.at[index, col] = f'{col}: {value}'

    dfs = []
    for column in columns:
        i = columns.index(column)+1
        if column == columns[-1] or column == columns[-2] or column == 'count_col' and not column == 'color':
            continue
        else:
            try:
                dfx = df.groupby([column, columns[i]])['count_col'].count().reset_index()
                dfx.columns = ['source', 'target', 'count']
                dfs.append(dfx)
            except Exception as e:
                print(f'columnname: {column}\n{repr(e)}')

    links = pd.concat(dfs, axis=0)
    unique_source_target = list(pd.unique(links[[
        'source', 'target']].values.ravel('K')))
    mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
    links['source'] = links['source'].map(mapping_dict)
    links['target'] = links['target'].map(mapping_dict)
    links_dict = links.to_dict(orient='list')

    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = '#D04A02', width = 0.1),
        label = unique_source_target,
        color = '#D04A02'
        ),
        link = dict(
        # color = '#707070',
        source = links_dict['source'],
        target = links_dict['target'],
        value = links_dict['count'],
    ))])

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)