import base64
import io
from dash import dcc, html, Input, Output, Dash
from controller import *

df = {}
available_columns = []
last_column_values = []
filter_by = []

app = Dash(__name__)

app.layout = html.Div(className='app-body', children=[
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
                "width": "98%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.Div(className="row", children=[
            html.Div(
                [html.Label('Select columns'),
                 dcc.Dropdown(
                    id='selection-source',
                    style = {
                    'margin-top': '1.8%',
                    'margin-left': '2.5%',
                    'width': '95%',
                    },
                    options=[{'label': opt, 'value': opt} for opt in available_columns],
                    multi=True,
                    placeholder='Select the columns you want to visualize',
                    value=[]
                ),
                 ],
                id='selection-source-container',
                style=dict(display='none'),
                className="nine columns pretty_container"
            ),
            html.Div(
                [html.Label('Filter by'),
                 dcc.Dropdown(
                    id='selection-target',
                    style = {
                    'margin-top': '1.8%',
                    'margin-left': '2.5%',
                    'width': '95%',
                    },
                    options=[{'label': opt, 'value': opt} for opt in last_column_values],
                    multi=True,
                    placeholder='Select the columns you want to visualize',
                    value=''
                ),
                 ],
                id='selection-target-container',
                style=dict(display='none'),
                className="three columns pretty_container"
            ),
        ]),
        dcc.Graph(
        id="sankey",
        style={"height": "1000px"}
        )
    ]
)

@app.callback(
    Output("selection-source-container", "style"),
    [Input("upload-data", "contents"),
     Input("upload-data", "filename")]
)
# --------------------------------------------------------------------------- 1
def upload_callback(contents, filename):
    # print('upload_callback')
    global df
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        show = len(df) > 2
        if show:
            return dict()
    return dict(display='none')


@app.callback(
    Output("selection-source", "options"),
    [Input("selection-source-container", "style")]
)

# --------------------------------------------------------------------------- 5
def available_options_changed_callback(style):
    # print('available_options_changed_callback')
    opts = []
    if 'display' in style.keys():
        return opts
    available_columns = list(df.columns)
    # print(available_columns)
    opts = [{'label': opt, 'value': opt} for opt in available_columns]
    return opts


@app.callback(
    Output("selection-target-container", "style"),
    [Input("selection-source", "value")]
)

# --------------------------------------------------------------------------- 2, 7
def selected_columns_changed_callback(value):
    # print('selected_columns_changed_callback')
    show = len(value) > 1
    if show:
        return dict()
    return dict(display='none')


@app.callback(
    Output("selection-target", "options"),
    [Input("selection-target-container", "style")]
)
def show_target_options_changed_callback(style):
    opts = []
    if 'display' in style.keys():
        return opts
    print(last_column_values)
    opts = [{'label': opt, 'value': opt} for opt in last_column_values]
    return opts


@app.callback(
    Output("submit", "style"),
    [Input("selection-target", "value")]
)

# --------------------------------------------------------------------------- 3
def select_all_none(value):
    # print('select_all_none')
    show = len(value) == 1
    if show:
        return dict()
    return dict(display='none')

@app.callback(
    Output('sankey', 'figure'),
    [Input("selection-source", "value"), Input("selection-target", "value")]
)

# --------------------------------------------------------------------------- 4
def update_graph(source, filter):
    # print('\n','UPDATE GRAPH:')
    global df, last_column_values
    fig, last_column_values = gen_sankey(
        df, source_columns=source, filter=filter, linear=True
        )
    last_column_values = last_column_values
    return fig

def parse_data(contents, filename):
    # print('parse_data')
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if "xlsx" in filename:
            return pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])
    return None

if __name__ == '__main__':
    app.run_server(debug=True)