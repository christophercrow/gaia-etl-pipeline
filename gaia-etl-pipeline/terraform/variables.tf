variable "aws_region" { type = string; default = "us-east-1" }
variable "admin_cidr" { type = string; default = "0.0.0.0/0" }
variable "db_instance_class" { type = string; default = "db.m5.large" }
variable "db_allocated_storage" { type = number; default = 100 }
variable "db_max_allocated_storage" { type = number; default = 500 }
variable "db_username" { type = string; default = "gaia" }
variable "db_password" { type = string; sensitive = true }
variable "ec2_ami_id" { type = string }
variable "ec2_instance_type" { type = string; default = "m5.xlarge" }
variable "ssh_key_name" { type = string }