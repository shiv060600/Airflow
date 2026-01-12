from datetime import tzinfo
from time import timezone
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
import pendulum


local_timezone = pendulum.timezone("America/New_York")

default_args = {
    'owner' : 'admin',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2024, 1, 1, tz = local_timezone),
    'retries': 0
}

pgc_pguk_dag = DAG(
    dag_id= 'pgc_pguk_full_report',
    description= 'run pgc pguk full report on the 5th of each month after run_daily_py',
    schedule='0 22 4 * *', #run monthly on the 5th at 10pm
    tags= ['pgc','pguk','monthly'],
    catchup = False,
    timezone = local_timezone
)

run_pgc_pguk = BashOperator(
    dag= pgc_pguk_dag,
    task_id='run_pgc_pguk',
    bash_command='powershell.exe -Command "cd H:\\Upgrading_Database_Reporting_Systems\\REPORTING_PIPELINE; conda activate reportingenv; python -m src.run_pgc_pguk"',
)