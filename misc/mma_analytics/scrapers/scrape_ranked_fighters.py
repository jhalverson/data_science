# Jonathan Halverson
# Monday, March 6, 2017
# Scrape the list of ranked UFC fighters from UFC.com

import time
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

url = 'http://www.ufc.com/rankings'
soup = BeautifulSoup(requests.get(url).content, 'lxml')
champions = soup('span', {'id':'champion-fighter-name', 'class':'fighter-name'})
tables = soup('table')[4:-1]
assert len(tables) == 10 and len(champions) == 10, 'Tables or champions mismatch'
ranked_fighters = []
for champion, table in zip(champions, tables):
  ranked_fighters.append(champion.find('a').string.strip())
  for row in table('tr'):
    name = row.find('td', {'class':'name-column'}).find('a').string
    ranked_fighters.append(unidecode(name.replace('(Interim Champion)', '').strip()))
assert len(ranked_fighters) == 10 * 16, 'Number of ranked fighters'

with open('../data/ranked_ufc_fighters_' + str(int(time.time())) + '.txt', 'w') as f:
  f.write('\n'.join(ranked_fighters))
