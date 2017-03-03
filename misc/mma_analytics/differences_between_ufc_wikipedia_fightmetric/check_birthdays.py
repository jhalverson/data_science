# Jonathan Halverson
# Tuesday, February 21, 2017
# Here we compare dates of birth, heights and reaches between FightMetric and Wikipedia
# We do not use fuzzy matching to connect active Wikipedia fighters to FightMetric

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

# get list of FightMetric figthers
iofile = 'fightmetric_fighters/fightmetric_fighters.csv'
fightmetric = pd.read_csv(iofile, header=0, parse_dates=['Dob'])

# try to guess links to nonactive FightMetric fighters
active_names, _ = zip(*active_fighters)
not_active = set(fightmetric.Name.tolist()) - set(active_names)
nonactive_fighters = []
for name in not_active:
  url = 'https://en.wikipedia.org/wiki/' + '_'.join(name.split())
  nonactive_fighters.append((name, url))

# for each url, if page looks like MMA bio then extract dob, height and reach
name_height_reach = []
for name, url in active_fighters + nonactive_fighters:
  soup = BeautifulSoup(requests.get(url).content, 'lxml')
  text_scan = any([('mixed martial' in p.text.lower()) or (' UFC ' in p.text.lower()) for p in soup('p')])
  table = soup.find('table', {'class':'infobox vcard'})
  bday = soup.find('span', {'class':'bday'})
  if (table and bday and not text_scan): print '********* Skipping ...', name, url
  print name, url
  if (text_scan and table and bday):
    # extract date of birth
    bday = bday.string.strip()
    reach = height = feet = inches = np.nan
    for tr in table('tr'):
      th = tr.find('th')
      td = tr.find('td')
      if th and td:
        if (th.get_text() and td.get_text()):
          # extract reach
    	  if (th.get_text().strip() == 'Reach'):
            reach = unidecode(td.get_text().strip())
            if ('in' in reach):
              reach = reach[:reach.index(' in')].strip()
              if '(' in reach: reach = reach[reach.index('(') + 1:]
              reach = float(reach)
          # extract height
          if (th.get_text().strip() == 'Height'):
            height = unidecode(td.get_text().strip())
            feet = height[:height.index(' ft')]
            if '(' in feet: feet = feet[feet.index('(') + 1:]
            inches = height[height.index('ft') + 2:height.index(' in')].strip()
            if ('1/2' in inches): inches = inches.replace('1/2', '').strip()
            if ('3/4' in inches): inches = inches.replace('3/4', '').strip()
            height = 12.0 * float(feet) + float(inches)
    print feet, inches, '--', height, name, reach, '--', reach, '--', url
    name_height_reach.append([name, bday, height, reach])

# create and write wikipedia dataframe
wiki = pd.DataFrame(name_height_reach, columns=['Name', 'Dob', 'Height', 'Reach'])
wiki.to_csv('wikipedia_bdays_height_reach.csv', index=False)

# suffixes for column name collisions
s = ('_wikipedia', '_fightmetric')

# display reach mismatches
wf = wiki[pd.notnull(wiki.Reach)].merge(fightmetric[pd.notnull(fightmetric.Reach)], on='Name', how='inner', suffixes=s)
wf['ReachDiff'] = np.abs(wf.Reach_wikipedia - wf.Reach_fightmetric)
print wf[wf.ReachDiff > 2.0][['Name', 'Reach_wikipedia', 'Reach_fightmetric']].to_string(index=False)

# display height mismatches
wf = wiki[pd.notnull(wiki.Height)].merge(fightmetric[pd.notnull(fightmetric.Height)], on='Name', how='inner', suffixes=s)
wf['HeightDiff'] = np.abs(wf.Height_wikipedia - wf.Height_fightmetric)
print wf[wf.HeightDiff > 2.0][['Name', 'Height_wikipedia', 'Height_fightmetric']].to_string(index=False)

# display date of birth mismatches
wf = wiki[pd.notnull(wiki.Dob)].merge(fightmetric[pd.notnull(fightmetric.Dob)], on='Name', how='inner', suffixes=s)
wf.Dob_wikipedia = pd.to_datetime(wf.Dob_wikipedia)
wf.Dob_fightmetric = pd.to_datetime(wf.Dob_fightmetric)
print wf[wf.Dob_wikipedia != wf.Dob_fightmetric][['Name', 'Dob_wikipedia', 'Dob_fightmetric']].to_string(index=False)
