import yaml
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import logging

logging.basicConfig( level = logging.INFO )
logger = logging.getLogger( __name__ )

def create_db_engine() -> Engine:
  config = yaml.safe_load( open( 'config/config.yaml' ) )
  
  db_config = config[ 'database' ]

  # Build connection string
  connection_string = (
    f"mysql+pymysql://{ db_config[ 'user' ] }:{ db_config[ 'password' ] }"
    f"@{ db_config[ 'host' ] }:{ db_config[ 'port' ] }/{ db_config[ 'database' ] }"
  )

  logger.info( f"Connecting to database: { db_config[ 'database' ] }" )
  
  return create_engine( connection_string, echo = False )

def test_db_connection() -> bool:
  try:
    logger.info( "Testing database connection..." )
    engine = create_db_engine()

    with engine.connect() as connection:
      result = connection.execute( text( "SELECT VERSION()" ) )
      logger.info( "Checking database version..." )
      version = result.fetchone()
      logger.info( f"Database version: { version[ 0 ] }" )

    logger.info( "Database connection test successful" )
    return True

  except Exception as e:
    logger.error( f"Error testing database connection: { e }" )
    return False

if __name__ == "__main__":
  # Test database connection on startup
  test_db_connection()