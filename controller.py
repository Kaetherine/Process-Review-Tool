import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import plotly.graph_objs as go

def gen_sankey(df, source_columns, target_column, linear=True, title='Sankey Diagram'):
    # print('source_columns:', source_columns, '\n')
    source_columns.append(source_columns[-1])
    target_column = source_columns[-1]
    # print('target_columns:', target_column, '\n')

    df['count_col'] = [f'count_{x}' for x in range(len(df))]
 
    if linear:
        for col in list(df.columns):
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