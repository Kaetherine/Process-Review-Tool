import pandas as pd

def gen_sankey(df, selected_columns=None, filter=None, linear=True, title='Sankey Diagram'):
    '''create the sankey diagram based on given params'''

    selected_columns.append(selected_columns[-1])
    last_column_values = sorted(df[selected_columns[-1]].unique()) 

    if filter:
        df = df.loc[df[selected_columns[-1]].isin(filter)]
 
    if linear:
        for col in list(df.columns):
            for index, value in enumerate(df[col]):
                if str(col) not in str(value):
                    df.at[index, col] = f'{value} ({col})'

    df['count_col'] = [f'count_{x}' for x in range(len(df))]

    # Create a list of dataframes with source and target columns
    dfs = []
    for column in selected_columns:
        i = selected_columns.index(column)+1
        if column == selected_columns[-1] or column == selected_columns[-2] or column == 'count_col':
            continue
        else:
            try:
                dfx = df.groupby([column, selected_columns[i]])['count_col'].count().reset_index()
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
                color='#2C66F6',
                width=0.1
            ),
            label=unique_source_target,
            color='#2C66F6'
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
        size=16
    )
)
    # Create sankey diagram
    fig = dict(data=[data], layout=layout)

    return fig, selected_columns
