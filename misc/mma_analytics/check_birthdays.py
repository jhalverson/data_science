# Jonathan Halverson
# Tuesday, February 21, 2017
# Here we compare birthdays between FightMetric and Wikipedia

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

# get Wikipedia links to active fighters
url = 'https://en.wikipedia.org/wiki/List_of_current_UFC_fighters'
soup = BeautifulSoup(requests.get(url).content, 'lxml')
tables = soup('table', {'class':'wikitable sortable'})
assert len(tables) == 11, 'Number of weight classes is not eleven'
active_fighters = []
for table in tables:
  for row in table('tr')[2:-1]:
    td = row('td')[1].find('span', {'class':'fn'})
    name = td.get_text().strip()
    if (td.find('a')):
      url = 'https://en.wikipedia.org' + td.find('a').get('href')
      if 'redlink' not in url: active_fighters.append((unidecode(name), url))

# for each active fighter get their Wikipedia birthday
wikipedia_bdays = []
for name, url in active_fighters:
  soup = BeautifulSoup(requests.get(url).content, 'lxml')
  first_p = soup.find('p').get_text()
  bday_from_first_p = ''
  if ('(born' in first_p):
    bday_from_first_p = first_p[first_p.index('(born'):first_p.index('(born') + 30]
  bday = soup.find('span', {'class':'bday'})
  if bday:
    wikipedia_bdays.append((name, bday.string.strip()))
    print name, bday.string.strip(), bday_from_first_p

# write out names and birthdays
with open('wikipedia_bdays.txt', 'w') as f:
  for name, bday in wikipedia_bdays:
    f.write('%s, %s\n' % (name, bday))

# get list of FightMetric figthers
fightmetric = pd.read_csv('fightmetric_fighters/fightmetric_fighters.csv', header=0, parse_dates=['Dob'])

# join Wikipedia dataframe to FightMetric
wiki = pd.DataFrame(wikipedia_bdays, columns=['Name', 'Bday'])
wiki.Bday = pd.to_datetime(wiki.Bday)
df = fightmetric.merge(wiki, how='inner', on='Name')

# print out mismatches
df.rename(columns={'Dob':'FightMetric_DOB', 'Bday':'Wikipedia_DOB'}, inplace=True)
print df[df.FightMetric_DOB != df.Wikipedia_DOB][['Name', 'FightMetric_DOB', 'Wikipedia_DOB']]
