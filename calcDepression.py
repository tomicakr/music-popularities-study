#!/usr/bin/python
from pyspark import SparkContext
from trackGrouping import tagsExtractor, getSongs, createGroups, printGroupsRanges, getGroupsRanges
import re
import json
import time

sc = SparkContext()
sc.setLogLevel('ERROR')

country_depression_groups = createGroups(sc.textFile('./depression/depression.csv').filter(lambda line: re.split(',', line)[2] == "2017").filter(lambda line: re.split(',', line)[1] != "").map(lambda line: (re.split(',', line)[0], float(re.split(',', line)[3]))))

groupRanges = getGroupsRanges(country_depression_groups)

genres_dict = dict()
genres_clean = sc.textFile('genres_clean.txt')

numberOfGroups = len(country_depression_groups)

def cleanup(tag_number):
    tag, number = tag_number
    newTag = tag.replace("-", " ").lower()
    return newTag, number

g = 1
for group in country_depression_groups:
    startGroup = time.time()
    groupOut = open("depression/group_{}".format(g), "w")
    for line in genres_clean.collect():
        genres_dict[line] = 0
    c = 1
    numberOfCountriesInGroup = len(group)

    depressionGroupsTags = []
    for country, deprRate in group:
        startCountry = time.time()
        i = 1
        print("country {}/{} in group {}/{}".format(c, numberOfCountriesInGroup, g, numberOfGroups))
        while True:
            print("   page {}/10".format(i))
            response = getSongs(country, 50, i)
            i += 1
            try:
                response = json.loads(response.content.decode("utf-8"))
            except:
                print(response)
            if response == b'' or i == 11:
                break
            if 'tracks' in response.keys() and response['tracks']['track'] is not None:
                sparkCountryTracks = sc.parallelize(response['tracks']['track'])
                countryTags = sparkCountryTracks.map(tagsExtractor)
                countryTags = countryTags.flatMap(lambda x: x).map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
                depressionGroupsTags.extend(list(countryTags.collect()))
        endCountry = time.time()
        c += 1
        print("time elapsed for country = {}".format(endCountry - startCountry))
        print("")
    print("\n\n")

    depressionGroupsTags = sc.parallelize(depressionGroupsTags).reduceByKey(lambda x, y: x + y)
    depressionGroupsTags = depressionGroupsTags.map(cleanup)

    for gt in depressionGroupsTags.collect(): 
        tag, number = gt
        if tag in genres_dict.keys():
            genres_dict[tag] = number

    range = groupRanges[g - 1]
    groupOut.write("{}-{}\n".format(range[0], range[1]))
    for key in genres_dict.keys():
        if genres_dict[key] != 0:
            groupOut.write("{}:{}\n".format(key, genres_dict[key]))
    
    endGroup = time.time()
    print("time elapsed for group = {}".format(endGroup - startGroup))
    print("\n")

    g += 1