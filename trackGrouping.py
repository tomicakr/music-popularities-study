#!/usr/bin/python
import re
import math
import requests
import json

def getSongInfo(mbid):
    return requests.get("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=101c6972f8adf89c5f3bdf67ff0efa0c&mbid={}&format=json".format(mbid))

def getSongInfoArtistAndName(artist, trackName):
    return requests.get("http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=101c6972f8adf89c5f3bdf67ff0efa0c&artist={}&track={}&format=json".format(artist, trackName))

def getSongs(country, limit, page):
    return requests.get("http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={}&api_key=101c6972f8adf89c5f3bdf67ff0efa0c&format=json&limit={}&page={}".format(country, limit, page))

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
        if len(tags) == 0:
            tags.append('---')
        return tags
    
    return ['---']

def createGroups(country_attribute):
    country_attribute = country_attribute.sortBy(lambda x: x[1]).collect()
    number_of_groups = 15
    number_of_countries = int(len(country_attribute)/number_of_groups)
    country_attribute_groups = []
    for i in range(0,number_of_groups):
        if i==number_of_groups-1:
            country_attribute_groups.append(country_attribute[number_of_countries*i : ])
            break
        country_attribute_groups.append(country_attribute[number_of_countries*i : number_of_countries*(i+1)])
    return country_attribute_groups

def printGroupsRanges(country_groups):
    number_of_groups = len(country_groups)
    for i in range (0, number_of_groups):
        group = country_groups[i]
        begin_range = group[0][1]
        end_range = group[-1][1]
        print("{} - {} : {}".format(begin_range, end_range, end_range-begin_range))
