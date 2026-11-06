{{
    config(
        materialized='view'
    )
}}
/*
    model: dq_project_alpha_weekly_latest_load

    purpose:
    expose only the latest weekly ingestion load for
    data quality validation.

    usage:
    all dq tests should reference this model instead of
    the historical table.

    logic:
    retrieve records belonging to the most recent
    ingestion event based on source_processed_date.
*/
with data as (
    select *
    from {{ ref('hist_project_alpha_weekly') }}

),
latest_load as (
    select *
    from data
    qualify dense_rank() over (
        order by source_processed_date desc
    ) = 1
)
select *
from latest_load