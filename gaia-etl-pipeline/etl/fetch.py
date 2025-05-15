import os
import random
import logging
import dask.dataframe as dd
import fsspec
random.seed(int(os.getenv("SAMPLE_SEED", "42")))

# Configurable via env vars:
# - GAIA_CSV_URL: glob or single URL (default: all DR3 CSVs)
# - SAMPLE_FRACTION: float in (0,1], fraction of files to load
GAIA_CSV_URL = os.getenv(
    "GAIA_CSV_URL",
    "http://cdn.gea.esac.esa.int/Gaia/gdr3/gaia_source/*.csv.gz"
)
SAMPLE_FRACTION = float(os.getenv("SAMPLE_FRACTION", "0"))

def load_gaia_dataframe():
    print(f">>> [fetch] GAIA_CSV_URL = {GAIA_CSV_URL}")
    logging.info(f"Loading Gaia data from {GAIA_CSV_URL}")

    # If SAMPLE_FRACTION is set, list and sample the file URLs:
    if 0 < SAMPLE_FRACTION < 1.0:
        fs, paths = fsspec.core.get_fs_token_paths(GAIA_CSV_URL, storage_options={})
        # paths is a tuple (fs, list_of_paths); we only need the list
        all_files = paths
        sample_count = max(1, int(len(all_files) * SAMPLE_FRACTION))
        sampled = random.sample(all_files, sample_count)
        logging.info(f"Sampling {sample_count}/{len(all_files)} files ({SAMPLE_FRACTION*100:.1f}%)")
        file_list = sampled
    else:
        # Default: pass the glob string, letting Dask expand itself
        file_list = GAIA_CSV_URL

    df = dd.read_csv(
        file_list,
        assume_missing=True,
        blocksize=None,
        sep=",",
        comment="#",
        header=0,
        on_bad_lines="skip",
        compression="gzip",
        dtype_backend="numpy_nullable"
    )
    return df
    # Note: dtype_backend="numpy_nullable" is needed for Dask 2023.7.0+