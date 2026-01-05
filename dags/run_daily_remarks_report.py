from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
import datetime


default_args = {
    "depends_on_past" : False,
    "retries" : 0,
    "start_date" : datetime.datetime(2024,1,1),
    "owner" : "admin"
}

with DAG(
    dag_id = 'daily_remarks_report',
    default_args = default_args,
    description = 'daily remarks report with latest remarks from singapore + sandy',
    schedule = '0 18 * * *',
    catchup = False,
    tags = ['daily','remarks']
) as daily_remarks_dag:
    
    daily_remarks_runner = BashOperator(
        task_id='run_daily_remarks_report',
        bash_command='powershell.exe -Command "cd H:\\Upgrading_Database_Reporting_Systems\\REPORTING_PIPELINE; conda activate reportingenv; python -m src.run_daily_remarks_report"',
        dag=daily_remarks_dag,
    )