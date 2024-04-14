from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import os

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    webdriver_service = Service(os.environ.get("CHROMEDRIVER_PATH"))
    return webdriver.Chrome(options=chrome_options, service=webdriver_service, )

def get_download_url(driver, track_url):
    driver.get("https://spotifymate.com/")
    input_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "url"))
    )
    input_box.send_keys(track_url)
    
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="send"]'))
    )
    submit_button.click()
    
    try:
        download_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='abuttons']/a"))
        )
        download_url = download_button.get_attribute("href")
        return download_url
    except TimeoutException:
        print("Download button not found.")
        return None
    finally:
        driver.quit()

def main(event, contect):
    print("Starting...")
    track_url = "https://open.spotify.com/track/4j9F9K3pSOzMSqyCk6LBXq?si=7652a765f1904691"
    driver = setup_driver()
    download_url = get_download_url(driver, track_url)
    if download_url:
        return {"statusCode": 200, "body": download_url}
    else:
        return {"statusCode": 500, "body": "Failed to retrieve download URL."}
