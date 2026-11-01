from airflow.decorators import dag
from airflow.utils.task_group import TaskGroup

from test.orchestrate.dags.project_alpha.task_configs import task_configs
from test.orchestrate.dags.utils.default_args import default_args

from test.orchestrate.dags.utils.operators.kdp_test_databricksoperator import (
    kdp_test_databricksoperator,
)

from test.orchestrate.dags.utils.operators.kdp_test_dbtoperator import (
    kdp_test_dbtoperator,
)

from test.orchestrate.dags.utils.sensors.wasbregexsensor import (
    WasbPrefixSensor,
)

dag_default_args = {
    **default_args.default_args,
    "email_on_failure": False,
    "retries": 0,
}

@dag(
    dag_id="project_alpha_monthly_weekly",
    default_args=dag_default_args,
    description="Project Alpha Monthly and Weekly Ingestion",
    schedule="0 */1 * * *",
    access_control={
        "test_Developer": {"can_read", "can_edit"},
        "test_Viewer": {"can_read"},
    },
    tags=[
        "project_alpha",
        "monthly",
        "weekly",
    ],
    catchup=False,
    max_active_runs=1,
)
def project_alpha_monthly_weekly():
    sensor_task = WasbPrefixSensor(
        task_id="sensor",
        container_name="{{ var.value.test_blob_container_name }}",
        prefix="{{ dag_run.conf.get('prefix', 'workspace/zone_07/module_x/') }}",
        wasb_conn_id="test_azure_blob_connection",
        poke_interval=900.0,
        mode="reschedule",
        soft_fail=True,
    )

    with TaskGroup("project_alpha_tasks") as project_alpha_tasks:
        monthly_decompress_config = next(
            cfg
            for cfg in task_configs
            if cfg["task_name"] == "1_project_alpha_monthly_decompress"
        )

        monthly_load_config = next(
            cfg
            for cfg in task_configs
            if cfg["task_name"] == "2_project_alpha_monthly_load"
        )

        weekly_decompress_config = next(
            cfg
            for cfg in task_configs
            if cfg["task_name"] == "3_project_alpha_weekly_decompress"
        )

        weekly_load_config = next(
            cfg
            for cfg in task_configs
            if cfg["task_name"] == "4_project_alpha_weekly_load"
        )

        monthly_decompress = kdp_test_databricksoperator(
            task_name="1_project_alpha_monthly_decompress",
            task_config=monthly_decompress_config,
            notebook_path="Databricks/scripts/Laguna/executors/transporter_exec_v2",
        )

        monthly_load = kdp_test_databricksoperator(
            task_name="2_project_alpha_monthly_load",
            task_config=monthly_load_config,
            notebook_path="Databricks/scripts/Laguna/executors/transporter_exec_v2",
        )

        weekly_decompress = kdp_test_databricksoperator(
            task_name="3_project_alpha_weekly_decompress",
            task_config=weekly_decompress_config,
            notebook_path="Databricks/scripts/Laguna/executors/transporter_exec_v2",
        )

        weekly_load = kdp_test_databricksoperator(
            task_name="4_project_alpha_weekly_load",
            task_config=weekly_load_config,
            notebook_path="Databricks/scripts/Laguna/executors/transporter_exec_v2",
        )

        dbt_project_alpha = kdp_test_dbtoperator(
            task_id="5_dbt_project_alpha",
            queue="kubernetes",
            bash_command="dbt run --select tag:project_alpha_monthly_weekly",
        )

        monthly_decompress >> monthly_load >> dbt_project_alpha
        weekly_decompress >> weekly_load >> dbt_project_alpha

    sensor_task >> project_alpha_tasks

dag = project_alpha_monthly_weekly()