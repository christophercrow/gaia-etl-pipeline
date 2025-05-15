import psycopg2
import io
import logging
from dask.dataframe import DataFrame as DaskDataFrame

def copy_partition_to_db(pdf, conn):
    csv_buffer = io.StringIO()
    pdf.to_csv(csv_buffer, index=False, header=False)
    csv_buffer.seek(0)
    cols = ",".join(pdf.columns)
    with conn.cursor() as cur:
        cur.copy_expert(
            f"COPY gaia_source({cols}) FROM STDIN WITH (FORMAT CSV)",
            csv_buffer
        )
    conn.commit()

def load_dask_dataframe_to_db(df: DaskDataFrame, db_dsn: str):
    logging.info("Connecting to DB")
    conn = psycopg2.connect(db_dsn)
    total = df.npartitions
    logging.info(f"Loading {total} partitions")
    for i in range(total):
        logging.info(f"Loading partition {i+1}/{total}")
        pdf = df.get_partition(i).compute()
        try:
            copy_partition_to_db(pdf, conn)
        except Exception as e:
            logging.error(f"Error on partition {i+1}: {e}")
            conn.rollback()
            continue
    conn.close()