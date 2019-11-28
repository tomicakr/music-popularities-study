#!/usr/bin/python
from pyspark import SparkContext
import re
import math
import requests
import json

sc = SparkContext()

def getSongInfo(mbid):
    return requests.get("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=101c6972f8adf89c5f3bdf67ff0efa0c&mbid={}&format=json".format(mbid))

def getSongInfoArtistAndName(artist, trackName):
    return requests.get("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=101c6972f8adf89c5f3bdf67ff0efa0c&artist={}&track={}&format=json".format(artist, trackName))

def getSongs(country, limit):
    return requests.get("http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={}&api_key=101c6972f8adf89c5f3bdf67ff0efa0c&format=json&limit={}".format(country, limit))

def extract2017Hdi(line):
    words = re.split(',', line)
    country = words[1].replace('"', '').lower()
    hdi = words[-1].replace('"', '')
    return (country, float(hdi))

def filterNonExistant(line):
    words = re.split(',', line)
    return words[-1].replace('"', '').replace('.','').isdigit()

def createHDIGroups(country_hdi):
    country_hdi = country_hdi.sortBy(lambda x: x[1]).collect()
    number_of_groups = 10
    number_of_countries = 19
    country_hdi_groups = []
    for i in range(0,number_of_groups):
        if i==number_of_groups-1:
            country_hdi_groups.append(country_hdi[number_of_countries*i : ])
            break
        country_hdi_groups.append(country_hdi[number_of_countries*i : number_of_countries*(i+1)])
    return country_hdi_groups

def printGroupsRanges(country_groups):
    number_of_groups = len(country_groups)
    for i in range (0, number_of_groups):
        group = country_groups[i]
        begin_range = group[0][1]
        end_range = group[-1][1]
        print("{} - {} : {}".format(begin_range, end_range, end_range-begin_range))

def tagsExtractor(track):
    mbid = track['mbid'].replace('"', '')
    response = None
    if mbid != '':
        response = getSongInfo(mbid)
    else:
        artist = track['artist']['name']
        trackName = track['name']
        response = getSongInfoArtistAndName(artist, trackName)
    
    response = json.loads(response.content)
    if 'track' in response.keys():
        topTagsAndLinks = response['track']['toptags']['tag']
        tags = []
        for tagsAndLinks in topTagsAndLinks:
            tags.append(tagsAndLinks['name'])
        return tags

hdis = './hdis.csv'
file = sc.textFile(hdis)
country_hdi = sc.textFile(hdis).filter(filterNonExistant)
country_hdi = country_hdi.map(extract2017Hdi)
country_hdi_groups = createHDIGroups(country_hdi)

for group in country_hdi_groups:
    hdiGroupsTags = []
    for country, hdi in group:
        response = getSongs(country, limit)
        response = json.loads(response.content)
        if 'tracks' in response.keys():
            sparkCountryTracks = sc.parallelize(response['tracks']['track'])
            countryTags = sparkCountryTracks
                                .map(tagsExtractor)
                                .flatMap(lambda x: x)
                                .map(lambda x: (x, 1))
                                .groupByKey()
                                .map(lambda x: (x[0], sum(x[1])))
            
            hdiGroupsTags.extend(list(countryTags.collect()))

    hdiGroupsTags = sc.parallelize(hdiGroupsTags)
                            .groupByKey()
                            .map(lambda x: (x[0], sum(x[1])))

    summ =  hdiGroupsTags.map(lambda x: x[1]).reduce(lambda x, y: x + y)

    avg = summ/hdiGroupsTags.count()
    print("avg = {}".format(avg))

    print("{}: ".format(group))
    for tags in hdiGroupsTags.collect():
        print("     {}".format(tags))

    print("\n")
