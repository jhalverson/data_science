# Jonathan Halverson
# Tuesday, November 22, 2016
# Spark Application

import csv
import matplotlib.pyplot as plt

from StringIO import StringIO
from datetime import datetime
from collections import namedtuple
from operator import add, itemgetter
from pyspark import SparkConf, SparkContext

APP_NAME = 'Flight Delay Analysis'
DATE_FMT = '%Y-%m-%d'
TIME_FMT = '%H%M'

fields = ['flight_date', 'airline_id', 'flight_num', 'origin', 'destination',
         'departure_time', 'departure_delay', 'arrival_time', 'arrival_delay', 'air_time', 'distance']
Flight = namedtuple('Flight', fields)


def main(sc):
  airlines = dict(sc.textFile('airlines.csv').map(split).collect())
  airline_lookup = sc.broadcast(airlines)

  flights = sc.textFile('flights.csv').map(split).map(parse)

  delays = flights.map(lambda f: (airline_lookup.value[f.airline_id], add(f.departure_delay, f.arrival_delay)))

  delays = delays.reduceByKey(add).collect()
  delays = sorted(delays, key=itemgetter(1))

  for d in delays:
    print '%0.0f minutes delayed\t%s' % (d[1], d[0])

  #plot(delays)


def split(line):
  reader = csv.reader(StringIO(line))
  return reader.next()


def parse(row):
  row[0] = datetime.strptime(row[0], DATE_FMT).date()
  row[5] = datetime.strptime(row[5], TIME_FMT).time()
  row[6] = float(row[6])
  row[7] = datetime.strptime(row[7], TIME_FMT).time()
  row[8] = float(row[8])
  row[9] = float(row[9])
  row[10] = float(row[10])
  return Flight(*row[:11])


if __name__ == '__main__':
  conf = SparkConf().setAppName('FLIGHT_DELAY')
  conf = conf.setMaster('local[*]')
  sc = SparkContext(conf=conf)
  main(sc)
  sc.stop()
