# System
import sys
import logging
from pathlib import Path

# Add parent directory to path to import database module
sys.path.append( str( Path( __file__ ).parent.parent.parent ) )
from src.database import create_db_engine
from src.ingestion.populate_dimensions import populate_dim_time, populate_dim_account
from src.ingestion.populate_facts import populate_fact_transactions, verify_referential_integrity, show_fraud_distribution

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def populate_star_schema() -> None:
  try:
    engine = create_db_engine()
    logger.info( "Populating star schema..." )

    populate_dim_time( engine )

    populate_dim_account( engine )

    populate_fact_transactions( engine )

    verify_referential_integrity( engine )

    show_fraud_distribution( engine )

    logger.info( "Star schema populated successfully" )

  except Exception as e:
    logger.error( f"Error populating star schema: { e }" )
    raise

if __name__ == "__main__":
  populate_star_schema()