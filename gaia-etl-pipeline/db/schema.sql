-- Enable PostGIS extension for spatial queries
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create parent partitioned table for Gaia source data
CREATE TABLE IF NOT EXISTS gaia_source (
    source_id BIGINT NOT NULL,
    ra DOUBLE PRECISION,
    dec DOUBLE PRECISION,
    parallax REAL,
    pmra REAL,
    pmdec REAL,
    phot_g_mean_mag REAL,
    geom GEOMETRY(Point, 4326)
) PARTITION BY HASH (source_id);

-- Create 16 hash partitions with padded names (e.g., gaia_source_part_00)
DO $$
DECLARE
  i INT;
  part_name TEXT;
BEGIN
  FOR i IN 0..15 LOOP
    part_name := lpad(i::text, 2, '0');
    EXECUTE format(
      'CREATE TABLE IF NOT EXISTS gaia_source_part_%s PARTITION OF gaia_source FOR VALUES WITH (MODULUS 16, REMAINDER %s)',
      part_name, i
    );
  END LOOP;
END
$$;

-- Create spatial indexes for each partition
DO $$
DECLARE
  i INT;
  part_name TEXT;
BEGIN
  FOR i IN 0..15 LOOP
    part_name := lpad(i::text, 2, '0');
    EXECUTE format(
      'CREATE INDEX IF NOT EXISTS idx_gaia_geom_part_%s ON gaia_source_part_%s USING GIST (geom)',
      part_name, part_name
    );
  END LOOP;
END
$$;
