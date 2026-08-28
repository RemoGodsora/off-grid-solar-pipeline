if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
import subprocess

@custom
def run_dbt_transformations(*args, **kwargs):
    """
    Acts as the relay switch: triggers the dbt compiler inside the container 
    the exact moment BigQuery confirms receipt of raw telemetry packets.
    """
    print("Ingestion verified. Triggering dbt transformation engine...")

    # Container path mapping to your local dbt project
    project_path = '/home/src/my_first_dbt_project'

    command = [
        'dbt', 'run',
        '--project-dir', project_path,
        '--profiles-dir', project_path
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("dbt compilation failed. Check logs above.")

    print("SUCCESS: dbt analytics models compiled and materialized.")
    return {}