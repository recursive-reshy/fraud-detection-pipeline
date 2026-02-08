# Schemas
from enum import Enum
from pydantic import BaseModel, Field

class TransactionType( str, Enum ):
  CASH_IN = 'CASH_IN'
  CASH_OUT = 'CASH_OUT'
  DEBIT = 'DEBIT'
  PAYMENT = 'PAYMENT'
  TRANSFER = 'TRANSFER'

class AccountType( str, Enum ):
  CUSTOMER = 'C'
  MERCHANT = 'M'

class TransactionRequest( BaseModel ):
  # Temporal features
  step: int = Field( ..., description = "Time step in hours", ge = 0 )
  hour: int = Field( ..., description = "Hour of the day", ge = 0, le = 23 )
  day: int = Field( ..., description = "Day number", ge = 0 )
  # Tx type
  type_encoded: int = Field( ..., description = "Encoded transaction type", ge = 0, le = 4 )
  # Account type
  origin_type_encoded: int = Field( ..., description = "Encoded origin account type", ge = 0, le = 1 )
  destination_type_encoded: int = Field( ..., description = "Encoded destination account type", ge = 0, le = 1 )
  # Tx measures
  amount: float = Field( ..., description = "Transaction amount", ge = 0 )
  old_balance_orig: float = Field( ..., description = "Original account balance before transaction", ge = 0 )
  new_balance_orig: float = Field( ..., description = "Original account balance after transaction", ge = 0 )
  old_balance_dest: float = Field( ..., description = "Destination account balance before transaction", ge = 0 )
  new_balance_dest: float = Field( ..., description = "Destination account balance after transaction", ge = 0 )
  # Engineered features
  balance_diff_orig: float = Field( ..., description = "Balance difference for original account" )
  balance_diff_dest: float = Field( ..., description = "Balance difference for destination account" )
  error_balance_orig: float = Field( ..., description = "Error in original account balance" )
  error_balance_dest: float = Field( ..., description = "Error in destination account balance" )
  is_round_amount: int = Field( ..., description = "Indicator for round amount transaction", ge = 0, le = 1 )
  origin_emptied: int = Field( ..., description = "Indicator for emptied original account", ge = 0, le = 1 )
  is_large_tx: int = Field( ..., description = "Indicator for large transaction", ge = 0, le = 1 )

  class Config:
    json_schema_extra = {
      "examples": {
        "step": 1,
        "hour": 1,
        "day": 0,
        "type_encoded": 1,
        "origin_type_encoded": 0,
        "dest_type_encoded": 1,
        "amount": 9839.64,
        "old_balance_orig": 170136.0,
        "new_balance_orig": 160296.36,
        "old_balance_dest": 0.0,
        "new_balance_dest": 0.0,
        "balance_diff_orig": -9839.64,
        "balance_diff_dest": 0.0,
        "error_balance_orig": 0.0,
        "error_balance_dest": -9839.64,
        "is_round_amount": 0,
        "origin_emptied": 0,
        "is_large_transaction": 0
      }
    }

class PredictionResponse( BaseModel ):
  is_fraud: bool = Field( ..., description = "Whether the transaction is fraudulent" )
  fraud_probability: float = Field( ..., description = "Probability of the transaction being fraudulent" )

  class Config:
    json_schema_extra = {
      "examples": {
        "is_fraud": False,
        "fraud_probability": 0.01,
      }
    }

class HealthResponse( BaseModel ):
  status: str = Field( ..., description = "Status of the service" )
  model_loaded: bool = Field( ..., description = "Whether the model is loaded" )

class ModelInfoResponse( BaseModel ):
  model_type: str = Field( ..., description = "Type of the model" )
  n_features: int = Field( ..., description = "Number of features used in the model" )
  feature_names: list[ str ] = Field( ..., description = "Names of the features used in the model" )
  test_accuracy: float = Field( ..., description = "Accuracy of the model on the test set" )
  test_precision: float = Field( ..., description = "Precision of the model on the test set" )
  test_recall: float = Field( ..., description = "Recall of the model on the test set" )
  test_f1: float = Field( ..., description = "F1 score of the model on the test set" )