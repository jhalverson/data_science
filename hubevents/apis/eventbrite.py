## Usage: ##
##   python eventbrite.py > boston_13nov2015.html ##

start_date = '2015-12-1'
end_date = '2015-12-5'

import os
my_token = os.environ['EVENTBRITE_SHELL_VAR']

url = 'https://www.eventbriteapi.com/v3/events/search/?start_date.range_start=' \
      + start_date + 'T13:00:00Z&start_date.range_end=' \
      + end_date + 'T13:00:00Z&token=' + my_token

import requests
payload = {'venue.city':'Cambridge', 'venue.region':'MA', 'venue.country':'US',
           'sort_by':'date', 'expand':'organizer,venue,ticket_classes', 'token':my_token}
response = requests.get(url, params=payload, headers = {"Authorization": "Bearer " + my_token,}, verify = True)
r = response.json()['events']

## 50 records per page so may need multiple pages ##
page_count = int(response.json()['pagination']['page_count'])
for p in range(2, page_count + 1):
  url += '&page=' + str(p)
  response = requests.get(url, params=payload, headers = {"Authorization": "Bearer " + my_token,}, verify = True)
  r.extend(response.json()['events'])

## start HTML output ##
print '<html><head></head><body>'
print 'page_count: ', page_count, ', total events: ', len(r), '<p><p>'
print '-------------------------------<p><p>'

## create list from all the records ##
for i, rr in enumerate(r):
  str_d = rr['start']['local']
  end_d = rr['end']['local']
  from datetime import date
  from datetime import time
  d_str = date(*map(int, str_d.split('T')[0].split('-')))
  d_end = date(*map(int, end_d.split('T')[0].split('-')))
  t_str = time(*map(int, str_d.split('T')[1].split(':')))
  t_end = time(*map(int, end_d.split('T')[1].split(':')))

  ## title and date ##
  title = rr['name']['text']
  if (title):
    print title.encode('ascii', 'ignore'), "<br>"
  if (d_str == d_end):
    print '{dt:%A}, {dt:%B} {dt.day}<br>'.format(dt=d_str) # requires Python 2.6
  else:
    print '{dt:%A}, {dt:%B} {dt.day}'.format(dt=d_str), '-', '{dt:%A}, {dt:%B} {dt.day}<br>'.format(dt=d_end)
  print t_str.strftime('%-I:%M %p'), '-', t_end.strftime('%-I:%M %p'), "<br>" # hack: remove zero padding

  ## location ##
  lctn = []
  venue_name = rr['venue']['name']
  if (venue_name): lctn.append(venue_name.encode('ascii', 'ignore'))
  venue_city = rr['venue']['address']['city']
  if (venue_city): lctn.append(venue_city.encode('ascii', 'ignore'))
  a1 = rr['venue']['address']['address_1']
  if (a1): lctn.append(a1.encode('ascii', 'ignore'))
  a2 = rr['venue']['address']['address_2']
  if (a2): lctn.append(a2.encode('ascii', 'ignore'))
  print '%s<br>' % ', '.join(lctn)

  ## rsvp ##
  rsvp = rr['url']
  if (rsvp):
    url = rsvp.rstrip('?aff=ebapi')
    print 'RSVP at <a href="' + url + '" target="_blank">' + url + '</a><br>'

  ## ticket cost ##
  ## note ticket can be free, donation or a cost ##
  ## if not free and not donation then cost ##
  costs = []
  num_tix = len(rr['ticket_classes'])
  for j in range(num_tix):
    tix = rr['ticket_classes'][j]
    if (tix['free']): costs.append('FREE')
    elif (not tix['free'] and tix['donation']): costs.append('Donation')
    elif (not tix['free'] and not tix['donation']):
      costs.append(tix['cost']['display'].encode('ascii', 'ignore'))
    else:
      print 'ERROR: SHOULD NOT BE HERE: ', tix['free'], tix['donation']
 
  # ensure FREE and Donation appear first
  costs = list(set(costs)) # remove duplicates
  if ('Donation' in costs):
    costs.remove('Donation')
    costs.insert(0, 'Donation')
  if ('FREE' in costs):
    costs.remove('FREE')
    costs.insert(0, 'FREE')
  if (costs != ['FREE'] and costs): print 'Cost:', ', '.join(costs), '<p>'
  else: print '<p>'

  ## description ##
  dscrpt = rr['description']['text']
  if (dscrpt):
    print '%s<p>' % dscrpt.encode('ascii', 'ignore')

  print '<p><p>-------------------------------<p><p>'
print '</body></html>'
