terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 bucket — stores release artifacts (diff files, release notes)
resource "aws_s3_bucket" "vaultops_artifacts" {
  bucket = "vaultops-artifacts-${var.environment}"
  force_destroy = true

  tags = {
    Project     = "VaultOps"
    Environment = var.environment
  }
}

# RDS PostgreSQL — stores releases, risk scores, BA decisions
resource "aws_db_instance" "vaultops_db" {
  identifier        = "vaultops-db"
  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  db_name           = "vaultops"
  username          = var.db_username
  password          = var.db_password
  publicly_accessible = true
  skip_final_snapshot = true

  tags = {
    Project = "VaultOps"
  }
}

# EC2 — runs the FastAPI backend
resource "aws_instance" "vaultops_backend" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2, us-east-1
  instance_type = "t3.micro"

  tags = {
    Name    = "vaultops-backend"
    Project = "VaultOps"
  }
}