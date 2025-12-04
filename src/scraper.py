
import time
import csv
import logging
from datetime import datetime, timedelta
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_PATH = DATA_DIR / "raw_tengri.csv"


def get_driver():
    """ headless Chrome for WSL/Airflow"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def scrape_page(driver, url, news_list, seen):
    """Parse single Tengrinews page into news_list."""
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        cards = driver.find_elements(By.CSS_SELECTOR, "div.content_main_item")

        page_count = 0
        for card in cards:
            try:
                link_element = card.find_element(By.TAG_NAME, "a")
                link = link_element.get_attribute("href")

                if link in seen:
                    continue
                seen.add(link)

                
                try:
                    title_span = card.find_element(By.CSS_SELECTOR, "span.content_main_item_title")
                    title = title_span.text.strip()
                except Exception:
                    title = card.text.split('\n')[0].strip()

                if not title:
                    continue

                
                
                lines = card.text.strip().split('\n')
                date_str = lines[-1].strip() if len(lines) > 1 else "N/A"

                img = None
                try:
                    img_element = card.find_element(By.TAG_NAME, "img")
                    img = img_element.get_attribute("src") or img_element.get_attribute("srcset")
                    if img and ',' in img:
                        img = img.split(',')[0].split(' ')[0]
                except Exception:
                    pass

                if not link.startswith("http"):
                    link = "https://tengrinews.kz" + link

                
                category = "other"
                categories_map = {
                    "/kazakhstan_news/": "kazakhstan",
                    "/world_news/": "world",
                    "/crime/": "crime",
                    "/events/": "events",
                    "/internet/": "internet",
                    "/science/": "science",
                    "/market/": "market",
                    "/sport/": "sport",
                    "/culture/": "culture",
                }

                for k, v in categories_map.items():
                    if k in link:
                        category = v
                        break

                news_list.append(
                    {
                        "title": title,
                        "link": link,
                        "date_raw": date_str,
                        "image": img or "N/A",
                        "category": category,
                    }
                )
                page_count += 1

            except Exception as e:
                logger.warning(f"Error parsing card: {e}")
                continue

        return page_count

    except Exception as e:
        logger.error(f"Error on page {url}: {e}")
        return 0


def scrape_tengri_extended(max_items=300):
    """scraping across several sections and archive pages."""
    logger.info("scraping Tengrinews...")
    

    driver = get_driver()

    news_list = []
    seen = set()

    try:
        sections = [
            ("Все новости", "https://tengrinews.kz/news/"),
            ("Казахстан", "https://tengrinews.kz/kazakhstan_news/"),
            ("Мир", "https://tengrinews.kz/world_news/"),
            ("События", "https://tengrinews.kz/events/"),
            ("Криминал", "https://tengrinews.kz/crime/"),
            ("Интернет", "https://tengrinews.kz/internet/"),
            ("Рынок", "https://tengrinews.kz/market/"),
            ("Наука", "https://tengrinews.kz/science/"),
            ("Спорт", "https://tengrinews.kz/sport/"),
            ("Культура", "https://tengrinews.kz/culture/"),
        ]

        for name, url in sections:
            logger.info(f"Section: {name} → {url}")
            count = scrape_page(driver, url, news_list, seen)
            logger.info(f"  Added: {count}, total: {len(news_list)}")

            if len(news_list) >= max_items:
                break

            time.sleep(2)

        if len(news_list) < 200:
            print("Parsing archive for last 7 days...")
            for i in range(7):
                date = datetime.now() - timedelta(days=i)
                date_str = date.strftime("%Y/%m/%d")
                archive_url = f"https://tengrinews.kz/news/{date_str}/"

                logger.info(f"Archive: {archive_url}")
                count = scrape_page(driver, archive_url, news_list, seen)
                logger.info(f"  Added: {count}, total: {len(news_list)}")

                if len(news_list) >= max_items:
                    break

                time.sleep(1)

    finally:
        driver.quit()

    # Save raw data to CSV
    if news_list:
        with RAW_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["title", "link", "date_raw", "image", "category"]
            )
            writer.writeheader()
            writer.writerows(news_list)

        logger.info(f"✓ Saved {len(news_list)} records to {RAW_PATH}")
    else:
        logger.warning("✗ No news scraped")


if __name__ == "__main__":
    scrape_tengri_extended()
