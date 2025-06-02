import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import current_timestamp, date_format, col, trim, lower

# Parámetros de entrada
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'database_name', 'table_name'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Leer desde Glue Catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database=args['database_name'],
    table_name=args['table_name']
)

# Convertir a DataFrame
df = datasource.toDF()

# ✅ Transformación 1: Agregar fecha de procesamiento
df = df.withColumn("processing_timestamp", current_timestamp())
df = df.withColumn("processing_date", date_format("processing_timestamp", "yyyy-MM-dd"))

# ✅ Transformación 2: Normalización de nombres (trim + lower)
df = df.withColumn("provider_name", lower(trim(col("provider_name"))))

# ✅ Transformación 3: Filtrado por tipo de energía (solo eólica)
df = df.filter(col("energy_type") == "eólica")

# Convertir a DynamicFrame
dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")

# Escribir en S3 en formato Parquet y particionado
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={
        "path": "s3://your-bucket/processed/providers/",
        "partitionKeys": ["processing_date"]
    },
    format="parquet"
)

job.commit()
