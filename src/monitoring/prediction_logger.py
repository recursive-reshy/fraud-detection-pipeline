# System
import json
import logging
import csv
from pathlib import Path
from datetime import datetime
from typing import List

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

class PredictionLogger:
  def __init__( self, log_file_path: str = 'logs/monitoring/predictions.jsonl' ) -> None:
    self.log_file_path = Path( log_file_path )
    self.log_file_path.parent.mkdir( parents = True, exist_ok = True )

  def log_prediction(
    self,
    features: dict,
    prediction: int,
    probability: float,
    actual_label: int = None
  ) -> None:
    log_entry = {
      'timestamp': datetime.now().isoformat(),
      'features': features,
      'prediction': prediction,
      'probability': probability,
      'actual_label': actual_label
    }
    
    with open( self.log_file_path, 'a' ) as file:
      file.write( json.dumps( log_entry ) + '\n' )

  def get_recent_predictions( self, n: int = 100 ) -> List[ dict ]:
    if not self.log_file_path.exists():
      return []
    
    predictions = []
    with open( self.log_file_path, 'r' ) as file:
      lines = file.readlines()
      for line in lines[ -n: ]:
        predictions.append( json.loads( line ) )
    
    return predictions

class PerformanceLogger:
  def __init__( self, log_file_path: str = 'logs/monitoring/performance.csv' ) -> None:
    if not self.log_file_path.exists():
      with open( self.log_file_path, 'w', newline = '' ) as file:
        writer = csv.writer( file )
        writer.writerow( [ 
          'timestamp', 
          'accuracy', 
          'precision', 
          'recall', 
          'f1', 
          'n_samples'
        ] )

      logger.info( f"Performance logger initialized at { self.log_file_path }" )

  def log_metrics(
    self,
    accuracy: float,
    precision: float,
    recall: float,
    f1: float,
    n_samples: int
  ) -> None:
    with open( self.log_file_path, 'a', newline='' ) as file:
      writer = csv.writer( file )
      writer.writerow( [
        datetime.now().isoformat(),
        accuracy,
        precision,
        recall,
        f1,
        n_samples
      ] )
