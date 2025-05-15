import os
import logging
from etl.fetch import load_gaia_dataframe
from etl.transform import process_gaia_dataframe
from etl.load import load_dask_dataframe_to_db

# Sanity print
print(">>> ETL started, GAIA_CSV_URL=", os.getenv("GAIA_CSV_URL"))

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        logging.error("DATABASE_URL not set")
        return
    df = load_gaia_dataframe()
    df2 = process_gaia_dataframe(df)
    load_dask_dataframe_to_db(df2, db_url)

if __name__ == "__main__":
    main()