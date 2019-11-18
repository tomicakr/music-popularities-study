#!/usr/bin/python
from pyspark import SparkContext
import re
import math
import requests

sc = SparkContext()

def movieRatingExtractor(line):
	words = re.split(',', line)
	userId,movieId,rating,timestamp = words
	return (movieId, float(rating))

hdis = './hdis.csv'
textRDD = sc.textFile(hdis)


print(textRDD.collect()[1])
# response = requests.get("http://api.open-notify.org/this-api-doesnt-exist")
