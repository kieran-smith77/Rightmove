locals {
  bucketname = "kieran-smith-rightmove"

}

# S3 Bucket for DB
resource "aws_s3_bucket" "db_store" {
  bucket = "${local.bucketname}-db"
}

resource "aws_s3_bucket_acl" "db_store_acl" {
  bucket = aws_s3_bucket.db_store.id
  acl    = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "db_store_encyption" {
  bucket = aws_s3_bucket.db_store.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 Bucket for Website Code
resource "aws_s3_bucket" "code_store" {
  bucket = "${local.bucketname}-code"
}

resource "aws_s3_bucket_acl" "code_store_acl" {
  bucket = aws_s3_bucket.code_store.id
  acl    = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "code_store_encyption" {
  bucket = aws_s3_bucket.code_store.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "null_resource" "remove_and_upload_to_s3" {
  provisioner "local-exec" {
    command = "aws s3 sync ../website s3://${aws_s3_bucket.code_store.id}  --exclude 'venv/*' --delete --profile personal"
  }
  triggers = {
    build_number = "16"
  }
}