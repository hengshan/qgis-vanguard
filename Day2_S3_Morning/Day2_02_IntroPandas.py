import pandas as pd

df = pd.DataFrame(
    {"a": [4, 5, 6],
     "b": [7, 8, 9],
     "c": [10, 11, 12]},
    index=[1, 2, 3])
print(df)

df1 = pd.DataFrame(
    {"a": [14, 15, 64],
     "b": [17, 18, 94],
     "c": [101, 111, 121]},
    index=[1, 2, 3])
print(df)

df2 = pd.DataFrame(
    [[40, 70, 10],
     [52, 82, 11],
     [62, 91, 12]],
    index=[1, 2, 3],
    columns=['d', 'e', 'f'])
print(df2)

# melt
print(pd.melt(df))
print(pd.melt(df, id_vars=['a']))
# print(pd.melt(df, id_vars=['a'], value_vars=['c', 'b'],
#               var_name='hello', value_name="world"))

# pivot
df_melt=pd.melt(df,id_vars=['a'])
print(df_melt.pivot(index='a',columns='variable', values='value'))

# append two data frames
print(pd.concat([df,df1]))
print(pd.concat([df,df2], axis=1))

# method chain
df_chain = (pd.melt(df)
	.rename(columns={
	'variable' : 'var',
	'value' : 'val'})
	.query('val >= 5')
	)
print(df_chain)

# sort value
print(df_chain.sort_values('val'))

# rename columns
df_rename=df.rename(columns = {'a':'a_new','b':'b_new'})
print(df_rename)

# drop columns
print(df.drop(columns=['a','b']))

# select columns
print(df.a)
df_conc=pd.concat([df,df2], axis=1).rename(columns={'d':'ad'})
print(df_conc.filter(regex='^a'))

# select rows
df.loc[:,'a':'ad'] #Select all columns between x2 and x4 (inclusive).
df.iloc[:,[1,2]] #Select columns in positions 1, 2 and 5 (first column is 0).
df.loc[df['a'] > 10, ['a','c']]	# Select rows meeting logical condition, and only the specific columns .
print(df_conc.filter(regex="d$"))

# summarize
print(df['a'].value_counts())
print(df['a'].nunique())
print(len(df))
print(df.describe())
print(df.std())

# make new columns
print(df.assign(d=lambda df: df.a+df.b))
df['e']=df.c
print(df)

# Group data
print(df.groupby(by="a").size())
# print(df.groupby(by="a").agg({'haha':['nunique']}))
print(df.agg(['sum','min']))
print(df.groupby(by='a').agg('sum'))
print(pd.concat([df]*2).groupby(by=['a','b']).agg('sum'))
print(pd.concat([df]*2).groupby(by=['a','b']).agg({'c':['sum']}))
print(df.groupby(by='a').cumsum())

# merge
df['m1']=list("abc")
df1['m1']=list("abc")
print(pd.merge(df, df1, how='left', on='m1')) #standard join
print(pd.merge(df, df1,how='outer',indicator=True)) # set-like operation

# Windows
print(df.expanding().sum())	#allowing summary functions to be applied cumulatively


