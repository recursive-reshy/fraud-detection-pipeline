## Fraud Detection Pipeline

End‑to‑end fraud detection project covering data ingestion, preprocessing, model development, API deployment with FastAPI, and basic monitoring.

### Overview

This repository implements a complete pipeline for detecting fraudulent financial transactions:

- **Data ingestion** into a relational database (star schema).
- **Preprocessing and feature engineering** for highly imbalanced transaction data.
- **Model development** using scikit‑learn (Random Forest).
- **Model serving** via a FastAPI application.
- **Monitoring utilities** for tracking model performance and drift.

The trained model is stored as a Joblib artifact and loaded by the API to serve real‑time predictions.

### Tech stack

- **Language**: Python (requires **Python >= 3.13**)
- **Core libraries**:
  - `pandas`, `numpy` for data manipulation
  - `scikit-learn`, `imbalanced-learn` for modeling
  - `fastapi`, `pydantic`, `uvicorn` for the API
  - `sqlalchemy`, `pymysql` for database access
  - `pyyaml` for configuration

All runtime dependencies are defined in `pyproject.toml`.

### Project structure

Key directories and modules:

- `src/database.py` – shared database utilities.
- `src/ingestion/`
  - `create_schema.py` – create database/schema objects.
  - `load_staging.py` – load raw/staging data.
  - `schema_validation.py` – validate incoming schema.
  - `populate_dimensions.py`, `populate_facts.py`, `populate_star_schema.py` – build the analytical star schema.
- `src/prepocessessing/`
  - `data_loader.py` – load raw/processed datasets.
  - `feature_engineering.py` – create domain‑specific features.
  - `resampling.py` – handle class imbalance.
  - `preprocess.py` – orchestrate preprocessing and write `data/processed/preprocessed_data.csv`.
- `src/model_development/`
  - `train_test_split.py` – split data into train/test sets.
  - `train_model.py` – train a Random Forest classifier.
  - `evaluate_model.py` – compute evaluation metrics and confusion matrix.
  - `model_development.py` – end‑to‑end model training, evaluation and saving of `models/fraud_detector.joblib`.
- `src/deployment/`
  - `app.py` – FastAPI application exposing prediction and monitoring endpoints.
  - `model_loader.py` – `ModelManager` for loading the trained model artifact and running predictions.
  - `schemas.py` – Pydantic models for request/response payloads.
- `src/monitoring/`
  - `prediction_logger.py` – log predictions and optional labels.
  - `performance_tracker.py` – aggregate performance metrics over a sliding window.
  - `drift_detector.py` – detect prediction and feature drift.
  - `monitor.py` – utilities to simulate traffic and inspect monitoring outputs.

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd fraud-detection-pipeline
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # on Windows (bash)
   # source .venv/bin/activate    # on macOS/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install -e .
   ```

4. **Create your configuration file**

   A sample configuration is provided at `config/config.example.yaml`. Copy it and update it with your environment‑specific values:

   ```bash
   cp config/config.example.yaml config/config.yaml
   ```

   In `config/config.yaml`, update at least:

   - **`database.host`, `database.port`** – where your MariaDB/MySQL instance is running.
   - **`database.user`, `database.password`** – credentials with permissions to create/use the `fraud_detection` database.
   - **`database.database`** – the database name to use; defaults to `fraud_detection`.
   - **`data.raw_csv`** – path to the raw PaySim CSV file you want to ingest (default `data/raw/paysim1_s.csv`).
   - **`logging.file`** – path for the pipeline log file (default `logs/pipeline.log`).

   The application code (e.g. `main.py`, `src/database.py`, `src/ingestion/load_staging.py`) reads from `config/config.yaml`, which is **ignored by git** to keep secrets out of version control.

### Data and model artifacts

- **Preprocessed data** is expected by default at:
  - `data/processed/preprocessed_data.csv`
- **Trained model artifact** is saved and loaded from:
  - `models/fraud_detector.joblib`

You may need to run the ingestion and preprocessing steps (see `src/ingestion` and `src/prepocessessing`) to generate the processed dataset before training the model.

### Training the model

The main entry point for model training and evaluation is `src/model_development/model_development.py`. From the repository root:

```bash
python src/model_development/model_development.py
```

This will:

- Load `data/processed/preprocessed_data.csv`.
- Split the data into train and test sets.
- Train a Random Forest model.
- Evaluate the model and compute metrics.
- Save `models/fraud_detector.joblib` containing:
  - the trained model
  - feature names
  - test metrics
  - confusion matrix

### Running the API

The API is implemented in `src/deployment/app.py` using FastAPI. After you have a trained model at `models/fraud_detector.joblib`, start the API from the project root:

```bash
uvicorn src.deployment.app:app --reload
```

By default, this will serve the API at `http://127.0.0.1:8000`.

The root endpoint (`/`) returns basic service information and a list of available endpoints. FastAPI’s automatic docs are also available at:

- `http://127.0.0.1:8000/docs` (Swagger UI)
- `http://127.0.0.1:8000/redoc` (ReDoc)

### Monitoring utilities

Monitoring components are initialized in `src/deployment/app.py` on startup:

- `PredictionLogger` – logs individual predictions.
- `PerformanceTracker` – computes rolling performance metrics.
- `DriftDetector` – detects prediction and feature drift.

You can also run the monitoring simulation script directly:

```bash
python src/monitoring/monitor.py
```

This script:

- Simulates a stream of predictions and (optionally) labels.
- Logs those predictions and metrics.
- Computes metrics, distributions, and drift diagnostics.

### API endpoints

All endpoints are defined in `src/deployment/app.py`:

- **`GET /`**
  - Returns a basic description, version, and links to key endpoints.

- **`GET /health`**
  - Returns a `HealthResponse` with:
    - `status`: string status (e.g. `"healthy"`)
    - `model_loaded`: `true` if the model was loaded successfully.

- **`GET /model-info`**
  - Returns a `ModelInfoResponse` containing:
    - `model_type`
    - `n_features`
    - `feature_names`
    - test metrics (accuracy, precision, recall, F1, AUC‑ROC).

- **`POST /predict`**
  - Request body: `TransactionRequest` with engineered numeric features such as:
    - temporal: `step`, `hour`, `day`
    - encoded types: `type_encoded`, `origin_type_encoded`, `destination_type_encoded`
    - balances and engineered features: `amount`, `old_balance_orig`, `new_balance_orig`, `old_balance_dest`, `new_balance_dest`, `balance_diff_orig`, `balance_diff_dest`, `error_balance_orig`, `error_balance_dest`, `is_round_amount`, `origin_emptied`, `is_large_tx`
  - Response: `PredictionResponse`:
    - `is_fraud`: boolean flag
    - `fraud_probability`: probability that the transaction is fraudulent.

- **`GET /monitoring/metrics`**
  - Returns performance metrics over a configurable window (`window_size` query parameter, default `100`).

- **`GET /monitoring/distribution`**
  - Returns prediction distribution statistics over the specified window.

- **`GET /monitoring/drift`**
  - Returns drift detection results for model predictions (`threshold` query parameter, default `0.1`).

Use the interactive docs at `/docs` to explore the request/response schemas defined in `src/deployment/schemas.py`.

### Notes and next steps

- Adjust default paths (data, models) as needed for your environment.
- Extend the monitoring layer to push metrics to your preferred observability stack (e.g. Prometheus, Grafana, CloudWatch).
- Add tests for the critical modules (ingestion, preprocessing, model development, and API) to ensure the pipeline remains robust as it evolves.

