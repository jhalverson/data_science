# Jonathan Halverson
# Wednesday, April 5, 2017

# flags to get updated data
scrape_event_list = False
scrape_cards = False
scrape_individual_fights = True
###################################

import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 200)

from glob import glob
prev_cards = set(glob('../data/fightmetric_cards/*.html'))
prev_individ_fights = set(glob('../data/fightmetric_individual_fights/*.html'))

# scrape events list if needed
events_file = '../data/fightmetric_cards/fightmetric_events.html'
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
  print title, date, location

  # download page
  iofile = '../data/fightmetric_cards/' + url.split('/')[-1] + '.html'
  if scrape_cards and iofile not in prev_cards:
    r = requests.get(url)
    with open(iofile, 'w') as f:
      f.write(r.content)
  # read html
  with open(iofile, 'r') as f:
    html_card = f.read()

  # extract table
  s = BeautifulSoup(html_card, 'lxml')
  fight_details_links = s('a', {'class':'b-flag b-flag_style_green'})
  fight_details_urls = [link.get('href') for link in fight_details_links]

  for url in fight_details_urls:
    iofile = '../data/fightmetric_individual_fights/' + url.split('/')[-1] + '.html'
    if scrape_individual_fights and iofile not in prev_individ_fights:
      r = requests.get(url)
      with open(iofile, 'w') as f:
        f.write(r.content)
    # read html
    with open(iofile, 'r') as f:
      html_individ = f.read()

    sp = BeautifulSoup(html_individ, 'lxml')
    for tr in sp.find('tbody', {'class':'b-fight-details__table-body'}).find_all('tr'):
      td = tr('td')
      fighter1 = td[0].find_all('p')[0].get_text().strip()
      fighter2 = td[0].find_all('p')[1].get_text().strip()
      knockdowns1 = td[1].find_all('p')[0].get_text().strip()
      knockdowns2 = td[1].find_all('p')[1].get_text().strip()
      sig_strikes1 = td[2].find_all('p')[0].get_text().strip()
      sig_strikes2 = td[2].find_all('p')[1].get_text().strip()
      # ignore sig. str. percentage
      total_strikes1 = td[4].find_all('p')[0].get_text().strip()
      total_strikes2 = td[4].find_all('p')[1].get_text().strip()
      takedowns1 = td[5].find_all('p')[0].get_text().strip()
      takedowns2 = td[5].find_all('p')[1].get_text().strip()
      # ignore takedown percentage
      sub_att1 = td[7].find_all('p')[0].get_text().strip()
      sub_att2 = td[7].find_all('p')[1].get_text().strip()
      pass1 = td[8].find_all('p')[0].get_text().strip()
      pass2 = td[8].find_all('p')[1].get_text().strip()
      reversal1 = td[9].find_all('p')[0].get_text().strip()
      reversal2 = td[9].find_all('p')[1].get_text().strip()

      # split on of
      sig_strikes_landed1 = sig_strikes1.split(' of ')[0]
      sig_strikes_attempts1 = sig_strikes1.split(' of ')[1]
      sig_strikes_landed2 = sig_strikes2.split(' of ')[0]
      sig_strikes_attempts2 = sig_strikes2.split(' of ')[1]

      tot_strikes_landed1 = total_strikes1.split(' of ')[0]
      tot_strikes_attempts1 = total_strikes1.split(' of ')[1]
      tot_strikes_landed2 = total_strikes2.split(' of ')[0]
      tot_strikes_attempts2 = total_strikes2.split(' of ')[1]

      td_landed1 = takedowns1.split(' of ')[0]
      td_attempts1 = takedowns1.split(' of ')[1]
      td_landed2 = takedowns2.split(' of ')[0]
      td_attempts2 = takedowns2.split(' of ')[1]

      extracted.append([date,
			fighter1, fighter2,
			knockdowns1, knockdowns2,
			sig_strikes_landed1, sig_strikes_attempts1,
			sig_strikes_landed2, sig_strikes_attempts2,
			tot_strikes_landed1, tot_strikes_attempts1,
			tot_strikes_landed2, tot_strikes_attempts2,
			td_landed1, td_attempts1,
			td_landed2, td_attempts2,
			sub_att1, sub_att2,
			pass1, pass2,
			reversal1, reversal2])

individ_fights = pd.DataFrame(extracted)
individ_fights.columns = ['Date', 'Fighter1', 'Fighter2',
                          'Knockdowns1', 'Knockdowns2',
                          'SigStrikesLanded1', 'SigStrikesAttempted1',
                          'SigStrikesLanded2', 'SigStrikesAttempted2',
                          'TotStrikesLanded1', 'TotStrikesAttempted1',
                          'TotStrikesLanded2', 'TotStrikesAttempted2',
                          'TakedownLanded1', 'TakedownAttempted1',
                          'TakedownLanded2', 'TakedownAttempted2',
                          'SubsAttempted1', 'SubsAttempted2',
                          'Pass1', 'Pass2',
                          'Reversal1', 'Reversal2']
individ_fights.to_csv('../data/fightmetric_individual_fights/detailed_stats_individual_fights.csv', index=False)
