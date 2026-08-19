import requests

# 1. The Fix: Import the unified callback router
if 'callback' not in globals():
    from mage_ai.data_preparation.decorators import callback

# 2. Tell the router to only fire on a 'failure' state
@callback('failure')
def alert_discord(parent_block_data, **kwargs):
    """
    Fires a REST POST payload to Discord and logs the HTTP response.
    """
    webhook_url = "https://discord.com/api/webhooks/1539475901975101570/lGTpOPk6ybiAC2w_qHSfEVlkFIqCOhdF6xhVig5JDHhIs3tzNOJ4j_bRL4SraPXJGbfd" # Ensure this is your actual URL
    
    payload = {
        "content": "🚨 **CRITICAL FAULT**: The Telemetry Pipeline just tripped a breaker."
    }
    
    # Fire the telemetry alert and capture the response
    response = requests.post(webhook_url, json=payload)
    
    # Read the diagnostic output
    print(f"Discord API Status Code: {response.status_code}")
    if response.status_code == 204:
        print("SUCCESS: Telemetry alert successfully transmitted to Discord.")
    else:
        print(f"FAULT: Discord rejected the payload. Reason: {response.text}")