# Jonathan Halverson
# Friday, March 3, 2017
# Choropleth map of US counties

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def draw_us_map():
  fig, ax = plt.subplots()
  # Set the lower left and upper right limits of the bounding box:
  lllon = -119
  urlon = -64
  lllat = 22.0
  urlat = 50.5
  # and calculate a centerpoint, needed for the projection:
  centerlon = float(lllon + urlon) / 2.0
  centerlat = float(lllat + urlat) / 2.0

  m = Basemap(resolution='i',  # crude, low, intermediate, high, full
	      llcrnrlon = lllon, urcrnrlon = urlon,
	      lon_0 = centerlon,
	      llcrnrlat = lllat, urcrnrlat = urlat,
	      lat_0 = centerlat,
	      projection='tmerc')

  # Read state boundaries.
  shp_info = m.readshapefile('st99_d00', 'states', drawbounds=True, color='lightgrey')

  # Read county boundaries
  shp_info = m.readshapefile('cb_2015_us_county_500k', 'counties', drawbounds=False)

  MAXSTATEFP = 78
  states = [None] * MAXSTATEFP
  for state in m.states_info:
      statefp = int(state["STATE"])
      # Many states have multiple entries in m.states (because of islands).
      # Only add it once.
      if not states[statefp]:
	  states[statefp] = state["NAME"]

  import pandas as pd
  df = pd.read_csv('county.txt', sep='\t', header=0)
  df = df.astype({'poverty':float})
  df = df.astype({'pop2010':float})
  df = df.astype({'med_income':float})
  cts = set([c.replace(' County', '').replace(' Parish', '').strip() for c in df.name.tolist()])
  print df.info()
  print df.describe()

  county_colors = {}
  for county, st, poverty in zip(df.name.tolist(), df.state.tolist(), df.poverty.tolist()):
      # What color is this county?
      red = poverty / df.poverty.max()
      county_colors["%s, %s" % (county.replace(' County', '').replace(' Parish', '').strip(), st)] = (1-red, red, 0)

  for i, county in enumerate(m.counties_info):
      countyname = county["NAME"]
      try:
	  statename = states[int(county["STATEFP"])]
      except IndexError:
	  print countyname, "has out-of-index statefp of", county["STATEFP"]
	  continue

      countystate = "%s, %s" % (countyname, statename)
      try:
	  ccolor = county_colors[countystate]
      except KeyError:
	  # No exact match; try for a fuzzy match
	  print "Color key not found", countystate
	  continue
	  """
	  fuzzyname = fuzzy_find(countystate, county_colors.keys())
	  if fuzzyname:
	      ccolor = county_colors[fuzzyname]
	      county_colors[countystate] = ccolor
	  else:
	      print "No match for", countystate
	      continue
	  """

      countyseg = m.counties[i]
      if statename == 'Hawaii':
	  countyseg = list(map(lambda (x,y): (x + 5750000, y-1400000), countyseg))
      poly = Polygon(countyseg, facecolor=ccolor)  # edgecolor="white"
      ax.add_patch(poly)

if __name__ == "__main__":
  draw_us_map()
  plt.title('Poverty by US Counties (green is high)')
  plt.tight_layout(pad=0, w_pad=0, h_pad=0)
  plt.show()
