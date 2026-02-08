# System
import sys
import logging
from pathlib import Path
from typing import Tuple, List, Dict, Any
# Machine Learning
from sklearn.ensemble import RandomForestClassifier
# Numerical computing
import numpy as np
# Saving and loading models
import joblib

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

class ModelManager:
  def __init__( self, model_path: str = 'models/fraud_detector.joblib' ) -> None:
    self.model_path = model_path
    self.model: RandomForestClassifier = None
    self.feature_names: List[ str ] = None
    self.test_metrics: Dict[ str, Any ] = None
    self.confusion_matrix = None
    self._load_model()

  def _load_model( self ) -> None:
    if not Path( self.model_path ).exists():
      raise FileNotFoundError( f"Model file not found at { self.model_path }" )

    artifact = joblib.load( self.model_path )

    self.model = artifact[ 'model' ]
    self.feature_names = artifact[ 'feature_names' ]
    self.test_metrics = artifact[ 'test_metrics' ]
    self.confusion_matrix = artifact[ 'confusion_matrix' ]

    logger.info( f"Model loaded successfully from { self.model_path }" )
    logger.info( f"Model type: { type( self.model ) }" )
    logger.info( f"Number of features: { len( self.feature_names ) }" )

  def predict( self, features: List[ float ] ) -> Tuple[ int, float ]:
    if self.model is None:
      raise RuntimeError( "Model not loaded" )
    
    if len( features ) != len( self.feature_names ):
      raise ValueError( f"Expected { len( self.feature_names ) } features, got { len( features ) }" )
    
    features_array = np.array( features ).reshape( 1, -1 )

    # Predict
    prediction = self.model.predict( features_array )[ 0 ]
    probability = self.model.predict_proba( features_array )[ 0 ]
    fraud_probability = probability[ 1 ]

    return int( prediction ), float( fraud_probability )

  def get_model_info( self ) -> Dict[ str, Any ]:
    return {
      'model_type': type( self.model ).__name__,
      'n_features': len( self.feature_names ),
      'feature_names': self.feature_names,
      'test_metrics': self.test_metrics
    }