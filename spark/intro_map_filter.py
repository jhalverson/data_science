"""Jonathan Halverson
   Friday, April 29, 2016

   This is a simple PySpark script to illustrate the basics.

   Usage: ~/software/spark-1.6.1-bin-hadoop2.6/bin/spark-submit --master local[*] --name "Simple map" intro_map_filter.py
   UI: http://localhost:4040
"""

from pyspark import SparkContext
from pyspark import SparkConf

conf = SparkConf().setMaster('local')
sc = SparkContext(conf=conf, appName='DemoMapFilter')
lines = sc.textFile('text_file.md')
print 'line count:', lines.count()

python_lines = lines.filter(lambda line: 'Python' in line)
print 'Python found in', python_lines.count(), 'lines'
print python_lines.take(5)

numRDD = lines.map(lambda line: len(line))
print numRDD.top(10)

# here we create the RDD locally
myRDD = sc.parallelize(range(10000))
print myRDD.stdev()

sc.stop()
