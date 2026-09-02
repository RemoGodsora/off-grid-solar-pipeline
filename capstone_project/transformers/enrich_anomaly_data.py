if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

@transformer
def transform(data, *args, **kwargs):
    """
    data: The Pandas DataFrame output from the SQL extraction block.
    """
    # 1. Calculate raw power draw (Watts = Volts * Amps)
    data['power_watts'] = data['voltage'] * data['current_amps']
    
    # 2. Assign hardware severity flags for the downstream monitoring dashboard
    data['severity'] = data['voltage'].apply(lambda v: 'CRITICAL' if v >= 51.5 else 'WARNING')
    
    # 3. Sort by the most recent anomalies first
    data = data.sort_values(by='timestamp', ascending=False)
    
    return data