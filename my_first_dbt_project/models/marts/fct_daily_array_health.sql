{{
    config(
        materialized='table'
    )
}}

with staging as (
    select * from {{ ref('stg_telemetry_events') }}
),

daily_health as (
    select
        array_id,
        date(recorded_at) as operation_date,
        
        -- Electrical Averages
        round(avg(pv_voltage_dc), 2) as avg_voltage,
        round(avg(pv_current_amps), 2) as avg_current,
        round(avg(inverter_load_watts), 2) as avg_load_watts,
        
        -- Battery Health Constraints
        round(min(battery_soc_percent), 2) as min_battery_soc,
        round(max(battery_soc_percent), 2) as max_battery_soc,
        
        -- Thermal Monitoring
        round(max(inverter_temp_celsius), 2) as peak_inverter_temp,
        
        -- Fault Detection Flag (Assuming hardware > 65C is a thermal risk)
        case 
            when max(inverter_temp_celsius) > 65.0 then true 
            else false 
        end as thermal_warning_flag

    from staging
    group by array_id, date(recorded_at)
)

select * from daily_health