# coding: utf-8
import os
from operator import add
from pyspark.sql import SparkSession
from pyspark.sql.types import *

APP_NAME = "Extract Food Hazard Events from Food News"
DATA_FILE = './data/food.csv.gz'

def word_count(spark):
    """A simple word count"""
    lines = spark.read.text(DATA_FILE).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))

def to_parquet(spark):
    """Save DF as parquet"""
    schema = StructType([
        StructField('idx', StringType(), False),
        StructField('media', StringType(), True),
        StructField('url', StringType(), True),
        StructField('title', StringType(), True),
        StructField('content', StringType(), True),
        StructField('datetime', StringType(), True),
    ])

    df = (spark.read
          .csv(DATA_FILE, sep='\t', header=True, schema=schema, timestampFormat='yyyy-MM-dd HH:mm:ss', nullValue='', nanValue=''))

    df.write.save(os.path.basename(DATA_FILE).split('.')[0] + '.parquet', format='parquet')

def main(spark):
    """Main function

    Args:
        sc (pyspark.SpartContext)
    """
    # word count
    # word_count(spark)

    to_parquet(spark)

if __name__ == "__main__":
    # Configure SparkConf
    spark = (SparkSession
        .builder
        .master('local[3]')
        .appName(APP_NAME)
        .getOrCreate())

    # Execute
    main(spark)