import dask.dataframe as dd
import logging

def process_gaia_dataframe(df: dd.DataFrame) -> dd.DataFrame:
    logging.info("Processing Gaia DataFrame")
    # Example: drop any unneeded columns
    cols_to_drop = ["random_index", "phot_variable_flag"]
    for col in cols_to_drop:
        if col in df.columns:
            df = df.drop(columns=col)
    # Cast source_id to int
    if "source_id" in df.columns:
        df["source_id"] = df["source_id"].astype("int64")
    # Drop rows missing coordinates
    df = df.dropna(subset=["ra", "dec"])
    # Repartition to ~100MB partitions
    df = df.repartition(partition_size="100MB")
    logging.info(f"Repartitioned into {df.npartitions} partitions")
    return df