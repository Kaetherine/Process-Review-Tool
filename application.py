import base64
import io
import dash
# from create_sankey_diagram import *
from functools import partial
import pandas as pd



df = pd.DataFrame()
available_columns = []
linear_bool = True
selected_columns = []
data = {}
filter_values = []

application = dash.Dash(__name__) 

application.layout = dash.html.Div(
    
    className='app-body', children=[
        dash.html.Img(
        src='assets\logo.png',
        alt='PwC Logo',
        style={'width':'160px',
                'position': 'fixed',
                'top': '2%',
                'right': '4.2%',
                }
            ),
        dash.dcc.Upload(
            id='upload-data',
            children=dash.html.Div(['Drag and Drop or ', dash.html.A('Select Files')]),
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
        dash.html.Div(className='row', children=[
            dash.html.Div(
                [dash.html.Label('Select columns'),
                 dash.dcc.Dropdown(
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
        dash.html.Div(className='row', children=[
            dash.html.Div(
                [dash.html.Label(
                    f'''Filter by {
                        selected_columns[count] if len(selected_columns) > count else ''
                        }'''
                    ),
                dash.dcc.Dropdown(
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
        dash.dcc.Graph(
        id='sankey',
        style={'height': '65vh'}
        )
    ]
)

# @application.callback(
#     Output('selection-source-container', 'style'),
#     [Input('upload-data', 'contents'),
#      Input('upload-data', 'filename')]
# )
# def upload_callback(contents, filename):
#     global df
#     if contents:
#         contents = contents[0]
#         filename = filename[0]
#         df = parse_data(contents, filename)
#         min_required_columns = len(df) > 2
#         if min_required_columns:
#             return dict()

# @application.callback(
#     Output('selection-source', 'options'),
#     [Input('selection-source-container', 'style')]
# )
# def available_options_changed_callback(style):
#     available_columns = list(df.columns)
#     opts = [{'label': opt, 'value': opt} for opt in available_columns]
#     return opts

# def selected_columns_changed_callback(value):
#     '''create diagram only if at leas two columns are selected'''
#     global selected_columns
#     selected_columns = value
#     min_required_columns = len(selected_columns) > 1
#     if min_required_columns:
#         return dict()

# for i in range(7):
#     application.callback(
#         Output(f'selection-target-container{i}', 'style'),
#         [Input('selection-source', 'value')]
#     )(selected_columns_changed_callback)

# def show_target_options_changed_callback(index, style):
#     if index >= len(selected_columns):
#         return []
#     column_values = df[selected_columns[index]].unique()
#     opts = [{'label': opt, 'value': opt} for opt in column_values]
#     return opts

# for i in range(7):
#     application.callback(
#         Output(f'selection-target{i}', 'options'),
#         [Input(f'selection-target-container{i}', 'style')]
#     )(partial(show_target_options_changed_callback, i))

# @application.callback(
#     Output('sankey', 'figure'),
#     [Input('selection-source', 'value')] + 
#     [Input(f'selection-target{i}', 'value') for i in range(7)]
# )
# def update_graph(source=None, *filters):
#     global df, selected_columns
#     if filters == ([], [], [], [], [], [], []):
#         filters = None
#     if not source:
#         try:
#             source = list(df.columns)
#         except Exception as e:
#             print(e)

#     title = 'Sankey Diagram'
#     if not df.empty:
#         title = df.name
#     fig = gen_sankey(
#             df, selected_columns=source, filter=filters, linear=linear_bool, title=title
#             )
#     return fig

# def parse_data(contents, filename):
#     content_string = contents.split(',')[1]
#     decoded = base64.b64decode(content_string)
#     try:
#         if "xlsx" in filename:
#             df = pd.read_excel(io.BytesIO(decoded))
#             df.name = filename
#             return df
#     except Exception as e:
#         print(e)
#         return html.Div(['There was an error processing this file.'])

if __name__ == '__main__':
    application.run_server(debug=True, port=8080)