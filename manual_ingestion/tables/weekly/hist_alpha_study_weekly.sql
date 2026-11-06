{{
    config(
        materialized='incremental',
        incremental_strategy='append',
        unique_key=[
            'source_file_name',
            'source_processed_date'
        ],
        full_refresh=false,
        on_schema_change='sync_all_columns'
    )
}}
/*
    model: hist_project_alpha_weekly

    purpose:
    maintain historical snapshots of weekly project alpha loads.

    incremental strategy:
    append

    uniqueness:
    source_file_name +
    source_processed_date

    metadata:
    source_file_name and source_processed_date are used to identify
    distinct ingestion events.

    notes:
    each file ingestion is stored once, allowing historical
    tracking of monthly source deliveries.
*/
with data as (
    select *
    from {{ ref('non_curated__raw_project_alpha_weekly') }}

)
select *
from data
{% if is_incremental() %}
where not exists (
    select 1
    from {{ this }} tgt
    where tgt.source_file_name = data.source_file_name
      and tgt.source_processed_date = data.source_processed_date

)
{% endif %}