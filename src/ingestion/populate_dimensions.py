# System imports
import logging
# Database
from sqlalchemy import Engine, text

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def populate_dim_time( engine: Engine ) -> int:
  logger.info( "Clearing existing data..." )

  with engine.connect() as connection:
    # connection.execute( text( "TRUNCATE TABLE dim_time" ) )
    # connection.commit()
    logger.info( "Existing data cleared" )
    
    # Insert unique steps into dim_time
    sql = """
      INSERT INTO dim_time (step, hour, day) 
      SELECT DISTINCT 
        step,
        step % 24 as hour,
        FLOOR(step / 24) as day 
      FROM staging_transactions 
      ORDER BY step
    """
    logger.info( "Inserting unique steps into dim_time..." )
    connection.execute( text( sql ) )
    connection.commit()

    # Verify
    count_result = connection.execute( text( "SELECT COUNT(*) FROM dim_time" ) )
    count = count_result.fetchone()[ 0 ]

    logger.info( f"Unique steps inserted into dim_time: { count }" )

  return count

def populate_dim_account( engine: Engine ) -> int:
  logger.info( "Clearing existing data..." )

  with engine.connect() as connection:
    # connection.execute( text( "TRUNCATE TABLE dim_account" ) )
    # connection.commit()
    logger.info( "Existing data cleared" )
    
    logger.info( "Inserting unique accounts into dim_account..." )
    
    # Insert unique accounts into dim_account
    # Note from raw data nameOrig (account id) is C1231006815, hence why we use SUBSTRING(account_id, 1, 1) to get the account type
    sql = """
      INSERT INTO dim_account (account_id, account_type) 
      SELECT DISTINCT 
        account_id,
        SUBSTRING(account_id, 1, 1) as account_type 
      FROM (
        SELECT nameOrig as account_id FROM staging_transactions 
        UNION 
        SELECT nameDest as account_id FROM staging_transactions 
      ) AS all_accounts 
      ORDER BY account_id
    """
    connection.execute( text( sql ) )
    connection.commit()

    # Verify
    count_result = connection.execute( text( "SELECT COUNT(*) FROM dim_account" ) )
    count = count_result.fetchone()[ 0 ]
    logger.info( f"Unique accounts inserted into dim_account: { count }" )

  return count