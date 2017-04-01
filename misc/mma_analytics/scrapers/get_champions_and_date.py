# -*- coding: utf-8 -*-

# Jonathan Halverson
# Friday, March 31, 2017
# Script to print champions

import numpy as np
import pandas as pd
from unidecode import unidecode
pd.set_option('display.width', 160)
pd.set_option('display.max_rows', 160)

cat = pd.DataFrame()
dfs = pd.read_html('https://en.wikipedia.org/wiki/List_of_UFC_champions', flavor='bs4')
for df in dfs[2:13]:
  df.columns = df.iloc[0]
  df.drop(0, axis=0, inplace=True)
  df = df[['Name', 'Date']]
  df = df.dropna()
  df.Name = df.Name.apply(lambda x: x if 'def.' not in x else x[:x.index('def.') - 1])
  cat = cat.append(df).reset_index(drop=True)

d = {' \\(2\\)':'', ' \\(3\\)':'', ' promoted to undisputed champion':''}
cat.Name = cat.Name.replace(d, regex=True)
cat.Name = cat.Name.apply(lambda x: unidecode(x))
cat.Name = cat.Name.replace('Antonio Rodrigo Nogueira', 'Minotauro Nogueira')
cat.Name = cat.Name.replace('T.J. Dillashaw', 'TJ Dillashaw')
cat.Name = cat.Name.replace('B.J. Penn', 'BJ Penn')
cat.Name = cat.Name.replace('Rafael dos Anjos', 'Rafael Dos Anjos')
cat.Name = cat.Name.replace('Junior dos Santos', 'Junior Dos Santos')
cat.Name = cat.Name.replace('Quinton Jackson', 'Rampage Jackson')
cat.Date = pd.to_datetime(cat.Date) + np.timedelta64(3, 'D')

iofile = '../data/fightmetric_cards/fightmetric_fights_CLEAN_3-6-2017.csv'
fights = pd.read_csv(iofile, header=0, parse_dates=['Date'])

win_lose = fights.Winner.append(fights.Loser)
print set(cat.Name) - set(win_lose)

final = cat.groupby('Name').min()
final.to_csv('../data/ufc_champions.csv', index=True)

# Note that we add 3 days to the date that the fighter
# became champion. This is deal with Japan and Australia.
#print set(final.Date) - set(fights.Date)
