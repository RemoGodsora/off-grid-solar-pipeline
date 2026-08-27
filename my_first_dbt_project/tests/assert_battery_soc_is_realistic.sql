-- This test will fail if any array reports an impossible physical metric.
-- If it returns rows, dbt trips the circuit breaker.

select
    array_id,
    recorded_at,
    pv_voltage_dc,
    inverter_temp_celsius
from {{ ref('stg_telemetry_events') }}
where 
    -- Testing for an impossible inverter temperature (e.g., > 150 Celsius)
    inverter_temp_celsius > 150.0 
    or inverter_temp_celsius < -50.0