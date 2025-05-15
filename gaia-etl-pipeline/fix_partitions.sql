-- fix_partitions.sql

-- 1) Drop any mis-named partitions with spaces in their names
DO $$
DECLARE
  r RECORD;
BEGIN
  FOR r IN (
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_name LIKE 'gaia_source_part_%'
      AND table_name LIKE '% %'  -- names containing spaces
  )
  LOOP
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
    EXECUTE
      'CREATE TABLE IF NOT EXISTS gaia_source_part_' || part_name ||
      ' PARTITION OF gaia_source FOR VALUES WITH (MODULUS 16, REMAINDER ' || i || ')';
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
    EXECUTE
      'CREATE INDEX IF NOT EXISTS idx_gaia_geom_part_' || part_name ||
      ' ON gaia_source_part_' || part_name || ' USING GIST (geom)';
  END LOOP;
END
$$;

