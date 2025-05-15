output "rds_endpoint" { value = aws_db_instance.gaia_db.address }
output "etl_server_ip" { value = aws_instance.etl_server.public_ip }