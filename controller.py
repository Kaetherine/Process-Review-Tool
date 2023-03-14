import pandas as pd
import plotly.graph_objects as go
# contributiony by ...

import pandas as pd
import plotly.graph_objs as go

def gen_sankey(df, source_columns, target_column, linear=True, title='Sankey Diagram'):
    # Add a count column to the dataframe
    df['count_col'] = [f'count_{x}' for x in range(len(df))]

    # Convert categorical columns to linear format
    if linear:
        for col in df.columns:
            for index, value in enumerate(df[col]):
                if str(col) not in str(value):
                    df.at[index, col] = f'{col}:{value}'

    # Create a list of dataframes with source and target columns
    dfs = []
    for column in source_columns:
        i = source_columns.index(column)+1
        if column == source_columns[-1] or column == source_columns[-2] or column == 'count_col':
            continue
        else:
            try:
                dfx = df.groupby([column, source_columns[i]])['count_col'].count().reset_index()
                dfx.columns = ['source', 'target', 'count']
                dfs.append(dfx)
            except Exception as e:
                print(f'columnname: {column}\n{repr(e)}')

    # Concatenate dataframes
    links = pd.concat(dfs, axis=0)
    unique_source_target = list(pd.unique(links[['source', 'target']].values.ravel('K')))
    mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
    links['source'] = links['source'].map(mapping_dict)
    links['target'] = links['target'].map(mapping_dict)
    links_dict = links.to_dict(orient='list')

    # Define sankey diagram nodes and links
    data = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color='#D04A02',
                width=0.1
            ),
            label=unique_source_target,
            color='#D04A02'
        ),
        link=dict(
            source=links_dict['source'],
            target=links_dict['target'],
            value=links_dict['count']
        )
    )

    # Define layout
    layout = dict(
        title=title,
        font=dict(
            size=10
        )
    )

    # Create sankey diagram
    fig = dict(data=[data], layout=layout)

    return fig




# def gen_sankey(df, linear=True, title='Sankey Diagram'):
#     # Read dataframe from file
#     if isinstance(df, str):
#         df = pd.read_excel(df)

#     # Add a count column to the dataframe
#     df['count_col'] = [f'count_{x}' for x in range(len(df))]

#     # Convert categorical columns to linear format
#     columns = list(df.columns)
#     if linear:
#         for col in df.columns:
#             for index, value in enumerate(df[col]):
#                 df.at[index, col] = f'{value}_({col})'

#     # Create a list of dataframes with source and target columns
#     dfs = []
#     for column in columns:
#         i = columns.index(column)+1
#         if column == columns[-1] or column == columns[-2] or column == 'count_col':
#             continue
#         else:
#             try:
#                 dfx = df.groupby([column, columns[i]])['count_col'].count().reset_index()
#                 dfx.columns = ['source', 'target', 'count']
#                 dfs.append(dfx)
#             except Exception as e:
#                 print(f'columnname: {column}\n{repr(e)}')

#     # Concatenate dataframes
#     links = pd.concat(dfs, axis=0)
#     unique_source_target = list(pd.unique(links[['source', 'target']].values.ravel('K')))
#     mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
#     links['source'] = links['source'].map(mapping_dict)
#     links['target'] = links['target'].map(mapping_dict)
#     links_dict = links.to_dict(orient='list')

#     # Define sankey diagram nodes and links
#     data = dict(
#         type='sankey',
#         node=dict(
#             pad=15,
#             thickness=20,
#             line=dict(
#                 color='#D04A02',
#                 width=0.1
#             ),
#             label=unique_source_target,
#             color='#D04A02'
#         ),
#         link=dict(
#             source=links_dict['source'],
#             target=links_dict['target'],
#             value=links_dict['count']
#         )
#     )

#     # Define layout
#     layout = dict(
#         title=title,
#         font=dict(
#             size=10
#         )
#     )

#     # Create sankey diagram
#     fig = dict(data=[data], layout=layout)

#     return fig


