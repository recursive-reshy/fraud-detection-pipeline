# System
import sys
import logging
from pathlib import Path
# FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to path to import model loader
sys.path.append( str( Path( __file__ ).parent.parent.parent ) )
from src.deployment.schemas import TransactionRequest, PredictionResponse, HealthResponse, ModelInfoResponse
from src.deployment.model_loader import ModelManager

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger( __name__ )

# Initialize FastAPI app
app = FastAPI( 
  title = "Fraud Detection API", 
  description = "API for fraud detection",
  version = "0.1.0"
)

# Add CORS middleware
app.add_middleware( 
  CORSMiddleware, 
  allow_origins = [ "*" ], 
  allow_credentials = True, 
  allow_methods = [ "*" ], 
  allow_headers = [ "*" ] 
)

# Load model at startup
model_manager = None

@app.on_event( "startup" )
async def startup_event():
  global model_manager
  try:
    model_manager = ModelManager()
    logger.info( "Model loaded successfully" )
  except Exception as e:
    logger.error( f"Error loading model: { e }" )
    raise

@app.get( "/", tags = [ "Root" ] )
async def root():
  return {
    "message": "Fraud Detection API",
    "version": "0.1.0",
    "endpoints": {
      "health": "/health",
      "predict": "/predict",
      "model_info": "/model-info",
    }
  }

@app.get( "/health", response_model = HealthResponse, tags = [ "Health" ] )
async def health():
  if model_manager is None:
    raise HTTPException( status_code = 500, detail = "Model not loaded" )
  return {
    "status": "healthy",
    "model_loaded": True
  }

@app.get( "/model-info", response_model = ModelInfoResponse, tags = [ "Model Info" ] )
async def model_info():
  if model_manager is None:
    raise HTTPException( status_code = 500, detail = "Model not loaded" )
  info = model_manager.get_model_info()
  
  return {
    "model_type": info[ 'model_type' ],
    "n_features": info[ 'n_features' ],
    "feature_names": info[ 'feature_names' ],
    "test_metrics": info[ 'test_metrics' ],
    "test_accuracy": info[ 'test_metrics' ].get( 'accuracy', 0.0 ),
    "test_precision": info[ 'test_metrics' ].get( 'precision', 0.0 ),
    "test_recall": info[ 'test_metrics' ].get( 'recall' ),
    "test_f1": info[ 'test_metrics' ].get( 'f1' ),
    "test_auc_roc": info[ 'test_metrics' ].get( 'auc_roc' )
  }

@app.post( "/predict", response_model = PredictionResponse, tags = [ "Predict" ] )
async def predict( transaction: TransactionRequest ):
  if model_manager is None:
    raise HTTPException( status_code = 500, detail = "Model not loaded" )

  try:
    features = [
      transaction.step,
      transaction.hour,
      transaction.day,
      transaction.type_encoded,
      transaction.origin_type_encoded,
      transaction.destination_type_encoded,
      transaction.amount,
      transaction.old_balance_orig,
      transaction.new_balance_orig,
      transaction.old_balance_dest,
      transaction.new_balance_dest,
      transaction.balance_diff_orig,
      transaction.balance_diff_dest,
      transaction.error_balance_orig,
      transaction.error_balance_dest,
      transaction.is_round_amount,
      transaction.origin_emptied,
      transaction.is_large_tx,
    ]

    prediction, probability = model_manager.predict( features )


    return {
      "is_fraud": prediction == 1,
      "fraud_probability": probability,
    }

  except Exception as e:
    logger.error( f"Error predicting transaction: { e }" )
    raise HTTPException( status_code = 500, detail = str( e ) )