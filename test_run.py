import unittest
import pandas as pd
from io import StringIO
from run import fetch_csv_from_gdrive, get_fields_as_json


class TestFetchCSV(unittest.TestCase):

    def test_fetch_csv_from_gdrive(self):
        # Test if the CSV fetch returns a DataFrame
        file_id = "1zLdEcpzCp357s3Rse112Lch9EMUWzMLE"
        df = fetch_csv_from_gdrive(file_id)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    def test_get_fields_as_json(self):
        # Sample CSV data
        csv_data = (
            "date,campaign,clicks\n2021-11-23,Campaign A,100\n2021-11-24,Campaign B,150"
        )
        df = pd.read_csv(StringIO(csv_data))

        # Test JSON output with selected fields
        fields = ["date", "clicks"]
        json_output = get_fields_as_json(df, fields)

        expected_output = {
            "data": [
                {"date": "2021-11-23", "clicks": 100},
                {"date": "2021-11-24", "clicks": 150},
            ]
        }

        # Convert expected output to JSON string
        import json

        expected_json = json.dumps(expected_output, indent=4)

        self.assertEqual(json_output, expected_json)

    def test_get_fields_as_json_invalid_field(self):
        # Sample CSV data
        csv_data = (
            "date,campaign,clicks\n2021-11-23,Campaign A,100\n2021-11-24,Campaign B,150"
        )
        df = pd.read_csv(StringIO(csv_data))

        # Test with an invalid field
        fields = ["date", "non_existent_field"]

        with self.assertRaises(KeyError):
            get_fields_as_json(df, fields)


if __name__ == "__main__":
    unittest.main()
