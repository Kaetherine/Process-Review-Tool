import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

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
