{{
    config(
        materialized='view'
    )
}}

with raw_source as (
    -- This pulls from the physical cloud database, breaking the loop
    select * from {{ source('raw_feed', 'raw_telemetry') }}
),

sanitized as (
    select
        cast(device_id as int64) as array_id,
        cast(ping_timestamp as timestamp) as recorded_at,
        
        coalesce(cast(bus_voltage as float64), 0.0) as pv_voltage_dc,
        coalesce(cast(line_current as float64), 0.0) as line_current_a,
        coalesce(cast(ambient_temp as float64), 25.0) as inverter_temp_celsius

    from raw_source
)

select * from sanitized