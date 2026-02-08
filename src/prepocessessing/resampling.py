# System
import logging
# Data manipulation
import pandas as pd
# Machine Learning
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def handle_class_imbalance( X: pd.DataFrame, Y: pd.Series, random_state: int = 42 ) -> tuple[ pd.DataFrame, pd.Series ]:
  logger.info( "Handling class imbalance..." )

  # Original distribution
  original_counts = Y.value_counts()

  min_samples = original_counts.min()

  if min_samples < 6:
    logger.warning( f"Minimum samples is less than 6, using 6 as minimum samples" )
    logger.warning( "SMOTE requires at least 6 samples per class (k_neighbors=6)" )
    logger.warning( "Skipping resampling for small datasets" )
    return X, Y
    
  # Define resampling strategy
  over_sampler = SMOTE( 
    sampling_strategy = 0.5, # Oversample fraud to 50% of legitimate
    random_state = random_state 
  )
  under_sampler = RandomUnderSampler( 
    sampling_strategy = 1, # Undersample to 1:1 ratio
    random_state = random_state 
  )

  # Create pipeline
  pipeline = Pipeline( [
    ( 'over', over_sampler ),
    ( 'under', under_sampler ),
  ] )

  # Fit and transform data
  X_resampled, Y_resampled = pipeline.fit_resample( X, Y )

  # New distribution
  resampled_counts = Y_resampled.value_counts()
  logger.info( f"Legitimate: { resampled_counts[ 0 ] }" )
  logger.info( f"Fraud: { resampled_counts[ 1 ] }" )
  logger.info( f"Ratio: { resampled_counts[ 1 ] / resampled_counts[ 0 ] }" )
  logger.info( f"Total: { resampled_counts[ 0 ] + resampled_counts[ 1 ] }" )

  return X_resampled, Y_resampled