"""
Date: November 16, 2015
Author: Jonathan Halverson (halverson.jonathan@gmail.com)

Usage: python format_bu.py > bu_24june2016.txt

This code formats the Boston University scraping data.
"""

import json
with open('boston_university.json') as data_file:
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

for event in events:
  print '%s' % event['title']
  edt = event['date_time'].replace('am  on', 'am on').replace('pm  on', 'pm on').encode('ascii', 'ignore')
  print printDate(edt)

  local = ['Boston University']
  if ('location' in event.keys()): local.append(event['location'])
  if ('building' in event.keys()): local.append(event['building'])
  if ('room' in event.keys()): local.append('Room ' + event['room'])
  print ', '.join(local)
  if ('cost' in event.keys()):
    if (event['cost'].strip().lower() != 'free'): print 'Cost: %s' % event['cost']
  if ('open_to' in event.keys()): print 'Open to: %s' % event['open_to'].replace('\n', ' ')

  print '\n'

  if ('speaker' in event.keys()): print 'Speaker(s): %s' % event['speaker']
  print '%s\n' % event['description']

  if ('more_info_url' in event.keys()): print 'More info: %s' % event['more_info_url']
  if ('register_url' in event.keys()): print 'RSVP at: %s' % event['register_url']
  if ('register_deadline' in event.keys()): print 'Registration deadline: %s' % event['register_deadline']
  if ('contact_organization' in event.keys()): print 'Contact organization: %s' % event['contact_organization']
  if ('phone' in event.keys()): print 'Phone : %s' % event['phone']
  if ('contact_name' in event.keys()): print 'Contact name: %s' % event['contact_name']
  if ('contact_email' in event.keys()): print 'Contact email: %s' % event['contact_email']
  print 'Source: %s' % event['credit_url']
  print '\n\n--------------------\n\n'
