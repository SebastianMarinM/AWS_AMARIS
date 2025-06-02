import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import input_file_name, regexp_extract, col
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ========= FUNCION GENÉRICA PARA PROCESAR CADA DATASET =========
def process_dataset(input_path, output_path, ctx_name):
    # Leer CSV como DynamicFrame
    dyf = glueContext.create_dynamic_frame.from_options(
        connection_type="s3",
        format="csv",
        connection_options={"paths": [input_path], "recurse": True},
        format_options={"withHeader": True},
        transformation_ctx=f"{ctx_name}_read"
    )

    # Convertir a DataFrame para transformación
    df = dyf.toDF()

    # Extraer año, mes y día desde el nombre del archivo (ej: 20250529_clients.csv)
    df = df.withColumn("file_path", input_file_name())
    df = df.withColumn("year", regexp_extract("file_path", r"(\d{4})", 1))
    df = df.withColumn("month", regexp_extract("file_path", r"\d{4}(\d{2})", 1))
    df = df.withColumn("day", regexp_extract("file_path", r"\d{6}(\d{2})", 1))

    # Eliminamos duplicados y filas vacías (mínima validación)
    df = df.dropDuplicates().na.drop()

    # Convertimos de nuevo a DynamicFrame
    dyf_out = DynamicFrame.fromDF(df.drop("file_path"), glueContext, f"{ctx_name}_out")

    # Guardamos en formato Parquet con particionado
    glueContext.write_dynamic_frame.from_options(
        frame=dyf_out,
        connection_type="s3",
        format="glueparquet",
        connection_options={
            "path": output_path,
            "partitionKeys": ["year", "month", "day"]
        },
        transformation_ctx=f"{ctx_name}_sink"
    )

# ========= PROCESAMIENTO POR CATEGORÍA =========
process_dataset(
    "s3://energy-trading-datalake-dev-raw-v2/clients/",
    "s3://energy-trading-datalake-dev-processed-v2/clients/",
    "clients"
)

process_dataset(
    "s3://energy-trading-datalake-dev-raw-v2/providers/",
    "s3://energy-trading-datalake-dev-processed-v2/providers/",
    "providers"
)

process_dataset(
    "s3://energy-trading-datalake-dev-raw-v2/transactions/",
    "s3://energy-trading-datalake-dev-processed-v2/transactions/",
    "transactions"
)

job.commit()
