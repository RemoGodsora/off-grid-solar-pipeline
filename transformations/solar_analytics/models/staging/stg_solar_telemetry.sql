{{ config(materialized='view') }}

with raw_source as (
    select * from {{ source('solar_raw', 'ENRICHED_ANOMALIES') }}
)

select
    cast("sensor_id" as varchar) as sensor_id,
    to_timestamp_ntz("timestamp") as event_recorded_at,
    cast("voltage" as float) as voltage_volts,
    cast("temperature" as float) as temperature_celsius,
    cast("power_watts" as float) as power_watts,
    upper(cast("severity" as varchar)) as fault_severity
from raw_source
where "voltage" is not null