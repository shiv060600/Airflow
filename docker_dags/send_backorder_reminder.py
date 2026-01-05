# Docker-compatible version of weekly backorders reminder DAG
# Replaces PowerShell commands with bash commands for Docker container

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
import datetime

default_args = {
    'owner' : 'admin',
    'depends_on_past': False,
    'start_date': datetime.datetime(2024,1,1),
    'retries' : 0
}

weekly_backorders_reminder = DAG(
    'remind_about_weekly_backorders',
    default_args = default_args,
    description = 'email the team to make sure the backorders  file is in the right place',
    schedule = '0 8 * * 5',
    catchup = False,
    tags = ['weekly','reminder']
)

send_backorders_email = BashOperator(
    task_id = "send_backorders_email",
    # Docker: Use bash command, no PowerShell/Conda needed
    bash_command='cd /opt/airflow/reporting_pipeline && python -m src.helpers.send_backorders_email',
    dag = weekly_backorders_reminder
)

