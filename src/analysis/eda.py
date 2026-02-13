import sys
import yaml
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def run_eda(file_path):
    # 1. Load Data
    print(f"--- Loading {file_path} ---")
    df = pd.read_csv(file_path)
    
    # 2. Structural Inspection
    print("\n### Data Shape:", df.shape)
    print("\n### Data Info:")
    print(df.info())
    
    # 3. Descriptive Statistics
    print("\n### Summary Statistics (Numerical):")
    print(df.describe())
    
    # 4. Check for Missing Values
    print("\n### Missing Values:")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "No missing values.")

    # --- Visualizations ---
    sns.set_theme(style="whitegrid")
    
    # 5. Numerical Distributions (Histograms)
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        df[num_cols].hist(figsize=(12, 10), bins=30)
        plt.suptitle("Numerical Distributions")
        plt.show()

    # 6. Correlation Heatmap
    if len(num_cols) > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.show()

if __name__ == "__main__":
    # If you don't have a CSV yet, seaborn has built-in ones for testing
    # Replace 'iris' with your actual 'data.csv' path
    if( len( sys.argv ) > 1 ):
      csv_file_path = sys.argv[ 1 ]
    else:
      # Use default path from config
      config = yaml.safe_load( open( 'config/config.yaml' ) )
      csv_file_path = config.get( 'data', {} ).get( 'raw_csv', 'data/raw/paysim1.csv' )

    run_eda(csv_file_path)