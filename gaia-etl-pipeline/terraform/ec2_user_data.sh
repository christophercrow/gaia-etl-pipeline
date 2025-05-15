#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y docker.io docker-compose git

# Clone and start services
cd /opt
if [ ! -d gaia-etl-pipeline ]; then
  git clone https://github.com/<your-user>/gaia-etl-pipeline.git
fi
cd gaia-etl-pipeline
docker compose up -d
