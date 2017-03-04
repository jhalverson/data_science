# Jonathan Halverson
# Sunday, February 26, 2017
# This script was designed to scrape Facebook pages by id and
# extract the person's location. It currently does not log in
# to Facebook which is a requirement for scraping.

import requests
from bs4 import BeautifulSoup

with open('fbids_MbtS.txt', 'r') as f:
  fbids = f.readlines()
fbids = [fbid.strip() for fbid in fbids]

data = {
    'lsd':'AVqAE5Wf',
    'charset_test': '',
    'version': 1,
    'ajax': 0,
    'width': 0,
    'pxr': 0,
    'gps': 0,
    'm_ts': 1392974963,
    'li': 'cxwHUxatQiaLv1nZEYPp0aTB'
}
data['email'] = 'halvers@mpip-mainz.mpg.de'
data['pass'] = '######'
data['login'] = 'Log In'


# class="_50f3"
locations = []
for fbid in ['1110657682282088']:
  url = 'http://www.facebook.com/' + fbid
  url = 'Ryan Layug.html'
  #soup = BeautifulSoup(requests.get(url, data=data).content, 'lxml')
  with open('Ryan Layug.html') as f: html = f.read()
  soup = BeautifulSoup(html, 'lxml')
  divs = soup('div')
  for div in divs:
    if 'Lives in' in div.get_text():
      link = div.find('a')
      if link: locations.append(link.string.strip())
print locations
