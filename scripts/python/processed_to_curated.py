import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ========= LECTURA DE PROCESSED =========
df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://energy-trading-datalake-dev-processed-v2/"], "recurse": True},
    format="parquet",
    transformation_ctx="read_processed"
).toDF()

# ========= TRANSFORMACIONES MÍNIMAS =========
# Eliminar duplicados, valores nulos y columnas innecesarias
df = df.dropDuplicates().na.drop()

# ========= ESCRITURA EN CURATED (Parquet particionado) =========
dyf_out = DynamicFrame.fromDF(df, glueContext, "curated_out")

glueContext.write_dynamic_frame.from_options(
    frame=dyf_out,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://energy-trading-datalake-dev-curated-v2/",
        "partitionKeys": ["year", "month", "day"]
    },
    transformation_ctx="curated_sink"
)

job.commit()
