# AWS region for deploying resources
variable "aws_region" {
  type    = string
  default = "us-east-1"
  description = "The AWS region to deploy the infrastructure in."
}

# CIDR block allowed to SSH into EC2 instances
variable "admin_cidr" {
  type    = string
  default = "0.0.0.0/0"
  description = "CIDR block that is allowed to access EC2 via SSH."
}

# RDS instance type and storage configuration
variable "db_instance_class" {
  type    = string
  default = "db.m5.large"
  description = "The class/type of the RDS PostgreSQL instance."
}

variable "db_allocated_storage" {
  type    = number
  default = 100
  description = "Initial allocated storage (in GB) for the RDS instance."
}

variable "db_max_allocated_storage" {
  type    = number
  default = 500
  description = "Maximum storage RDS can scale to (in GB)."
}

# RDS credentials
variable "db_username" {
  type        = string
  default     = "gaia"
  description = "Database admin username."
}

variable "db_password" {
  type      = string
  sensitive = true
  description = "Database admin password."
}

# EC2 instance configuration
variable "ec2_ami_id" {
  type        = string
  description = "AMI ID for the EC2 instance."
}

variable "ec2_instance_type" {
  type    = string
  default = "m5.xlarge"
  description = "Instance type for the ETL EC2 server."
}

# SSH key for EC2 access
variable "ssh_key_name" {
  type        = string
  description = "Name of the SSH key pair to access the EC2 instance."
}
