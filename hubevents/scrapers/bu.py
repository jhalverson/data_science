"""
Date: August 8, 2015
Author: Jonathan Halverson (halverson.jonathan@gmail.com)

Approach: We first get the HTML for each day in the desired range. For each
day we extract the urls to the various events. These pages are downloaded
and one-by-one the event info is extracted.
"""

import requests
from bs4 import BeautifulSoup

days = ['2015-8-' + str(day) for day in range(10, 20)]

base_url = 'http://www.bu.edu'
unique_href = '.calendar.bu.edu'

trans = {'When':'date_time', 'Contact Name':'contact_name',
         'Contact Email':'contact_email', 'Contact Organization':'contact_organization',
         'Phone':'phone', 'Location':'location', 'Building':'building', 'Fees':'cost',
         'Room':'room', 'Open To':'open_to', 'Fee': 'cost', 'Speakers':'speaker'}

events = []
for day in days:
  r = requests.get(base_url + '/calendar/?day=' + day)
  s = BeautifulSoup(r.content, 'lxml')
  urls = [a.get('href') for a in s.find_all('a') if (unique_href in a.get('href'))]
  for url in urls:
    event = {'credit_url':base_url + url}
    r = requests.get(base_url + url)
    s = BeautifulSoup(r.content, 'lxml')
    try:
      sct = s.find('section', {'id':'event-detail'})
    except:
      continue
    if (sct.find('h1')):
      event['title'] = sct.find('h1').text
      event['description'] = sct.find('p').text
      for td, th in zip(sct.find_all('td'), sct.find_all('th')):
	th_key = th.text
	if (th_key not in trans.keys()):
	  th_key = th_key.replace(' ', '_').lower()
	  event[th_key] = td.text
	  print "WARNING:", th.text, "converted to", th_key, "and added to dictionary"
	else:
	  event[trans[th_key]] = td.text
      if (sct.find('a', {'class':'more-info'})):
        event['more_info_url'] = sct.find('a', {'class':'more-info'}).get('href')
      if (sct.find('a', {'class':'register'})):
        event['register_url'] = sct.find('a', {'class':'register'}).get('href')
      if (sct.find('span', {'class':'deadline'})):
        event['register_deadline'] = sct.find('span', {'class':'deadline'}).text
      events.append(event)

import json
with open('boston_university.json', 'w') as outfile:
  json.dump(events, outfile)
