# coding: utf-8
import os
from operator import add
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import concat_ws
from pyspark.sql.functions import udf
from pyspark.sql import Row
from konlpy.tag import Mecab

APP_NAME = "Food - Mecab"
PREFIX = ''
DATA_FILE = '{}data/food.csv.gz'.format(PREFIX)
DATA_PARQUET = '{}output/food.parquet'.format(PREFIX)
OUTPUT_DIR = '{}output'.format(PREFIX)

def get_filename(fpath):
    return os.path.basename(fpath).split('.')[0]

def tag_content(iterator):
    tagger = Mecab()
    PosContent = Row('uid', 'tags')
    for row in iterator:
        try:
            tags = tagger.pos(row.content)
        except AttributeError:
            tags = []
        yield PosContent(row.uid, tags)
    del tagger

def analyze_text(spark, df):
    tag_rdd = df.rdd.mapPartitions(tag_content)
    # tag_rdd = df.sample(False, 0.01).repartition(3).rdd.mapPartitions(tag_content)
    tag_df = spark.createDataFrame(tag_rdd)
    tag_df.write.save(os.path.join(OUTPUT_DIR, 'food_pos.parquet'),
                      format='parquet',
                      mode='overwrite')

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

    # add uid
    df_with_uid = df.withColumn('uid', concat_ws('_', df.media, df.idx))

    # save
    df_with_uid.write.save(DATA_PARQUET, format='parquet', mode='overwrite')

def main(spark):
    """Main function

    Args:
        sc (pyspark.SpartContext)
    """
    # tagging
    df = spark.read.parquet(DATA_PARQUET)
    analyze_text(spark, df)

if __name__ == "__main__":
    # Configure SparkConf
    spark = (SparkSession
        .builder
        .appName(APP_NAME)
        .getOrCreate())

    # Execute
    main(spark)