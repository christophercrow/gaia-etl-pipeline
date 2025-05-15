#!/bin/bash
set -e

# Create root directory
mkdir -p gaia-etl-pipeline
cd gaia-etl-pipeline

# Create Python package structure
echo "Creating ETL package..."
mkdir -p etl
touch etl/__init__.py etl/fetch.py etl/transform.py etl/load.py etl/__main__.py

echo "Creating API package..."
mkdir -p api
touch api/__init__.py api/main.py api/routes.py api/models.py

# Create database scripts
echo "Creating DB schema files..."
mkdir -p db
touch db/schema.sql db/partition_fn.sql

# Create Terraform config
echo "Creating Terraform infrastructure..."
mkdir -p terraform
touch terraform/main.tf terraform/variables.tf terraform/outputs.tf terraform/ec2_user_data.sh

# Create CI/CD pipeline
echo "Creating GitHub Actions workflow..."
mkdir -p .github/workflows
touch .github/workflows/ci.yml

# Create root files
echo "Creating root configuration files..."
touch docker-compose.yml Dockerfile.etl Dockerfile.api requirements.txt README.md

echo "Project structure created successfully!"
tree -aI .git
