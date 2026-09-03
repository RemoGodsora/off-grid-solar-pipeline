{{ config(materialized='table') }}

with staging as (
    select * from {{ ref('stg_solar_telemetry') }}
),

windowed_metrics as (
    select
        sensor_id,
        event_recorded_at,
        voltage_volts,
        temperature_celsius,
        power_watts,
        fault_severity,
        avg(voltage_volts) over (
            partition by sensor_id 
            order by event_recorded_at 
            rows between 5 preceding and current row
        ) as rolling_avg_voltage,
        dense_rank() over (
            partition by sensor_id 
            order by voltage_volts desc
        ) as severity_rank
    from staging
)

select
    sensor_id,
    event_recorded_at,
    voltage_volts,
    round(rolling_avg_voltage, 2) as rolling_avg_voltage,
    temperature_celsius,
    power_watts,
    fault_severity,
    severity_rank,
    case 
        when voltage_volts >= 52.0 then true 
        else false 
    end as is_critical_overvoltage
from windowed_metrics