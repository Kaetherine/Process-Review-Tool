from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

df = pd.read_excel('Sample_Data_Set.xlsx')

app = Dash(__name__)

app.layout = html.Div([
    html.H2(
        'Process Review Tool',
        style={
            'color': '#757575',
            'margin-left': '5%',
            'margin-top': '5%',
            'font-family': 'Helvetica Neue',
        }
    ),
    dcc.Dropdown(
        style = {
            'margin-top': '1.8%',
            'margin-left': '2.5%',
            'width': '95%',
        },
        id='df-dropdown',
        options=[{'label': i, 'value': i} for i in df.columns.unique()],
        multi=True, 
        placeholder='Select the columns you want to visualize'
    ),
    html.Div(id='output-container'),
    dcc.Graph(id="graph",),
])

@app.callback(
    Output('graph', 'figure'),
    Input("df-dropdown", "value"))
def update_output(value):
    df['count_col'] = [f'count_{x}' for x in range(len(df))]
    columns = list(df.columns)

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

    return value

def display_sankey(value, linear = True):
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

app.run_server(debug=True)