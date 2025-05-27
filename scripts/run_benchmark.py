import pandas as pd
import requests
import time

# Paths
csv_path = "excerpts.csv"
output_csv_path = "excerpts_updated.csv"

# Model endpoints
MODEL_1_URL = "http://160.40.54.136:8000/extract-requirements"
MODEL_2_URL = "http://160.40.50.58:8110/extract-requirements"

# Constant request parameter
STANDARD = "ISO/IEC 27001"

def call_model(endpoint, excerpt):
    try:
        response = requests.post(endpoint, json={
            "standard": STANDARD,
            "excerpt": excerpt
        }, timeout=60)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        print(f"Error calling {endpoint}: {e}")
        return "ERROR"

def main():
    df = pd.read_csv(csv_path)

    # Ensure required columns exist
    for col in ["MODEL 1 (Same Thread)", "MODEL 2 (DifferentThread)"]:
        if col not in df.columns:
            df[col] = ""

    for index, row in df.iterrows():
        excerpt = row["Excerpt"]

        if not excerpt or pd.isna(excerpt):
            print(f"Skipping empty excerpt at row {index}")
            continue

        print(f"Processing row {index}...")

        model1_output = call_model(MODEL_1_URL, excerpt)
        df.at[index, "MODEL 1 (Same Thread)"] = model1_output

        model2_output = call_model(MODEL_2_URL, excerpt)
        df.at[index, "MODEL 2 (DifferentThread)"] = model2_output

        df.to_csv(output_csv_path, index=False)
        print(f"Row {index} done and saved.")

    print("All rows processed successfully.")

if __name__ == "__main__":
    main()
