# etl/fetch.py
import dask.dataframe as dd
import logging

GAIA_CSV_URL = "http://cdn.gea.esac.esa.int/Gaia/gdr3/gaia_source/*.csv.gz"

def load_gaia_dataframe():
    logging.info("Loading Gaia CSV data via Dask")
    df = dd.read_csv(
        GAIA_CSV_URL,
        assume_missing=True,
        blocksize="64MB",
        compression="gzip",
        dtype_backend="numpy_nullable"
    )
    return df
