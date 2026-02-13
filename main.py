import sys
import yaml

from src.ingestion.create_schema import create_star_schema, create_staging_table
from src.ingestion.load_staging import load_staging_table
from src.ingestion.populate_star_schema import populate_star_schema
from src.prepocessessing.preprocess import preprocess_data
from src.model_development.model_development import develop_model


def main():
    # 1. Database schema + staging
    create_star_schema()
    create_staging_table()

    # 2. Determine CSV source (CLI arg overrides config)
    if len(sys.argv) > 1:
        csv_file_path = sys.argv[1]
    else:
        config = yaml.safe_load(open("config/config.yaml"))
        csv_file_path = config.get("data", {}).get("raw_csv", "data/raw/paysim1.csv")

    # 3. Ingest into staging and populate star schema
    load_staging_table(csv_file_path)
    populate_star_schema()

    # 4. Preprocess data into features/labels CSV
    preprocess_data()

    # 5. Train and evaluate model, saving artifact to models/fraud_detector.joblib
    develop_model()


if __name__ == "__main__":
    main()
