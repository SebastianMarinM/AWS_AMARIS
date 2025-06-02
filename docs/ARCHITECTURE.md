# Arquitectura del Data Lake para Comercializadora de Energía

## Descripción General
Este documento describe la arquitectura completa del sistema de Data Lake implementado para la comercializadora de energía, incluyendo todos los componentes, flujos de datos, recursos desplegados con CloudFormation y consideraciones de seguridad.

## Componentes Principales

### 1. Capa de Almacenamiento (S3)

#### Raw Zone (Bronze)
- **Propósito**: Almacenamiento de datos crudos en formato CSV.
- **Estructura**:
  ```
  s3://energy-trading-datalake-dev/raw/
  ├── providers/
  │   └── 20250529_providers/
  ├── clients/
  │   └── 20250529_clients/
  └── transactions/
      └── 20250529_transactions/
  ```
- **Retención**: 90 días

#### Processed Zone (Silver)
- **Propósito**: Almacena datos transformados y validados en formato Parquet.
- **Estructura**:
  ```
  s3://energy-trading-datalake-dev/processed/
  ├── providers/
  │   └── 20250529_providers/
  ├── clients/
  │   └── 20250529_clients/
  └── transactions/
      └── 20250529_transactions/
  ```
- **Optimizaciones**:
  - Compresión Snappy
  - Particionamiento por fecha

#### Curated Zone (Gold)
- **Propósito**: Datos agregados para análisis.
- **Estructura**:
  ```
  s3://energy-trading-datalake-dev/curated/
  ├── daily_energy_consumption/20250529/
  ├── provider_performance/20250529/
  └── client_analytics/20250529/
  ```
- **Formato**: Parquet optimizado para Athena

### 2. Procesamiento de Datos

#### AWS Glue

- **Crawlers** (definidos en CloudFormation con `AWS::Glue::Crawler`):
  - `raw-data-crawler`: Detecta esquemas de datos crudos
  - `processed-data-crawler`: Detecta esquemas en zona transformada

- **Jobs ETL** (definidos con `AWS::Glue::Job`):
  1. `raw-to-processed`:
     - Lee CSV de zona raw
     - Aplica limpieza y normalización
     - Convierte a Parquet
     - Escribe en zona processed
  2. `processed-to-curated`:
     - Agrega datos
     - Calcula KPIs
     - Optimiza para consultas
  3. `curated-to-redshift`:
     - Extrae datos agregados desde la zona curated
     - Realiza carga incremental hacia Amazon Redshift
     - Usa conexión JDBC configurada mediante Glue Connection

#### Lake Formation
- Catálogo centralizado
- Permisos a través de `AWS::LakeFormation::Permissions`

### 3. Análisis y Consulta

#### Athena (definido con `AWS::Athena::WorkGroup`)
- Workgroups: `analysts`, `reporting`, `data-science`
- Consultas automáticas vía script Python con `boto3`

#### Amazon Redshift
- Destino final del pipeline
- Carga desde zona curated usando Glue Job y conexión JDBC
- Glue Connection: definida con `AWS::Glue::Connection` en CloudFormation

### 4. Seguridad y Monitoreo

- IAM Roles mínimos y con políticas gestionadas (CloudFormation `AWS::IAM::Role`)
- S3 cifrado con SSE-KMS
- TLS en tránsito
- Logs activados:
  - S3 Access Logs
  - CloudTrail
  - Lake Formation Audit

## Infraestructura como Código

Todo el entorno se despliega con CloudFormation en YAML:
- Buckets S3 (`AWS::S3::Bucket`)
- Glue Crawlers y Jobs
- Bases de datos Glue (`AWS::Glue::Database`)
- Workgroups y databases Athena
- Roles IAM y políticas
- Lake Formation Permissions
- Glue Connection JDBC
- Opcional: Redshift Cluster (`AWS::Redshift::Cluster`)

## Pipeline de Datos (Resumen)

1. Sistema transaccional exporta CSV → S3 (raw)
2. Crawler detecta esquema y lo registra en Glue Data Catalog
3. Job `raw-to-processed` limpia y transforma los datos a Parquet
4. Job `processed-to-curated` agrega y optimiza
5. Crawler actualiza Catálogo
6. Consultas desde Athena y carga a Redshift (`curated-to-redshift`)
