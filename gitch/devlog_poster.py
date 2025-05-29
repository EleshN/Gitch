import os
os.environ["WDM_CACHE"] = "false"  # Disable caching in webdriver_manager
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

ITCH_LOGIN_URL = "https://itch.io/login"
ITCH_NEW_DEVLOG_URL = "https://itch.io/dashboard/game/3209624/new-devlog"

def get_driver(headless=False):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
     # This should now download fresh driver
    driver_path = ChromeDriverManager(driver_version="136.0.7103.116").install()
    print("Downloaded driver path:", driver_path)

    return webdriver.Chrome(service=Service(driver_path), options=options)

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
    login_button = driver.find_element(By.CLASS_NAME, 'button')
    print(login_button.text);
    # login_button = WebDriverWait(driver, 5).until(
    #         EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
    #     )

    username_input.send_keys(USERNAME)
    print("entered username")
    password_input.send_keys(PASSWORD)
    print("entered password")
    time.sleep(1)
    login_button.click()
    print("clicked login")

    # Wait for login to complete by checking for redirect
    WebDriverWait(driver, 5).until(
        EC.url_changes(ITCH_LOGIN_URL)
    )
    print("✅ Logged in to itch.io")

def post_devlog(title: str, body: str):
    print("Posting devlog")
    driver = get_driver()

    try:
        login_to_itch(driver)

        print("Logged in")
        driver.get(ITCH_NEW_DEVLOG_URL)
        time.sleep(1)

        update_button = driver.find_element(By.CSS_SELECTOR, 'input[name="post[user_classification]"][value="general_update"]')
        update_button.click()
        print("Clicked update button")

        title_box = driver.find_element(By.NAME, "post[title]")
        title_box.send_keys(title)
        print("Entered title")

        body_box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
        body_box.send_keys(body)
        print("Entered body")

        time.sleep(10)

        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'post[published]'))
        )
        if not checkbox.is_selected():
            checkbox.click()
        print("Checked published box")

        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))
        )
        save_button.click()
        print("Clicked save")

        time.sleep(10)

        print("✅ Devlog posted successfully!")
    except Exception as e:
        print(f"❌ Error during devlog posting: {e}")
    finally:
        driver.quit()
