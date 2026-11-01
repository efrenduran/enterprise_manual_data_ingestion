task_configs = [
    # Monthly Ingestion
    {
        "task_name": "1_project_alpha_monthly_decompress",
        "task_type": "transporter_exec",
        "force_ingestion": "true",
        "source_connection": {
            "inherit_from": "blob_conn",
            "file_path": "workspace/zone_07/module_x/monthly/inbound/DATASET_X_[A-Z]{3}\\d{6}_MONTHLY\\.[Zz][Ii][Pp]",
            "file_format": "zip",
            "transactional_log": "true",
            "extra_imports": [
                "from datetime import datetime"
            ],
            "archive_or_delete": "archive",
            "archive_path": "workspace/zone_07/module_x/monthly/processed/{input_key.split('/')[-1]}"
        },
        "target_connection": {
            "inherit_from": "blob_conn",
            "file_path": "workspace/zone_07/module_x/monthly/uncompressed/",
            "file_format": "csv"
        }
    },
    {
        "task_name": "2_project_alpha_monthly_load",
        "task_type": "transporter_exec",
        "force_ingestion": "true",
        "source_connection": {
            "inherit_from": "blob_conn",
            "extra_imports": [
                "from datetime import datetime"
            ],
            "file_path": "workspace/zone_07/module_x/monthly/uncompressed/DATASET_X_[A-Z]{3}\\d{6}_MONTHLY\\.(csv|CSV)$",
            "file_format": "csv",
            "delimiter": "|",
            "encoding": "utf-8",
            "transactional_log": "true",
            "accepted_and_rejected_archiving": "true",
            "archive_or_delete": "archive",
            "archive_path": "workspace/zone_07/module_x/monthly/processed/{input_key.split('/')[-1]}",
            "data_expectations": [
                {
                    "expectation": "expect_column_to_exist",
                    "args": {
                        "columns": [
                            "source_id",
                            "processing_flag",
                            "quantity",
                            "amount_local",
                            "amount_usd",
                            "cost_local",
                            "cost_usd",
                            "inventory_quantity",
                            "inventory_cost_local",
                            "inventory_cost_usd",
                            "record_status",
                            "category_level_1",
                            "category_level_2",
                            "category_level_3",
                            "category_level_4",
                            "category_level_5",
                            "reference_code",
                            "reference_name",
                            "group_name",
                            "channel_name",
                            "channel_category",
                            "region_name",
                            "segment_name",
                            "cluster_name",
                            "classification",
                            "customer_name",
                            "period_month",
                            "period_year",
                            "period_year_month",
                            "period_end"
                        ]
                    },
                    "severity_level": "CRITICAL"
                },
                {
                    "expectation": "expect_table_column_count_to_equal",
                    "args": {
                        "value": 30
                    },
                    "severity_level": "CRITICAL"
                }
            ],
            "dtype": {
                "source_id": "object",
                "processing_flag": "object",
                "quantity": "double",
                "amount_local": "double",
                "amount_usd": "double",
                "cost_local": "double",
                "cost_usd": "double",
                "inventory_quantity": "double",
                "inventory_cost_local": "double",
                "inventory_cost_usd": "double",
                "record_status": "object",
                "category_level_1": "object",
                "category_level_2": "object",
                "category_level_3": "object",
                "category_level_4": "object",
                "category_level_5": "object",
                "reference_code": "object",
                "reference_name": "object",
                "group_name": "object",
                "channel_name": "object",
                "channel_category": "object",
                "region_name": "object",
                "segment_name": "object",
                "cluster_name": "object",
                "classification": "object",
                "customer_name": "object",
                "period_month": "object",
                "period_year": "object",
                "period_year_month": "object",
                "period_end": "object"
            },
            "add_file_name": "true",
            "file_name_col_alias": "source_file_name",
            "add_file_processing_date": "true",
            "file_processing_date_col_alias": "source_processed_date"
        },
        "target_connection": {
            "inherit_from": "snowflake_conn",
            "table_name": "RAW_PROJECT_ALPHA_MONTHLY",
            "namespace": "non_curated",
            "update_strategy": "overwrite"
        }
    },

    # Weekly Ingestion
    {
        "task_name": "3_project_alpha_weekly_decompress",
        "task_type": "transporter_exec",
        "force_ingestion": "true",
        "source_connection": {
            "inherit_from": "blob_conn",
            "file_path": "workspace/zone_07/module_x/weekly/inbound/DATASET_X_[A-Z]{3}\\d{6}_WEEKLY\\.[Zz][Ii][Pp]",
            "file_format": "zip",
            "transactional_log": "true",
            "extra_imports": [
                "from datetime import datetime"
            ],
            "archive_or_delete": "archive",
            "archive_path": "workspace/zone_07/module_x/weekly/processed/{input_key.split('/')[-1]}"
        },
        "target_connection": {
            "inherit_from": "blob_conn",
            "file_path": "workspace/zone_07/module_x/weekly/uncompressed/",
            "file_format": "csv"
        }
    },
    {
        "task_name": "4_project_alpha_weekly_load",
        "task_type": "transporter_exec",
        "force_ingestion": "true",
        "source_connection": {
            "inherit_from": "blob_conn",
            "extra_imports": [
                "from datetime import datetime"
            ],
            "file_path": "workspace/zone_07/module_x/weekly/uncompressed/DATASET_X_[A-Z]{3}\\d{6}_WEEKLY\\.(csv|CSV)$",
            "file_format": "csv",
            "delimiter": "|",
            "encoding": "utf-8",
            "transactional_log": "true",
            "accepted_and_rejected_archiving": "true",
            "archive_or_delete": "archive",
            "archive_path": "workspace/zone_07/module_x/weekly/processed/{input_key.split('/')[-1]}",
            "data_expectations": [
                {
                    "expectation": "expect_table_column_count_to_equal",
                    "args": {
                        "value": 31
                    },
                    "severity_level": "CRITICAL"
                }
            ],
            "dtype": {
                "source_id": "object",
                "snapshot_a": "object",
                "snapshot_b": "object",
                "processing_flag": "object",
                "quantity": "double",
                "amount_local": "double",
                "amount_usd": "double",
                "cost_local": "double",
                "cost_usd": "double",
                "inventory_quantity": "double",
                "inventory_cost_local": "double",
                "inventory_cost_usd": "double",
                "record_status": "object",
                "category_level_1": "object",
                "category_level_2": "object",
                "category_level_3": "object",
                "category_level_4": "object",
                "category_level_5": "object",
                "reference_code": "object",
                "reference_name": "object",
                "group_name": "object",
                "channel_name": "object",
                "channel_category": "object",
                "region_name": "object",
                "segment_name": "object",
                "classification": "object",
                "customer_name": "object",
                "period_month": "object",
                "period_year": "object",
                "period_year_month": "object",
                "period_end": "object"
            },
            "add_file_name": "true",
            "file_name_col_alias": "source_file_name",
            "add_file_processing_date": "true",
            "file_processing_date_col_alias": "source_processed_date"
        },
        "target_connection": {
            "inherit_from": "snowflake_conn",
            "table_name": "RAW_PROJECT_ALPHA_WEEKLY",
            "namespace": "non_curated",
            "update_strategy": "overwrite"
        }
    }
]