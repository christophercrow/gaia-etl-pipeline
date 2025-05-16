import os
import logging
from etl.fetch import load_gaia_dataframe
from etl.process import process_gaia_dataframe
from etl.load import load_dask_dataframe_to_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info(">>> Starting Gaia ETL pipeline")

    df = load_gaia_dataframe()
    df = process_gaia_dataframe(df)

    db_url = os.getenv("DB_URL", "postgresql://gaia:mysecretpassword@db:5432/gaia")
    load_dask_dataframe_to_db(df, db_url)

if __name__ == "__main__":
    main()
