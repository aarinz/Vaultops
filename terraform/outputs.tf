output "ec2_public_ip" {
  value = aws_instance.vaultops_backend.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.vaultops_db.endpoint
}

output "s3_bucket_name" {
  value = aws_s3_bucket.vaultops_artifacts.bucket
}