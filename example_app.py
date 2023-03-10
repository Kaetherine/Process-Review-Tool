import dash
import pandas as pd
import plotly.express as px

import pandas as pd
import plotly.graph_objects as go
import random
import dash
import openpyxl
from dash import Dash, dcc, html, Input, Output

app = dash.Dash()

# Beispieldaten erstellen
df = pd.DataFrame({'Source': ['A', 'B', 'C', 'A', 'B', 'C'],
                   'Target': ['D', 'D', 'D', 'E', 'E', 'E'],
                   'Wert': [1, 2, 3, 4, 5, 6]})

app.layout = html.Div([
    # Dropdown-Menü zum Auswählen von Spalten
    dcc.Dropdown(id='column-dropdown',
                 options=[{'label': col, 'value': col} for col in df.columns],
                 multi=True,
                 value=['Source', 'Target', 'Wert']),
    # Ausgabebereich für das Sankey-Diagramm
    dcc.Graph(id='sankey-graph')
])

@app.callback(
    dash.dependencies.Output('sankey-graph', 'figure'),
    [dash.dependencies.Input('column-dropdown', 'value')])
def update_graph(columns):
    # Neues DataFrame aus den gewählten Spalten erstellen
    selected_df = df[columns]
    # Sankey-Diagramm erstellen und zurückgeben
    fig = px.sankey(selected_df, source='Source', target='Target', value='Wert')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)



# from dash import Dash, dcc, html, Input, Output

dcc.Dropdown(
        list(df.columns),
        'NYC',
        id='demo-dropdown',
        multi=True
        ),

def random_color_hex():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

df = pd.read_excel('Sample_Data_Set.xlsx')
df['count_col'] = [f'count_{x}' for x in range(len(df))]
# df['color'] = [random_color_hex() for x in range(len(df))]

columns = list(df.columns)

linear =True
if linear:
  for col in df.columns:
    for index, value in enumerate(df[col]):
        df.at[index, col] = f'{value}_({col})'

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
      source = links_dict['source'],
      target = links_dict['target'],
      value = links_dict['count'],
      # lable = 'test'
  ))])

fig.update_layout(
  title_text='Draft: Process Review Tool',
  font_size=10)
# fig.show()

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(list(df.columns), 'NYC', id='demo-dropdown', multi=True),
    html.Div(id='output-container'),
    dcc.Graph(
    figure=fig
            )
          ])


@app.callback(
    Output('output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'

if __name__ == '__main__':
    app.run_server(debug=True)

