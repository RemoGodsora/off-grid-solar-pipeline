import json
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data_from_file(*args, **kwargs):
    """
    Reads the simulated edge telemetry from the local buffer.
    """
    # The physical path inside the Docker container mapping to your local drive
    file_path = '/home/src/ingestion/raw_telemetry_buffer.json'
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    # Cast the raw JSON into a Pandas DataFrame for downstream SQL casting
    df = pd.DataFrame(data)
    
    print(f"SUCCESS: Loaded {len(df)} telemetry records from edge buffer.")
    return df