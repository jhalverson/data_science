# Jonathan Halverson
# Saturday, February 25, 2017

import os
import json
import facebook
import requests

if __name__ == '__main__':
  token = os.environ.get('FACEBOOK_TEMP_TOKEN')
  graph = facebook.GraphAPI(token)
  profile = graph.get_object('me', fields='name,location{location},birthday,friends')
  posts = graph.get_connections('me', 'posts')
  while 1:
    try:
      for post in posts['data']:
        print post
      posts = requests.get(posts['paging']['next']).json()
    except KeyError:
      break

  print json.dumps(profile, indent=4)
