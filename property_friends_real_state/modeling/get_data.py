import boto3
import os
import pandas as pd
from pathlib import Path
from loguru import logger

# AWS Configuration (Set these using GitHub Secrets)
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = "case-property-friends"
TEST_DATA_PATH = "test.csv"
TRAIN_DATA_PATH = "train.csv"

PROJ_ROOT = Path(__file__).resolve().parents[2]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")



LOCAL_TEST_PATH = PROJ_ROOT / "data/processed/test.csv"
LOCAL_TRAIN_PATH = PROJ_ROOT / "data/processed/train.csv"

# Temporary path for GitHub Actions

# Create directories if they don't exist
LOCAL_TEST_PATH.parent.mkdir(parents=True, exist_ok=True)
LOCAL_TRAIN_PATH.parent.mkdir(parents=True, exist_ok=True)


# Download test dataset from S3
def download_data(s3_path, local_path):
    s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    s3.download_file(S3_BUCKET, s3_path, local_path)
    print(f"Test dataset downloaded to {local_path}")
    


# Load test data as DataFrame
def load_data(LOCAL_TEST_PATH):
    return pd.read_csv(LOCAL_TEST_PATH)

if __name__ == "__main__":
    download_data(TEST_DATA_PATH, LOCAL_TEST_PATH)
    download_data(TRAIN_DATA_PATH, LOCAL_TRAIN_PATH)
    test_df = load_data(LOCAL_TEST_PATH)
    trin_df = load_data(LOCAL_TRAIN_PATH)
    print("Test Data Loaded Successfully!")
    print(test_df.head())  # Preview data
    