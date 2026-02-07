# System imports
import sys
import logging
from pathlib import Path
# DB
from sqlalchemy import Engine, text

# Add parent directory to path to import database module
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.database import create_db_engine

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

# Helper function to read SQL file
def read_sql_file( file_path: str ) -> str:
  with open( file_path, 'r' ) as file:
    return file.read()

# Helper function to verify that the tables were created successfully
def verify_table_creation( engine: Engine, expected_tables: list[ str ] ) -> None:
  logger.info( "Verifying that the tables were created successfully..." )

  with engine.connect() as connection:
    result = connection.execute( text( "SHOW TABLES" ) )
    tables = result.fetchall()
    actual_tables = [ table[ 0 ] for table in tables ]
    for table in expected_tables:
      if table not in actual_tables:
        logger.error( f"Table { table } was not created" )
        raise Exception( f"Table { table } was not created" )
    logger.info( "All tables were created successfully" )


def create_star_schema() -> None:
  try:
    engine = create_db_engine()
    logger.info( "Creating star schema..." )

    sql_content = read_sql_file( 'sql/create_star_schema.sql' )
    
    # Split the SQL content into separate statements and execute them individually
    statements = [ statement.strip() for statement in sql_content.split( ';' ) if statement.strip() ]

    with engine.connect() as connection:
      for statement in statements:
        connection.execute( text( statement ) )
        connection.commit()
    
    verify_table_creation( engine, [ 'dim_transaction_type', 'dim_time', 'dim_account', 'fact_transactions' ] )

    logger.info( "Star schema created successfully" )
  except Exception as e:
    logger.error( f"Error creating star schema: { e }" )
    raise

def create_staging_table() -> None:
  try:
    engine = create_db_engine()
    logger.info( "Creating staging table..." )

    sql_content = read_sql_file( 'sql/create_staging_table.sql' )
    statements = [ statement.strip() for statement in sql_content.split( ';' ) if statement.strip() ]

    with engine.connect() as connection:
      for statement in statements:
        connection.execute( text( statement ) )
        connection.commit()
    
    verify_table_creation( engine, [ 'staging_transactions' ] )

    logger.info( "Staging table created successfully" )
  except Exception as e:
    logger.error( f"Error creating staging table: { e }" )
    raise

if __name__ == "__main__":
  create_star_schema()
  create_staging_table()