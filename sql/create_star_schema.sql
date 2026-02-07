DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS dim_account;
DROP TABLE IF EXISTS dim_transaction_type;
DROP TABLE IF EXISTS dim_time;

CREATE TABLE dim_transaction_type (
  id CHAR(36) NOT NULL DEFAULT (UUID()) PRIMARY KEY,
  type_name ENUM('CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_time (
  id CHAR(36) NOT NULL DEFAULT (UUID()) PRIMARY KEY,
  hour INT NOT NULL,
  date DATE NOT NULL
);

CREATE TABLE dim_account (
  id CHAR(36) NOT NULL DEFAULT (UUID()) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  type ENUM('CUSTOMER', 'MERCHANT') NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_transactions (
  id CHAR(36) NOT NULL DEFAULT (UUID()) PRIMARY KEY,

  -- Foreign keys to dimension tables
  time_key CHAR(36) NOT NULL,
  type_key CHAR(36) NOT NULL,
  origin_account_key CHAR(36) NOT NULL,
  destination_account_key CHAR(36) NOT NULL,

  -- Measures
  amount DECIMAL(10, 2) NOT NULL,
  old_balance_orig DECIMAL(10, 2) NOT NULL DEFAULT 0,
  new_balance_orig DECIMAL(10, 2) NOT NULL DEFAULT 0,
  old_balance_dest DECIMAL(10, 2) NOT NULL DEFAULT 0,
  new_balance_dest DECIMAL(10, 2) NOT NULL DEFAULT 0,

  -- Fraud indicators
  is_fraud TINYINT(1) NOT NULL DEFAULT 0,
  is_flagged_fraud TINYINT(1) NOT NULL DEFAULT 0,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  -- Foreign keys constraints
  FOREIGN KEY (time_key) REFERENCES dim_time(id),
  FOREIGN KEY (type_key) REFERENCES dim_transaction_type(id),
  FOREIGN KEY (origin_account_key) REFERENCES dim_account(id),
  FOREIGN KEY (destination_account_key) REFERENCES dim_account(id),

  -- Indexes for common queries
  INDEX idx_fraud (is_fraud),
  INDEX idx_time (time_key),
  INDEX idx_type (type_key),
  INDEX idx_origin (origin_account_key),
  INDEX idx_destination (destination_account_key)
);