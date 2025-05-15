output "rds_endpoint" {
  description = "RDS endpoint"
  value       = aws_db_instance.gaia_db.address
}

output "etl_server_ip" {
  description = "ETL server public IP"
  value       = aws_instance.etl_server.public_ip
}
