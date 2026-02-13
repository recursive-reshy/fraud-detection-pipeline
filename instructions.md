# Fraud Detection Pipeline: Implementation Plan

This document outlines the sequential steps for building the fraud detection system using **uv**, **MariaDB ColumnStore**, and **FastAPI**.

---

## STEP 1: Project Setup
- [ ] **1.1. Create project directory structure** `mkdir -p config data/raw src logs models notebooks`
- [ ] **1.2. Initialize uv project** `uv init`

---

## STEP 2: Database Infrastructure
- [ ] **2.1. Verify MariaDB ColumnStore is running**
- [ ] **2.2. Create configuration file** Define `config/config.yaml` with DB credentials and environment settings.
- [ ] **2.3. Create database connection utility** Develop `src/database.py` using SQLAlchemy or the MariaDB connector.
- [ ] **2.4. Test database connection**

---

## STEP 3: Star Schema Creation
- [ ] **3.1. Write SQL scripts for dimension tables** (`dim_transaction_type`, `dim_time`, `dim_account`)
- [ ] **3.2. Write SQL script for fact table** (`fact_transactions`)
- [ ] **3.3. Create Python module to execute schema creation**
- [ ] **3.4. Run schema creation and verify tables exist**

---

## STEP 4: Data Ingestion - Staging
- [ ] **4.1. Create staging table** Match the raw PaySim1 CSV structure.
- [ ] **4.2. Implement CSV schema validation**
- [ ] **4.3. Load PaySim1 CSV into staging table**
- [ ] **4.4. Verify row counts and data integrity**

---

## STEP 5: Data Ingestion - Populate Star Schema
- [ ] **5.1. Populate dim_transaction_type** (5 transaction types)
- [ ] **5.2. Populate dim_time** (Extract unique steps)
- [ ] **5.3. Populate dim_account** (Extract unique accounts from `nameOrig` + `nameDest`)
- [ ] **5.4. Populate fact_transactions** (With FK lookups)
- [ ] **5.5. Verify referential integrity**

---

## STEP 6: Data Preprocessing
- [ ] **6.1. Query data from star schema** (JOIN tables)
- [ ] **6.2. Implement feature engineering**
- [ ] **6.3. Implement class imbalance handling** (SMOTE + undersampling)
- [ ] **6.4. Save processed dataset for model training**

---

## STEP 7: Model Development
- [ ] **7.1. Implement train/test split**
- [ ] **7.2. Train Random Forest model**
- [ ] **7.3. Evaluate model** (Metrics + confusion matrix)
- [ ] **7.4. Save trained model** (Export to `models/`)

---

## STEP 8: Model Deployment
- [ ] **8.1. Create FastAPI application**
- [ ] **8.2. Implement /predict endpoint**
- [ ] **8.3. Load saved model**
- [ ] **8.4. Test API locally**

---

## STEP 9: Model Monitoring (Stubbed)
- [ ] **9.1. Create monitoring plan document**
- [ ] **9.2. Design predictions logging table**
- [ ] **9.3. Outline drift detection approach**

---

## STEP 10: Documentation
- [ ] **10.1. Create pipeline execution logs**
- [ ] **10.2. Document each stage for Report 2**
- [ ] **10.3. Generate diagrams** (ERD, pipeline flow)