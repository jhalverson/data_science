# Jonathan Halverson
# Wednesday, December 21, 2016

# This code uses alternating least squares to make
# recommendations for movies

from __future__ import print_function

import sys
import random
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

APP_NAME = "Movie Recommender"

if (__name__ == '__main__'):
  spark = SparkSession.builder.appName(APP_NAME).getOrCreate()

  lines = spark.read.text('sample_movielens_ratings.txt').rdd.map(lambda x: x.value.split('::'))
  ratingsRDD = lines.map(lambda x: Row(user=int(x[0]), film=int(x[1]), rating=float(x[2])))
  print(ratingsRDD.first())

  ratings = spark.createDataFrame(ratingsRDD)
  print(ratings.show())
  (training, test) = ratings.randomSplit([0.8, 0.2])

  num_training = training.count()
  num_validation = test.count()

  print('Training: %d' % num_training)
  print('Validation: %d' % num_validation)

  # setup ALS
  rank_ = 12
  num_iterations = 8
  lambda_ = 0.1

  als = ALS(rank=rank_, maxIter=num_iterations, regParam=lambda_, userCol="user",
            itemCol="film", ratingCol="rating", coldStartStrategy="drop")
  model = als.fit(training)

  # Evaluate the model by computing the RMSE on the test data
  predictions = model.transform(test)
  evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
  rmse = evaluator.evaluate(predictions)
  print("Root-mean-square error = " + str(rmse))

  userRecs = model.recommendForAllUsers(10)
  userRecs.show()

  # make recommendations for user 19
  filmIDs = ratings.select('film').distinct().sort('film').rdd.map(lambda x: x[0])
  pred = model.transform(spark.createDataFrame(filmIDs.map(lambda x: Row(user=19, film=x))))
  cmb = pred.join(ratings, on=['user', 'film'], how='left_outer')
  print(cmb.orderBy('film').show(n=100))

  spark.stop()
