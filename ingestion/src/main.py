from config import SOURCE_URL, LOCAL_FILE_PATH, S3_BUCKET_BRONZE, S3_BRONZE_KEY
from validator import validate_parquet
from s3_uploader import upload_file
from downloader import (download_file, calculate_sha256)

def main():
    if not S3_BUCKET_BRONZE:
        raise ValueError("S3_BUCKET_BRONZE is not configured.")
    
    print("Starting NYC Taxi Data Ingestion")

    # Step 1 - Download
    file_path = download_file(SOURCE_URL, LOCAL_FILE_PATH)

    # Step 2 - Checksum
    checksum = calculate_sha256(file_path)

    # Step 3 - Validate parquet file
    metadata = validate_parquet(file_path)

    print("\nDownload and Validation Successful...")

    # Step 4 - Upload to S3
    status = upload_file(
        file_path, S3_BUCKET_BRONZE, S3_BRONZE_KEY, checksum
    )

    # Step 5: Report

    print("\nIngestion Summary")
    print("-------------------")

    print("File:", file_path.name)
    print("SHA256:", checksum)
    print("Records:", metadata["records"])
    print("Columns:", metadata["columns"])
    print("Row Groups:", metadata["row_groups"])
    print("S3 Key (Bronze):", S3_BRONZE_KEY)
    print("Status:", status)

    print("\nIngestion Completed.")



if __name__ == "__main__":
    main()