import pandas as pd
# contributiony by ...

def gen_sankey(df, columns=None, value_columns='', title='Sankey Diagram'):
    # maximum of 6 value columns -> 6 colors
    if columns is None:
        columns = []
    color_palette = ['#D85604', '#D85604', '#D85604', '#D85604', '#D85604']
    label_list = []
    color_num_list = []
    for cat_col in columns:
        label_list_temp = list(set(df[cat_col].values))
        color_num_list.append(len(label_list_temp))
        label_list = label_list + label_list_temp

    # remove duplicates from label_list
    label_list = list(dict.fromkeys(label_list))

    # define colors based on number of levels
    colorList = []
    for idx, color_num in enumerate(color_num_list):
        colorList = colorList + [color_palette[idx]] * color_num

    # transform df into a source-target pair
    for i in range(len(columns) - 1):
        if i == 0:
            sourcetarget_df = df[[columns[i], columns[i + 1], value_columns]]
            sourcetarget_df.columns = ['source', 'target', 'count']
        else:
            tempDf = df[[columns[i], columns[i + 1], value_columns]]
            tempDf.columns = ['source', 'target', 'count']
            sourcetarget_df = pd.concat([sourcetarget_df, tempDf])
        sourcetarget_df = sourcetarget_df.groupby(['source', 'target']).agg({'count': 'sum'}).reset_index()

    # add index for source-target pair
    sourcetarget_df['sourceID'] = sourcetarget_df['source'].apply(lambda x: label_list.index(x))
    sourcetarget_df['targetID'] = sourcetarget_df['target'].apply(lambda x: label_list.index(x))

    # creating the sankey diagram
    data = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color="#D85604",
                width=0.5
            ),
            label=label_list,
            color=colorList
        ),
        link=dict(
            source=sourcetarget_df['sourceID'],
            target=sourcetarget_df['targetID'],
            value=sourcetarget_df['count']
        )
    )

    layout = dict(
        title=title,
        font=dict(
            size=10
        )
    )

    fig = dict(data=[data], layout=layout)
    return fig