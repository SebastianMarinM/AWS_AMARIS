
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

# Leer todos los datos del bucket processed sin partición
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://energy-trading-datalake-dev-processed-v2/"], "recurse": True},
    format="parquet",
    transformation_ctx="datasource"
)


# Escribir en zona curated
sink = glueContext.getSink(
    path="s3://energy-trading-datalake-dev-curated-v2/",
    connection_type="s3",
    updateBehavior="LOG",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="sink"
)
sink.setFormat("glueparquet")
sink.writeFrame(datasource)

job.commit()
