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
        round(avg(pv_current_amps), 2) as avg_current
        
    from staging
    group by array_id, date(recorded_at)
)

select * from daily_health