"""Jonathan Halverson
   Friday, May 6, 2016

   This PySpark script illustrates piping to external R code.

   Usage: ~/software/spark-1.6.1-bin-hadoop2.6/bin/spark-submit pipe_example_R.py
"""

import os
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark import SparkFiles

conf = SparkConf().setMaster('local')
sc = SparkContext(conf=conf, appName='DemoPipeR')

contactsContactList = sc.parallelize([('null', '45.4,34.2,90.3,66.1'),
			              ('null', '49.3,31.6,42.3,76.7'),
				      ('null', '40.9,36.2,99.8,16.0')])

# Compute the distance of each call using an external R program
distScript = os.getcwd() + "/find_distance.R"
distScriptName = "find_distance.R"
sc.addFile(distScript)

def hasDistInfo(call):
    """Verify that a call has the fields required to compute the distance"""
    requiredFields = ["mylat", "mylong", "contactlat", "contactlong"]
    return all(map(lambda f: call[f], requiredFields))

def formatCall(call):
    """Format a call so that it can be parsed by our R program"""
    return "{0},{1},{2},{3}".format(
        call["mylat"], call["mylong"],
        call["contactlat"], call["contactlong"])

# here we do not bother with storing dictionaries in contactsContactList
#pipeInputs = contactsContactList.values().flatMap(lambda calls: map(formatCall, filter(hasDistInfo, calls)))
pipeInputs = contactsContactList.values()
distances = pipeInputs.pipe(SparkFiles.get(distScriptName))
print distances.collect()
