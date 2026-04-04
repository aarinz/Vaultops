variable "aws_region" {
  default = "us-east-1"
}

variable "environment" {
  default = "dev"
}

variable "db_username" {
  default = "vaultops_user"
}

variable "db_password" {
  description = "Postgres password"
  sensitive   = true
}