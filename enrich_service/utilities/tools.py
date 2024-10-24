import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Regular expression for basic email validation

def is_valid_email(payload):
    response_data = {"successful":[],"unsuccessful":[]}
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    for item in payload:
        if item["mapping"]["tableName"] == "Profile":
            if not re.match(pattern, item["query"]["context"]["emailAddress"]) is not None and item["query"]["context"]["emailAddress"] :
                item["mapping"]["error"]="email is not valid"
                response_data["unsuccessful"].append(item["mapping"])

    return response_data
    

def driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options = options)
    return driver

   