import os
import dask.dataframe as dd
import logging

# Pull from env var if present (for sample tests), else default to the full Gaia DR3 glob
GAIA_CSV_URL = os.getenv(
    "GAIA_CSV_URL",
    "http://cdn.gea.esac.esa.int/Gaia/gdr3/gaia_source/*.csv.gz"
)

def load_gaia_dataframe():
    # Sanity print so we know exactly what URL/glob is being used
    print(f">>> [fetch] GAIA_CSV_URL = {GAIA_CSV_URL}")

    logging.info(f"Loading Gaia data from {GAIA_CSV_URL}")
    # Read in CSV(s) via Dask, skipping any comment lines and malformed rows
    df = dd.read_csv(
        GAIA_CSV_URL,
        assume_missing=True,    # allow integer columns with NaNs
        blocksize=None,         # gzip cannot be split into byte ranges
        sep=",",                # explicit comma delimiter
        comment="#",            # skip ESA metadata lines
        header=0,               # first non-comment line is header
        on_bad_lines="skip",    # drop any malformed rows
        compression="gzip",
        dtype_backend="numpy_nullable"
    )
    return df
