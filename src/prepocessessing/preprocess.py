# System
import sys
import logging
from pathlib import Path
# Database
from sqlalchemy.engine import Engine
# Data manipulation
import pandas as pd
# Add parent directory to path to import database module
sys.path.append( str( Path( __file__ ).parent.parent.parent ) )
from src.database import create_db_engine
from src.prepocessessing.data_loader import load_data_from_star_schema
from src.prepocessessing.feature_engineering import engineer_features, select_features
from src.prepocessessing.resampling import handle_class_imbalance

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def preprocess_data( save_path: str = 'data/processed/preprocessed_data.csv' ) -> pd.DataFrame:
  try:
    logger.info( "Preprocessing data..." )

    engine = create_db_engine()

    # Load data
    df = load_data_from_star_schema( engine )

    # Feature engineering
    df = engineer_features( df )

    # Feature selection
    X, Y, feature_cols = select_features( df )

    # Class imbalance handling
    X_resampled, Y_resampled = handle_class_imbalance( X, Y )

    # Save data
    Path( save_path ).parent.mkdir( parents = True, exist_ok = True )

    # Combine X and Y for saving
    df_processed = pd.DataFrame( X_resampled, columns = feature_cols )
    df_processed[ 'is_fraud' ] = Y_resampled.values

    df_processed.to_csv( save_path, index = False )

    logger.info( f"Data saved to { save_path }" )
    return df_processed

  except Exception as e:
    logger.error( f"Error preprocessing data: { e }" )
    raise

if __name__ == "__main__":
  preprocess_data()