#type: ignore
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
import datetime

default_args = {
    'owner' : 'admin',
    'depends_on_past': False,
    'start_date': datetime.datetime(2024,1,1),
    'retries' : 0
}

monthly_sales_reminder = DAG(
    'remind_about_sales',
    default_args = default_args,
    description = 'email the team to make sure the monthly sales file is in the right place',
    schedule = '0 9 5 * *',
    catchup = False,
    tags = ['monthly','reminder']
)

send_email = BashOperator(
    task_id = "send_monthly_email",
    bash_command='powershell.exe -Command "cd H:\\Upgrading_Database_Reporting_Systems\\REPORTING_PIPELINE; conda activate reportingenv; python -m src.helpers.send_email"',
    dag = monthly_sales_reminder
)

