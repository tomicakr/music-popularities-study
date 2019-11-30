#!/usr/bin/python
from pyspark import SparkContext
from trackGrouping import tagsExtractor, getSongs, createGroups, printGroupsRanges
import re
import json

sc = SparkContext()
country_depression_groups = createGroups(sc.textFile('./depression.csv').filter(lambda line: re.split(',', line)[2] == "2017").filter(lambda line: re.split(',', line)[1] != "").map(lambda line: (re.split(',', line)[0], float(re.split(',', line)[3]))))

printGroupsRanges(country_depression_groups)

for group in country_depression_groups:
    depressionGroupsTags = []
    for country, hdi in group:
        response = getSongs(country, 5)
        response = json.loads(response.content)
        if 'tracks' in response.keys():
            sparkCountryTracks = sc.parallelize(response['tracks']['track'])
            countryTags = sparkCountryTracks.map(tagsExtractor).flatMap(lambda x: x).map(lambda x: (x, 1)).groupByKey().map(lambda x: (x[0], sum(x[1])))
            depressionGroupsTags.extend(list(countryTags.collect()))

    depressionGroupsTags = sc.parallelize(depressionGroupsTags).groupByKey().map(lambda x: (x[0], sum(x[1])))
    summ =  depressionGroupsTags.map(lambda x: x[1]).reduce(lambda x, y: x + y)
    avg = summ/depressionGroupsTags.count()

    print("{}: ".format(group))
    print("avg genre count per group = {}".format(avg))
    for tags in depressionGroupsTags.collect():
        print("     {}".format(tags))
    print("\n")
