from bs4 import BeautifulSoup
import time
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the environment variable
SBR_WEBDRIVER  = os.getenv("SBR_WEBDRIVER")
print("SBR_WEBDRIVER URL:", SBR_WEBDRIVER)


def scrape_website(website):
    print("launching web browser")

    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:

        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source

        return html

# cleaning the HTML content

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body

    if body_content:
        return str(body_content)
    else:
        return ""


def clean_body_content(body_content):
    soup=BeautifulSoup(body_content, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text(separator='\n')

    cleaned_content ="\n".join(line.strip() for line in text.split() if line.strip())

    return cleaned_content


def split_dom_content(dom_content,max_length=6000):
    return [dom_content[i:i+max_length] for i in range(0,len(dom_content),max_length)]