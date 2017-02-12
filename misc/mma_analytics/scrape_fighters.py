# Jonathan Halverson
# Saturday, February 11, 2017

# flag to get updated data or not
scrape_fighters = False

# store the 26 characters of the English alphabet
import string
chars = string.ascii_lowercase

###################################
# scrape new fighter data if needed
if scrape_fighters:
  import requests
  for char in chars:
    url = 'http://fightmetric.com/statistics/fighters?char=' + char + '&page=all'
    r = requests.get(url)
    with open('fightmetric_fighters_' + char + '.html', 'w') as f:
      f.write(r.content)

import numpy as np
import pandas as pd

to_be_concat = []

# read tables from html into a list of dataframes
with open('fightmetric_fighters_a.html', 'r') as f:
  html = f.read()

dfs = pd.read_html(html)
df = dfs[0]

# reassign column labels
df.columns = [column.strip() for column in df.columns]

# drop the first empty row and re-index
df.drop(0, axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)

df.replace('--', np.nan, inplace=True)
df.Belt = 0
df = df.astype({'W':int, 'L':int, 'D':int, 'Belt':int})

df.Reach = df.Reach.str.replace('"', '')
df.Reach = df.Reach.astype(float)

df['Wt.'] = df['Wt.'].str.replace('lbs.', '')
df['Wt.'] = df['Wt.'].astype(float)

def full_name(x):
  return x['First'] + ' ' + x['Last']
df['Full'] = df.apply(full_name, axis=1)

def convert_height(x):
  if pd.isnull(x): return x
  height = x.split('\'')
  feet = int(height[0])
  inches = int(height[1].replace('"', ''))
  return feet + inches / 12.0

df['Height'] = df['Ht.'].apply(convert_height)

print df
print df.info()
print df.columns
print df.Reach.mean()
print df['Wt.'].mean()
print df['Height'].mean()

# using BS4 to identify the champions
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')

# we find the table rows and if an <img> tag is present (image of UFC belt) in the
# row then we extract the name via the <a> tags (the find_all method is implied)
for row in soup('tr', {'class':'b-statistics__table-row'}):
  if row.find('img', {'class':'b-list__icon'}):
    firstname = row('a')[0].string
    lastname = row('a')[1].string
    idx = df[(df.First == firstname) & (df.Last == lastname)].index
    df.set_value(idx, 'Belt', 1)

to_be_concat.append(df)

fighters = pd.concat(to_be_concat, ignore_index=True)
print df.Stance.value_counts()
