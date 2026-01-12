import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

local_timezone = pendulum.timezone("America/New_York")

default_args = {
    "start_date" : pendulum.datetime(2024, 1, 1, tz=local_timezone),
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

    daily_remakrs_reminder_runner = BashOperator(
        task_id = 'run_remarks_reminder_email',
        bash_command='powershell.exe -Command "cd H:\\Upgrading_Database_Reporting_Systems\\REPORTING_PIPELINE; conda activate reportingenv; python -m src.helpers.daily_remarks_reminder"',
        dag = daily_remarks_reminder
    )