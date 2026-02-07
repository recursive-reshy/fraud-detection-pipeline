# System imports
import sys
import logging
# Data manipulation
import pandas as pd

logging.basicConfig(
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

# Expected columns from PaySim1 dataset
EXPECTED_COLUMNS: set[ str ] = {
  'step',
  'type',
  'amount',
  'nameOrig',
  'oldbalanceOrg',
  'newbalanceOrig',
  'nameDest',
  'oldbalanceDest',
  'newbalanceDest',
  'isFraud',
  'isFlaggedFraud'
}

EXPECTED_TYPES: set[ str ] = {
  'CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'
}

def validate_schema( csv_file_path: str ) -> bool:
  try:
    logger.info( f"Validating schema for { csv_file_path }..." )

    # Read the first 1000 rows of the CSV file to validate the schema
    data_frame = pd.read_csv( csv_file_path, nrows = 1000 )

    # Check if the columns are as expected
    missing_cols = ( EXPECTED_COLUMNS ) - set[ str ]( data_frame.columns )
    if missing_cols:
      logger.error( f"Missing columns: { missing_cols }" )
      raise ValueError( f"Missing columns: { missing_cols }" )

    extra_cols = set[ str ]( data_frame.columns ) - ( EXPECTED_COLUMNS )
    if extra_cols:
      logger.error( f"Extra columns: { extra_cols }" )
      raise ValueError( f"Extra columns: { extra_cols }" )

    unique_types = set[ str ]( data_frame[ 'type' ].unique() )
    invalid_types = unique_types - EXPECTED_TYPES

    if invalid_types:
      logger.error( f"Invalid types: { invalid_types }" )
      raise ValueError( f"Invalid types: { invalid_types }" )

    # Check data types
    if not pd.api.types.is_integer_dtype( data_frame[ 'step' ] ):
      logger.error( f"Step column is not an integer" )
      raise ValueError( f"Step column is not an integer" )

    if not pd.api.types.is_float_dtype( data_frame[ 'amount' ] ):
      logger.error( f"Amount column is not a float" )
      raise ValueError( f"Amount column is not a float" )

    if not pd.api.types.is_integer_dtype( data_frame[ 'isFraud' ] ):
      logger.error( f"isFraud column is not an integer" )
      raise ValueError( f"isFraud column is not an integer" )

    logger.info( "Schema validation successful" )
    return True

  except Exception as e:
    logger.error( f"Error validating schema: { e }" )
    return False

if __name__ == "__main__":
  if( len( sys.argv ) > 1 ):
    csv_file_path = sys.argv[ 1 ]
    validate_schema( csv_file_path )
  else:
    print("Usage: python schema_validator.py <path_to_csv>")