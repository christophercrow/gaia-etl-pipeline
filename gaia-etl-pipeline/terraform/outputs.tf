# Public endpoint of the RDS PostgreSQL instance
output "rds_endpoint" {
  description = "Hostname endpoint of the Gaia RDS PostgreSQL instance"
  value       = aws_db_instance.gaia_db.address
}

# Public IP of the EC2 instance running the ETL pipeline
output "etl_server_ip" {
  description = "Public IP address of the EC2 instance for running ETL tasks"
  value       = aws_instance.etl_server.public_ip
}
