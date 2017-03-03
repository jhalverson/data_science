# Download zip file from EC2: scp -i "winter2017.pem" ec2-user@ec2-52-90-235-168.compute-1.amazonaws.com:pz.tar.gz .  

# flags to get updated data
scrape_fighters = False
scrape_birthdays = True
###################################

import time
import requests
session = requests.Session()
#session.headers = {}
#session.headers['User-Agent'] = 'Mozilla/5.0'
print session.headers
from bs4 import BeautifulSoup

# store the 26 characters of the English alphabet
import string
chars = string.ascii_lowercase

# scrape new fighter data if needed
base_path = 'fightmetric_fighters_'
if scrape_fighters:
  for char in chars:
    url = 'http://fightmetric.com/statistics/fighters?char=' + char + '&page=all'
    r = session.get(url)
    with open(base_path + char + '.html', 'w') as f:
      f.write(r.content)

# get list of all previously downloaded files
import os
import glob

header = ['First', 'Last', 'Nickname', 'Height', 'Weight', 'Reach',
          'Stance', 'Win', 'Loss', 'Draw', 'Belt']
chars = 'abcdefghijklmno'
chars = 'pqrstuvwxyz'
for char in chars:
  # read tables from html into a list of dataframes
  with open(base_path + char + '.html', 'r') as f:
    html = f.read()

  # we find the table rows and if an <img> tag is present (image of UFC belt) in the
  # row then we extract the name via the <a> tags (the find_all method is implied)
  soup = BeautifulSoup(html, 'lxml')
  for row in soup.findAll('tr', {'class':'b-statistics__table-row'}):
    # get link to individual fighter if exists
    if row.find('td', {'class':'b-statistics__table-col'}):
      if row.find('a'):
        if scrape_birthdays: time.sleep(0)
        url = row.find('a').get('href')
        # get page by scraping or from file
        iofile = url.split('/')[-1] + '.html'
        if scrape_birthdays:
          print char, url, iofile
          r = session.get(url, headers=session.headers)
          with open(iofile, 'w') as f:
            f.write(r.content)
