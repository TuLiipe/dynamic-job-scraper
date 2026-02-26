import os
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# ----------------------------
# Setup logging
# ----------------------------
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# Create output directory
# ----------------------------
os.makedirs("output", exist_ok=True)

# ----------------------------
# Setup Selenium driver
# ----------------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    url = "https://realpython.github.io/fake-jobs/"
    logging.info("Opening website...")
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    jobs = []

    job_cards = soup.find_all("div", class_="card-content")

    for job in job_cards:
        try:
            title = job.find("h2", class_="title").text.strip()
            company = job.find("h3", class_="company").text.strip()
            location = job.find("p", class_="location").text.strip()

            # Data validation
            if title and company and location:
                jobs.append({
                    "Title": title,
                    "Company": company,
                    "Location": location
                })

        except Exception as e:
            logging.warning(f"Error parsing job: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(jobs)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Save files
    df.to_csv("output/jobs.csv", index=False)
    df.to_json("output/jobs.json", orient="records", indent=4)

    logging.info("Scraping completed successfully.")
    print("Scraping completed successfully!")

except Exception as e:
    logging.error(f"Fatal error: {e}")
    print("Something went wrong. Check scraper.log")

finally:
    driver.quit()