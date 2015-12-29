"""
Date: November 16, 2015
Author: Jonathan Halverson (halverson.jonathan@gmail.com)

This code formats the Boston University scraping data.
"""

import json
with open('harvard_university.json') as data_file:
  events = json.load(data_file)

def printDate(e):
  import datetime
  days = [datetime.date(2001, 1, i).strftime('%A,') for i in range(1, 8)]
  months = [datetime.date(2001, i, 1).strftime('%B') for i in range(1, 13)]
  hr_min = [str(i) + ':0' + str(j) for i in range(1, 13) for j in range(0, 10)]
  hr_min += [str(i) + ':' + str(j) for i in range(1, 13) for j in range(10, 60)]
  items = e.split()
  if (len(items) == 10 and
      items[0] in hr_min and
      items[3] in hr_min and
      items[6] in days and
      items[7] in months):
    fmt = ' '.join([items[0], items[1].upper(), '-', items[3], items[4].upper()])
    return '%s %s %s\n%s' % (items[6], items[7], items[8].rstrip(','), fmt)
  elif (len(items) == 7 and
      items[0] in hr_min and
      items[3] in days and
      items[4] in months):
    fmt = ' '.join([items[0], items[1].upper()])
    return '%s %s %s\n%s' % (items[3], items[4], items[5].rstrip(','), fmt)
  else:
    return e

print '<html><head></head><body><p>'
for event in events:
  print '%s<p>' % event['title'].encode('ascii', 'ignore')
  edt = event['date_time'].replace('am  on', 'am on').replace('pm  on', 'pm on').encode('ascii', 'ignore')
  #print printDate(edt) + '<br>'

  local = ['Harvard University']
  #if ('location' in event.keys()): local.append(event['location'])
  #if ('building' in event.keys()): local.append(event['building'])
  #if ('room' in event.keys()): local.append('Room ' + event['room'])
  print ', '.join(local) + '<br>'
  #if ('cost' in event.keys()):
  #  if (event['cost'].strip().lower() != 'free'): print 'Cost: %s<br>' % event['cost'].encode('ascii', 'ignore')
  #if ('open_to' in event.keys()): print 'Open to: %s<br>' % event['open_to'].replace('\n', ' ')

  print '\n'

  if ('speaker' in event.keys()): print 'Speaker(s): %s<br>' % event['speaker']

  d = event['description'].replace('<b>', '').replace('</b>', '')
  target = '<br />Gazette Classification:&nbsp;'
  if (target in d):
    d = d[:d.index(target)] + d[d.find(' <br />', d.index(target) + len(target)):]
    print '%s<p>\n' % d
  else:
    print '%s<p>\n' % d

  if ('more_info_url' in event.keys()): print 'More info: %s<br>' % event['more_info_url']
  if ('register_url' in event.keys()): print 'RSVP at: %s<br>' % event['register_url']
  if ('register_deadline' in event.keys()): print 'Registration deadline: %s<br>' % event['register_deadline']
  if ('contact_organization' in event.keys()): print 'Contact organization: %s<br>' % event['contact_organization'].encode('ascii', 'ignore')
  if ('phone' in event.keys()): print 'Phone : %s<br>' % event['phone']
  if ('contact_name' in event.keys()): print 'Contact name: %s<br>' % event['contact_name']
  if ('contact_email' in event.keys()): print 'Contact email: %s<br>' % event['contact_email']
  print 'Source: %s<p>' % event['credit_url']
  print '<p><p>\n\n--------------------\n\n<p><p>'
print '</body></html>'
