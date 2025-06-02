import boto3
import os
from datetime import datetime

def upload_to_s3(local_file, bucket, s3_key, region='us-east-1'):
    s3 = boto3.client('s3', region_name=region)
    try:
        s3.upload_file(local_file, bucket, s3_key)
        print(f"[OK] Uploaded {local_file} to s3://{bucket}/{s3_key}")
    except Exception as e:
        print(f"[ERROR] Failed to upload {local_file} → {e}")

def main():
    bucket = os.getenv('DATA_LAKE_BUCKET', 'your-energy-trading-datalake')
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    # Fecha actual
    timestamp = datetime.now().strftime('%Y%m%d')
    year, month, day = timestamp[:4], timestamp[4:6], timestamp[6:8]

    files = {
        "providers": f"data/raw/providers_{timestamp}.csv",
        "clients": f"data/raw/clients_{timestamp}.csv",
        "transactions": f"data/raw/transactions_{timestamp}.csv"
    }

    for entity, local_path in files.items():
        if os.path.exists(local_path):
            s3_key = f"raw/{entity}/year={year}/month={month}/day={day}/{os.path.basename(local_path)}"
            upload_to_s3(local_path, bucket, s3_key, region)
        else:
            print(f"[WARN] File not found: {local_path}")

if __name__ == "__main__":
    main()
