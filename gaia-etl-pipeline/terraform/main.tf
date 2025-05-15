terraform {
  required_providers {
    aws = { source = "hashicorp/aws" }
  }
}
provider "aws" { region = var.aws_region }

resource "aws_security_group" "etl_sg" {
  name        = "gaia-etl-sg"
  ingress = [
    { protocol = "tcp", from_port = 22, to_port = 22, cidr_blocks = [var.admin_cidr] },
    { protocol = "tcp", from_port = 8000, to_port = 8000, cidr_blocks = ["0.0.0.0/0"] }
  ]
  egress = [{ protocol = "-1", from_port = 0, to_port = 0, cidr_blocks = ["0.0.0.0/0"] }]
}
resource "aws_security_group" "db_sg" {
  name        = "gaia-db-sg"
  ingress     = [{ protocol = "tcp", from_port = 5432, to_port = 5432, security_groups = [aws_security_group.etl_sg.id] }]
  egress      = [{ protocol = "-1", from_port = 0, to_port = 0, cidr_blocks = ["0.0.0.0/0"] }]
}
resource "aws_db_instance" "gaia_db" {
  engine            = "postgres"
  engine_version    = "14.8"
  instance_class    = var.db_instance_class
  allocated_storage = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage
  db_name           = "gaia"
  username          = var.db_username
  password          = var.db_password
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  skip_final_snapshot    = true
}
resource "aws_instance" "etl_server" {
  ami                    = var.ec2_ami_id
  instance_type          = var.ec2_instance_type
  vpc_security_group_ids = [aws_security_group.etl_sg.id]
  key_name               = var.ssh_key_name
  user_data              = file("ec2_user_data.sh")
}