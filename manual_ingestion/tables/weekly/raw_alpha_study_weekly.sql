{{
    config(
        materialized='table',
        full_refresh=true,
        transactional_log=true,
        on_schema_change='sync_all_columns'
    )
}}
/*
    model: l0_raw_project_alpha_weekly

    purpose:
    store the raw weekly dataset received from source files
    without applying any business transformation.

    load strategy:
    full refresh

    source:
    raw_project_alpha_weekly

    notes:
    - data loaded through transporter_exec_v2
    - overwrite strategy configured in ingestion layer
    - source metadata preserved for lineage and traceability
*/
select
    source_id,
    snapshot_a,
    snapshot_b,
    processing_flag,
    quantity,
    amount_local,
    amount_usd,
    cost_local,
    cost_usd,
    inventory_quantity,
    inventory_cost_local,
    inventory_cost_usd,
    record_status,
    category_level_1,
    category_level_2,
    category_level_3,
    category_level_4,
    category_level_5,
    reference_code,
    reference_name,
    group_name,
    channel_name,
    channel_category,
    region_name,
    segment_name,
    classification,
    customer_name,
    period_month,
    period_year,
    period_year_month,
    period_end,
    /* ingestion metadata */
    source_file_name,
    source_processed_date
from {{ source('non_curated', 'raw_project_alpha_weekly') }}