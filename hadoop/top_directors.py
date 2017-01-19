# Jonathan Halverson
# Wednesday, January 18, 2017
# Scraping the-numbers.com data

from __future__ import print_function

# the webpage containing the data
url = 'http://www.the-numbers.com/people/worldwide-records/technical-roles/Director'

############################
## BeautifulSoup Approach ##
############################

import requests
from bs4 import BeautifulSoup

# download the HTML page and construct the parse tree
r = requests.get(url)
s = BeautifulSoup(r.content, 'lxml')

# extract the one and only table
tables = s.find_all('table')
table = tables[0]

# extract the data from each row
rows = []
for row in table.find_all('tr'):
  rows.append([data.text for data in row.find_all('td') + row.find_all('th')])

# convert list of lists to a Pandas dataframe
import pandas as pd
df = pd.DataFrame(rows[1:], columns=rows[0])

# add new columns in numeric data types
df['ave_num'] = df['Average'].replace('[\$,]', '', regex=True).astype(long)
df['ave_total'] = df['Total Box Office'].replace('[\$,]', '', regex=True).astype(long)

print('\n\n\n############## BeautifulSoup Approach ##############')
print(df.head(5))
print(df.info())
print(df.columns.values) 
print(df.shape)
print(df.describe())

#####################
## Pandas Approach ##
#####################

# use read_html to get a list of dataframes of the tables in the HTML
dfs = pd.read_html(url, flavor='bs4')

# extract the one and only dataframe
df = dfs[0]

# add new columns in numeric data types
df['ave_num'] = df['Average'].replace('[\$,]', '', regex=True).astype(long)
df['ave_total'] = df['Total Box Office'].replace('[\$,]', '', regex=True).astype(long)

print('\n\n\n############## Pandas Approach ##############')
print(df.head(5))
print(df.info())
print(df.columns.values) 
print(df.shape)
print(df.describe())
