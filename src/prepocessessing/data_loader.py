# System
import logging
# Database
from sqlalchemy import Engine, text
# Data manipulation
import pandas as pd

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def load_data_from_star_schema( engine: Engine ) -> pd.DataFrame:
  try:
    logger.info( "Loading data from star schema..." )

    sql = """
      SELECT 
        -- Time features
        dt.step,
        dt.hour,
        dt.day,

        -- Tx type
        tt.type_name,

        -- Account info 
        da_orig.account_id as origin_account,
        da_orig.account_type as origin_type,
        da_dest.account_id as destination_account,
        da_dest.account_type as destination_type,

        -- Tx amount
        ft.amount,
        ft.old_balance_orig,
        ft.new_balance_orig,
        ft.old_balance_dest,
        ft.new_balance_dest,

        -- Tx measures
        ft.is_fraud,
        ft.is_flagged_fraud 

      FROM fact_transactions ft 
      INNER JOIN dim_time dt ON ft.time_key = dt.id 
      INNER JOIN dim_transaction_type tt ON ft.type_key = tt.id 
      INNER JOIN dim_account da_orig ON ft.origin_account_key = da_orig.id 
      INNER JOIN dim_account da_dest ON ft.destination_account_key = da_dest.id 
    """

    with engine.connect() as connection:
      df = pd.read_sql_query( sql, connection )

    logger.info( f"Data loaded successfully: { df.shape[0] } rows" )

    return df
  except Exception as e:
    logger.error( f"Error loading data: { e }" )
    raise