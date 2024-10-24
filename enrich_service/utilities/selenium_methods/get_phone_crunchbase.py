import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def get_contact_from_crunchbase(search_keywords):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--headless")
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options = options)
    driver.get("https://www.google.com")
    time.sleep(1)
    search_box = driver.find_element(By.NAME, 'q')

    search_box.send_keys(search_keywords + " crunchbase")
    search_box.send_keys(Keys.RETURN)
    time.sleep(1)
    base_soup = BeautifulSoup(driver.page_source, "html.parser")
    results = base_soup.find_all("div", {"class": "tF2Cxc"})
    