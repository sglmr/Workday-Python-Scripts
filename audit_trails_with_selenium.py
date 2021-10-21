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
    PROD_URL="https://www.myworkday.com/tenant/d/home.htmld?redirect=n"
    SANDBOX_URL="https://impl.workday.com/wday/authgwy/tenant/login.htmld?redirect=n"
"""
user = os.environ.get("USERNAME")
pw = os.environ.get("PASSWORD")
# url = os.environ.get("PROD_URL")  # Prod
url = os.environ.get("SANDBOX_URL")  # Sandbox


# Config for Script
from_date = "07142021"  # MMDDYYYY
from_time = "120000AM"  # hhmmss(A/P)M
to_date = "10122021"  # MMDDYYYY
to_time = "120000AM"  # hhmmss(A/P)M


# Read objects to audit from CSV file
""" 
Sample CSV File:
    object_name,wid,object_type
    "Report 1","4461c48083e980e0364","report"
    "Integration 1","4461c4ccb510e4565","integration"
"""
csv_file_name = "audit_objects.csv"
csv_file_path = os.path.join(sys.path[0], csv_file_name)

# Read all the lines of the file into a list of dictionaries
wd_objects = list()
with open(csv_file_path) as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        wd_objects.append(row)


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

# Reserve a string variable to store the home URL
home_url = ""

for item in tqdm(wd_objects):
    try:
        # Click on Search Bar
        driver.find_element_by_xpath(
            "//input[@data-automation-id='globalSearchInput']"
        ).click()

        # Save the home_url the first time to go back to if there is an error
        if home_url == "":
            home_url = f"{driver.current_url}"
            pass

        # Wait for pop up to show up
        select = driver.find_element_by_xpath(
            "//div[@data-automation-id='searchInputRecentSearchPopup']"
        )

        # Enter search term
        select = driver.find_element_by_xpath(
            "//input[@data-automation-id='globalSearchInput']"
        )
        select.send_keys("wid:" + item["wid"])
        time.sleep(0.5)
        select.send_keys(Keys.RETURN)

        # Wait for Page to load
        driver.find_element_by_xpath("//*[@id='wd-SearchResultsPanel']")

        # Click on Related Actions
        driver.find_element_by_xpath(
            "//ul/li/img[@data-automation-id='RELATED_TASK_charm']"
        ).click()

        # Click on "Audit Trail"
        driver.find_element_by_xpath(
            "//div[@data-automation-id='relatedActionsItemLabel' and @data-automation-label='Audits']"
        ).click()

        # Wait for "From Box" to load
        # select = driver.find_element_by_xpath("//span[text()='View Audit Trail']")
        select = driver.find_element_by_xpath(
            "//span[@data-automation-id='dateSectionDay']"
        )
        time.sleep(2)

        # Find Date Entry Boxes
        select = driver.find_elements_by_xpath(
            "//input[@data-automation-id='dateWidgetInputBox']"
        )

        # from date
        for c in from_date:
            select[0].send_keys(c)
            time.sleep(0.1)

        # to date
        for c in to_date:
            select[1].send_keys(c)
            time.sleep(0.1)

        # Find Time Entry Boxes
        select = driver.find_elements_by_xpath(
            "//input[@data-automation-id='timeWidgetInputBox']"
        )

        # from time
        for c in from_time:
            select[0].send_keys(c)
            time.sleep(0.1)

        # to time
        for c in to_time:
            select[1].send_keys(c)
            time.sleep(0.1)

        # Click OK
        select = driver.find_element_by_xpath("//button/span[text()='OK']")
        select.click()

        # Click PDF Download
        select = driver.find_element_by_xpath(
            "//div[@title='View printable version (PDF)']"
        )
        select.click()

        # Wait for Export Doc Pop Up
        select = driver.find_element_by_xpath("//h2[text()='Export Document']")
        time.sleep(0.1)

        # Click Download Button
        select = driver.find_element_by_xpath("//button/span[text()='Download']")
        select.click()
        time.sleep(1)

        # Clear Search for Next search term
        driver.find_element_by_xpath(
            "//*[@id='wd-searchInput']/button[@aria-label='clear search']"
        ).click()

    # Handle reporting an error
    except Exception as e:
        tqdm.write(
            f"Error getting audit file for: {item['object_name']} ({item['wid']})"
        )
        tqdm.write(f"{e}")

        # Go back home to restart
        driver.get(home_url)


# Exit
time.sleep(10)  # Make sure downloads are done
driver.quit()
