{{
    config(
        materialized='view'
    )
}}

with raw_source as (
    select * from {{ source('raw_feed', 'raw_telemetry') }}
),

sanitized as (
    select
        cast(array_id as string) as array_id,
        cast(recorded_at as timestamp) as recorded_at,
        cast(pv_voltage_dc as float64) as pv_voltage_dc,
        cast(pv_current_amps as float64) as pv_current_amps,
        cast(battery_soc_percent as float64) as battery_soc_percent,
        cast(inverter_load_watts as float64) as inverter_load_watts,
        cast(inverter_temp_celsius as float64) as inverter_temp_celsius
    from raw_source
    where array_id is not null
)

select * from sanitized