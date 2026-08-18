-- We physically materialize this as a table to optimize downstream BI dashboard costs
{{ config(materialized='table') }}

WITH raw_data AS (
    SELECT 
        device_id,
        -- Cast the ISO string timestamp to a pure Date format for daily aggregations
        DATE(TIMESTAMP(timestamp)) AS telemetry_date,
        voltage,
        -- Escape the reserved keyword using BigQuery backticks
        `current`,
        inverter_temp_c,
        battery_soc_pct,
        is_faulting
    FROM 
        `de-zoomcamp-2026-502910.solar_telemetry_raw.raw_telemetry`
)

SELECT 
    device_id,
    telemetry_date,
    ROUND(AVG(voltage), 2) AS avg_voltage_dc,
    -- Safely aggregate the escaped column
    ROUND(MAX(`current`), 2) AS peak_current_amps,
    ROUND(MAX(inverter_temp_c), 2) AS peak_inverter_temp_c,
    ROUND(MIN(battery_soc_pct), 2) AS min_battery_soc,
    COUNTIF(is_faulting = true) AS daily_fault_count
FROM 
    raw_data
GROUP BY 
    device_id,
    telemetry_date