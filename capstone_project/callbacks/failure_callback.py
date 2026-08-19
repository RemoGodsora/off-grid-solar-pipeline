import requests

if 'failure_callback' not in globals():
    from mage_ai.data_preparation.decorators import failure_callback

@failure_callback
def alert_discord(kwargs, **kwargs_extra):
    """
    Fires a REST POST payload to Discord if the pipeline trips a breaker.
    """
    # Replace with your actual Discord Webhook URL
    webhook_url = "https://discord.com/api/webhooks/1539475901975101570/lGTpOPk6ybiAC2w_qHSfEVlkFIqCOhdF6xhVig5JDHhIs3tzNOJ4j_bRL4SraPXJGbfd"
    
    payload = {
        "content": "🚨 **CRITICAL FAULT**: The Solar Telemetry Pipeline just tripped a breaker. Check the Mage orchestrator logs immediately."
    }
    
    # Fire the telemetry alert
    requests.post(webhook_url, json=payload)
    
    print("Telemetry alert successfully transmitted to Discord.")