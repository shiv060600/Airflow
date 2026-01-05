# Docker DAGs Folder

This folder contains Docker-compatible versions of your Airflow DAGs.

## Purpose

- **`airflow/dags/`** - Original DAGs for WSL Airflow (uses PowerShell)
- **`airflow/docker_dags/`** - Docker-compatible DAGs (uses bash)

This separation allows you to:
- Keep your WSL Airflow running with original DAGs
- Test Docker Airflow with Docker-compatible DAGs
- Switch between them without conflicts

## Changes Made

All DAGs have been updated to replace PowerShell commands with bash commands:

**Before (WSL):**
```python
bash_command='powershell.exe -Command "cd H:\\...; conda activate reportingenv; python -m src.run_daily"'
```

**After (Docker):**
```python
bash_command='cd /opt/airflow/reporting_pipeline && python -m src.run_daily'
```

## DAGs Included

1. `run_daily_dag.py` - Daily mapping upload and reports
2. `run_weekly_dag.py` - Weekly backorders
3. `run_monthly_dag.py` - Monthly sales upload
4. `run_pgc_pguk_dag.py` - PGC/PGUK full report
5. `run_daily_remarks_report.py` - Daily remarks report
6. `send_reminder_dag.py` - Monthly sales reminder
7. `send_backorder_reminder.py` - Weekly backorders reminder
8. `run_daily_remarks_report_reminder.py` - Daily remarks reminder

## How It Works

When Docker starts:
- Mounts `airflow/docker_dags/` to `/opt/airflow/dags/` in container
- Airflow reads DAGs from this mounted folder
- DAGs execute using bash commands (no PowerShell/Conda needed)

## Testing

1. Start Docker: `cd docker && docker-compose up -d`
2. Access UI: http://localhost:8080
3. Verify DAGs appear (should see all 8 DAGs)
4. Test a DAG run to ensure bash commands work

## Notes

- All schedules and configurations match original DAGs
- Only the bash_command has changed
- Your REPORTING_PIPELINE code runs unchanged

