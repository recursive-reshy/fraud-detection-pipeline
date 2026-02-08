# System
import sys
import logging
from pathlib import Path
# Save and load models
import joblib
# Data manipulation
import pandas as pd

# Add parent directory to path to import database module
sys.path.append( str( Path( __file__ ).parent.parent.parent ) )
from src.model_development.train_test_split import split_data
from src.model_development.train_model import train_random_forest
from src.model_development.evaluate_model import evaluate_model

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def develop_model( 
  data_path: str = 'data/processed/preprocessed_data.csv',
  model_path: str = 'models/fraud_detector.joblib',
) -> tuple[ object, dict ]:
  try:
    logger.info( "Starting model development..." )
    df = pd.read_csv( data_path )

    # Separate features and target
    X = df.drop( 'is_fraud', axis = 1 )
    Y = df[ 'is_fraud' ]

    # Train / test split
    X_train, X_test, Y_train, Y_test = split_data( X, Y )

    # Train model
    model = train_random_forest( X_train, Y_train )

    # Evaluate model
    metrics = evaluate_model( model, X_train, Y_train, X_test, Y_test )

    # Save model
    Path( model_path ).parent.mkdir( parents = True, exist_ok = True )

    # Save model with metadata
    logger.info( f"Saving model to { model_path }" )
    model_artifact = {
      'model': model,
      'feature_names': X.columns.tolist(),
      'test_metrics': metrics[ 'test_metrics' ],
      'confusion_matrix': metrics[ 'confusion_matrix' ]
    }
    joblib.dump( model_artifact, model_path )

    return model, metrics

  except Exception as e:
    logger.error( f"Error developing model: { e }" )
    raise

if __name__ == "__main__":
  develop_model()