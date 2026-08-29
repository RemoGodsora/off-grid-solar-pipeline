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
        -- 🛠️ THE FIX: Read the physical 'device_id' pin and output it as 'array_id'
        SAFE_CAST(device_id as string) as array_id,
        SAFE_CAST(timestamp as timestamp) as recorded_at,
        SAFE_CAST(voltage as float64) as pv_voltage_dc,
        -- Escape the reserved 'current' keyword with backticks
        SAFE_CAST(`current` as float64) as pv_current_amps
    from raw_source
    -- Explicitly drop the header row and corrupted payloads using the raw column name
    where device_id is not null 
      and device_id != 'device_id'
)

select * from sanitized