#!/usr/bin/env python

import pandas as pd

df = pd.read_csv('bcur202510.csv')
df1 = pd.read_csv('abc-ranking.csv')

df.set_index('学校名称')
df1.set_index('学校名称')

# df1 = df1.join(df[['标签']], how='left')
# df1['标签'] = df['标签'].reindex(df1.index)
for idx, row1 in df1.iterrows():
    row = df[df['学校名称'] == row1['学校名称']]
    df1.at[idx, '标签'] = None if row.empty else row['标签'].values[0]

df1.fillna('-', inplace=True)
df1.to_csv('abc-ranking-with-labels.csv', index=False)
