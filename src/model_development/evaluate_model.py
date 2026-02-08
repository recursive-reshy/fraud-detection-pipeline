# System
import logging
# Data manipulation
import pandas as pd
import numpy as np
# Machine Learning
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

def evaluate_model( model: object, X_train: pd.DataFrame, Y_train: pd.Series, X_test: pd.DataFrame, Y_test: pd.Series ) -> dict:
  logger.info( "Evaluating model..." )
  
  # Predictions
  Y_train_pred = model.predict( X_train )
  Y_test_pred = model.predict( X_test )

  # Prediction probabilities
  Y_train_pred_proba = model.predict_proba( X_train )[ :, 1]
  Y_test_pred_proba = model.predict_proba( X_test )[ :, 1]

  # Calculate metrics
  logger.info( "Train metrics" )
  train_metrics = {
    'accuracy': accuracy_score( Y_train, Y_train_pred ),
    'precision': precision_score( Y_train, Y_train_pred, zero_division = 0 ),
    'recall': recall_score( Y_train, Y_train_pred, zero_division = 0 ),
    'f1': f1_score( Y_train, Y_train_pred, zero_division = 0 ),
    'auc_roc': roc_auc_score( Y_train, Y_train_pred_proba ) if len( np.unique( Y_train ) ) > 1 else 0.0
  }

  test_metrics = {
    'accuracy': accuracy_score( Y_test, Y_test_pred ),
    'precision': precision_score( Y_test, Y_test_pred, zero_division = 0 ),
    'recall': recall_score( Y_test, Y_test_pred, zero_division = 0 ),
    'f1': f1_score( Y_test, Y_test_pred, zero_division = 0 ),
    'auc_roc': roc_auc_score( Y_test, Y_test_pred_proba ) if len( np.unique( Y_test ) ) > 1 else 0.0
  }

  # Classification report
  logger.info( "Classification report" )
  report = classification_report( 
    Y_train,
    Y_train_pred,
    target_names = [ 'not fraud', 'fraud' ],
    zero_division = 0
  )

  cm = confusion_matrix( Y_train, Y_train_pred )
  
  return {
    'train_metrics': train_metrics,
    'test_metrics': test_metrics,
    'confusion_matrix': cm,
    'y_test_pred': Y_test_pred,
    'y_test_pred_proba': Y_test_pred_proba,
    'classification_report': report,
  }