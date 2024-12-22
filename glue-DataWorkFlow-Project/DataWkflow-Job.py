import sys
import boto3
import json
from typing import Dict, List
from datetime import date, timedelta

from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.functions import to_date, when, datediff, current_date, year, avg, count

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Init Boto clients
glue_client = boto3.client("glue", region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')
ses_client = boto3.client('ses', region_name='us-east-1')

# Init Workflow params
args = getResolvedOptions(sys.argv, ['WORKFLOW_NAME', 'WORKFLOW_RUN_ID'])
workflow_name = args['WORKFLOW_NAME']
workflow_run_id = args['WORKFLOW_RUN_ID']
workflow_params = glue_client.get_workflow_run_properties(Name=workflow_name, RunId=workflow_run_id)["RunProperties"]

def read_parquet_s3(bucket: str, key: str) -> DataFrame:
    """
    Read parquet file from S3
    :param bucket: S3 bucket
    :param key: S3 key
    :return: Spark DataFrame
    """
    return spark.read.parquet(f"s3://{bucket}/{key}")

def data_cleaning(df: DataFrame) -> DataFrame:
    """
    Data cleaning
    :param df: Spark DataFrame
    :return: Spark DataFrame
    """
    df_clean = df.dropna(subset=['price', 'bed', 'bath'])
    df_clean = df_clean.dropDuplicates()
    df_clean = df_clean.withColumn('prev_sold_date', to_date(df_clean['prev_sold_date'], 'yyyy-MM-dd'))
    
    return df_clean

def calculate_final_df(df: DataFrame) -> DataFrame:
    """
    Calculate final df with new columns
    :param df: Spark DataFrame
    :return: Spark DataFrame with new columns
    """
    df = df.withColumn('house_age', datediff(current_date(), 'prev_sold_date') / 365)

    df = df.withColumn('price_per_sqft', df['price'] / df['house_size'])

    df = df.withColumn('total_rooms', df['bed'] + df['bath'])

    df = df.withColumn('price_per_room', df['price'] / df['total_rooms'])

    df = df.withColumn('price_per_acre', df['price'] / df['acre_lot'])

    df = df.fillna({'house_age': 0, 'price_per_sqft': 0, 'total_rooms': 0, 'price_per_room': 0, 'price_per_acre': 0})

    return df

def save_to_s3(df: DataFrame, bucket: str, key: str) -> None:
    """
    Save data to S3
    :param df: Spark DataFrame
    :param bucket: S3 bucket
    :param key: S3 key
    """
    df.write.parquet(f"s3://{bucket}/{key}")

def main() -> None:
    bucket = workflow_params['S3_BUCKET']
    path = workflow_params['PATH_RAW_DATA']
    
    df = read_parquet_s3(bucket, path)
    df.printSchema()
    
    df_clean = data_cleaning(df)
    df_clean.printSchema()
    print(f"Number of rows after cleaning: {df_clean.count()}")
    
    df_final = calculate_final_df(df_clean)
    df_final.printSchema()
    
    save_to_s3(df_final, bucket, workflow_params['OUTPUT_TABLE_PATH_S3'])
    

if __name__ == "__main__":
    main()