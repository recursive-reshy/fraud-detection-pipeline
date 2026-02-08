# System
import logging
# Data manipulation
import pandas as pd

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def engineer_features( df: pd.DataFrame ) -> pd.DataFrame:
  try:
    logger.info( "Engineering features..." )

    initial_cols = len( df.columns )

    # Balance changes
    df[ 'balance_diff_orig' ] = df[ 'new_balance_orig' ] - df[ 'old_balance_orig' ]
    df[ 'balance_diff_dest' ] = df[ 'new_balance_dest' ] - df[ 'old_balance_dest' ]

    # Balance errors (detect inconsistencies)
    df[ 'error_balance_orig' ] = df[ 'balance_diff_orig' ] + df[ 'amount' ]
    df[ 'error_balance_dest' ] = df[ 'balance_diff_dest' ] - df[ 'amount' ]

    # Fraud indicators
    df[ 'is_round_amount' ] = ( df[ 'amount' ] % 1000 == 0 ).astype( int )
    df[ 'origin_emptied' ] = ( df[ 'new_balance_orig' ] == 0 ).astype( int )
    df[ 'is_large_tx' ] = ( df[ 'amount' ] > df[ 'amount' ].quantile( 0.90 ) ).astype( int )

    # Encode categorical variables
    df[ 'type_encoded' ] = df[ 'type_name' ].astype( 'category' ).cat.codes
    df[ 'origin_type_encoded' ] = df[ 'origin_type' ].astype( 'category' ).cat.codes
    df[ 'destination_type_encoded' ] = df[ 'destination_type' ].astype( 'category' ).cat.codes

    final_cols = len( df.columns )
    new_features = final_cols - initial_cols

    logger.info( f"Engineered { new_features } new features" )

    return df

  except Exception as e:
    logger.error( f"Error performing feature engineering: { e }" )
    raise

def select_features( df: pd.DataFrame ) -> tuple[ pd.DataFrame, pd.Series, list[ str ] ]:
  logger.info( "Selecting features..." )

  feature_cols = [
    # Temporal features
    'step', 'hour', 'day',

    # Tx type
    'type_encoded',

    # Account info
    'origin_type_encoded', 'destination_type_encoded',
    
    # Tx measures
    'amount', 'old_balance_orig', 'new_balance_orig', 'old_balance_dest', 'new_balance_dest',

    # Engineered features
    'balance_diff_orig', 'balance_diff_dest', 'error_balance_orig', 'error_balance_dest', 'is_round_amount', 'origin_emptied', 'is_large_tx',
  ]

  # Verify features exist
  missing_features = set( feature_cols ) - set( df.columns )
  if missing_features:
    logger.error( f"Missing features: { missing_features }" )
    raise ValueError( f"Missing features: { missing_features }" )
  
  X = df[ feature_cols ].copy()
  Y = df[ 'is_fraud' ].copy()

  logger.info( f"Selected { len( X.columns ) } features" )
  logger.info( f"Feature matrix shape: { X.shape }" )
  logger.info( f"Target vector shape: { Y.shape }" )

  return X, Y, feature_cols