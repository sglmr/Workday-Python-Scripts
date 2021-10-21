import getpass
import requests
from urllib.parse import quote


# Prompt Integration System User (ISU) Credentials
username = input("ISU Username: ")
password = getpass.getpass("ISU Password: ")

tenant = input("WD Tenant: ")


test_email = "test@email.com"
while test_email:
    # Request data for a single employee with an email addres specified in the vairable "test_email"
    test_email = input("\nEnter an Email Address: ")

    if test_email:
        email = quote(test_email, safe="")  # % escape special characters in the email

        # Sandbox
        url = f"https://wd2-impl-services1.workday.com/ccx/service/customreport2/{tenant}/rpt_owner/rpt_name?email={email}&format=json"
        # Production
        # url = f'https://services1.myworkday.com/ccx/service/customreport2/{tenant}/rpt_owner/rpt_name?email={email}&format=json'

        # Get the JSON response from Workday using Basic Auth
        wd_response = requests.get(url, auth=(username, password))

        # Print the result
        print(f"{wd_response.text}")
        print(f"{wd_response.elapsed.microseconds / 1000} ms")
