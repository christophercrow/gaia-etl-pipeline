# etl/transform.py

import dask.dataframe as dd
import logging

# The exact set of table columns in public.gaia_source (geom is omitted here)
DESIRED_COLS = [
    "source_id",
    "ra",
    "dec",
    "parallax",
    "pmra",
    "pmdec",
    "phot_g_mean_mag",
]

def process_gaia_dataframe(df: dd.DataFrame) -> dd.DataFrame:
    logging.info("Processing Gaia DataFrame")

    to_drop = ["random_index", "phot_variable_flag", "solution_id"]
    existing_drops = [c for c in to_drop if c in df.columns]
    if existing_drops:
        logging.info(f"Dropping columns: {existing_drops}")
        df = df.drop(columns=existing_drops)

    available = [c for c in DESIRED_COLS if c in df.columns]
    missing = set(DESIRED_COLS) - set(available)
    if missing:
        logging.warning(f"Expected columns missing from CSV and will be null: {missing}")
    df = df[available]

    if "source_id" in df.columns:
        df["source_id"] = df["source_id"].astype("int64")

    df = df.dropna(subset=["ra", "dec"])

    df = df.repartition(partition_size="100MB")
    logging.info(f"Repartitioned into {df.npartitions} partitions")

    return df
