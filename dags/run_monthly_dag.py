import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

local_timezone = pendulum.timezone("America/New_York")

default_args = {
    'owner' : 'admin',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2024, 1, 1, tz=local_timezone),
    'retries': 0
}

monthly_dag = DAG(
    'monthly_sales_upload',
    default_args = default_args,
    description = 'monthly upload of ingram sales',
    schedule = "0 17 5 * *", #monthly on the 5th day at 5pm
    tags = ['monthly','sales','ingram'],
    catchup = False,
    timezone = local_timezone
)


upload_monthly_sales = BashOperator(
    task_id='upload_monthly_sales',
    bash_command='powershell.exe -Command "cd H:\\Upgrading_Database_Reporting_Systems\\REPORTING_PIPELINE; conda activate reportingenv; python -m src.run_monthly"',
    dag=monthly_dag,
)

