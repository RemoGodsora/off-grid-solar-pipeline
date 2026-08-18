import subprocess
from pandas import DataFrame

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

@custom
def execute_dbt(*args, **kwargs):
    """
    Acts as a physical relay switch, triggering the dbt compiler 
    immediately after the BigQuery ingestion completes.
    """
    print("Mage Ingestion Complete. Engaging dbt compiler...")
    
    # The absolute path to your dbt project inside the Docker container
    dbt_project_dir = '/home/src/transformations/solar_analytics'
    
    # Fire the dbt engine. We pass '--profiles-dir .' to force it to use 
    # the localized Docker profile we just created in Step 1.
    result = subprocess.run(
        ['dbt', 'run', '--profiles-dir', '.'],
        cwd=dbt_project_dir,
        capture_output=True,
        text=True
    )
    
    # Print the dbt terminal output into the Mage console
    print(result.stdout)
    
    # If the circuit trips, raise an immediate fault alert
    if result.returncode != 0:
        print(result.stderr)
        raise Exception("CRITICAL FAULT: dbt compilation failed. Check logs.")
        
    print("SUCCESS: AC Metrics Table Materialized Autonomously.")
    return {}