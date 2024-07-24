import argparse
import requests
import pandas as pd
import json
import logging
from io import StringIO

# Configure logging
logging.basicConfig(level=logging.INFO)


# Function to fetch CSV from Google Drive
def fetch_csv_from_gdrive(file_id: str) -> pd.DataFrame:
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = pd.read_csv(StringIO(response.text))
        return csv_data
    except requests.RequestException as e:
        logging.error(f"Error fetching the CSV: {e}")
        raise
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing the CSV data: {e}")
        raise


# Function to get selected fields and return JSON
def get_fields_as_json(data: pd.DataFrame, fields: list) -> str:
    try:
        selected_data = data[fields]
        json_data = {"data": selected_data.to_dict(orient="records")}
        return json.dumps(json_data, indent=4)
    except KeyError as e:
        logging.error(f"Field not found: {e}")
        raise


# Main function to run the script
def main():
    # Define command-line arguments
    parser = argparse.ArgumentParser(
        description="Fetch CSV data from Google Drive and return selected fields in JSON format."
    )
    parser.add_argument(
        "--fields",
        type=str,
        required=True,
        help="Comma-separated list of fields to return.",
    )
    args = parser.parse_args()

    # Define Google Drive file ID
    file_id = "1zLdEcpzCp357s3Rse112Lch9EMUWzMLE"

    # Fetch CSV data
    data = fetch_csv_from_gdrive(file_id)

    # Parse fields from the arguments
    fields = [field.strip() for field in args.fields.split(",")]

    # Get JSON output for selected fields
    try:
        json_output = get_fields_as_json(data, fields)
        print(json_output)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
