import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

local_timezone = pendulum.timezone("America/New_York")

default_args = {
    'owner' : 'admin',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2024, 1, 1, tz=local_timezone),
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
    bash_command='powershell.exe -Command "cd H:\\Upgrading_Database_Reporting_Systems\\REPORTING_PIPELINE; conda activate reportingenv; python -m src.helpers.send_backorders_email"',
    dag = weekly_backorders_reminder
)