import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Procesar CLIENTS
clients_df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://energy-trading-datalake-dev-raw-v2/clients/"], "recurse": True},
    format_options={"withHeader": True},
    transformation_ctx="clients_df"
)

glueContext.write_dynamic_frame.from_options(
    frame=clients_df,
    connection_type="s3",
    format="glueparquet",
    connection_options={"path": "s3://energy-trading-datalake-dev-processed-v2/clients/", "partitionKeys": []},
    transformation_ctx="clients_sink"
)

# Procesar PROVIDERS
providers_df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://energy-trading-datalake-dev-raw-v2/providers/"], "recurse": True},
    format_options={"withHeader": True},
    transformation_ctx="providers_df"
)

glueContext.write_dynamic_frame.from_options(
    frame=providers_df,
    connection_type="s3",
    format="glueparquet",
    connection_options={"path": "s3://energy-trading-datalake-dev-processed-v2/providers/", "partitionKeys": []},
    transformation_ctx="providers_sink"
)

# Procesar TRANSACTIONS
transactions_df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://energy-trading-datalake-dev-raw-v2/transactions/"], "recurse": True},
    format_options={"withHeader": True},
    transformation_ctx="transactions_df"
)

glueContext.write_dynamic_frame.from_options(
    frame=transactions_df,
    connection_type="s3",
    format="glueparquet",
    connection_options={"path": "s3://energy-trading-datalake-dev-processed-v2/transactions/", "partitionKeys": []},
    transformation_ctx="transactions_sink"
)

job.commit()
