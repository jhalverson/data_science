"""
Date: August 25, 2015
Author: Tom Lukasiak

Approach: Parse the RSS feed. Use BeautifulSoup for parsing HTML inside the RSS feed entries.
"""

# All categories
RSS_URL = 'http://www.trumba.com/calendars/gazette.rss?filterview=Gazette+Classification'

import feedparser
from IPython.display import HTML
from bs4 import BeautifulSoup
import json

def parse_rss(rss):
    events = []
    for entry in rss.entries:
        event = {}
        event['title'] = entry['title']
        event['credit_url'] = entry['link']

        # Most of the interesting information is in the HTML-formatted summary
        event['description'] = entry['summary']
        # BeautifulSoup is a good way to parse this HTML
        soup = BeautifulSoup(event['description'], 'lxml')
        
        items = soup.find('p').findAll(text=True)
        date_found = False
        for idx, item in enumerate(items):
            if item[:4] in ['Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.', 'Sun.']:
                date_found = True
                dt = item.strip()
                dt = dt.replace(u'\xa0', '')
                event['date_time'] = dt.replace(u'\u2013', '-')
                assert(len(event['date_time'].split(','))>2)
                
                event['building'] = ', '.join(items[:idx]).strip()
        if not date_found:
            print items
        
        # There may be some other interesting tags in some entries...future work maybe :)
        for node in soup.findAll('b'):
            node_text = ''.join(node.findAll(text=True))
            if node_text == 'Gazette Classification':
                event['category'] = node.next.next[2:].strip()
            elif node_text == 'Organization/Sponsor':
                event['contact_organization'] = node.next.next[2:].strip()
            elif node_text == 'Cost':
                event['cost'] = node.next.next[2:].strip()
            elif node_text == 'Contact Info':        
                event['contact_email'] = node.next.next.next.find(text=True)
            elif node_text == 'More info':        
                event['more_info_url'] = node.next.next.next['href']     
            else:
                pass
        events.append(event)
    return events
        
if __name__ == '__main__':
    rss = feedparser.parse(RSS_URL)
    events = parse_rss(rss)
    with open('harvard_university.json', 'w') as outfile:
        json.dump(events, outfile)