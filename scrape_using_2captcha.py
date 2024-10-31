'''
here we are trying to use 2captcha to solve captcha
'''
import os
import time
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("5ce463f3eaf59cf2d6a9f7fda8168fc2")  # Your 2Captcha API Key

def detect_captcha(driver):
    try:
        # Check for reCAPTCHA v2
        driver.find_element(By.CLASS_NAME, "g-recaptcha")
        return "recaptcha_v2"
    except:
        pass

    try:
        # Check for hCaptcha
        driver.find_element(By.CLASS_NAME, "h-captcha")
        return "hcaptcha"
    except:
        pass

    try:
        # Check for reCAPTCHA v3 (often has "grecaptcha-badge" class)
        driver.find_element(By.CLASS_NAME, "grecaptcha-badge")
        return "recaptcha_v3"
    except:
        pass

    try:
        # Check for image CAPTCHA
        if driver.find_elements(By.CSS_SELECTOR, "img[src*='captcha']"):
            return "image_captcha"
    except:
        pass

    # Check for text-based CAPTCHA
    if "Type the characters you see in this image:" in driver.page_source or "Type the characters" in driver.page_source:
        return "text_captcha"

    return "unknown"
def solve_captcha(captcha_type, site_key, url):
    api_url = "http://2captcha.com/in.php"
    data = {
        "key": API_KEY,
        "method": captcha_type,
        "googlekey": site_key,
        "pageurl": url,
        "json": 1
    }
    response = requests.post(api_url, data=data)
    request_id = response.json().get("request")

    # Check if the CAPTCHA solving request was successful
    if response.json().get("status") != 1:
        raise Exception("Error submitting CAPTCHA solving request.")

    # Poll for CAPTCHA solution
    result_url = f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={request_id}&json=1"
    while True:
        result_response = requests.get(result_url)
        if result_response.json().get("status") == 1:
            return result_response.json().get("request")
        time.sleep(5)

def scrape_website(website):
    # Initialize the WebDriver
    driver = webdriver.Chrome()
    driver.get(website)

    # Detect the CAPTCHA type
    captcha_type = detect_captcha(driver)
    if captcha_type == "unknown":
        print("Unknown CAPTCHA type. Exiting...")
        driver.quit()
        return

    # Get the site key and solve the CAPTCHA
    if captcha_type in ["recaptcha_v2", "hcaptcha", "recaptcha_v3","image_captcha","text_captcha"]:
        site_key = driver.find_element(By.CLASS_NAME, "g-recaptcha").get_attribute("data-sitekey")
        captcha_response = solve_captcha(captcha_type, site_key, driver.current_url)

        # Execute JavaScript to fill the CAPTCHA response
        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{captcha_response}';")
        driver.execute_script("onCaptchaCompleted();")  # Trigger any site-specific callback if needed

        # Submit the form
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit_button_id"))
        )
        submit_button.click()

        print("CAPTCHA solved and form submitted!")

    try:
            # Wait for a success message or element that appears upon successful form submission
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "success_message_id"))
            )
            print("Form submitted successfully! Success message found.")
    except:
        print("Failed to submit the form or solve the CAPTCHA.")
        print("Current page HTML after submission attempt:")
        print(driver.page_source)  # Print page source if failed

    time.sleep(5)  # Keep the browser open for a while to see the result
    driver.quit()

    time.sleep(5)  # Keep the browser open for a while to see the result
    driver.quit()


