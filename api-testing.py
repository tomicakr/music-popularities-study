#!/usr/bin/python
from pyspark import SparkContext
import re
import math
import requests
import json

sc = SparkContext()

def extract2017Hdi(line):
	words = re.split(',', line)
	country = words[1].replace('"', '').lower()
	hdi = words[-1].replace('"', '')
	return (country, float(hdi))

def filterNonExistant(line):
	words = re.split(',', line)
	#print(words[-1])
	return words[-1].replace('"', '').replace('.','').isdigit()

hdis = './hdis.csv'
file = sc.textFile(hdis)
country_hdi = sc.textFile(hdis).filter(filterNonExistant)
country_hdi = country_hdi.map(extract2017Hdi)

# for line in country_hdi.collect():
# 	# words = re.split(',', line)
# 	# country = words[1]
# 	# hdi = words[-1]
# 	country, hdi = line
# 	print("{} : {}".format(country, hdi))

first = country_hdi.collect()[0]
response = requests.get("http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={}&api_key=101c6972f8adf89c5f3bdf67ff0efa0c&format=json".format(first[0]))
response = json.loads(response.content)

#print(json.dumps(response, indent=2))
#print(json.dumps(response['tracks']['track'][0]['mbid'], indent=2))
mbid = response['tracks']['track'][0]['mbid'].replace('"', '')

response = requests.get("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=101c6972f8adf89c5f3bdf67ff0efa0c&mbid={}&format=json".format(mbid))
response = json.loads(response.content)

topTagsAndLinks = response['track']['toptags']['tag']
sparkTopTagsAndLinks = sc.parallelize(topTagsAndLinks)
sparkTopTags = sparkTopTagsAndLinks.map(lambda ob: ob['name'])
print(sparkTopTags.collect())

# for country, hdi in country_hdi.collect():	
# 	response = requests.get("http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={}&api_key=101c6972f8adf89c5f3bdf67ff0efa0c&format=json".format(country))

