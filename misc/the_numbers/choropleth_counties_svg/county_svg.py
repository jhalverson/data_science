# Jonathan Halverson
# Friday, March 3, 2017
# Usage: python county_svg.py > poverty.svg
# This script makes a choropleth map of us counties
# http://flowingdata.com/2009/11/12/how-to-make-a-us-county-thematic-map-using-free-tools/

import pandas as pd
from bs4 import BeautifulSoup

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'}

# create a list of counties found in the SVG file
svg_counties = []
svg = open('USA_Counties_with_FIPS_and_names.svg', 'r').read()
#soup = BeautifulSoup(svg, 'lxml', selfClosingTags=['defs', 'sodipodi:namedview'])
soup = BeautifulSoup(svg, 'lxml')
for path in soup('path'):
  try:
    svg_counties.append(path['inkscape:label'])
  except:
    pass

# read in the census data
df = pd.read_csv('county.txt', sep='\t', header=0)
df.name = df.name.str.replace(' County| Parish', '')
df.state = df.state.replace(us_state_abbrev)
df = df.astype({'poverty':float})

# create a list of counties found in the data
data_counties = []
for c, s in zip(df.name, df.state):
  data_counties.append(c + ', ' + s)

#print set(svg_counties) - set(data_counties)
#print set(data_counties) - set(svg_counties)

# associate county with its numerical value
poverty = {}
for c, s, p in zip(df.name, df.state, df.poverty):
  poverty[c + ', ' + s] = 12 * (p / df.poverty.max())

# map colors
colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

# county style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

# Color the counties based on poverty rate
for p in soup('path'):
  if p['id'] not in ["State_Lines", "separator"]:
    try:
      rate = poverty[p['inkscape:label']]
    except:
      continue

    if rate > 10:
      color_class = 5
    elif rate > 8:
      color_class = 4
    elif rate > 6:
      color_class = 3
    elif rate > 4:
      color_class = 2
    elif rate > 2:
      color_class = 1
    else:
      color_class = 0

    p['style'] = path_style + colors[color_class]

print soup
