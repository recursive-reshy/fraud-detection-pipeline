import sys
import yaml

from src.ingestion.create_schema import create_star_schema, create_staging_table
from src.ingestion.load_staging import load_staging_table
from src.ingestion.populate_star_schema import populate_star_schema
from src.prepocessessing.preprocess import preprocess_data

def main():
    create_star_schema()
    create_staging_table()

    if len(sys.argv) > 1:
        csv_file_path = sys.argv[1]
    else:
        config = yaml.safe_load(open("config/config.yaml"))
        csv_file_path = config.get("data", {}).get("raw_csv", "data/raw/paysim1.csv")

    load_staging_table(csv_file_path)
    populate_star_schema()
    preprocess_data()

if __name__ == "__main__":
    main()
