#!/usr/bin/python
import re
import math
import requests
import json

api_key = "f15e8c8ea5e04aa8c52151a8baf84334"
api_base = "http://ws.audioscrobbler.com/2.0/"

def getSongInfo(mbid):
    return requests.get("{}?method=track.getInfo&api_key={}&mbid={}&format=json".format(api_base, api_key, mbid))

def getSongInfoArtistAndName(artist, trackName):
    return requests.get("{}?method=track.getInfo&api_key={}&artist={}&track={}&format=json".format(api_base, api_key, artist, trackName))

def getSongs(country, limit, page):
    return requests.get("{}?method=geo.gettoptracks&country={}&api_key={}&format=json&limit={}&page={}".format(api_base, country, api_key, limit, page))

def tagsExtractor(track):
    mbid = track['mbid'].replace('"', '')
    response = None
    if mbid != '':
        response = getSongInfo(mbid)
    else:
        artist = track['artist']['name'].encode("utf-8")
        trackName = track['name'].encode("utf-8")
        response = getSongInfoArtistAndName(artist, trackName)
    

    if response.content is None or response.content == '':
        return ['---']
    
    if not response.ok:
        print(response.json())

    try:
        response = json.loads(response.content.decode("utf-8"))
    except:
        print(response.content)
        return ['---']
    
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
    number_of_countries = int(math.ceil(len(country_attribute)/number_of_groups))
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

def getGroupsRanges(country_groups):
    number_of_groups = len(country_groups)
    ranges = []
    for i in range (0, number_of_groups):
        group = country_groups[i]
        begin_range = group[0][1]
        end_range = group[-1][1]
        ranges.append((begin_range, end_range))

    return ranges
