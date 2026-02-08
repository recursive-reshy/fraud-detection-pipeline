# System imports
import sys
import yaml
import logging
from pathlib import Path
# Database
from sqlalchemy import Engine, text
# Data manipulation
import pandas as pd

# Add parent directory to path to import custom modules
sys.path.append( str( Path( __file__ ).parent.parent.parent ) )
from src.database import create_db_engine
from src.ingestion.schema_validation import validate_schema

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def verify_ingestion( engine: Engine, expected_rows: int ) -> None:
  try:
    logger.info( f"Verifying ingestion..." )
  
    with engine.connect() as connection:
      result = connection.execute( text( "SELECT COUNT(*) FROM staging_transactions" ) )
      actual_rows = result.fetchone()[ 0 ]

      if actual_rows != expected_rows:
        logger.error( f"Expected { expected_rows } rows, but got { actual_rows }" )
        raise ValueError( f"Expected { expected_rows } rows, but got { actual_rows }" )
      else:
        logger.info( f"Row count matches" )
      
      # Check fraud distribution
      result = connection.execute( text(
        "SELECT isFraud, COUNT(*) as count "
        "FROM staging_transactions "
        "GROUP BY isFraud"
      ) )

      logger.info( "Fraud distribution:" )
      for row in result:
        fraud_label = "fraudulent" if row[ 0 ] == 1 else "not fraudulent"
        count = row[ 1 ]
        percentage = ( count / expected_rows ) * 100
        logger.info( f"{ fraud_label }: { count } rows ({ percentage:.2f}%)" )

      # Check transaction types
      result = connection.execute( text( 
        "SELECT type, COUNT(*) as count "
        "FROM staging_transactions "
        "GROUP BY type "
        "ORDER BY count DESC "
      ) )

      logger.info( "Transaction type distribution:" )
      for row in result:
        logger.info( f"{ row[ 0 ] }: { row[ 1 ] } rows" )

      logger.info( f"Ingestion verified successfully" )

  except Exception as e:
    logger.error( f"Error verifying ingestion: { e }" )
    raise

def load_staging_table( csv_file_path: str, chunk_size: int = 1000 ) -> None:
  try:

    validate_schema( csv_file_path )
    
    engine = create_db_engine()

    logger.info( "Clearing existing data..." )
    # Clear existing data
    with engine.connect() as connection:
      connection.execute( text( "TRUNCATE TABLE staging_transactions" ) )
      connection.commit()
    logger.info( "Existing data cleared" )

    logger.info( f"Loading staging table from { csv_file_path }..." )

    logger.info( "Counting rows..." )
    with open( csv_file_path, 'r' ) as file:
      total_rows = sum( 1 for _ in file ) - 1 # Subtract header row
    logger.info( f"Total rows: { total_rows }" )

    # Load in chunks for memory efficiency
    rows_ingested = 0
    for chunk in pd.read_csv( csv_file_path, chunksize = chunk_size ):
      chunk.to_sql( 
        'staging_transactions', 
        con = engine, 
        if_exists = 'append', 
        index = False,
        method = 'multi'
      )

    rows_ingested += len( chunk )
  
    logger.info( "CSV ingestion completed" )
    
    verify_ingestion( engine, total_rows )

  except Exception as e:
    logger.error( f"Error loading staging table: { e }" )
    raise

if __name__ == "__main__":
  if( len( sys.argv ) > 1 ):
    csv_file_path = sys.argv[ 1 ]
  else:
    # Use default path from config
    config = yaml.safe_load( open( 'config/config.yaml' ) )
    csv_file_path = config.get( 'data', {} ).get( 'raw_csv', 'data/raw/paysim1.csv' )

  load_staging_table( csv_file_path )
  