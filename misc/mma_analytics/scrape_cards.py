# -*- coding: utf-8 -*-

# Jonathan Halverson
# Sunday, February 12, 2017

from __future__ import print_function

# flag to get updated data or not
scrape = False

if scrape:
  import requests
  url = 'https://en.wikipedia.org/wiki/List_of_UFC_events'
  r = requests.get(url)
  with open('list_of_ufc_events.html', 'w') as f:
    f.write(r.content)

  # load HTML file containing all events
  with open('list_of_ufc_events.html', 'r') as f:
    html = f.read()

  # download page for each link
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(html, 'lxml')
  past = soup.find('table', {'id':'Past_events'})
  cards = []
  for row in past('tr')[1:]:
    items = row('td')
    link = items[1].find('a')
    title = link.get('href').replace('/', '_').replace('%', '_').replace('#', '_').replace(':', '')[1:]
    status = items[-1].string
    if (status != 'Cancelled'):
      print('Scraping ' + title + ' ...')
      url = 'https://en.wikipedia.org' + link.get('href')
      r = requests.get(url)
      outfile = title + '.html'
      with open(outfile, 'w') as f:
	f.write(r.content)
      cards.append(outfile)
    else:
      print('Not scraping ' + title)

if not scrape:
  # create a list of the card numbers
  import glob
  cards = glob.glob('wiki_*.html')

import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 200)

# store the table index for each card
table_idx = dict([(card, 2) for card in cards])
table_idx['wiki_UFC_31.html'] = 3
table_idx['wiki_UFC_40.html'] = 3
table_idx['wiki_UFC_57.html'] = 3
table_idx['wiki_2012_in_UFC_UFC_149_Faber_vs._Bar.C3.A3o.html'] = 21
#table_idx['wiki_The_Ultimate_Fighter_Team_Nogueira_vs._Team_Mir_Finale.html']=

info_idx = dict([(card, 0) for card in cards])
info_idx['wiki_UFC_31.html'] = 1
info_idx['wiki_UFC_57.html'] = 1
info_idx['wiki_2012_in_UFC_UFC_149_Faber_vs._Bar.C3.A3o.html'] = 19

for card in cards:
  # read tables from html into a list of dataframes
  with open(card, 'r') as f:
    html = f.read()
  dfs = pd.read_html(html)
  info_idx = -1
  table_idx = -1
  table_df = pd.DataFrame()
  info_df = pd.DataFrame()
  for i, df in enumerate(dfs):
    rows, cols = df.shape
    if (rows > 8) and (cols == 4):
      info_idx = i
      info_df = df
    if (rows > 6) and (cols == 8):
      table_idx = i
      table_df = df[df[2].isin(['def.', 'vs.', 'def', 'vs'])]
  print('*****', card, '*****')
  print('table_idx=', table_idx, table_df.shape)
  print(table_df.iloc[0])
  print('info_idx=', info_idx, info_df.shape)
  print(info_df.iloc[0])
  print([(i, dfs[i].shape) for i in range(len(dfs)) if dfs[i].shape not in [(1, 2), (1, 3), (11, 2)]])
  print('\n')

#  if (info_idx == -1 or table_idx == -1): print(card, [(i, dfs[i].shape) for i in range(len(dfs))])

  # extract table
  #df = dfs[table_idx[card]].copy()
  # drop rows and concatenate
  #df = df[df[2].isin(['def.', 'vs.', 'def', 'vs'])]
  # load table of fight card meta data
  #print(card, [(i, dfs[i].shape) for i in range(len(dfs))])
 
import sys
sys.exit(1)

fights = pd.DataFrame()
for card in cards:
  # read tables from html into a list of dataframes
  with open('wikipedia_cards_' + str(card) + '.html', 'r') as f:
    html = f.read()
  # extract table
  dfs = pd.read_html(html)
  df = dfs[table_idx[card]].copy()
  # drop rows and concatenate
  df = df[df[2].isin(['def.', 'vs.', 'def', 'vs'])]
  # load table of fight card meta data
  #print card, [(i, dfs[i].shape) for i in range(len(dfs))]
  venue = dfs[info_idx[card]]
  venue.set_index(0, inplace=True)
  # add new columns
  df['Card'] = 'UFC ' + str(card)
  df['Location'] = venue.loc['City', 1]
  df['Date'] = venue.loc['Date', 1]
  fights = pd.concat([fights, df], ignore_index=True)

fights.reset_index(drop=True, inplace=True)
fights.drop(labels=[7], axis=1, inplace=True)
fights.columns = ['Weight', 'Winner', 'DefVs', 'Loser', 'Method', 'Round', 'Time', 'Card', 'Location', 'Date'] 

# clean names
fights['Winner'] = fights['Winner'].str.replace('\\(c\\)|\\(ic\\)|\\(UFC Champion\\)', repl='').str.strip()
fights['Loser'] = fights['Loser'].str.replace('\\(c\\)|\\(ic\\)|\\(Pride Champion\\)', repl='').str.strip()

# clean dates
fights.Date = fights.Date.str.encode('ascii', errors='ignore')
fights.Date = fights.Date.apply(lambda x: x if '(' not in x else x[x.index('(') + 1:-1])
fights.Date = fights.Date.str.replace('\\[.\\]', '')
fights.Date = pd.to_datetime(fights.Date)

fighter = u'José Aldo'
fighter = 'Nick Diaz'
fighter = 'Carlos Condit'
fighter = u'Patrick Côté'
fighter = 'Georges St-Pierre'
fighter = 'Rafael dos Anjos'
fighter = 'Conor McGregor'
fighter = 'Anderson Silva'

#print fights[(fights.Winner.str.contains('Georges')) | (fights.Loser.str.contains('Georges'))]
#print fights[(fights.Winner == fighter) | (fights.Loser == fighter)]
#print fights[(~fights.DefVs.isin(['def\.'])) & (fights.DefVs.isin(['def']))]
#print fights[(~fights.Method.str.contains('TKO')) & (fights.Method.str.contains('KO'))]
#print fights[fights.Method.str.contains('no contest', case=False)]
#print fights.Winner.apply(lambda x: x if len(x.split()) < 2 else 'NaN').unique()
#print fights.Date.apply(lambda x: x.year).value_counts().sort_index()

#fights['DayOfWeek'] = fights.Date.dt.weekday_name
#print fights[['Card', 'Location', 'Date', 'DayOfWeek']].drop_duplicates().DayOfWeek.value_counts()

# Submissions vs KOs in championship rounds
#print fights[(fights.Round.isin(['4', '5'])) & (fights.Method.str.contains('Submission', case=False))]
#print fights[(fights.Round.isin(['4', '5'])) & (fights.Method.str.contains('KO', case=False))]
