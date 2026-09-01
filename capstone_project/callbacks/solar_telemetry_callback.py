import requests

if 'callback' not in globals():
    from mage_ai.data_preparation.decorators import callback

@callback('failure')
def alert_discord(parent_block_data, **kwargs):
    """
    Fires a REST POST payload to Discord if the pipeline trips a breaker.
    """
    webhook_url = "https://discord.com/api/webhooks/1544312709426716714/qRAzdEsd4rvuIxxNlQxs4nIxAvG4L-bFQJuJBA3QQcQF-GHkD7XpRUAyG9wpzlmb-ZVF" 
    
    payload = {
        "content": "🚨 **CRITICAL FAULT**: The solar_edge_ingestion pipeline just tripped a breaker. Check the Mage logs."
    }
    
    requests.post(webhook_url, json=payload)
    print("Telemetry alert successfully transmitted to Discord.")