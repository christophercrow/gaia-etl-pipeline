-- fix_partitions.sql
-- This script ensures clean partitioning for the `gaia_source` table.
-- It drops malformed partitions, recreates correct ones, and sets up spatial indexes.

-- 1) Drop any partitions with invalid names (e.g. containing spaces)
DO $$
DECLARE
  r RECORD;
BEGIN
  FOR r IN (
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_name LIKE 'gaia_source_part_%'
      AND table_name LIKE '% %'  -- detect names with spaces
  ) LOOP
    RAISE NOTICE 'Dropping malformed partition: %', r.table_name;
    EXECUTE format('DROP TABLE IF EXISTS %I', r.table_name);
  END LOOP;
END
$$;

-- 2) Recreate 16 hash partitions with zero-padded names
DO $$
DECLARE
  i INT;
  part_name TEXT;
BEGIN
  FOR i IN 0..15 LOOP
    part_name := lpad(i::text, 2, '0');
    EXECUTE format('
      CREATE TABLE IF NOT EXISTS gaia_source_part_%s
      PARTITION OF gaia_source
      FOR VALUES WITH (MODULUS 16, REMAINDER %s)
    ', part_name, i);
  END LOOP;
END
$$;

-- 3) Recreate spatial indexes on each partition
DO $$
DECLARE
  i INT;
  part_name TEXT;
BEGIN
  FOR i IN 0..15 LOOP
    part_name := lpad(i::text, 2, '0');
    EXECUTE format('
      CREATE INDEX IF NOT EXISTS idx_gaia_geom_part_%s
      ON gaia_source_part_%s USING GIST (geom)
    ', part_name, part_name);
  END LOOP;
END
$$;
