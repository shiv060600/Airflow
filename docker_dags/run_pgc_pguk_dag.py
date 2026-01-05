# Docker-compatible version of PGC/PGUK DAG
# Replaces PowerShell commands with bash commands for Docker container

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
import datetime

default_args = {
    'owner' : 'admin',
    'depends_on_past': False,
    'start_date': datetime.datetime(2024,1,1),
    'retries': 0
}

pgc_pguk_dag = DAG(
    dag_id= 'pgc_pguk_full_report',
    description= 'run pgc pguk full report on the 5th of each month after run_daily_py',
    schedule='0 22 4 * *', #run monthly on the 5th at 10pm
    tags= ['pgc','pguk','monthly'],
    catchup = False,
    default_args=default_args
)

run_pgc_pguk = BashOperator(
    dag= pgc_pguk_dag,
    task_id='run_pgc_pguk',
    # Docker: Use bash command, no PowerShell/Conda needed
    bash_command='cd /opt/airflow/reporting_pipeline && python -m src.run_pgc_pguk',
)

