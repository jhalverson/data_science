# Jonathan Halverson
# Wednesday, March 1, 2017
# This script compares three data sources and outputs large differences

import pprint
import numpy as np
import pandas as pd
pd.set_option('display.width', 150)

wiki = pd.read_csv('wikipedia_bdays_height_reach.csv', header=0, parse_dates=['Dob'])
wiki['Age'] = (pd.to_datetime('today') - wiki.Dob) / np.timedelta64(1, 'Y')
wiki.columns = ['Dob_wikipedia' if col == 'Dob' else col for col in wiki.columns]

ufc = pd.read_csv('ufc_dot_com_fighter_data_CLEAN_28Feb2017.csv', header=0)
ufc = ufc[['Name', 'Age', 'Reach', 'Height']]

fm = pd.read_csv('fightmetric_fighters/fightmetric_fighters.csv', header=0, parse_dates=['Dob'])
fm['Age'] = (pd.to_datetime('today') - fm.Dob) / np.timedelta64(1, 'Y')
fm = fm[['Name', 'Dob', 'Age', 'Reach', 'Height']]
fm.columns = ['Name', 'Dob_fightmetric', 'Age_fightmetric', 'Reach_fightmetric', 'Height_fightmetric']

s = ('_ufc', '_wikipedia')
tmp = pd.merge(ufc, wiki, on='Name', how='inner', suffixes=s)

s = ('', '_fightmetric')
tmp = pd.merge(tmp, fm, on='Name', how='inner', suffixes=s)

# display date of birth mismatches
pd.set_option('display.max_rows', 150)
cols = ['Name', 'Age_ufc', 'Age_wikipedia', 'Age_fightmetric', 'Dob_wikipedia', 'Dob_fightmetric']
j = tmp[(tmp.Dob_wikipedia != tmp.Dob_fightmetric) & pd.notnull(tmp.Age_fightmetric)][cols].applymap(lambda x: round(x, 1) if type(x) == float else x)
j = j[(j.Name != 'Michael McDonald')]
j = j[(j.Name != 'Dong Hyun Kim')]
j.reset_index(inplace=True, drop=True)
pprint.pprint(j)

# display reach mismatches
tmp['ReachDiff'] = np.abs(tmp.Reach_wikipedia - tmp.Reach_fightmetric)
h = tmp[tmp.ReachDiff > 2.0][['Name', 'Reach_ufc', 'Reach_wikipedia', 'Reach_fightmetric']]
h = h[(h.Name != 'Dong Hyun Kim')]
h.reset_index(inplace=True, drop=True)
pprint.pprint(h)

# display height mismatches
tmp['HeightDiff'] = np.abs(tmp.Height_wikipedia - tmp.Height_fightmetric)
k = tmp[tmp.HeightDiff > 2.0][['Name', 'Height_ufc', 'Height_wikipedia', 'Height_fightmetric']]
k = k[(h.Name != 'Dong Hyun Kim')]
k = k[(h.Name != 'Michael McDonald')]
k.reset_index(inplace=True, drop=True)
pprint.pprint(k)
