import urllib2
import json
import csv
import collections
import time
import requests
from requests.exceptions import HTTPError

try:
		# API_KEY="d8f924f5-8658-4786-8df3-8e8f86b05a68" #dvslanti
		API_KEY="ce7efa3b-d7f5-41dc-909e-b11ace8dbd1b" #darnmarshall
except ImportError:
		raise ImportError('You need your API key in a secret file! See the README')

# Globals for the URL
SEASON = "SEASON2015"
VERSION_STATS = "v1.3"
VERSION_RANK = "v2.5"

# Ranking integers:
rank = {'BRONZE':0, 'SILVER':1, 'GOLD':2, 'PLATINUM':3, 'DIAMOND':4, 'MASTER':5, 'CHALLENGER':6}

def aggregate(data_array):
	player_data_aggregate = [0,0,0,0,0,0,0,0,0,0,0,0,0]
	total_champions = len(data_array)
	for count in range(0,len(data_array)):
		player_data_aggregate[0] += data_array[count]["stats"]["totalPhysicalDamageDealt"]
		player_data_aggregate[1] += data_array[count]["stats"]["totalTurretsKilled"]
		player_data_aggregate[2] += data_array[count]["stats"]["totalSessionsPlayed"]
		player_data_aggregate[3] += data_array[count]["stats"]["totalAssists"]
		player_data_aggregate[4] += data_array[count]["stats"]["totalDamageDealt"]
		player_data_aggregate[5] += data_array[count]["stats"]["totalDeathsPerSession"]
		player_data_aggregate[6] += data_array[count]["stats"]["totalSessionsWon"]
		player_data_aggregate[7] += data_array[count]["stats"]["totalGoldEarned"]
		player_data_aggregate[8] += data_array[count]["stats"]["totalChampionKills"]
		player_data_aggregate[9] += data_array[count]["stats"]["totalMinionKills"]
		player_data_aggregate[10] += data_array[count]["stats"]["totalSessionsLost"]
		player_data_aggregate[11] += data_array[count]["stats"]["totalDamageTaken"]
		player_data_aggregate[12] += data_array[count]["stats"]["totalMagicDamageDealt"]
	
	for count in range(0,len(player_data_aggregate)):
		player_data_aggregate[count] = player_data_aggregate[count]/total_champions 
	
	return player_data_aggregate

outfile = open('features8.csv', 'aw+')
outfile_results = open('target8.csv', 'aw+')
countline = 0

with open('list8.txt', 'rU') as f:
	for line in f:
		countline += 1
		print countline
		not_found = False
		# First we'll write the features
		url_data = "https://na.api.pvp.net/api/lol/na/" + VERSION_STATS + "/stats/by-summoner/" + line.rstrip() + "/ranked?season=" + SEASON + "&api_key=" + API_KEY
		try:
			result_champions = urllib2.urlopen(url_data)
		except urllib2.HTTPError:
			time.sleep(30)
			try:
				result_champions = urllib2.urlopen(url_data)
			except urllib2.HTTPError:
				print "No match data found for ", line.rstrip()
				not_found = True
		url_rank = "https://na.api.pvp.net/api/lol/na/" + VERSION_RANK + "/league/by-summoner/" + line.rstrip() + "/entry?api_key=" + API_KEY
		try:
			result_rank = urllib2.urlopen(url_rank)
		except urllib2.HTTPError:
			time.sleep(5)
			try:
				result_rank = urllib2.urlopen(url_rank)
			except urllib2.HTTPError:
				print "No ranked league found for ", line.rstrip()
				not_found = True
		if not not_found:
			# First write features
			data = json.load(result_champions)
			weight = aggregate((data["champions"]))
			data_string = ','.join(map(str, weight))
			outfile.write(data_string)
			outfile.write("\n")
	
			# Now write the target
			data = json.load(result_rank)
			print "Rank: ", data[line.rstrip()][0]["tier"]
			outfile_results.write(str(rank[data[line.rstrip()][0]["tier"]]))
			outfile_results.write("\n")
		
			# We don't want too may requests too fast, or we get rate-limited
			time.sleep(5)

outfile.close()
outfile_results.close()
f.close()
