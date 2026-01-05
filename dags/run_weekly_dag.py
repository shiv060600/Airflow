#type: ignore
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner' : 'admin',
    'depends_on_past': False,
    'start_date': datetime(2024,1,1),
    'retries': 0
}

weekly_dag = DAG(
    'weekly_backorders',
    default_args = default_args,
    description = 'Weekly Backorders, Executed Friday 10PM',
    schedule = '0 22 * * 5', #10pm Frdiday
    catchup = False,
    tags = ['backorders','weekly']
)

run_upload_backorders = BashOperator(
    task_id='run_upload_backorders',
    bash_command='powershell.exe -Command "cd H:\\Upgrading_Database_Reporting_Systems\\REPORTING_PIPELINE; conda activate reportingenv; python -m src.database_uploads.upload_backorders"',
    dag=weekly_dag,
)

run_book_level_reports = BashOperator(
    task_id='run_booklevel_reports',
    bash_command='powershell.exe -Command "cd H:\\Upgrading_Database_Reporting_Systems\\REPORTING_PIPELINE; conda activate reportingenv; python -m src.run_weekly_book_level_reports"',
    dag=weekly_dag
)

run_upload_backorders >> run_book_level_reports