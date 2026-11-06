import pyarrow.parquet as pq

def validate_parquet(file_path):
    # Check the valid of parquet file (structure & metadata)
    try:
        parquet_file = pq.ParquetFile(file_path)

        metadata = parquet_file.metadata
        schema = parquet_file.schema_arrow

        record_count = metadata.num_rows
        column_count = len(schema.names)

        if record_count == 0:
            raise ValueError("Parquet contains no record")
        if column_count == 0:
            raise ValueError("Parquet contains no columns")

        result = {
            "records": record_count,
            "columns": column_count,
            "schema": str(schema),
            "row_groups": metadata.num_row_groups
        }

        return result


    except Exception as error:
        raise ValueError(f"Parquet validation failed: {error}") from error