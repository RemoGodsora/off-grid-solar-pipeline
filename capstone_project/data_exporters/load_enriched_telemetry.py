from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.snowflake import Snowflake
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_snowflake(df: DataFrame, **kwargs) -> None:
    """
    Routes the enriched telemetry matrix across the network to the Snowflake warehouse.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Snowflake.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            table_name='ENRICHED_ANOMALIES',
            database='SOLAR_TELEMETRY',
            schema='GOLD',
            if_exists='replace', # Idempotent write: overwrites with fresh data on each batch
        )