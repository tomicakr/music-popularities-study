#!/usr/bin/python
from pyspark import SparkContext
from trackGrouping import tagsExtractor, getSongs, createGroups, printGroupsRanges, getGroupsRanges
import re
import json
import time

sc = SparkContext()
sc.setLogLevel('ERROR')

country_hdi_groups = createGroups(sc.textFile('./hdi/hdis.csv').filter(lambda line: re.split(',', line)[-1].replace('"', '').replace('.','').isdigit()).map(lambda line: (re.split(',', line)[1].replace('"', '').lower(), float(re.split(',', line)[-1].replace('"', '')))))

groupRanges = getGroupsRanges(country_hdi_groups)

genres_dict = dict()
genres_clean = sc.textFile('genres_clean.txt')

numberOfGroups = len(country_hdi_groups)

def cleanup(tag_number):
    tag, number = tag_number
    newTag = tag.replace("-", " ").lower()
    return newTag, number

g = 1

for group in country_hdi_groups:
    startGroup = time.time()
    groupOut = open("hdi/group_{}".format(g), "w")
    for line in genres_clean.collect():
        genres_dict[line] = 0
    c = 1
    numberOfCountriesInGroup = len(group)
    
    hdiGroupsTags = []
    for country, hdi in group:
        startCountry = time.time()
        i = 1
        print("country {}/{} in group {}/{}".format(c, numberOfCountriesInGroup, g, numberOfGroups))
        while True:
            print("   page {}/10".format(i))
            response = getSongs(country, 50, i)
            i += 1
            # if response.error != '':
            #     print("        error:   {}".format(response.error))
            response = json.loads(response.content.decode("utf-8"))
            if response == b'' or i == 11:
                break
            if 'tracks' in response.keys() and response['tracks']['track'] is not None:
                sparkCountryTracks = sc.parallelize(response['tracks']['track'])
                countryTags = sparkCountryTracks.map(tagsExtractor)
                countryTags = countryTags.flatMap(lambda x: x).map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
                hdiGroupsTags.extend(list(countryTags.collect()))
        c += 1
        endCountry = time.time()
        print("time elapsed for country = {}".format(endCountry - startCountry))
        print("")
    print("\n\n")

    hdiGroupsTags = sc.parallelize(hdiGroupsTags).reduceByKey(lambda x, y: x + y)
    hdiGroupsTags = hdiGroupsTags.map(cleanup)

    for gt in hdiGroupsTags.collect(): 
        tag, number = gt
        if tag in genres_dict.keys():
            genres_dict[tag] = number
            
    range = groupRanges[g - 1]
    groupOut.write("{}-{}\n".format(range[0], range[1]))
    for key in genres_dict.keys():
        if genres_dict[key] != 0:
            groupOut.write("{}:{}\n".format(key, genres_dict[key]))
    
    print("time elapsed for group = {}".format(endGroup - startGroup))
    print("\n")
    endGroup = time.time()

    g += 1
