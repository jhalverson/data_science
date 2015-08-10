"""
Date: August 9, 2015
Author: Ryan Louie (ryan.louie@students.olin.edu)

Approach: The events are gathered through the RSS feed. This should
work if the institution is using the Trumba Calendar RSS Feed' tool.
"""

import os
import sys
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs

def save_json_array(json_array, outputDirectory, location):
    """ saves a json array of events, to an output directory,
    named {location + date + .json} """
    # save!
    date = datetime.now().date().__str__()
    out_file = os.path.join(
          outputDirectory
        , "%s_%s.json" % (location, date)
        )

    with open(out_file, mode='w') as feedsjson:
        for entry in json_array:
            json.dump(entry, feedsjson)
            feedsjson.write('\n')

def main(argv):
    if len(argv) < 2:

        print "Usage: python tufts.py <output_directory>"
        return

    outputDirectory = argv[1]

    base_url = "http://www.trumba.com/calendars/tufts.rss"
    r = requests.get(base_url)
    s = bs(r.content)

    tags = [
          'title'
        , 'description'
        , 'link'
        , 'x-trumba:ealink'
        , 'category'
        , 'pubDate'
    ]

    events = []

    for i, item in enumerate(s.find_all('item')):
        event = {}
        for tag in tags:
            try:
                event[tag] = item.find(tag).string
            except:
                continue
        events.append(event)

    save_json_array(events, outputDirectory, 'tufts')

if __name__ == '__main__':
    main(sys.argv)
