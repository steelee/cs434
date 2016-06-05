import urllib2
import json
import os.path
from random import randint

if os.path.isfile("matches8.json") is False:
	print "Getting a new seed file, please wait..."
        localfile = open('matches8.json', 'aw')
	response = urllib2.urlopen('https://s3-us-west-1.amazonaws.com/riot-api/seed_data/matches1.json')
	html = response.read()
	localfile.write(html)
	data = json.loads(html)
else:
 	localfile = open('matches8.json')
	data = localfile.read()
	data = json.loads(data)
	print "Opened local file"

outfile = open('list.txt', 'aw+')
for count in range(0,100):
	outfile.write(str(data["matches"][count]["participantIdentities"][randint(0,1)]["player"]["summonerId"]))
	outfile.write("\n")
	outfile.write(str(data["matches"][count]["participantIdentities"][randint(2,3)]["player"]["summonerId"]))
	outfile.write("\n")
	outfile.write(str(data["matches"][count]["participantIdentities"][randint(4,5)]["player"]["summonerId"]))
	outfile.write("\n")
	outfile.write(str(data["matches"][count]["participantIdentities"][randint(6,7)]["player"]["summonerId"]))
	outfile.write("\n")
	outfile.write(str(data["matches"][count]["participantIdentities"][randint(8,9)]["player"]["summonerId"]))
	outfile.write("\n")
outfile.close()
