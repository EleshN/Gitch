from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time

ITCH_LOGIN_URL = "https://itch.io/login"
ITCH_NEW_DEVLOG_URL = "https://itch.io/dashboard/game/3209624/new-devlog"

def get_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    return webdriver.Chrome(options=options)

def login_to_itch(driver):
    load_dotenv()
    USERNAME = os.environ.get("GITCH_ITCH_USERNAME")
    PASSWORD = os.environ.get("GITCH_ITCH_PASSWORD")

    driver.get(ITCH_LOGIN_URL)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
        )

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    login_button.click()

    # Wait for login to complete by checking for redirect
    WebDriverWait(driver, 10).until(
        EC.url_changes(ITCH_LOGIN_URL)
    )
    print("✅ Logged in to itch.io")

def post_devlog(title: str, body: str):
    driver = get_driver()

    try:
        login_to_itch(driver)

        driver.get(ITCH_NEW_DEVLOG_URL)
        time.sleep(3)

        update_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[.//strong[text()='General Update or Announcement']]"))
        )
        update_button.click()

        title_box = driver.find_element(By.NAME, "post[title]")
        title_box.send_keys(title)

        body_box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
        body_box.send_keys(body)

        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))
        )
        save_button.click()

        print("✅ Devlog posted successfully!")
    except Exception as e:
        print(f"❌ Error during devlog posting: {e}")
    finally:
        driver.quit()
