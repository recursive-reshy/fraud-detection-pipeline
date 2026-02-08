# System
import logging
# Machine Learning
from sklearn.model_selection import train_test_split
# Data manipulation
import pandas as pd

logging.basicConfig( 
  level = logging.INFO,
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def split_data( 
  X: pd.DataFrame,
  Y: pd.Series,
  test_size: float = 0.2,
  random_state: int = 42
) -> tuple[ pd.DataFrame, pd.DataFrame, pd.Series, pd.Series ]:
  logging.info( "Splitting data into train and test sets..." )

  X_train, X_test, Y_train, Y_test = train_test_split( 
    X,
    Y,
    test_size = test_size,
    random_state = random_state,
    stratify = Y # Maintain fraud ratio in both sets
  )

  train_fraud_count = pd.Series( Y_train ).value_counts()
  test_fraud_count = pd.Series( Y_test ).value_counts()

  logging.info( f"Train set fraud distribution: { train_fraud_count }" )
  logging.info( f"Test set fraud distribution: { test_fraud_count }" )

  return X_train, X_test, Y_train, Y_test