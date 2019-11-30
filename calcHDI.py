#!/usr/bin/python
from pyspark import SparkContext
from trackGrouping import tagsExtractor, getSongs, createGroups, printGroupsRanges
import re
import json

sc = SparkContext()
country_hdi_groups = createGroups(sc.textFile('./hdis.csv').filter(lambda line: re.split(',', line)[-1].replace('"', '').replace('.','').isdigit()).map(lambda line: (re.split(',', line)[1].replace('"', '').lower(), float(re.split(',', line)[-1].replace('"', '')))))

for group in country_hdi_groups:
    hdiGroupsTags = []
    for country, hdi in group:
        response = getSongs(country, 5)
        response = json.loads(response.content)
        if 'tracks' in response.keys():
            sparkCountryTracks = sc.parallelize(response['tracks']['track'])
            countryTags = sparkCountryTracks.map(tagsExtractor).flatMap(lambda x: x).map(lambda x: (x, 1)).groupByKey().map(lambda x: (x[0], sum(x[1])))
            hdiGroupsTags.extend(list(countryTags.collect()))

    hdiGroupsTags = sc.parallelize(hdiGroupsTags).groupByKey().map(lambda x: (x[0], sum(x[1])))
    summ =  hdiGroupsTags.map(lambda x: x[1]).reduce(lambda x, y: x + y)
    avg = summ/hdiGroupsTags.count()

    print("{}: ".format(group))
    print("avg genre count per group = {}".format(avg))
    for tags in hdiGroupsTags.collect():
        print("     {}".format(tags))
    print("\n")
