import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'table_name',
    'redshift_temp_dir',
    'redshift_connection',
    'processed_bucket'
])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Leer datos desde S3 (processed)
input_path = f"s3://{args['processed_bucket']}/processed/{args['table_name']}/"
dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [input_path]},
    format="parquet"
)

# Cargar a Redshift
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="redshift",
    connection_options={
        "dbtable": args['table_name'],
        "database": "energy_trading",
        "redshiftTmpDir": args['redshift_temp_dir']
    }
)

job.commit()
