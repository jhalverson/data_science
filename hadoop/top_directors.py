# Jonathan Halverson
# Wednesday, January 18, 2017
# Scraping the-numbers.com data

import requests
from bs4 import BeautifulSoup

# download the HTML page
url = 'http://www.the-numbers.com/people/worldwide-records/technical-roles/Director'
r = requests.get(url)

# construct a parse tree using BeautifulSoup
s = BeautifulSoup(r.content, 'lxml')

#print len(s.find_all('table'))
#print s.find_all('table')
sct = s.find_all('table')

print sct
for item in sct.find_all('td', {'class':'data'}):
  print item.text

import sys; sys.exit(0)





for item in s.find_all('a'):
  print item.text

for item in s.find_all('tr'):
  print item.text
