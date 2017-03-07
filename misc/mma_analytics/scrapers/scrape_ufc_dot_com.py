# Jonathan Halverson
# Monday, February 27, 2017
# This script scrapes current and former fighter data from ufc.com

import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from unidecode import unidecode

# store fields names in a set
skill = set()
info = set()

data = []
for i in range(0, 1900 + 1, 20):

  url = 'http://www.ufc.com/fighter/Weight_Class/filterFighters?offset=' + str(i)
  url += '&sort=lastName&order=asc&weightClass=&fighterFilter=All'

  soup = BeautifulSoup(requests.get(url).content, 'lxml')
  table = soup.find('table', {'class':'fighter-listing'})
  fighters = table('tr', {'class':'fighter'})
  for fighter in fighters:

    active = 0 if fighter.find('div', {'id':'former-fighter-title'}) else 1
    link = fighter.find('a', {'class':'fighter-name'})
    name = unidecode(link.string.strip())
    if name == "Davis LC": continue
    # LC Davis,,0,23-8-0,36.0,68.0,135.0,69.0,,"Kansas City, Missouri USA","Kansas City, Missouri USA",,,
    url = 'http://www.ufc.com' + link.get('href')
    s = BeautifulSoup(requests.get(url).content, 'lxml')
    name = unidecode(s.find('div', {'class':'floatl current', 'id':'fighter-breadcrumb'}).find('h1').string.strip())

    # get record and summary if available
    record = summary = ''
    div = s.find('div', {'class':'skill-breakdown', 'id':'skill-breakdown'})
    if div:
      for tr in div('tr'):
	td = tr('td')
	skill.add(td[0].string)
	if (td[0].get_text() == 'Record:'): record = td[1].get_text().strip()
	if (td[0].get_text() == 'Summary:'): summary = td[1].get_text().strip()
    print i, name, record
    # get data from fighter info block
    age = reach = height = weight = leg_reach = ''
    college = degree = nickname = fights_out = fighter_from = ''
    div = s.find('div', {'class':'fighter-info', 'id':'fighter-info'})
    if div:
      for tr in div('tr'):
	td = tr('td')
	key = td[0].get_text()
	value = td[1].get_text().strip()
	info.add(td[0].string)
	if (key == 'Age:'): age = value
	if (key == 'Height:'): height = value
	if (key == 'Weight:'): weight = value
	if ('Reach' in key and 'Leg' not in key): reach = value.replace('"', '')
	if ('Leg Reach' in key): leg_reach = value.replace('"', '')
	if (key == 'Nickname:'): nickname = value
	if (key == 'Fights Out Of:'): fights_out = value
	if (key == 'From:'): fighter_from = value
	if (key == 'College:'): college = value
	if (key == 'Degree:'): degree = value

    # clean, transform and replace empty values with NaN
    nickname = np.nan if nickname == '' else unidecode(nickname)
    record = np.nan if record == '' else record
    college = np.nan if college == '' else unidecode(college)
    degree = np.nan if degree == '' else unidecode(degree)
    summary = np.nan if summary == '' else unidecode(summary)
    fights_out = unidecode(' '.join(fights_out.split())) if fights_out != '' else np.nan
    fighter_from = unidecode(' '.join(fighter_from.split())) if fighter_from != '' else np.nan
    reach = np.nan if reach == '' else reach
    leg_reach = np.nan if leg_reach == '' else leg_reach
    age = np.nan if age == '' else age
    if height != '':
      assert '"' in height and '\'' in height, 'Height format is wrong'
      feet = height[:height.index('\'')].strip()
      inches = height[height.index('\'') + 1:height.index('"')].strip()
      height = 12.0 * int(feet) + int(inches)
    else:
      height = np.nan
    if weight != '':
      assert ('lb' in weight) and ('(' in weight) and (')' in weight), 'Weight format is wrong'
      weight = weight[:weight.index('lb')].strip()
    else:
      weight = np.nan
    data.append([name, nickname, active, record, age, height, weight, reach,
                 leg_reach, fights_out, fighter_from, college, degree, summary])

cols = ['Name', 'Nickname', 'Active', 'Record', 'Age', 'Height', 'Weight', 'Reach',
        'LegReach', 'OutOf', 'From', 'College', 'Degree', 'Summary']
df = pd.DataFrame(data, columns=cols)
df = df.astype({'Age':float, 'Weight':float, 'Reach':float, 'LegReach':float})
df.to_csv('../data/ufc_dot_com_fighter_data_RAW_28Feb2017.csv', index=False)
print df
print df.info()
print df.describe()

# print the fields
print skill
print info
