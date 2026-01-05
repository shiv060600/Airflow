#!/bin/bash

# Change to airflow directory
cd /mnt/h/Upgrading_Database_Reporting_Systems/airflow

# Startup script for Apache Airflow
echo "Starting Apache Airflow..."

# Set Airflow Home
export AIRFLOW_HOME=/mnt/h/Upgrading_Database_Reporting_Systems/airflow

# Set password file path (overrides config)
export AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_PASSWORDS_FILE=/mnt/h/Upgrading_Database_Reporting_Systems/airflow/simple_auth_manager_passwords.json

# Activate virtual environment
source /mnt/h/Upgrading_Database_Reporting_Systems/airflow/airflow_env_linux/bin/activate

# Set full path to Python interpreter (bypasses broken shebang in airflow script)
# Detect which Python executable exists
VENV_BIN=/mnt/h/Upgrading_Database_Reporting_Systems/airflow/airflow_env_linux/bin
if [ -f "$VENV_BIN/python3" ]; then
    PYTHON_CMD="$VENV_BIN/python3"
elif [ -f "$VENV_BIN/python" ]; then
    PYTHON_CMD="$VENV_BIN/python"
elif [ -f "$VENV_BIN/python3.12" ]; then
    PYTHON_CMD="$VENV_BIN/python3.12"
else
    echo "ERROR: Python interpreter not found in virtual environment!"
    exit 1
fi

# Start API server in background
echo "Starting Airflow API Server on port 8080..."
nohup $PYTHON_CMD -m airflow api-server --port 8080 > logs/api_server.log 2>&1 &
API_PID=$!

# Wait a moment for API server to initialize
sleep 3

# Start scheduler in background
echo "Starting Airflow Scheduler..."
nohup $PYTHON_CMD -m airflow scheduler > logs/scheduler.log 2>&1 &
SCHEDULER_PID=$!

# Start DAG processor in background
echo "Starting Airflow DAG Processor..."
nohup $PYTHON_CMD -m airflow dag-processor > logs/dag_processor.log 2>&1 &
DAG_PROCESSOR_PID=$!

# Wait for services to start
echo "Waiting for services to initialize..."
sleep 5

# Check if processes are running
if kill -0 $API_PID 2>/dev/null; then
    echo "API Server: RUNNING (PID: $API_PID)"
else
    echo "API Server: FAILED TO START"
fi

if kill -0 $SCHEDULER_PID 2>/dev/null; then
    echo "Scheduler: RUNNING (PID: $SCHEDULER_PID)"
else
    echo "Scheduler: FAILED TO START"
fi

if kill -0 $DAG_PROCESSOR_PID 2>/dev/null; then
    echo "DAG Processor: RUNNING (PID: $DAG_PROCESSOR_PID)"
else
    echo "DAG Processor: FAILED TO START"
fi

echo ""
echo "Airflow is starting up!"
echo "Web UI: http://localhost:8080"
echo "Username: admin"
echo "Password: admin"
echo ""
echo "Logs:"
echo "  API Server: tail -f logs/api_server.log"
echo "  Scheduler: tail -f logs/scheduler.log"
echo "  DAG Processor: tail -f logs/dag_processor.log"
echo ""
echo "To stop Airflow, run: ./stop_airflow.sh"
