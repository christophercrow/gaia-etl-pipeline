# Variables
GAIA_CSV_URL=http://cdn.gea.esac.esa.int/Gaia/gdr3/gaia_source/GaiaSource_000000-003111.csv.gz
DB_CONTAINER=gaia-etl-pipeline-db-1
SAMPLE_FRACTION=0.001

# Build Docker images
build:
	docker compose build --no-cache

# Start only the database
start-db:
	docker compose up -d db

# Load schema and extensions (handled by container entrypoint)
init-db: start-db

# Run ETL with a small sample
etl-sample:
	docker compose run --rm -e GAIA_CSV_URL=$(GAIA_CSV_URL) etl

# Run ETL over full dataset with sampling
etl-full:
	docker compose run --rm -e SAMPLE_FRACTION=$(SAMPLE_FRACTION) etl

# Apply PostGIS geometry for spatial queries
apply-geom:
	docker exec -i $(DB_CONTAINER) psql -U gaia -d gaia -c "UPDATE gaia_source SET geom = ST_SetSRID(ST_MakePoint(ra, dec), 4326);"

# Start API
start-api:
	docker compose up -d api

# Test API with example query
test-api:
	curl "http://localhost:8000/stars?ra=45.0&dec=0.0&radius=0.5"

# Shutdown everything and wipe volumes
reset:
	docker compose down -v

# All-in-one pipeline
all: build init-db etl-sample apply-geom start-api test-api
