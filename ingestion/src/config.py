import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT/"data"
LOG_DIR = PROJECT_ROOT/"logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

YEAR = "2024"
MONTH = "01"
DATASET = "yellow"

FILE_NAME = (f"{DATASET}_tripdata_{YEAR}-{MONTH}.parquet")

SOURCE_URL = (
    "https://d37ci6vzurychx.cloudfront.net/"
    f"trip-data/{FILE_NAME}"
)

LOCAL_FILE_PATH = DATA_DIR / FILE_NAME

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-southeast-1"
)

S3_BUCKET_BRONZE = os.getenv("S3_BUCKET_BRONZE")

S3_BRONZE_PREFIX = (
    f"bronze/{DATASET}_taxi/"
    f"year={YEAR}/month={MONTH}"
)

S3_BRONZE_KEY = f"{S3_BRONZE_PREFIX}/{FILE_NAME}"