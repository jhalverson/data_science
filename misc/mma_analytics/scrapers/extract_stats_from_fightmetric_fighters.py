import glob
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

records = []
html_files = glob.glob('../data/fightmetric_fighters/*.html')
html_files = filter(lambda x: 'fightmetric_fighters_' not in x, html_files)
for i, html_file in enumerate(html_files):
  print i, html_file
  with open(html_file) as f:
    html = f.read()
  soup = BeautifulSoup(html, 'lxml')
  name = soup.find('span', {'class':'b-content__title-highlight'})

  slpm = str_acc = sapm = str_def = td_avg = td_acc = td_def = sub_avg = '-100'
  li_tags = soup('li', {'class':'b-list__box-list-item b-list__box-list-item_type_block'})
  for li_tag in li_tags:
    txt = li_tag.get_text()
    if ('SLpM:' in txt): slpm = txt.replace('SLpM:', ' ').strip()
    if ('Str. Acc.:' in txt): str_acc = txt.replace('Str. Acc.:', ' ').strip()
    if ('SApM:' in txt): sapm = txt.replace('SApM:', ' ').strip()
    if ('Str. Def:' in txt): str_def = txt.replace('Str. Def:', ' ').strip()
    if ('TD Avg.:' in txt): td_avg = txt.replace('TD Avg.:', ' ').strip()
    if ('TD Acc.:' in txt): td_acc = txt.replace('TD Acc.:', ' ').strip()
    if ('TD Def.:' in txt): td_def = txt.replace('TD Def.:', ' ').strip()
    if ('Sub. Avg.:' in txt): sub_avg = txt.replace('Sub. Avg.:', ' ').strip()

  slpm = float(slpm)
  str_acc = float(str_acc.replace('%', '')) / 100.0
  sapm = float(sapm)
  str_def = float(str_def.replace('%', '')) / 100.0
  td_avg = float(td_avg)
  td_acc = float(td_acc.replace('%', '')) / 100.0
  td_def = float(td_def.replace('%', '')) / 100.0
  sub_avg = float(sub_avg)

  print name.string.strip(), slpm, str_acc, sapm, str_def, td_avg, td_acc, td_def, sub_avg
  assert slpm > -0.1, 'slpm'
  assert str_acc > -0.1, 'slpm'
  assert sapm > -0.1, 'slpm'
  assert str_def > -0.1, 'slpm'
  assert td_avg > -0.1, 'slpm'
  assert td_acc > -0.1, 'slpm'
  assert td_def > -0.1, 'slpm'
  assert sub_avg > -0.1, 'slpm'

  records.append((name.string.strip(), slpm, str_acc, sapm, str_def, td_avg, td_acc, td_def, sub_avg))
  cols = ['Name', 'slpm', 'str_acc', 'sapm', 'str_def', 'td_avg', 'td_acc', 'td_def', 'sub_avg']
  df = pd.DataFrame(records, columns=cols)
  df.to_csv('../data/fightmetric_career_stats.csv', index=False)
