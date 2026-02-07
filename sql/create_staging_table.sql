DROP TABLE IF EXISTS staging_transactions;

CREATE TABLE staging_transactions (
  id CHAR(36) NOT NULL DEFAULT (UUID()) PRIMARY KEY,
  step INT NOT NULL,
  type ENUM('CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER') NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  nameOrig VARCHAR(255) NOT NULL,
  oldbalanceOrg DECIMAL(10, 2) NOT NULL DEFAULT 0,
  newbalanceOrig DECIMAL(10, 2) NOT NULL DEFAULT 0,
  nameDest VARCHAR(255) NOT NULL,
  oldbalanceDest DECIMAL(10, 2) NOT NULL DEFAULT 0,
  newbalanceDest DECIMAL(10, 2) NOT NULL DEFAULT 0,
  isFraud TINYINT(1) NOT NULL DEFAULT 0,
  isFlaggedFraud TINYINT(1) NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  -- Indexes for common queries
  INDEX idx_step (step),
  INDEX idx_type (type),
  INDEX idx_is_fraud (isFraud)
);