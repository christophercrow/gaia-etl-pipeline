variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region"
}

variable "admin_cidr" {
  type        = string
  default     = "0.0.0.0/0"
  description = "SSH access CIDR"
}

variable "db_instance_class" {
  type        = string
  default     = "db.m5.large"
  description = "RDS instance class"
}

variable "db_allocated_storage" {
  type        = number
  default     = 100
  description = "Initial DB storage (GB)"
}

variable "db_max_allocated_storage" {
  type        = number
  default     = 500
  description = "Max DB auto-scale (GB)"
}

variable "db_username" {
  type        = string
  default     = "gaia"
  description = "DB admin user"
}

variable "db_password" {
  type        = string
  description = "DB admin password"
  sensitive   = true
}

variable "ec2_ami_id" {
  type        = string
  description = "AMI ID for ETL host"
}

variable "ec2_instance_type" {
  type        = string
  default     = "m5.xlarge"
  description = "ETL EC2 instance type"
}

variable "ssh_key_name" {
  type        = string
  description = "Name of SSH key pair"
}
