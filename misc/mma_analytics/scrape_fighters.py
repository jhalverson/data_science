# Jonathan Halverson
# Saturday, February 11, 2017

# flags to get updated data
scrape_fighters = False
scrape_birthdays = True
###################################

import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 200)

# store the 26 characters of the English alphabet
import string
chars = string.ascii_lowercase

# scrape new fighter data if needed
base_path = 'fightmetric_fighters/fightmetric_fighters_'
if scrape_fighters:
  for char in chars:
    url = 'http://fightmetric.com/statistics/fighters?char=' + char + '&page=all'
    r = requests.get(url)
    with open(base_path + char + '.html', 'w') as f:
      f.write(r.content)

header = ['First', 'Last', 'Nickname', 'Height', 'Weight', 'Reach',
          'Stance', 'Win', 'Loss', 'Draw', 'Belt']
fighters = pd.DataFrame()
chars = 'abcdefghijklmno'
chars = 'pqrstuvwxyz'
chars = ['p']
for char in chars:
  # read tables from html into a list of dataframes
  with open(base_path + char + '.html', 'r') as f:
    html = f.read()
  dfs = pd.read_html(html)
  df = dfs[0]

  # reassign column labels, drop first two rows and re-index
  df.columns = header
  df.drop(0, axis=0, inplace=True)
  df.replace('--', np.nan, inplace=True)

  df.Weight = df.Weight.str.replace('lbs\\.', '')
  df.Weight = df.Weight.astype(float)

  # when '--' replaced by nan, dtype can change to float and str will fail so make object
  df.Reach = df.Reach.astype(np.object)
  df.Reach = df.Reach.str.replace('"', '')
  df.Reach = df.Reach.astype(np.float)

  # create of field of full name
  def full_name(x):
    return x['First'] + ' ' + x['Last']
  df['Name'] = df.apply(full_name, axis=1)

  # convert the height to inches
  def convert_height(x):
    if pd.isnull(x): return x
    height = x.split('\'')
    feet = int(height[0])
    inches = int(height[1].replace('"', ''))
    return 12.0 * feet + inches
  df['Height'] = df['Height'].apply(convert_height)

  # we find the table rows and if an <img> tag is present (image of UFC belt) in the
  # row then we extract the name via the <a> tags (the find_all method is implied)
  dob = []
  df.Belt = 0
  soup = BeautifulSoup(html, 'lxml')
  for row in soup('tr', {'class':'b-statistics__table-row'}):
    # find champion belt image if exists
    if row.find('img', {'class':'b-list__icon'}):
      firstname = row('a')[0].string
      lastname = row('a')[1].string
      idx = df[(df.First == firstname) & (df.Last == lastname)].index
      df.set_value(idx, 'Belt', 1)
    # get link to individual fighter if exists
    if row.find('td', {'class':'b-statistics__table-col'}):
      if row.find('a'):
        if scrape_birthdays: time.sleep(0)
        url = row.find('a').get('href')
        # get page by scraping or from file
        iofile = 'fightmetric_fighters/' + url.split('/')[-1] + '.html'
        if scrape_birthdays:
          r = requests.get(url, headers={'User_agent':'Mozilla/5.0'})
          with open(iofile, 'w') as f:
            f.write(r.content)
          s = BeautifulSoup(r.content, 'lxml')
        else:
          with open(iofile, 'r') as f:
            html = f.read()
          s = BeautifulSoup(html, 'lxml')
        # find tag containing date of birth
        div = s.find('div', {'class':'b-list__info-box b-list__info-box_style_small-width js-guide'})
        for item in div('li', {'class':'b-list__box-list-item b-list__box-list-item_type_block'}):
          if ('DOB' in item.get_text()):
            b = item.get_text().replace('DOB:', '').replace('--', '').strip()
            birthday = b if (b != '') else np.nan
            dob.append(birthday)
      else:
        dob.append(np.nan)
  df['Dob'] = pd.to_datetime(pd.Series(dob))

  # append to previous results
  fighters = pd.concat([fighters, df], ignore_index=True)

print fighters
print fighters.info()
print fighters.describe()
print fighters.Stance.value_counts()
print min(fighters.Dob), max(fighters.Dob)
print fighters[fighters.Nickname.str.contains(',', na=False)]
fighters.to_csv('fightmetric_fighters/fighters.csv', index=False)
