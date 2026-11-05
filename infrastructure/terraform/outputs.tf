output "data_lake_bucket_name" {
  description = "S3 Data Lake Bucket Name"
  value       = aws_s3_bucket.data_lake.bucket
}

output "data_lake_bucket_arn" {
  description = "S3 Data Lake Bucket ARN"
  value       = aws_s3_bucket.data_lake.arn
}