# def gen_sankey(df, columns=None, value_columns='', title='Sankey Diagram'):
#     # maximum of 6 value columns -> 6 colors
#     if columns is None:
#         columns = []
#     color_palette = ['#D85604', '#D85604', '#D85604', '#D85604', '#D85604']
#     label_list = []
#     color_num_list = []
#     for cat_col in columns:
#         label_list_temp = list(set(df[cat_col].values))
#         color_num_list.append(len(label_list_temp))
#         label_list = label_list + label_list_temp

#     # remove duplicates from label_list
#     label_list = list(dict.fromkeys(label_list))

#     # define colors based on number of levels
#     colorList = []
#     for idx, color_num in enumerate(color_num_list):
#         colorList = colorList + [color_palette[idx]] * color_num

#     # transform df into a source-target pair
#     for i in range(len(columns) - 1):
#         if i == 0:
#             sourcetarget_df = df[[columns[i], columns[i + 1], value_columns]]
#             sourcetarget_df.columns = ['source', 'target', 'count']
#         else:
#             tempDf = df[[columns[i], columns[i + 1], value_columns]]
#             tempDf.columns = ['source', 'target', 'count']
#             sourcetarget_df = pd.concat([sourcetarget_df, tempDf])
#         sourcetarget_df = sourcetarget_df.groupby(['source', 'target']).agg({'count': 'sum'}).reset_index()

#     # add index for source-target pair
#     sourcetarget_df['sourceID'] = sourcetarget_df['source'].apply(lambda x: label_list.index(x))
#     sourcetarget_df['targetID'] = sourcetarget_df['target'].apply(lambda x: label_list.index(x))

#     # creating the sankey diagram
#     data = dict(
#         type='sankey',
#         node=dict(
#             pad=15,
#             thickness=20,
#             line=dict(
#                 color="#D85604",
#                 width=0.5
#             ),
#             label=label_list,
#             color=colorList
#         ),
#         link=dict(
#             source=sourcetarget_df['sourceID'],
#             target=sourcetarget_df['targetID'],
#             value=sourcetarget_df['count']
#         )
#     )

#     layout = dict(
#         title=title,
#         font=dict(
#             size=10
#         )
#     )

#     fig = dict(data=[data], layout=layout)
#     return fig


# def gen_sankey(df, linear = True): #, columns=None, value_columns='', title='Sankey Diagram'):
#     df = pd.read_excel(df)
#     df['count_col'] = [f'count_{x}' for x in range(len(df))]
#     # df['color'] = [random_color_hex() for x in range(len(df))]

#     columns = list(df.columns)
#     if linear:
#         for col in df.columns:
#             for index, value in enumerate(df[col]):
#                 df.at[index, col] = f'{value}_({col})'

#     dfs = []
#     for column in columns:
#         i = columns.index(column)+1
#         if column == columns[-1] or column == columns[-2] or column == 'count_col' and not column == 'color':
#             continue
#         else:
#             try:
#                 dfx = df.groupby([column, columns[i]])['count_col'].count().reset_index()
#                 dfx.columns = ['source', 'target', 'count']
#                 dfs.append(dfx)
#             except Exception as e:
#                 print(f'columnname: {column}\n{repr(e)}')

#     links = pd.concat(dfs, axis=0)
#     unique_source_target = list(pd.unique(links[[
#         'source', 'target']].values.ravel('K')))
#     mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
#     links['source'] = links['source'].map(mapping_dict)
#     links['target'] = links['target'].map(mapping_dict)
#     links_dict = links.to_dict(orient='list')

#     fig = go.Figure(data=[go.Sankey(
#         node = dict(
#             pad = 15,
#             thickness = 20,
#             line = dict(color = '#D04A02', width = 0.1),
#             label = unique_source_target,
#             color = '#D04A02'
#         ),
#         link = dict(
#             source = links_dict['source'],
#             target = links_dict['target'],
#             value = links_dict['count']
#         ))])
      
#     return fig