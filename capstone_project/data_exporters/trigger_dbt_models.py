if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import subprocess

@data_exporter
def export_data(*args, **kwargs):
    """
    Bypasses the Mage UI and explicitly triggers the dbt compiler via the container terminal.
    """
    print("Initiating dbt compilation sequence...")

    # The absolute path inside the Docker container to your dbt project
    project_path = '/home/src/my_first_dbt_project'

    # Hardwiring the terminal command
    command = [
        'dbt', 'run', 
        '--select', 'fct_daily_array_health',
        '--project-dir', project_path, 
        '--profiles-dir', project_path
    ]

    # Execute the terminal command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the terminal logs to the Mage UI so we can monitor it
    print(result.stdout)

    # If the compiler throws an error, intentionally fail the Mage block
    if result.returncode != 0:
        print(result.stderr)
        raise Exception("dbt compilation failed. Check the logs above.")

    print("dbt transformation complete. AC power is flowing.")
    return {}