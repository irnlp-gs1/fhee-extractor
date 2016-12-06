# coding: utf-8
from __future__ import unicode_literals
import os
import re
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
TAGS_PARQUET = '{}output/food_pos.parquet'.format(PREFIX)
OUTPUT_DIR = '{}output'.format(PREFIX)

def extract_tags(spark):
    """Extract tags from df"""
    df = spark.read.parquet(TAGS_PARQUET)
    target_tags = ['NNG', 'NNP', 'NNB', 'NNBC', 'NR', 'NP',
                   'JK.*', 'JX', 'JC']
    tag_pattern = re.compile('(' + '|'.join(target_tags) + ')')
    tag_sentences = df.rdd.map(lambda r: ' '.join(['{}_{}'.format(token, tag) for (token, tag) in r.tags if tag_pattern.match(tag)]).strip())
    tag_sentences.saveAsTextFile(os.path.join(OUTPUT_DIR, 'food_pos_sentences.text'))
    # df_tag_sentences = spark.createDataFrame(tag_sentences)
    # df_tag_sentences.write.save(os.path.join(OUTPUT_DIR, 'food_pos_sentences.parquet'), format='parquet', mode='overwrite')

def main(spark):
    """Main function

    Args:
        sc (pyspark.SpartContext)
    """
    # tagging
    extract_tags(spark)

if __name__ == "__main__":
    # Configure SparkConf
    spark = (SparkSession
        .builder
        .appName(APP_NAME)
        .getOrCreate())

    # Execute
    main(spark)