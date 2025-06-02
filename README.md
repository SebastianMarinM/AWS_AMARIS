
# Energy Trading Data Lake Project

## Overview
This project implements a data lake solution for an energy trading company using AWS services. It processes data from providers, customers, and transactions, building an ETL pipeline with governance and analytics.

## Architecture
The solution follows a multi-layer data lake design:
- **Landing Zone**: Raw CSV exports from source systems
- **Raw Zone**: Validated and versioned files in S3
- **Transform Zone**: Data transformed and stored in Parquet format
- **Curated Zone**: Optimized, clean datasets for analytics
- **Analytics Zone**: Athena queries and reports
- **Redshift Zone**: Optional destination for advanced analytics from curated data

## Technologies Used
- **Amazon S3** – Scalable object storage for data lake
- **AWS Glue** – ETL jobs, schema detection (crawlers), and cataloging
- **AWS Lake Formation** – Governance and fine-grained access control
- **Amazon Athena** – Serverless SQL querying over S3 data
- **Amazon Redshift** – Optional data warehouse for advanced analytics
- **AWS CloudFormation** – Infrastructure as Code (IaC)
- **Python** – Scripts for ETL orchestration and data handling

## Prerequisites
- AWS CLI configured with credentials
- Python >= 3.8
- AWS account with permissions for S3, Glue, Athena, and Lake Formation
- IAM roles and policies already defined or created via CloudFormation templates

## Project Structure
```
├── infrastructure/
│ └── cloudformation/
│ ├── s3.yaml
│ ├── lakeformation.yaml
│ ├── redshift.yaml
│ └── glue_jobs/
├── src/
│ ├── etl/
│ ├── utils/
│ ├── sql/
│ └── scripts/
├── data/
│ ├── raw/
│ ├── processed/
│ └── curated/
├── tests/
├── docs/
└── README.md
```

## Quick Start
```bash
# 1. Deploy infrastructure with CloudFormation
aws cloudformation deploy --template-file infrastructure/cloudformation/s3.yaml --stack-name datalake-s3
aws cloudformation deploy --template-file infrastructure/cloudformation/lakeformation.yaml --stack-name lake-permissions
aws cloudformation deploy --template-file infrastructure/cloudformation/redshift.yaml --stack-name redshift-cluster

# 2. Generate sample data
python src/scripts/generate_sample_data.py

# 3. Upload to S3
python src/scripts/upload_to_s3.py

# 4. Run Glue ETL jobs (trigger via AWS Console or boto3 script)
```

## Redshift Integration
- The datasets from the **Curated Zone** (e.g., `daily_energy_consumption`, `client_analytics`) are loaded into Amazon Redshift for advanced BI and reporting.
- Glue Job `curated-to-redshift` (to be implemented) loads the Parquet files from S3 into Redshift tables using the `COPY` command.
- The `GlueToRedshiftConnection` defined in `cloudformation/redshift.yaml` provides JDBC access, and appropriate IAM roles ensure secure communication.

## Security and Monitoring
- Encryption at rest (S3 default encryption)
- Fine-grained access via Lake Formation
- CloudWatch monitoring for Glue jobs and Athena queries

## License
MIT License