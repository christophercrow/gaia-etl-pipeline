-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Parent partitioned table
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

-- Create 16 hash partitions with zero-padded names
DO $$
DECLARE
  i INT;
  part_name TEXT;
BEGIN
  FOR i IN 0..15 LOOP
    part_name := lpad(i::text, 2, '0');
    EXECUTE
      'CREATE TABLE IF NOT EXISTS gaia_source_part_' || part_name || 
      ' PARTITION OF gaia_source FOR VALUES WITH (MODULUS 16, REMAINDER ' || i || ')';
  END LOOP;
END
$$;

-- Create GIST index on each partition
DO $$
DECLARE
  i INT;
  part_name TEXT;
BEGIN
  FOR i IN 0..15 LOOP
    part_name := lpad(i::text, 2, '0');
    EXECUTE
      'CREATE INDEX IF NOT EXISTS idx_gaia_geom_part_' || part_name || 
      ' ON gaia_source_part_' || part_name || ' USING GIST (geom)';
  END LOOP;
END
$$;