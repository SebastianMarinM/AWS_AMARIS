# Guía de Inicio Rápido

Esta guía te ayudará a poner en marcha el proyecto de Data Lake para la comercializadora de energía usando CloudFormation.

## Prerrequisitos

### AWS CLI, Python
```bash
brew install awscli python
aws configure
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## Configuración Inicial

### Parámetros (ejemplo para línea de comandos)
```bash
export ENVIRONMENT="dev"
export PROJECT_NAME="energy-trading"
export DATA_LAKE_BUCKET_NAME="energy-trading-datalake-dev"
export ATHENA_OUTPUT_BUCKET="energy-trading-athena-results-dev"
```

## Despliegue con CloudFormation
```bash
cd infrastructure/cloudformation

aws cloudformation deploy   --template-file main_stack.yaml   --stack-name energy-data-lake-stack   --capabilities CAPABILITY_NAMED_IAM   --parameter-overrides     Environment=$ENVIRONMENT     ProjectName=$PROJECT_NAME     DataLakeBucketName=$DATA_LAKE_BUCKET_NAME     AthenaOutputBucket=$ATHENA_OUTPUT_BUCKET
```

## Carga de Datos (ejemplo manual)
```bash
aws s3 cp data/raw/clients/sample_clients.csv s3://energy-trading-datalake-dev/raw/20250529_clients/
```

## Ejecución de Crawlers y Jobs (deben estar creados por CloudFormation)
```bash
aws glue start-crawler --name energy-trading-raw-crawler
aws glue start-job-run --job-name raw-to-processed
```

## Validación con Athena
```sql
SELECT * FROM processed.clients LIMIT 10;
```

## Consulta con Boto3 desde Python
```python
import boto3

athena = boto3.client('athena')
athena.start_query_execution(
  QueryString='SELECT * FROM processed.transactions LIMIT 10;',
  ResultConfiguration={'OutputLocation': 's3://energy-trading-athena-results-dev/'}
)
```