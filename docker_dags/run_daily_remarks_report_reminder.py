# Docker-compatible version of daily remarks reminder DAG
# Replaces PowerShell commands with bash commands for Docker container

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
import datetime

default_args = {
    "start_date" : datetime.datetime(2024,1,1),
    "retries" : 0,
    "depends_on_past" : False,
    "owner" : "admin"
}

with DAG(
    dag_id = 'send_reminder_remarks_report',
    tags = ['daily','reminder'],
    schedule = "30 8 * * 1-5",
    catchup = False,
    default_args = default_args
    ) as daily_remarks_reminder:

    daily_remarks_reminder_runner = BashOperator(
        task_id = 'run_remarks_reminder_email',
        # Docker: Use bash command, no PowerShell/Conda needed
        bash_command='cd /opt/airflow/reporting_pipeline && python -m src.helpers.daily_remarks_reminder',
        dag = daily_remarks_reminder
    )

