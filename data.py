import urllib2
import json
from secrets import *
from pprint import pprint
# Globals for the URL
SEASON = "SEASON2015"
VERSION = "v1.3"

with open('list.txt', 'rU') as f:
  for line in f:
     url = "https://na.api.pvp.net/api/lol/na/" + VERSION + "/stats/by-summoner/" + line.rstrip() + "/ranked?season=" + SEASON + "&api_key=" + API_KEY
     result = urllib2.urlopen(url)
     data = json.load(result)
     print(data["champions"][0])
