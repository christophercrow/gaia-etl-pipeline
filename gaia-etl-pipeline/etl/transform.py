import dask.dataframe as dd
import logging
import time

# Columns we want to retain in the transformed dataset
DESIRED_COLS = [
    "source_id", "ra", "dec", "parallax",
    "pmra", "pmdec", "phot_g_mean_mag"
]

def process_gaia_dataframe(df: dd.DataFrame) -> dd.DataFrame:
    """
    Transforms a Dask DataFrame by selecting relevant columns,
    ensuring data types, and cleaning invalid rows.

    Args:
        df (dd.DataFrame): Raw Gaia data.

    Returns:
        dd.DataFrame: Cleaned and filtered data.
    """
    logging.info("[transform] Starting transformation process")
    start = time.time()

    # Drop specific unnecessary columns if they exist
    drop_candidates = ["random_index", "phot_variable_flag", "solution_id"]
    to_drop = [col for col in drop_candidates if col in df.columns]
    if to_drop:
        logging.info(f"[transform] Dropping columns: {to_drop}")
        df = df.drop(columns=to_drop)

    # Select the desired columns, warn if some are missing
    available = [col for col in DESIRED_COLS if col in df.columns]
    missing = set(DESIRED_COLS) - set(available)
    if missing:
        logging.warning(f"[transform] Missing expected columns: {missing}")
    df = df[available]

    # Enforce correct data types
    if "source_id" in df.columns:
        df["source_id"] = df["source_id"].astype("int64")

    # Drop rows with missing coordinates
    df = df.dropna(subset=["ra", "dec"])

    # Repartition the data for optimal chunk size
    before = df.npartitions
    df = df.repartition(partition_size="100MB")
    after = df.npartitions

    logging.info(f"[transform] Repartitioned from {before} to {after} partitions")
    logging.info(f"[transform] Completed in {time.time() - start:.2f} seconds")
    return df
