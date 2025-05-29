import os
os.environ["WDM_CACHE"] = "false"

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver_path = ChromeDriverManager(driver_version="136.0.7103.116").install()
print("Downloaded driver path:", driver_path)

driver = webdriver.Chrome(service=Service(driver_path), options=options)
print("ChromeDriver version:", driver.capabilities["chrome"]["chromedriverVersion"])

driver.quit()
