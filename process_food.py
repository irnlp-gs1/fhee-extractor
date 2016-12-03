# coding: utf-8
import os
from operator import add
from pyspark.sql import SparkSession

APP_NAME = "Extract Food Hazard Events from Food News"
DATA_FILE = './data/food.csv'

def word_count(spark):
    """A simple word count"""
    lines = spark.read.text(DATA_FILE).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))

def main(spark):
    """Main function

    Args:
        sc (pyspark.SpartContext)
    """
    # word count
    word_count(spark)

if __name__ == "__main__":
    # Configure SparkConf
    spark = (SparkSession
        .builder
        .master('local[3]')
        .appName(APP_NAME)
        .getOrCreate())

    # Execute
    main(spark)