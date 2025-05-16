#!/bin/bash
set -e

# Description:
# This script runs on EC2 instance startup to install required tools
# and launch the Gaia ETL pipeline via Docker Compose.

export DEBIAN_FRONTEND=noninteractive

# Update packages and install Docker tools
apt-get update
apt-get install -y docker.io docker-compose git

# Enable and start Docker service
systemctl enable docker
systemctl start docker

# Clone the project repository
cd /opt
if [ ! -d "gaia-etl-pipeline" ]; then
  git clone https://github.com/christophercrow/gaia-etl-pipeline.git
fi

cd gaia-etl-pipeline

# Launch the pipeline using Docker Compose
docker compose up -d
