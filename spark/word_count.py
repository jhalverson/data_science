"""Jonathan Halverson
   Friday, April 29, 2016

   This is a simple PySpark script to illustrate the basics.
"""

from pyspark import SparkContext
from pyspark import SparkConf
from operator import add

conf = SparkConf().setMaster('local')
sc = SparkContext(conf=conf, appName='DemoMapFilter')

# create an RDD
lines = sc.textFile('text_file.md')

# create RDD of the words, make tuples and reduce
words = lines.flatMap(lambda line: line.split())
counts = words.map(lambda word: (word, 1)).reduceByKey(add)

# write out the tuples
counts.saveAsTextFile('counts')

# print to the screen
for word, count in counts.collect():
  print word, count

sc.stop()
