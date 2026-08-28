import requests

if 'callback' not in globals():
    from mage_ai.data_preparation.decorators import callback

@callback('failure')
def alert_discord(parent_block_data, **kwargs):
    """
    Fires a REST POST payload to Discord and logs the HTTP response.
    """
    webhook_url = "https://discord.com/api/webhooks/1542731123941974137/YjKaBNmQ5UO8k23QBK2WfUbcJffiNqV0yqWJbV-vb1bEcbOcHcoEEGOpsRNO5G_mVZSA" 
    
    payload = {
        "content": "🚨 **CRITICAL FAULT**: The Telemetry Pipeline just tripped a breaker."
    }
    
    response = requests.post(webhook_url, json=payload)
    
    print(f"Discord API Status Code: {response.status_code}")
    if response.status_code == 204:
        print("SUCCESS: Telemetry alert successfully transmitted to Discord.")
    else:
        print(f"FAULT: Discord rejected the payload. Reason: {response.text}")