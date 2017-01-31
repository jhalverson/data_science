# Jonathan Halverson
# Tuesday, January 31, 2017
# Script that scrapes, cleans and formats some tabular data

import pandas as pd
print pd.__version__
pd.set_option('display.width', 160)

# download and extract the second table
dfs = pd.read_html('http://www.the-numbers.com/weekend-box-office-chart', flavor='bs4', thousands=',')
df = dfs[1]

# set the columns as the first row and drop first row
df.columns = df.iloc[0]
df.drop(0, axis=0, inplace=True)

# Fill in the missing column names
df.columns = ['Rank', 'Prev. Rank'] + df.columns[2:].tolist()

# reset the index (both ways are equivalent)
df.reset_index(drop=True, inplace=True)
### alternative: df.index = range(df.shape[0])

# convert data types
df = df.astype({'Rank':int})
df['Gross'] = df['Gross'].replace('[\$,]', '', regex=True).astype(int)

# replace NaN with 0 for df.Change
df['Change'].fillna(0, inplace=True)
df['Change'] = df['Change'].replace('[\$,%]', '', regex=True).astype(int) / 100.0

print df
print df.info(null_counts=True)
print 'Mean gross = %.1f' % df.Gross.mean()
