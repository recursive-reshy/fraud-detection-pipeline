# System
import logging
import random
import sys
from pathlib import Path
# Add parent directory to path to import modules
sys.path.append( str( Path( __file__ ).parent.parent.parent ) )
from src.monitoring.prediction_logger import PredictionLogger, PerformanceLogger
from src.monitoring.performance_tracker import PerformanceTracker
from src.monitoring.drift_detector import DriftDetector

logging.basicConfig(
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )


def run_monitoring_dashboard():
  tracker = PerformanceTracker()
  drift_detector = DriftDetector()

  metrics = tracker.calculate_metrics( window_size = 100 )
  distribution = tracker.get_prediction_distribution( window_size = 100 )
  drift_result = drift_detector.detect_prediction_drift( threshold = 0.1 )
  feature_drift = drift_detector.detect_feature_drift( 'amount' )

  return {
    'metrics': metrics,
    'distribution': distribution,
    'drift': drift_result,
    'feature_drift': feature_drift
  }


def simulate_monitoring():
  pred_logger = PredictionLogger()
  perf_logger = PerformanceLogger()

  for i in range( 50 ):
    features = {
      'step': i,
      'amount': random.uniform( 100, 10000 ),
      'hour': random.randint( 0, 23 )
    }
    prediction = random.choice( [ 0, 0, 0, 1 ] )
    probability = random.uniform( 0.1, 0.9 )
    actual_label = random.choice( [ 0, 0, 0, 1, None ] )
    pred_logger.log_prediction( features, prediction, probability, actual_label )

  tracker = PerformanceTracker()
  metrics = tracker.calculate_metrics()

  if metrics.get( 'n_samples', 0 ) > 0:
    perf_logger.log_metrics(
      accuracy = metrics[ 'accuracy' ],
      precision = metrics[ 'precision' ],
      recall = metrics[ 'recall' ],
      f1 = metrics[ 'f1_score' ],
      n_samples = metrics[ 'n_samples' ]
    )


if __name__ == "__main__":
  simulate_monitoring()
  run_monitoring_dashboard()
