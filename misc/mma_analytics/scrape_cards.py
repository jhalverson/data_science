# -*- coding: utf-8 -*-

# Jonathan Halverson
# Sunday, February 12, 2017

# flag to get updated data or not
scrape_cards = False

# create a list of the card numbers
cards = range(1, 209)
cards.reverse()
cards.remove(151)
cards.remove(176)

# scrape new card data if needed
if scrape_cards:
  import requests
  for card in cards:
    url = 'https://en.wikipedia.org/wiki/UFC_' + str(card)
    r = requests.get(url)
    with open('wikipedia_cards_' + str(card) + '.html', 'w') as f:
      f.write(r.content)

import numpy as np
import pandas as pd

# store the table index for each card
table_idx = dict([(card, 2) for card in cards])
table_idx[31] = 3
table_idx[40] = 3
table_idx[57] = 3
table_idx[149] = 21

info_idx = dict([(card, 0) for card in cards])
info_idx[149] = 19
info_idx[57] = 1
info_idx[31] = 1

fights = pd.DataFrame()
for card in cards:
  # read tables from html into a list of dataframes
  with open('wikipedia_cards_' + str(card) + '.html', 'r') as f:
    html = f.read()
  # extract table
  dfs = pd.read_html(html)
  df = dfs[table_idx[card]]
  # drop rows and concatenate
  df = df[df[2].isin(['def.', 'vs.', 'def', 'vs'])]
  # load table of fight card meta data
  print card, [(i, dfs[i].shape) for i in range(len(dfs))]
  venue = dfs[info_idx[card]]
  venue.set_index(0, inplace=True)
  # add new columns
  df['Location'] = venue.loc['City', 1]
  df['Date'] = venue.loc['Date', 1]
  fights = pd.concat([fights, df], ignore_index=True)

fights.reset_index(drop=True, inplace=True)
fights.drop(labels=[7], axis=1, inplace=True)
fights.columns = ['Weight', 'Winner', 'DefVs', 'Loser', 'Method', 'Round', 'Time', 'Location', 'Date'] 

fights['Winner'] = fights['Winner'].str.replace('\(c\)|\(ic\)|\(UFC Champion\)', repl='').str.strip()
fights['Loser'] = fights['Loser'].str.replace('\(c\)|\(ic\)|\(Pride Champion\)', repl='').str.strip()
fights.Date = fights.Date.str.encode('ascii', errors='ignore')

fighter = 'Conor McGregor'
fighter = u'José Aldo'
fighter = 'Nick Diaz'
fighter = 'Carlos Condit'
fighter = 'Georges St-Pierre'
fighter = u'Patrick Côté'
fighter = 'Anderson Silva'
fighter = 'Rafael dos Anjos'

#print fights[(fights.Winner.str.contains('Georges')) | (fights.Loser.str.contains('Georges'))]
#print fights[(fights.Winner == fighter) | (fights.Loser == fighter)]
#print fights[(~fights.DefVs.isin(['def\.'])) & (fights.DefVs.isin(['def']))]
#print fights[(~fights.Method.str.contains('TKO')) & (fights.Method.str.contains('KO'))]
#print fights[fights.Method.str.contains('no contest', case=False)]
#print fights.Winner.apply(lambda x: x if len(x.split()) < 2 else 'NaN').unique()
print fights.Date.unique()
