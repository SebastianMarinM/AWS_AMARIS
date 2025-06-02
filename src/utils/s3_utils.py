import boto3
import os
from botocore.exceptions import ClientError

def upload_file_to_s3(local_path, bucket, s3_key):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_path, bucket, s3_key)
        print(f"Uploaded {local_path} to s3://{bucket}/{s3_key}")
    except ClientError as e:
        print(f"Error uploading {local_path}: {str(e)}")

def download_file_from_s3(bucket, s3_key, local_path):
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket, s3_key, local_path)
        print(f"Downloaded s3://{bucket}/{s3_key} to {local_path}")
    except ClientError as e:
        print(f"Error downloading {s3_key}: {str(e)}")
