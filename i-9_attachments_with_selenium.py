import os, sys
import time
import csv
from tqdm import tqdm

from dotenv import load_dotenv

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


# Login Information
load_dotenv()
"""
Sample .env file:
    USERNAME=login@email.com
    PASSWORD=*password123*
    I9_TASK_URL="https://impl.workday.com/wday/authgwy/tenant/login.htmld?redirect=n"
    TEST_WORKER="12345"
"""
user = os.environ.get("USERNAME")
pw = os.environ.get("PASSWORD")
url = os.environ.get("I9_TASK_URL")
test_worker = os.environ.get("TEST_WORKER")

# Selenium Driver Settings
opts = Options()
opts.set_headless(headless=False)  # View Screen
# opts.set_headless(headless=True)  # Headless
driver = Chrome(options=opts)
# driver.maximize_window()
driver.implicitly_wait(10)


# Log in to the tenant
driver.get(url)
select = driver.find_element_by_xpath("//input[@aria-label='Username']")
select.send_keys(user)
select = driver.find_element_by_xpath("//input[@aria-label='Password']")
select.send_keys(pw)
select = driver.find_element_by_xpath("//button[@data-automation-id='goButton']")
select.click()

# Wait for page load
driver.find_element_by_xpath("//span[contains(@title,'Workday page is loaded')]")

# Enter worker to search for
select = driver.find_element_by_xpath("//input[@data-automation-id='searchBox']")
for c in test_worker:
    select.send_keys(c)
    time.sleep(0.1)
select.send_keys(Keys.RETURN)

# Exit
time.sleep(10)  # Make sure downloads are done
driver.quit()
