# src/loader.py
from pathlib import Path
import sqlite3
import logging 
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CLEAN_PATH = DATA_DIR / "clean_tengri.csv"
DB_PATH = DATA_DIR / "output.db"
TABLE_NAME = "news"


def load_to_sqlite():
    logger.info("Loading cleaned data into SQLite")

    if not CLEAN_PATH.exists():
        raise FileNotFoundError(f"Clean file not found: {CLEAN_PATH}")

    df = pd.read_csv(CLEAN_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()


    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            date_raw TEXT,
            date_parsed TEXT,
            image TEXT,
            category TEXT,
            has_image INTEGER
        )
        """
    )
    conn.commit()

    cur.execute(f"DELETE FROM {TABLE_NAME}")
    conn.commit()

    # Convert bools to int for SQLite
    if "has_image" in df.columns:
        df["has_image"] = df["has_image"].astype(int)

    df[["title", "link", "date_raw", "date_parsed", "image", "category", "has_image"]].to_sql(
        TABLE_NAME, conn, if_exists="append", index=False
    )

    conn.commit()
    conn.close()

    logger.info(f"Loaded {len(df)} rows into {DB_PATH} (table {TABLE_NAME})")



if __name__ == "__main__":
    load_to_sqlite()
