import base64
import io
from dash import dcc, html, Input, Output, Dash, dash_table
from controller import *

df = pd.DataFrame()
available_columns = []
last_column_values = []
linear_bool = True
dropdowns = []
source_cols = []

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
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin-bottom": "9px",
            },
            multiple=True,
        ),
        html.Div(className="row", children=[
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
                className="twelve columns pretty_container"
            ),
        ]),
        html.Div(className="row", children=[
            html.Div(
                [html.Label(
                    f'''Filter by {
                        source_cols[id_index] if len(source_cols) > id_index else ""
                        }'''
                    ),
                dcc.Dropdown(
                    id=f'selection-target{id_index}',
                    multi=True,
                    placeholder='Select the row values you want to include',
                    value=[]
                ),
                ],
                id=f'selection-target-container{id_index}',
                className="two columns pretty_container"
            ) for id_index in range(7)
        ]),
        dcc.Graph(
        id="sankey",
        style={"height": "65vh"}
        )
    ]
)


@app.callback(
    Output("selection-source-container", "style"),
    [Input("upload-data", "contents"),
     Input("upload-data", "filename")]
)
def upload_callback(contents, filename):
    global df
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        min_required_columns = len(df) > 2
        if min_required_columns:
            return dict()


@app.callback(
    Output("selection-source", "options"),
    [Input("selection-source-container", "style")]
)
def available_options_changed_callback(style):
    opts = []
    available_columns = list(df.columns)
    opts = [{'label': opt, 'value': opt} for opt in available_columns]
    return opts


def selected_columns_changed_callback(value):
    '''create diagram only if at leas two columns are selected'''
    selected_columns = value
    min_required_columns = len(selected_columns) > 1
    if min_required_columns:
        return dict()

for i in range(7):
    app.callback(
        Output(f"selection-target-container{i}", "style"),
        [Input("selection-source", "value")]
)(selected_columns_changed_callback)


def show_target_options_changed_callback(style):
    opts = []
    opts = [{'label': opt, 'value': opt} for opt in last_column_values]
    return opts

for i in range(7):
    app.callback(
        Output(f"selection-target{i}", "options"),
        [Input(f"selection-target-container{i}", "style")]
)(show_target_options_changed_callback)


@app.callback(
    Output('sankey', 'figure'),
    [Input("selection-source", "value"), Input("selection-target0", "value")]
)
def update_graph(source=None, filter=None):
    global df, last_column_values, source_cols
    if not source:
        try:
            source = list(df.columns)
        except Exception as e:
            print(e)
    fig, source_columns, last_column_values = gen_sankey(
            df, source_columns=source, filter=filter, linear=linear_bool, title=df.name
            )
    return fig


def parse_data(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if "xlsx" in filename:
            df = pd.read_excel(io.BytesIO(decoded))
            df.name = filename
            return df
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

if __name__ == '__main__':
    app.run_server(debug=True)