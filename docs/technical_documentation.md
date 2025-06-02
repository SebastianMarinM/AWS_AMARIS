# Technical Documentation: Energy Trading Data Lake

## Overview
This document explains the key components, flow, and configurations of the energy trading data lake project built on AWS using CloudFormation as Infrastructure as Code (IaC).

## Glue Jobs
- Each ETL script transforms raw CSV data into Parquet format partitioned by date.
- Jobs are orchestrated individually and can be triggered via schedule or event.
- The first job (`raw-to-processed`) validates and formats raw data.
- The second job (`processed-to-curated`) aggregates and enriches data for analytics.

## Data Catalog
- Managed using AWS Glue Crawlers to keep schema updated automatically.
- Crawlers scan raw and processed data and register the schema in the Glue Data Catalog.

## CloudFormation Modules
- `s3`: Defines buckets for raw, processed, and curated data with necessary IAM policies.
- `glue`: Provisions Glue Jobs, Crawlers, IAM Roles, and Glue Databases.
- `lakeformation`: Sets up centralized governance, data sharing, and access controls.
- `athena`: Creates Athena Workgroups and output configurations.
- `redshift`: Provisions Redshift cluster, IAM roles, and schemas for analytics layer.

## Athena
- Used for ad hoc queries and business analysis.
- Connected via Python scripts using Boto3 to execute SQL over processed data in S3.

## Redshift
- The curated data is loaded into Amazon Redshift from S3 using COPY commands.
- Data is available in structured format for BI tools and analytics teams.
- Integration enabled through Redshift IAM roles and access to curated zone.
- Schema Example:
  - `analytics.providers`
  - `analytics.clients`
  - `analytics.transactions`

## Security & Governance
- IAM roles and policies are provisioned per principle of least privilege.
- Buckets encrypted with SSE-KMS.
- TLS used for data in transit.
- Audit enabled using CloudTrail, S3 access logs, and Lake Formation logging.

## Summary
This project sets up a full-scale analytical environment using AWS-native services and CloudFormation. It provides structured ingestion, transformation, cataloging, and querying, and supports downstream Redshift data warehousing for deeper analytics.
