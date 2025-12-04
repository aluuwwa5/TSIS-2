# airflow_dag.py
from datetime import datetime, timedelta
from pathlib import Path
import logging 
from airflow import DAG
from airflow.operators.python import PythonOperator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import sys
sys.path.insert(0, str(PROJECT_ROOT))

from src.scraper import scrape_tengri_extended
from src.cleaner import clean_tengri
from src.loader import load_to_sqlite



default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="tengrinews_pipeline",
    default_args=default_args,
    description="Daily Tengrinews ETL: scrape → clean → load",
    schedule_interval="@daily",  # no more than once per 24h
    start_date=datetime(2025, 11, 1),
    catchup=False,
    max_active_runs=1,
    tags=["tengrinews", "etl", "selenium"],
) as dag:

    def _scrape(**context):
        logger.info("Running scraper")
    
        scrape_tengri_extended(max_items=300)

    def _clean(**context):
        logger.info("Running cleaner")
        clean_tengri()

    def _load(**context):
        logger.info("Running loader into SQLite")
        load_to_sqlite()

    scrape_task = PythonOperator(
        task_id="scrape_tengrinews",
        python_callable=_scrape,
    )

    clean_task = PythonOperator(
        task_id="clean_tengrinews",
        python_callable=_clean

    )

    load_task = PythonOperator(
        task_id="load_tengrinews_sqlite",
        python_callable=_load,
    )

    scrape_task >> clean_task >> load_task
