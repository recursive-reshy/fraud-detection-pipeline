# System
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

logger = logging.getLogger( __name__ )


class DriftDetector:
  def __init__(
    self,
    prediction_log: str = "logs/monitoring/predictions.jsonl",
    baseline_window: int = 1000,
    current_window: int = 100
  ) -> None:
    self.prediction_log = Path( prediction_log )
    self.baseline_window = baseline_window
    self.current_window = current_window
    logger.info( f"Drift detector initialized" )
    logger.info( f"  Baseline window: { baseline_window }" )
    logger.info( f"  Current window: { current_window }" )

  def detect_prediction_drift( self, threshold: float = 0.1 ) -> Dict:
    if not self.prediction_log.exists():
      logger.warning( "No prediction log found" )
      return { 'drift_detected': False, 'message': 'No log available' }

    # Read predictions
    with open( self.prediction_log, 'r' ) as f:
      lines = f.readlines()

    if len( lines ) < self.baseline_window + self.current_window:
      logger.warning( f"Insufficient data for drift detection" )
      return {
        'drift_detected': False,
        'message': f'Need { self.baseline_window + self.current_window } samples, have { len( lines ) }'
      }

    # Get baseline predictions (older data)
    baseline_start = -( self.baseline_window + self.current_window )
    baseline_end = -self.current_window
    baseline_predictions = [
      json.loads( line )[ 'prediction' ]
      for line in lines[ baseline_start:baseline_end ]
    ]

    # Get current predictions (recent data)
    current_predictions = [
      json.loads( line )[ 'prediction' ]
      for line in lines[ -self.current_window: ]
    ]

    # Calculate fraud rates
    baseline_fraud_rate = np.mean( baseline_predictions )
    current_fraud_rate = np.mean( current_predictions )

    # Calculate drift
    drift = abs( current_fraud_rate - baseline_fraud_rate )
    drift_detected = drift > threshold

    result = {
      'drift_detected': drift_detected,
      'baseline_fraud_rate': baseline_fraud_rate,
      'current_fraud_rate': current_fraud_rate,
      'drift_magnitude': drift,
      'threshold': threshold,
      'baseline_samples': len( baseline_predictions ),
      'current_samples': len( current_predictions )
    }

    return result
