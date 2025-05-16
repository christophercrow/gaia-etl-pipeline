import os
import logging
from astropy.table import Table
import dask.dataframe as dd
import pandas as pd

logger = logging.getLogger(__name__)

def load_gaia_dataframe():
    gaia_csv_url = os.getenv("GAIA_CSV_URL")
    sample_fraction = os.getenv("SAMPLE_FRACTION")

    if gaia_csv_url:
        logger.info(f"[fetch] GAIA_CSV_URL = {gaia_csv_url}")
        return load_gaia_dataframe_from_ecsv(gaia_csv_url)
    elif sample_fraction:
        logger.info(f"[fetch] SAMPLE_FRACTION = {sample_fraction}")
        # Optional: implement logic to download random subset using TAP service
        raise NotImplementedError("Sampling via TAP is not implemented yet.")
    else:
        raise ValueError("Either GAIA_CSV_URL or SAMPLE_FRACTION must be set.")

def load_gaia_dataframe_from_ecsv(url: str) -> dd.DataFrame:
    logger.info(f"Loading Gaia data from {url}")
    table = Table.read(url, format='ascii.ecsv')
    df = table.to_pandas()
    return dd.from_pandas(df, npartitions=1)
