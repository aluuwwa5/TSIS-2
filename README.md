# TengriNews Data Pipeline  
A complete mini data pipeline that dinamically extracts news articles from TengriNews, cleans the data, stores it in SQLite, and automates this workflow using Apache Airflow.

---

## 📌 Project Overview

This project shows a full ETL pipeline:

1. **Scraping** dynamic content from the TengriNews, which load articles dynamically on scroll.
2. **Cleaning & preprocessing** scraped data.
3. **Loading** processed data into a SQLite database.
4. **Automating** the workflow using Apache Airflow (runs once per day).

The final dataset contains at least **100 cleaned news articles** with fields:
- `id`
- `title`
- `link`
- `date`
- `category`
- `has_image`

---

## Website Description
📎 https://tengrinews.kz/

TengriNews is a popular Kazakh news website.  
Tengrinews category pages dynamically load new news via AJAX when the user scrolls down the page. Because of this, the data does not appear in HTML immediately, and regular requests are not suitable — you need Selenium, which can execute JavaScript.

---

## How to run scraping
We can run scraping without Airflow, directly via Python.

```python src/scraper.py```

This saves raw scraped data to:

```data/raw.json```


## How to run Airflow

1) Initialize Airflow
   
```airflow db init```

2) Create User

 ```airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```


3) Run Scheduler:

```airflow scheduler```

4) In another WSL tab run Webserver:

```airflow webserver -p 8080```

5) Open in browser:

``` http://localhost:8080```

## Expected Output

SQLite Table: 
<img width="1441" height="233" alt="image" src="https://github.com/user-attachments/assets/da9e224a-8934-42f9-ab60-b8e9c2b88a9e" /> <img width="182" height="134" alt="image" src="https://github.com/user-attachments/assets/ab8b7c97-007d-4cdc-a2e3-e38acb63db74" />





