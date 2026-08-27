{{ config(materialized='table') }}

with staging as (
    select * from {{ ref('stg_telemetry_events') }}
),

daily_health as (
    select
        array_id,
        date(recorded_at) as operation_date,
        
        -- Aggregated Electrical Metrics
        round(avg(pv_voltage_dc), 2) as avg_voltage,
        round(avg(line_current_a), 2) as avg_current, -- The Rewired Pin
        round(max(inverter_temp_celsius), 2) as peak_inverter_temp,
        
        -- Thermal Fault Detection
        case 
            when max(inverter_temp_celsius) > 65.0 then true 
            else false 
        end as thermal_warning_flag
    from staging
    group by array_id, date(recorded_at)
)

select * from daily_health