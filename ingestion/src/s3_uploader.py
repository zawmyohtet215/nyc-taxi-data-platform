import boto3
from botocore.exceptions import ClientError
from config import AWS_REGION

def get_s3_client():
    return boto3.client("s3", region_name=AWS_REGION)

def check_existing_object(s3, bucket, key, checksum):
    try:
        response = s3.head_object(Bucket=bucket, Key=key)

        existing_checksum = (response.get("Metadata", {}).get("sha256"))

        if existing_checksum == checksum:
            print("File already exists with the same checksum")

            return True

        raise ValueError(
            "Existing s3 object has a different checksum."
            "Do not overwrite immutable Bronze data."
        )
    
    except ClientError as error:

        status = error.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        code = error.response.get("Error", {}).get("Code")

        if status == 404 or code in ("404", "NoSuchKey", "NotFound"):
            return False

        raise


def upload_file(local_path, bucket, key, checksum):

    s3 = get_s3_client()

    exists = check_existing_object(s3, bucket, key, checksum)

    if exists:
        return "SKIPPED"

    s3.upload_file(str(local_path), bucket, key,
                   ExtraArgs={
                       "ContentType": "application/vnd.apache.parquet",
                       "Metadata": {
                           "sha256": checksum,
                           "source": "nyc-tlc",
                           "dataset": "yellow-taxi"
                       }
                   })

    response = s3.head_object(Bucket=bucket, Key=key)

    if response["ContentLength"] != local_path.stat().st_size:
        raise ValueError(
            "Uploaded object size verification failed"
        )

    print("S3 Upload Successful")

    return "UPLOADED"