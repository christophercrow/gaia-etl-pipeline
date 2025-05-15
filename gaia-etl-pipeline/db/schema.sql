CREATE EXTENSION IF NOT EXISTS postgis;

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

DO $$
BEGIN
    FOR i IN 0..15 LOOP
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS gaia_source_part_%02s PARTITION OF gaia_source FOR VALUES WITH (MODULUS 16, REMAINDER %s)',
            i, i);
    END LOOP;
END$$;

DO $$
BEGIN
    FOR i IN 0..15 LOOP
        EXECUTE format(
            'CREATE INDEX IF NOT EXISTS idx_gaia_geom_part_%02s ON gaia_source_part_%02s USING GIST (geom)',
            i, i);
    END LOOP;
END$$;
