import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import os
os.makedirs("output", exist_ok=True)
# Setup driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://realpython.github.io/fake-jobs/"
driver.get(url)
time.sleep(3)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

jobs = []

for job in soup.find_all("div", class_="card-content"):
    title = job.find("h2", class_="title").text.strip()
    company = job.find("h3", class_="company").text.strip()
    location = job.find("p", class_="location").text.strip()

    jobs.append({
        "Title": title,
        "Company": company,
        "Location": location
    })

# Convert to DataFrame
df = pd.DataFrame(jobs)

# Save CSV
df.to_csv("output/jobs.csv", index=False)

# Save JSON
df.to_json("output/jobs.json", orient="records", indent=4)

print("Scraping completed successfully!")