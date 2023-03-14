import base64
import io
import dash
from dash import dcc, html, Input, Output, Dash
import plotly.graph_objs as go
from controller import *

df = {}
available_columns = []
selected_columns = []
app = Dash(__name__)

app.layout = html.Div(className='app-body', children=[
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
            multiple=True,
        ),
        html.Div(className="row", children=[
            html.Div(
                [html.Label('Select source columns'),
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
                className="four columns pretty_container"
            ),
            html.Div(
                [html.Label('Select target column'),
                 dcc.Dropdown(
                    id='selection-target',
                    style = {
                    'margin-top': '1.8%',
                    'margin-left': '2.5%',
                    'width': '95%',
                    },
                    options=[{'label': opt, 'value': opt} for opt in available_columns],
                    multi=True,
                    placeholder='Select the columns you want to visualize',
                    value=''
                ),
                 ],
                id='selection-target-container',
                style=dict(display='none'),
                className="four columns pretty_container"
            ),
        ]),
        html.Button('Refresh', id='submit', n_clicks=0, style=dict(display='none')),
        dcc.Graph(id="sankey")
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
    return dict(display='none')


@app.callback(
    Output("selection-source", "options"),
    [Input("selection-source-container", "style")]
)
def available_options_changed_callback(style):
    opts = []
    if 'display' in style.keys():
        return opts
    available_columns = list(df.columns)
    print(available_columns)
    opts = [{'label': opt, 'value': opt} for opt in available_columns]
    return opts


@app.callback(
    Output("selection-target-container", "style"),
    [Input("selection-source", "value")]
)
def selected_columns_changed_callback(value):
    #global selected_columns
    #selected_columns = value
    #print(selected_columns)
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
    available_columns = list(df.columns)
    print(available_columns)
    opts = [{'label': opt, 'value': opt} for opt in available_columns]
    return opts


@app.callback(
    Output("submit", "style"),
    [Input("selection-target", "value")]
)
def select_all_none(value):
    show = len(value) == 1
    if show:
        return dict()
    return dict(display='none')

@app.callback(
    Output('sankey', 'figure'),
    [Input("selection-source", "value"), Input("selection-target", "value")]
)
def update_graph(source, target):
    global df
    columns_selcted = len(source)
    if 1 < columns_selcted < 20 and target != '':
        fig = gen_sankey(df, source_columns=source, target_column=target)
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


def extract_df():
    new_df = df[selected_columns].copy()
    return new_df


if __name__ == '__main__':
    app.run_server(debug=True)
