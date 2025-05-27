from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import pickle

COOKIE_PATH = os.path.expanduser("~/.gitch/cookies.pkl")
ITCH_NEW_DEVLOG_URL = "https://itch.io/devlog/new"

def get_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    return webdriver.Chrome(options=options)

def save_cookies(driver):
    with open(COOKIE_PATH, "wb") as f:
        pickle.dump(driver.get_cookies(), f)

def load_cookies(driver):
    if not os.path.exists(COOKIE_PATH):
        return False
    with open(COOKIE_PATH, "rb") as f:
        cookies = pickle.load(f)
    driver.get("https://itch.io")  # Must visit domain before adding cookies
    for cookie in cookies:
        driver.add_cookie(cookie)
    return True

def manual_login_flow():
    driver = get_driver()
    driver.get("https://itch.io/login")
    print("Please log in manually. Close the browser when done.")
    while True:
        input("Press Enter here after you've logged in and closed the browser...")
        try:
            save_cookies(driver)
            break
        except Exception as e:
            print(f"Failed to save cookies: {e}")
    driver.quit()

def post_devlog(title: str, body: str):
    driver = get_driver()
    logged_in = load_cookies(driver)

    if not logged_in:
        print("You need to log in manually first.")
        manual_login_flow()
        driver = get_driver()
        load_cookies(driver)

    driver.get(ITCH_NEW_DEVLOG_URL)
    time.sleep(3)

    try:
        # Fill in title
        title_box = driver.find_element(By.NAME, "devlog[title]")
        title_box.send_keys(title)

        # Fill in body (WYSIWYG editor uses iframe)
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe.wysiwyg"))
        body_box = driver.find_element(By.CSS_SELECTOR, "body")
        body_box.send_keys(body)
        driver.switch_to.default_content()

        # Click publish
        publish_button = driver.find_element(By.NAME, "commit")
        publish_button.click()

        print("Devlog posted!")
    except Exception as e:
        print(f"Error during posting: {e}")
    finally:
        driver.quit()
