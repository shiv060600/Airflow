#!/bin/bash

# Change to airflow directory
cd /mnt/h/Upgrading_Database_Reporting_Systems/airflow

echo "Stopping Apache Airflow..."

# Kill all airflow processes
pkill -9 -f "airflow"

echo "Airflow stopped!"
