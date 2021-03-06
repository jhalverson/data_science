# Jonathan Halverson
# Saturday, February 11, 2017

# flags to get updated data
scrape_fighters = False
scrape_birthdays = False
###################################

import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0'
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 200)

# store the 26 characters of the English alphabet
import string
chars = string.ascii_lowercase

# scrape new fighter data if needed
base_path = '../data/fightmetric_fighters/fightmetric_fighters_'
if scrape_fighters:
  for char in chars:
    url = 'http://fightmetric.com/statistics/fighters?char=' + char + '&page=all'
    r = session.get(url)
    with open(base_path + char + '.html', 'w') as f:
      f.write(r.content)

# get list of all previously downloaded files
from os.path import getsize
from glob import glob
previous = set(filter(lambda x: getsize(x) > 50, glob('../data/fightmetric_fighters/*.html')))

header = ['First', 'Last', 'Nickname', 'Height', 'Weight', 'Reach',
          'Stance', 'Win', 'Loss', 'Draw', 'Belt']
fighters = pd.DataFrame()
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
  soup = BeautifulSoup(html, 'lxml').find('table', {'class':'b-statistics__table'}).find('tbody')
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
        url = row.find('a').get('href')
        # get page by scraping or from file
        iofile = '../data/fightmetric_fighters/' + url.split('/')[-1] + '.html'
        if scrape_birthdays and iofile not in previous:
          print char, url, ' scraping file ...'
          r = session.get(url, headers=session.headers)
          with open(iofile, 'w') as f:
            f.write(r.content)
          s = BeautifulSoup(r.content, 'lxml')
        else:
          print char, row.find('a').get_text(), iofile, ' reading file from disk'
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
    if scrape_birthdays: time.sleep(0)

  # make indices of dataframe and series the same
  df.reset_index(drop=True, inplace=True)
  assert df.shape[0] == len(dob), 'DataFrame-Series mismatch'
  df['Dob'] = pd.to_datetime(pd.Series(dob))

  # append to previous results
  fighters = pd.concat([fighters, df], ignore_index=True)

print fighters
print fighters.info()
print fighters.describe()
print fighters.Stance.value_counts()
print fighters[fighters.Nickname.str.contains(',', na=False, regex=False)]
fighters.to_csv('../data/fightmetric_fighters/fightmetric_fighters.csv', index=False)
