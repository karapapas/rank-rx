import os
import subprocess
import pandas as pd

# Careful we are working with "DepMap Public 24Q2" make sure all files are from the same publication.

class DataLoader:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.file_links = {
            "Model": "https://plus.figshare.com/ndownloader/files/46489732",
            "OmicsExpressionProteinCodingGenesTPMLogp1BatchCorrected": "https://plus.figshare.com/ndownloader/files/46493230",
            "SangerDoseResponse": "https://storage.googleapis.com/depmap-external-downloads/processed_portal_downloads/gdsc-drug-set-export-658c.5/sanger-dose-response.csv?GoogleAccessId=depmap-external-downloads%40broad-achilles.iam.gserviceaccount.com&Expires=1724170312&Signature=GfdB0AACJp7P7vmAkJPlpJ%252B0%252FD30W3S2SZURJqTyZnyfdsT2MLEi054ws7lavScx5W5bwWIj0Gr8et%252BNry3I0S%252BC23hThHYnlgRFrq2iyCLCb8UcL3Q9z9Eea9mCP9XcI9fgL1Wo9PexQNtc1BHdoppm4t5kPtrpaynBNa%252BB%252F0%252BJcth2bdcgVhyOdeDNRa8JhSgLu9H7lGbPqufAD83q0EwUEBXcJZN%252BxclAfnPtSS7CLESe9k6%252FurylxhKSdITXrRYVSbZvJHOsyWHiSzdxJFiO8vXH4q7iVnHhY6LDufqmtEgrDhULDpUnAs3QA9tVFS3Eu8YIB1jD0N1AXYtiaw%3D%3D&userProject=broad-achilles"
        }

    def load_data(self, filename):
        # Ensure the directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Construct the full file path
        file_path = os.path.join(self.data_dir, filename)

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"{filename} not found, downloading...")
            
            # Get the download URL for the specified file
            download_url = self.file_links.get(filename)
            if not download_url:
                print(f"No download link found for {filename}")
                return None

            # Use curl to download the file
            curl_command = f'curl -o "{file_path}" "{download_url}"'
            try:
                subprocess.run(curl_command, shell=True, check=True)
                print(f"{filename} downloaded successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to download {filename}: {e}")
                return None

        # Read the CSV file using Polars
        try:
            df = pd.read_csv(file_path)
            if df is not None and isinstance(df, pd.DataFrame) and len(df) > 0:
                print(f"{filename} read successfully.")
                return df
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return None
