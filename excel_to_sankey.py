import pandas as pd
import plotly.graph_objects as go

def excel_to_sankey_viz(path_to_file, linear = True):
  df = pd.read_excel(path_to_file)
  df['count_col'] = [f'count_{x}' for x in range(len(df))]

  columns = list(df.columns)
  if linear:
    for col in df.columns:
      for index, value in enumerate(df[col]):
          df.at[index, col] = f'{value}_({col})'

  dfs = []
  for column in columns:
    i = columns.index(column)+1
    if column == columns[-1] or column == columns[-2] or column == 'count_col':
      continue
    else:
      try:
        dfx = df.groupby([column, columns[i]])['count_col'].count().reset_index()
        dfx.columns = ['source', 'target', 'count']
        dfs.append(dfx)
      except Exception as e:
        print(repr(e))

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
        value = links_dict['count']
    ))])

  fig.update_layout(
    title_text='Draft: Process Review Tool',
    font_size=10)
  fig.show()

excel_to_sankey_viz('Process-Review\\Sample_Data_Set.xlsx', True)
