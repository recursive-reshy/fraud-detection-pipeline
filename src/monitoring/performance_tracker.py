# System
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logger = logging.getLogger( __name__ )


class PerformanceTracker:
  def __init__( self, prediction_log: str = "logs/monitoring/predictions.jsonl" ) -> None:
    self.prediction_log = Path( prediction_log )
    logger.info( f"Performance tracker initialized: { self.prediction_log }" )

  def calculate_metrics( self, window_size: Optional[ int ] = None ) -> Dict:
    if not self.prediction_log.exists():
      logger.warning( "No prediction log found" )
      return {}

    # Read predictions
    predictions = []
    actuals = []

    with open( self.prediction_log, 'r' ) as f:
      lines = f.readlines()

      # Apply window if specified
      if window_size:
        lines = lines[ -window_size: ]

      for line in lines:
        entry = json.loads( line )

        # Only include if actual label is available
        if entry.get( 'actual_label' ) is not None:
          predictions.append( entry[ 'prediction' ] )
          actuals.append( entry[ 'actual_label' ] )

    if len( predictions ) == 0:
      logger.warning( "No predictions with actual labels found" )
      return {
        'n_samples': 0,
        'message': 'No labeled data available for evaluation'
      }

    # Calculate metrics
    metrics = {
      'n_samples': len( predictions ),
      'accuracy': accuracy_score( actuals, predictions ),
      'precision': precision_score( actuals, predictions, zero_division = 0 ),
      'recall': recall_score( actuals, predictions, zero_division = 0 ),
      'f1_score': f1_score( actuals, predictions, zero_division = 0 )
    }

    return metrics

  def get_prediction_distribution( self, window_size: Optional[ int ] = None ) -> Dict:
    if not self.prediction_log.exists():
      return {}

    predictions = []

    with open( self.prediction_log, 'r' ) as f:
      lines = f.readlines()

      if window_size:
        lines = lines[ -window_size: ]

      for line in lines:
        entry = json.loads( line )
        predictions.append( entry[ 'prediction' ] )

    total = len( predictions )
    fraud_count = sum( predictions )
    legitimate_count = total - fraud_count

    distribution = {
      'total': total,
      'fraud': fraud_count,
      'legitimate': legitimate_count,
      'fraud_rate': fraud_count / total if total > 0 else 0
    }

    return distribution
