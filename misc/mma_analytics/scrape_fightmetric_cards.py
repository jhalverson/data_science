# Jonathan Halverson
# Wednesday, February 15, 2017

# flags to get updated data
scrape_event_list = False
scrape_cards = False
###################################

import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 200)

# scrape new fighter data if needed
events_file = 'fightmetric_cards/fightmetric_events.html'
if scrape_event_list:
  url = 'http://fightmetric.com/statistics/events/completed?page=all'
  r = requests.get(url)
  with open(events_file, 'w') as f:
    f.write(r.content)

# read list of events
with open(events_file, 'r') as f:
  html_events = f.read()

extracted = []
soup = BeautifulSoup(html_events, 'lxml')
events = soup.find('tbody').find_all('tr', {'class':'b-statistics__table-row'})[1:]
for tr in events:
  # extract title, date and url from the first row
  td_title_date = tr.find('td', {'class':'b-statistics__table-col'})
  link = td_title_date.find('a', {'class':'b-link b-link_style_black'})
  url = link.get('href')
  title = link.string.strip()
  date = td_title_date.find('span').string.strip()
  # extract location from second row
  td_location = tr.find('td', {'class':'b-statistics__table-col b-statistics__table-col_style_big-top-padding'})
  location = td_location.string.strip()

  # download page
  iofile = 'fightmetric_cards/' + url.split('/')[-1] + '.html'
  if scrape_cards:
    r = requests.get(url)
    with open(iofile, 'w') as f:
      f.write(r.content)

  # read html
  with open(iofile, 'r') as f:
    html_card = f.read()
  # extract table
  s = BeautifulSoup(html_card, 'lxml')
  for tr in s.find('tbody', {'class':'b-fight-details__table-body'}).find_all('tr'):
    td = tr.find_all('td')
    outcome = ''.join(td[0].get_text().strip().split())
    fighter1 = td[1].find_all('p')[0].get_text().strip()
    fighter2 = td[1].find_all('p')[1].get_text().strip()
    weight = td[6].find('p').get_text().strip()
    method = td[7].find_all('p')[0].get_text().strip()
    notes = td[7].find_all('p')[1].get_text().strip()
    round_ = td[8].find('p').get_text().strip()
    time = td[9].find('p').get_text().strip()
    extracted.append([outcome, fighter1, fighter2, weight, method, notes, round_, time, title, date, location])

fights = pd.DataFrame(extracted)
fights.columns = ['Outcome', 'Winner', 'Loser', 'WeightClass', 'Method', 'MethodNotes', 'Round', 'Time', 'Event', 'Date', 'Location']
fights.Outcome = fights.Outcome.replace({'win':'Win', 'drawdraw':'Draw', 'ncnc':'NC'})
cities = {'Sao Paulo, Sao Paulo, Brazil':'Sao Paulo, Brazil',
          'Barueri, Sao Paulo, Brazil':'Sao Paulo, Brazil',
          'New York City, New York, USA':'New York, New York, USA',
          'Brooklyn, New York, USA':'New York, New York, USA'}
fights.Location = fights.Location.replace(cities)
fights.Date = pd.to_datetime(fights.Date)
fights.Round = fights.Round.astype(int)
fights.to_csv('fightmetric_cards/fightmetrics_fights.csv', index=False)

#print fights[['Outcome', 'Winner', 'Loser', 'WeightClass', 'Method', 'Round', 'Time', 'Date', 'Location']]
print fights.groupby('Event').first().Location.value_counts()
print fights.groupby('Event').first().Date.apply(lambda x: x.year).value_counts()
print fights.WeightClass.value_counts()
print fights.Method.value_counts()
print fights[~fights.Event.str.contains('UFC|Ultimate|TUF')][['Winner', 'Loser', 'Time', 'Event', 'Date', 'Location']]

fighter = 'Conor McGregor'
fighter = 'Anderson Silva'
fighter = 'Nick Diaz'
fighter = 'Georges St-Pierre'
fighter = 'Michael Bisping'
print fights[(fights.Winner == fighter) | (fights.Loser == fighter)]

import sys
sys.exit(0)

from geopy.geocoders import Nominatim
for locale in fights.Location.unique():
  geolocator = Nominatim()
  location = geolocator.geocode(str(locale))
  if location: print locale, location.latitude, location.longitude
  else: print locale


