# Data Pipeline for Tengrinews.kz

## Website Description:
[Tengrinews](https://tengrinews.kz/) is a Kazakhstani online news portal and media site, one of the largest information resources in the country
Tengrinews.kz publishes content such as:
- News about Kazakhstan and the world (politics, economy, society, incidents)
- Topics such as business, science and technology, health, and education
- Culture, entertainment, sports, and travel
- Author’s articles, opinions, blogs, analytical reviews
- Multimedia content: photos, videos, interviews, special projects

This script scrapes news from various sections (e.g., Kazakhstan, World, Crime, Science, and others)
Tengrinews category pages dynamically load new news via AJAX when the user scrolls down the page. Because of this, the data does not appear in HTML immediately, and regular requests are not suitable — you need Selenium, which can execute JavaScript.


##  Project Overview

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


## How to Run Scraping

To scrape the latest news data from Tengrinews.kz, we can run the scraper manually or automate it using Apache Airflow.

### 1. Install Dependencies

Before running the scraper, make sure you have installed all necessary dependencies. You can do this by running:

```bash
pip install -r requirements.txt
```


We can also run scraping without Airflow, directly via Python.

```python src/scraper.py```

This saves raw scraped data to:

```data/raw.json```



### Run the Scraper Manually

If you prefer to run the scraper manually to collect the latest data from Tengrinews.kz, follow these steps:

1. Open a terminal and navigate to the project directory.
2. Ensure you have all dependencies installed by running:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the scraper script with the following command:

    ```bash
    python src/scraper.py
    ```

#### What this does:
- The script opens a headless browser (via Selenium) to scrape data from various sections of the Tengrinews website (e.g., Kazakhstan, World, Crime, Science).
- It collects news articles and saves them in a CSV file: `data/raw_tengri.csv`.
- The scraper handles dynamic content loading, ensuring that only the most up-to-date articles are captured.

Once the script finishes running, you can check the `data/raw_tengri.csv` file for the raw scraped data.


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




