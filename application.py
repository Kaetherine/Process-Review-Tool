import base64
import io
from dash import dcc, html, Input, Output, Dash
from create_sankey_diagram import *
from functools import partial

app = Dash(__name__) 

app.layout = html.Div(
    
    className='app-body', children=[
        html.Img(
        src='assets\logo.png',
        alt='PwC Logo',
        style={'width':'160px',
                'position': 'fixed',
                'top': '2%',
                'right': '4.2%',
                }
            ),
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
            style={
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin-bottom': '9px',
            },
            multiple=True,
        ),
        html.Div(className='row', children=[
            html.Div(
                [html.Label('Select columns'),
                 dcc.Dropdown(
                    id='selection-source',
                    multi=True,
                    placeholder='Select the columns you want to visualize',
                    value=[]
                ),
                 ],
                id='selection-source-container',
                className='twelve columns pretty_container'
            ),
        ]),
        html.Div(className='row', children=[
            html.Div(
                [html.Label(
                    f'Filter by'
                    ),
                dcc.Dropdown(
                    id=f'selection-target{count}',
                    multi=True,
                    placeholder='Select the row values you want to include',
                    value=[]
                ),
                ],
                id=f'selection-target-container{count}',
                className='two columns pretty_container'
            ) for count in range(7)
        ]),
        dcc.Graph(
        id='sankey',
        style={'height': '65vh'}
        ),
              dcc.Store(id='store'),
              dcc.Store(id='filename-store'),
              dcc.Store(id='selected-columns-store'),
    ]
)

@app.callback(
    Output('store', 'data'),
    Output('filename-store', 'data'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')]
)
def upload_callback(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        return df.to_json(date_format='iso', orient='split'), filename  # convert df to json


@app.callback(
    Output('selection-source', 'options'),
    [Input('store', 'data')]
)
def available_options_changed_callback(data):
    df = pd.read_json(data, orient='split') if data else pd.DataFrame()
    available_columns = list(df.columns)
    opts = [{'label': opt, 'value': opt} for opt in available_columns]
    return opts

@app.callback(
    Output('selected-columns-store', 'data'),
    [Input('selection-source', 'value')]
)
def selected_columns_changed_callback(value):
    '''create diagram only if at least two columns are selected'''
    return value

def show_target_options_changed_callback(index, style, data, selected_columns):
    df = pd.read_json(data, orient='split') if data else pd.DataFrame()
    if index >= len(selected_columns):
        return []
    column_values = df[selected_columns[index]].unique()
    opts = [{'label': opt, 'value': opt} for opt in column_values]
    return opts

for i in range(7):
    app.callback(
        Output(f'selection-target{i}', 'options'),
        [Input(f'selection-target-container{i}', 'style'),
        Input('store', 'data'),
        Input('selected-columns-store', 'data')]
    )(partial(show_target_options_changed_callback, i))

@app.callback(
    Output('sankey', 'figure'),
    [Input('store', 'data'),
     Input('filename-store', 'data'),
     Input('selected-columns-store', 'data')] +
    [Input(f'selection-target{i}', 'value') for i in range(7)]
)
def update_graph(data=None, filename=None, selected_columns = None, *filters):
    df = pd.read_json(data, orient='split') if data else pd.DataFrame()
    if filters == ([], [], [], [], [], [], []):
        filters = None
    if not selected_columns:
        try:
            selected_columns = list(df.columns)
        except Exception as e:
            print(e)

    title = 'Sankey Diagram'
    if not df.empty:
        title = filename
    fig = gen_sankey(
            df, selected_columns=selected_columns, filter=filters, linear=True, title=title
            )
    return fig

def parse_data(contents, filename):
    content_string = contents.split(',')[1]
    decoded = base64.b64decode(content_string)
    try:
        if "xlsx" in filename:
            df = pd.read_excel(io.BytesIO(decoded))
            df.name = filename
            return df
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])


# application = app.server

if __name__ == '__main__':
    app.run(debug=True)