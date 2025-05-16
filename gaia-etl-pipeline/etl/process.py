import logging
import dask.dataframe as dd

logger = logging.getLogger(__name__)

def process_gaia_dataframe(df: dd.DataFrame) -> dd.DataFrame:
    logger.info("Processing Gaia DataFrame")
    
    # Drop unnecessary columns if they exist
    drop_columns = [col for col in ['random_index', 'phot_variable_flag', 'solution_id'] if col in df.columns]
    if drop_columns:
        logger.info(f"Dropping columns: {drop_columns}")
        df = df.drop(columns=drop_columns)
    
    return df
