#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y docker.io docker-compose git
cd /opt
git clone https://github.com/<your-user>/gaia-etl-pipeline.git || true
cd gaia-etl-pipeline
docker compose up -d