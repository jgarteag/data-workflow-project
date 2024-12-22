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
from pyspark.sql.functions import col, year, month, dayofmonth, to_date, date_sub, current_date, lit, date_format, current_timestamp, from_utc_timestamp

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