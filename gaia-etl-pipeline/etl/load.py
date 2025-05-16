import os
import time
import logging
import dask.dataframe as dd
from sqlalchemy import create_engine

def load_dask_dataframe_to_db(df: dd.DataFrame, db_url: str):
    """
    Writes a Dask DataFrame to a PostgreSQL database using SQLAlchemy.

    Each partition is processed and inserted in bulk using pandas and `to_sql`.

    Args:
        df (dd.DataFrame): Transformed Gaia data.
        db_url (str): SQLAlchemy-compatible database URL.
    """
    engine = create_engine(db_url)
    total_parts = df.npartitions

    logging.info(f"[load] Connecting to database at {db_url}")
    logging.info(f"[load] Preparing to write {total_parts} partitions")

    overall_start = time.time()
    delayed_parts = df.to_delayed()

    for idx, part in enumerate(delayed_parts, start=1):
        try:
            part_start = time.time()
            pdf = dd.from_delayed(part).compute()
            pdf.to_sql(
                "gaia_source",
                engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=10000
            )
            logging.info(f"[load] Partition {idx}/{total_parts} inserted in {time.time() - part_start:.2f}s")
        except Exception as e:
            logging.error(f"[load] Failed to insert partition {idx}: {e}")

    logging.info(f"[load] All partitions processed in {time.time() - overall_start:.2f}s")

if __name__ == "__main__":
    from etl.fetch import load_gaia_dataframe
    from etl.transform import process_gaia_dataframe

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    df = load_gaia_dataframe()
    df = process_gaia_dataframe(df)
    db_url = os.getenv("DATABASE_URL", "postgresql://gaia:mysecretpassword@db:5432/gaia")
    load_dask_dataframe_to_db(df, db_url)
