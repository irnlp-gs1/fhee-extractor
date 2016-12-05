# coding: utf-8
import os
from operator import add
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import concat_ws
from pyspark.sql.functions import udf
from pyspark.sql import Row

APP_NAME = "Extract Food Hazard Events from Food News"
DATA_FILE = 'gs://irnlp-gs1/data/food.csv.gz'
DATA_PARQUET = 'gs://irnlp-gs1/output/food.parquet'
OUTPUT_DIR = 'gs://irnlp-gs1/output'

def get_filename(fpath):
    return os.path.basename(fpath).split('.')[0]

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
    # text to parquet
    to_parquet(spark)

if __name__ == "__main__":
    # Configure SparkConf
    spark = (SparkSession
        .builder
        .appName(APP_NAME)
        .master('yarn')
        .getOrCreate())

    # Execute
    main(spark)