from google.cloud import bigquery
from google.oauth2 import service_account
from pandas import DataFrame

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
    """
    Transmits the edge payload directly to the Google BigQuery warehouse.
    """
    # 1. Define the network route
    project_id = 'de-zoomcamp-2026-502910' 
    dataset_name = 'solar_telemetry_raw'
    table_name = 'raw_telemetry'
    
    table_id = f"{project_id}.{dataset_name}.{table_name}"

    # 2. Authenticate using the volume-mounted security badge
    key_path = '/home/src/infrastructure/keys.json'
    credentials = service_account.Credentials.from_service_account_file(key_path)
    
    client = bigquery.Client(credentials=credentials, project=project_id)

    # 3. Configure the transmission protocol
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND", # Append new telemetry chunks, don't overwrite
    )

    print(f"Initiating direct uplink to {table_id}...")

    # 4. Transmit the payload
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )

    # 5. Block the thread until Google confirms receipt of the packets
    job.result()

    print(f"SUCCESS: {job.output_rows} rows permanently stored in the BigQuery battery bank.")