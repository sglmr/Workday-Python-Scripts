import os, sys
import time
from tqdm import tqdm

from dotenv import load_dotenv

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# Login Information
load_dotenv()
"""
Sample .env file:
    USERNAME=login@email.com
    PASSWORD=*password123*
    I9_TASK_URL="https://impl.workday.com/wday/authgwy/tenant/login.htmld?redirect=n"
    DOWNLOAD_FOLDER="user/Downloads"
"""
user = os.environ.get("USERNAME")
pw = os.environ.get("PASSWORD")
url = os.environ.get("I9_TASK_URL")
download_folder = os.environ.get("DOWNLOAD_FOLDER")

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

worker_list = []

# Grab docs for every worker
for worker in tqdm(worker_list):

    # Wait for page load
    driver.find_element_by_xpath("//span[contains(@title,'Workday page is loaded')]")

    # Enter worker to search for
    try:
        select = driver.find_element_by_id(
            "56$202554--uid4-input"
        )  # input box to search for worker
        time.sleep(1)
        for c in worker:  # Type in employee ID
            select.send_keys(c)
            time.sleep(0.1)
        select.send_keys(Keys.RETURN)
        driver.find_element_by_xpath("//div[@data-automation-id='selectedItem']")
        driver.find_element_by_xpath("//button/span[@title='OK']").click()
    except Exception as e:
        tqdm.write(f"Error finding I9 for worker: {worker}.")

    # Download files
    driver.find_element_by_xpath("//span[contains(@title,'Workday page is loaded')]")
    doc_id = 1
    xpath = "//div[@data-automation-id='uploadRowAttachment']/div/div"
    try:
        for element in driver.find_elements_by_xpath(xpath):
            # Right click the element to get the URL to download
            action = ActionChains(driver)
            action.move_to_element(element).perform()  # Move to element
            action.context_click(on_element=element).perform()  # Right click Element
            time.sleep(1)

            # File name & Download doc URL
            file_name = element.text
            copy_url = driver.find_element_by_xpath(
                "//div[@data-automation-id='copyUrl']"
            ).get_attribute("data-clipboard-text")

            # Download File
            driver.get(copy_url)

            # Wait until file is downloaded
            path_to_file = os.path.join(download_folder, file_name)
            while os.path.exists(path_to_file) is False:
                time.sleep(0.1)

            # Rename File
            path_to_new_file = os.path.join(
                download_folder, f"{worker}-{doc_id}-{file_name}"
            )
            os.rename(path_to_file, path_to_new_file)

            # Increment Doc ID
            doc_id += 1
    except Exception as e:
        tqdm.write(f"Error downloading I9 attachments for: {worker}.")
        tqdm.write(f"{e}")
        continue

    # Go back to the task for the next worker.
    driver.get(url)

# Exit
driver.quit()
