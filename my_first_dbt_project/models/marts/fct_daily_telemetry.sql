{{
    config(
        materialized='table'
    )
}}

with staging as (
    select * from {{ ref('stg_telemetry_events') }}
),

daily_summary as (
    select
        array_id,
        cast(recorded_at as date) as ping_date,
        
        -- Aggregate network health
        count(*) as total_pings,
        
        -- Aggregate electrical metrics
        round(avg(pv_voltage_dc), 2) as avg_bus_voltage,
        round(avg(pv_current_amps), 2) as avg_line_current,
        
        -- Sum up hardware faults
        sum(case when pv_voltage_dc <= 0.0 then 1 else 0 end) as voltage_dropouts

    from staging
    group by 1, 2
)

select * from daily_summary