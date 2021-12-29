import os, sys
import time
from tqdm import tqdm

from dotenv import load_dotenv

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Logging Setup
import logging

logging.basicConfig(
    filename="i-9_attachment.log",
    filemode="w",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)


class EnvVars:
    def __init__(self):
        load_dotenv()
        """
        Sample .env file:
            USERNAME=login@email.com
            PASSWORD=*password123*
            I9_TASK_URL="https://impl.workday.com/tenant/d/task/2997$4717.htmld"
            DOWNLOAD_FOLDER="user/Downloads"
        """
        self.user = os.environ.get("USERNAME")
        self.pw = os.environ.get("PASSWORD")
        self.url = os.environ.get("I9_TASK_URL")
        self.download_folder = os.environ.get("DOWNLOAD_FOLDER")


class WorkerList:
    def __init__(self):
        self.workers = list()

        i9_worker_list_fp = os.path.join(sys.path[0], "i-9_worker_list.txt")

        with open(i9_worker_list_fp) as f:
            for line in f:
                self.workers.append(line.strip())


class Driver:
    def __init__(self):
        # Get environment variables
        self.env = EnvVars()

        # Driver Options
        opts = Options()
        opts.headless = False

        # Initialize Chrome Driver
        self.driver = Chrome(options=opts)
        self.driver.implicitly_wait(10)

        # Document Counter
        self.doc_id = 1

        # Xpath References
        self.attachment_xpath = (
            "//div[@data-automation-id='uploadRowAttachment']/div/div"
        )

    def tenant_login(self):
        self.driver.get(self.env.url)
        select = self.driver.find_element_by_xpath("//input[@aria-label='Username']")
        select.send_keys(self.env.user)
        select = self.driver.find_element_by_xpath("//input[@aria-label='Password']")
        select.send_keys(self.env.pw)
        select = self.driver.find_element_by_xpath(
            "//button[@data-automation-id='goButton']"
        )
        select.click()

        # Wait for the page to load
        self.page_load_wait()

    def page_load_wait(self):
        self.driver.find_element_by_xpath(
            "//span[contains(@title,'Workday page is loaded')]"
        )

    def find_worker_i9(self, worker):
        # Search for a worker in the View Form I-9 for Worker Task

        self.worker = worker

        # Go to the view Form I-9 for Worker Task
        self.driver.get(self.env.url)
        self.page_load_wait()

        # Find the search Box
        select = self.driver.find_element_by_id("56$202554--uid4-input")
        time.sleep(1)

        # Type in employee ID
        for c in worker:
            select.send_keys(c)
            time.sleep(0.1)
        select.send_keys(Keys.RETURN)

        # Click Okay
        self.driver.find_element_by_xpath("//div[@data-automation-id='selectedItem']")
        self.driver.find_element_by_xpath("//button/span[@title='OK']").click()

        # Wait for the page to load
        self.page_load_wait()

        # Check and handle multiple I9s
        self.multi_i9_handler()

    def multi_i9_handler(self):
        multi_i9_xpath = "//div[@data-automation-id='menuItem']//div[@data-automation-id='promptOption']"

        # Search for attachments and leave if found
        if len(self.driver.find_elements_by_xpath(self.attachment_xpath)) > 0:
            logging.info(f"{self.worker} - Found Attachments")
            return True

        # If there are multiple I-9's, pick the first one
        elif len(self.driver.find_elements_by_xpath(multi_i9_xpath)) > 1:
            self.driver.find_elements_by_xpath(multi_i9_xpath)[0].click()
            logging.info(f"{self.worker} - Found multiple i9's")
            self.page_load_wait()
            return True

        # Something Unexpected Happened
        return False

    def download_attachments(self):
        downloads = 0

        # Find each attachment and download
        for element in self.driver.find_elements_by_xpath(self.attachment_xpath):
            try:
                # Right click the element to get the URL to download
                action = ActionChains(self.driver)
                action.move_to_element(element).perform()  # Move to element
                action.context_click(
                    on_element=element
                ).perform()  # Right click Element
                time.sleep(1)

                # File name & Download doc URL
                file_name = element.text
                attachment_url = self.driver.find_element_by_xpath(
                    "//div[@data-automation-id='copyUrl']"
                ).get_attribute("data-clipboard-text")

                # Download File
                self.driver.get(attachment_url)

                # Wait until file is downloaded
                path_to_file = os.path.join(self.env.download_folder, file_name)
                while os.path.exists(path_to_file) is False:
                    time.sleep(1)

                # Rename File
                path_to_new_file = os.path.join(
                    self.env.download_folder, f"{self.worker}-{self.doc_id}-{file_name}"
                )
                os.rename(path_to_file, path_to_new_file)

                # Increment download count
                downloads += 1

                # Increment Doc ID
                self.doc_id += 1
            except Exception as e:
                logging.error(
                    f"{mydriver.worker} - Error downloading attachment {file_name} for - {e}"
                )
                continue

        return downloads


def main():

    # Get Environment Variables
    mydriver = Driver()

    # Read off a list of workers from a text file
    worker_list = WorkerList().workers

    # Log into the tenant
    try:
        mydriver.tenant_login()
    except Exception as e:
        logging.critical(f"Login - Could not log into the tenant. - {e}")
        # TODO: Exit

    # Grab docs for every worker
    for worker in tqdm(worker_list):

        # Load I-9 Worker search Page:
        try:
            mydriver.find_worker_i9(worker)
        except Exception as e:
            logging.error(f"{mydriver.worker} - Error getting to i-9 page - {e}")

        # Download files
        download_count = mydriver.download_attachments()
        logging.info(f"{mydriver.worker} - downloaded {download_count} attachments")

    # Exit
    mydriver.driver.quit()


if __name__ == "__main__":
    main()
