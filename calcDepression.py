#!/usr/bin/python
from pyspark import SparkContext
from trackGrouping import tagsExtractor, getSongs, createGroups, printGroupsRanges
import re
import json

sc = SparkContext()
sc.setLogLevel('ERROR')
logger = sc._jvm.org.apache.log4j
logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )

country_depression_groups = createGroups(sc.textFile('./depression.csv').filter(lambda line: re.split(',', line)[2] == "2017").filter(lambda line: re.split(',', line)[1] != "").map(lambda line: (re.split(',', line)[0], float(re.split(',', line)[3]))))

#printGroupsRanges(country_depression_groups)

genres_dict = dict()
genres_clean = sc.textFile('genres_clean.txt')

numberOfGroups = len(country_depression_groups)

def cleanup(tag_number):
    tag, number = tag_number
    newTag = tag.replace("-", " ").lower()
    return newTag, number

g = 1
for group in country_depression_groups:
    for line in genres_clean.collect():
        genres_dict[line] = 0
    c = 1
    numberOfCountriesInGroup = len(group)

    depressionGroupsTags = []
    for country, hdi in group:
        i = 1
        print("country {}/{} in group {}/{}".format(c, numberOfCountriesInGroup, g, numberOfGroups))
        while True:
            print("   page {}/5".format(i))
            response = getSongs(country, 50, i)
            i += 1
            response = json.loads(response.content)
            if response == b'' or i == 6:
                break
            if 'tracks' in response.keys() and response['tracks']['track'] is not None:
                sparkCountryTracks = sc.parallelize(response['tracks']['track'])
                countryTags = sparkCountryTracks.map(tagsExtractor)
                countryTags = countryTags.flatMap(lambda x: x).map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
                depressionGroupsTags.extend(list(countryTags.collect()))
        c += 1
        print("")
    g += 1
    print("\n\n")

    depressionGroupsTags = sc.parallelize(depressionGroupsTags).reduceByKey(lambda x, y: x + y)
    depressionGroupsTags = depressionGroupsTags.map(cleanup)

    for gt in depressionGroupsTags.collect(): 
        tag, number = gt
        if tag in genres_dict.keys():
            genres_dict[tag] = number

    for key in genres_dict.keys():
        if genres_dict[key] != 0:
            print("         {}: {}".format(key, genres_dict[key]))
    print("\n")
