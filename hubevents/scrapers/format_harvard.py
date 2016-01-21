"""
Date: November 16, 2015
Author: Jonathan Halverson (halverson.jonathan@gmail.com)

This code formats the Harvard University scraping data.
"""

import json
with open('harvard_university.json') as data_file:
  events = json.load(data_file)

print '<html><head></head><body><p>'
for event in events:
  print '%s<p>' % event['title'].encode('ascii', 'ignore')
  edt = event['date_time'].replace('am  on', 'am on').replace('pm  on', 'pm on').encode('ascii', 'ignore')
  edt = edt.replace('Mon.', 'Monday').replace('Tue.', 'Tuesday').replace('Wed.', 'Wednesday')
  edt = edt.replace('Thu.', 'Thursday').replace('Fri.', 'Friday')
  edt = edt.replace('Sat.', 'Saturday').replace('Sun.', 'Sunday')
  edt = edt.replace('Jan.', 'January')
  edt = edt.replace('Feb.', 'February')
  edt = edt.replace('Mar.', 'March')
  edt = edt.replace('Apr.', 'April')
  edt = edt.replace('Jun.', 'June')
  edt = edt.replace('Jul.', 'July')
  edt = edt.replace('Aug.', 'August')
  edt = edt.replace('Sep.', 'September')
  edt = edt.replace('Oct.', 'October')
  edt = edt.replace('Nov.', 'November')
  edt = edt.replace('Dec.', 'December')

  weekday_month_day, time_range = edt.split(', 201')
  hours = ('').join(time_range[3:].split(' ')) # remove white space
  hours = hours.replace('-', ' - ').replace('a.m.', ' AM').replace('p.m.', ' PM')
  print weekday_month_day + '<br>'
  print hours + '<br>'
  print 'Harvard University, ' + event['building'] + '<p>'

  print '\n'

  if ('speaker' in event): print 'Speaker(s): %s<br>' % event['speaker']

  d = event['description'].replace('<b>', '').replace('</b>', '')
  target = '<br /><br />'
  if (target in d):
    d = d[d.index(target) + len(target):]

  target = 'Gazette Classification:&nbsp;'
  if (target in d):
    d = d[:d.index(target)] + d[d.find(' <br />', d.index(target) + len(target)) + len('<br />') + 1:]
    print '%s\n' % d
  else:
    print '%s\n' % d

  #TODO: remove image
  #target = '<img height'

  if ('more_info_url' in event): print 'More info: %s<br>' % event['more_info_url']
  if ('register_url' in event): print 'RSVP at: %s<br>' % event['register_url']
  if ('register_deadline' in event): print 'Registration deadline: %s<br>' % event['register_deadline']
  if ('contact_organization' in event): print 'Contact organization: %s<br>' % event['contact_organization'].encode('ascii', 'ignore')
  if ('phone' in event): print 'Phone : %s<br>' % event['phone']
  if ('contact_name' in event): print 'Contact name: %s<br>' % event['contact_name']
  if ('contact_email' in event):
    if (event['contact_email']):
      print 'Contact email: %s<br>' % event['contact_email'].encode('ascii', 'ignore')
  print 'Source: %s<p>' % event['credit_url']
  print '<p><p>\n\n--------------------\n\n<p><p>'
print '</body></html>'
