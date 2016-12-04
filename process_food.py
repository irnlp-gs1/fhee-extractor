# coding: utf-8
import os
from operator import add
from pyspark.sql import SparkSession
from pyspark.sql.types import *

APP_NAME = "Extract Food Hazard Events from Food News"
DATA_FILE = './data/food.csv.gz'
DATA_PARQUET = './output/food.parquet'

def get_filename(fpath):
    return os.path.basename(fpath).split('.')[0]

def word_count(spark):
    """A simple word count"""
    lines = spark.read.text(DATA_FILE).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))

def to_parquet(spark, data_file=DATA_FILE):
    """Save DF as parquet"""
    schema = StructType([
        StructField('idx', IntegerType(), False),
        StructField('media', StringType(), True),
        StructField('url', StringType(), True),
        StructField('title', StringType(), True),
        StructField('content', StringType(), True),
        StructField('datetime', TimestampType(), True),
    ])

    df = (spark.read
          .csv(data_file, sep='\t', header=True, schema=schema, timestampFormat='yyyy-MM-dd HH:mm:ss', nullValue='', nanValue='', mode='DROPMALFORMED'))

    df.write.save('./output/' + get_filename(data_file) + '.parquet', format='parquet')

def add_uid(spark, data_file=DATA_PARQUET):
    df = spark.read.parquet(data_file)
    df_with_uid = df.withColumn('uid', '{}_{}'.format(df.media, df.idx)) 
    df_with_uid.write.save(os.path.join('./output', get_filename(data_file) + '_with_uid' + '.parquet'), format='parquet', mode='overwrite')

def main(spark):
    """Main function

    Args:
        sc (pyspark.SpartContext)
    """
    # word count
    # word_count(spark)

    # to_parquet(spark)
    add_uid(spark)

if __name__ == "__main__":
    # Configure SparkConf
    spark = (SparkSession
        .builder
        .master('local[3]')
        .appName(APP_NAME)
        .getOrCreate())

    # Execute
    main(spark)