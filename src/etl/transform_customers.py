import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import current_timestamp, date_format, col

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'database_name', 'table_name'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource = glueContext.create_dynamic_frame.from_catalog(
    database=args['database_name'],
    table_name=args['table_name']
)

df = datasource.toDF()

df = df.withColumn("processing_timestamp", current_timestamp())
df = df.withColumn("processing_date", date_format("processing_timestamp", "yyyy-MM-dd"))

df = df.withColumn("city", col("city").cast("string"))
df = df.withColumn("client_type", col("client_type").cast("string"))
df = df.withColumn("id_type", col("id_type").cast("string"))
df = df.withColumn("identification", col("identification").cast("string"))

dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")

glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={
        "path": "s3://your-bucket/processed/clients/",
        "partitionKeys": ["processing_date"]
    },
    format="parquet"
)

job.commit()