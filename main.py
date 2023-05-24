import base64
import io
from dash import dcc, html, Input, Output, Dash, dash_table
from controller import *

df = pd.DataFrame()
available_columns = []
last_column_values = []
filter_by = []
linear_bool = True
dropdowns = []

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
                "margin-bottom": "20px",
            },
            multiple=True,
        ),
        html.Div(className="row", children=[
            html.Div(
                [html.Label('Select columns'),
                 dcc.Dropdown(
                    id='selection-source',
                    options=[{'label': opt, 'value': opt} for opt in available_columns],
                    multi=True,
                    placeholder='Select the columns you want to visualize',
                    value=[]
                ),
                 ],
                id='selection-source-container',
                # style=dict(display='none'),
                className="twelve columns pretty_container"
            ),
        ]),
        html.Div(className="row", children=[
            html.Div(
                [html.Label('Filter by'),
                dcc.Dropdown(
                    id=f'selection-target{value}',
                    options=[{'label': opt, 'value': opt} for opt in last_column_values],
                    multi=True,
                    placeholder='Select the row values you want to include',
                    value=''
                ),
                ],
                id=f'selection-target-container{value}',
                className="two columns pretty_container"
            ) for value in range(7)
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
        show = len(df) > 2
        if show:
            return dict()
    # return dict(display='none')


@app.callback(
    Output("selection-source", "options"),
    [Input("selection-source-container", "style")]
)
def available_options_changed_callback(style):
    opts = []
    if 'display' in style.keys():
        return opts
    available_columns = list(df.columns)
    opts = [{'label': opt, 'value': opt} for opt in available_columns]
    return opts


@app.callback(
    Output("selection-target-container0", "style"),
    [Input("selection-source", "value")]
)
def selected_columns_changed_callback(value):
    show = len(value) > 1
    if show:
        return dict()
    # return dict(display='none')


@app.callback(
    Output("selection-target0", "options"),
    [Input("selection-target-container0", "style")]
)
def show_target_options_changed_callback(style):
    opts = []
    if 'display' in style.keys():
        return opts
    opts = [{'label': opt, 'value': opt} for opt in last_column_values]
    return opts


@app.callback(
    Output('sankey', 'figure'),
    [Input("selection-source", "value"), Input("selection-target0", "value")]
)
def update_graph(source=None, filter=None):
    global df, last_column_values
    if not source:
        try:
            source = list(df.columns)
        except Exception as e:
            print(e)
    fig, last_column_values = gen_sankey(
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
