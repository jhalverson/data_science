# Jonathan Halverson
# Friday, December 16, 2016

# This code uses alternating least squares to make
# recommendations for those on a dating site

from __future__ import print_function

import sys
import random
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

APP_NAME = "Dating Recommender"

def parse_rating(line, sep=','):
  u = line.strip().split(sep)
  return Row(userID=int(u[0]), profileID=int(u[1]), rating=float(u[2]))

def parse_user(line, sep=','):
  fields = line.strip().split(sep)
  user_id = int(fields[0])
  gender = fields[1]
  return (user_id, gender)

if (__name__ == '__main__'):
  spark = SparkSession.builder.appName(APP_NAME).getOrCreate()

  matchseeker = int(sys.argv[1])
  gender_filter = sys.argv[2]

  lines = spark.read.text('ratings.dat').rdd
  ratingsRDD = lines.map(parse_rating)
  print(ratingsRDD.count())
  lines = spark.read.text('gender.dat').rdd
  users = dict(lines.map(parse_user).collect())

  ratings = spark.createDataFrame(ratingsRDD)
  (training, test) = ratings.randomSplit([0.8, 0.2])

  num_training = training.count()
  num_validation = test.count()

  print('Training: %d' % num_training)
  print('Validation: %d' % num_validation)

  # setup ALS
  rank = 8
  num_iterations = 8
  lambda_ = 0.1

  als = ALS(maxIter=num_interations, regParam=lambda_, userCol="userID", itemCol="profileID", ratingCol="rating")
  model = als.fit(training)

  # Evaluate the model by computing the RMSE on the test data
  predictions = model.transform(test)
  evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating",
                                  predictionCol="prediction")
  rmse = evaluator.evaluate(predictions)
  print("Root-mean-square error = " + str(rmse))

  spark.stop()
