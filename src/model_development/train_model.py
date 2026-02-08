# System
import logging
# Machine Learning
from sklearn.ensemble import RandomForestClassifier
# Data manipulation
import pandas as pd

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def train_random_forest(  X_train: pd.DataFrame, Y_train: pd.Series, config = None ) -> RandomForestClassifier:
  default_config = {
    'n_estimators': 100, # Number of trees in the forest
    'max_depth': None, # Maximum depth of the trees
    'min_samples_split': 2, # Minimum number of samples required to split an internal node
    'min_samples_leaf': 1, # Minimum number of samples required to be at a leaf node
    'random_state': 42, # Random state for reproducibility
    'n_jobs': -1, # Number of jobs to run in parallel
    'class_weight': 'balanced', # Class weight for imbalanced classes
    'verbose': 1, # Verbosity of the model
  }

  if config:
    default_config.update( config )
  
  logger.info( f"Hyperparameters: { default_config }" )
  for key, value in default_config.items():
    if key != 'verbose': # Don't log verbose
      logger.info( f"{ key }: { value }" )
  
  # Initialize model
  model = RandomForestClassifier( **default_config )

  # Train model
  logger.info( "Training Random Forest model..." )
  model.fit( X_train, Y_train )
  
  # Train accuracy
  train_accuracy = model.score( X_train, Y_train )
  logger.info( f"Train accuracy: { train_accuracy }" )

  return model