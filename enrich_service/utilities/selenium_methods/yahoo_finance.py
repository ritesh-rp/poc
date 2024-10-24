from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import re


def extract_last_value_within_parentheses(text):
    pattern = r'\((.*?)\)$'
    # Search for the pattern in the text
    match = re.search(pattern, text)
    # Extract the last value within parentheses
    if match:
        result = match.group(1)
        return result
    else:
        return None


def  scrap_yahooFinance(company_name):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--headless")
    driver = webdriver.Chrome(options = options)

    url = "https://finance.yahoo.com/"
    driver.get(url)    

    search_field = driver.find_element(By.ID, 'yfin-usr-qry')
    search_field.send_keys(company_name)
    driver.find_element(By.ID, 'header-desktop-search-button').click()
    time.sleep(2)
    current_url = driver.current_url
    # give error if redirected to google
    if "finance.yahoo.com/quote" in current_url:

        # Scraping SUmmary Page
        summary_html = BeautifulSoup(driver.page_source, "html.parser")
        company_header = summary_html.find("div", id="quote-header-info")
        ticker = extract_last_value_within_parentheses(company_header.find('h1').text)
        

        # Scraping FInancial data
        driver.find_element(By.LINK_TEXT, "Financials").click()
        time.sleep(10)
        financial_html = BeautifulSoup(driver.page_source, "html.parser")
        first_revenue_div = financial_html.find_all(attrs={"data-test": "fin-row"})[0]
        try:
            revenue = first_revenue_div.find_all("span")[1].string
            lowest_revenue = first_revenue_div.find_all("span")[-1].string
        except Exception as E:
            print(E,"error")
            revenue, lowest_revenue ='', ''
        
        # Scraping Company Profile data
        driver.find_element(By.LINK_TEXT, "Profile").click()
        # Find heading with text Industry 
        try:
            driver.find_element(By.LINK_TEXT, "Profile").click()
            profile_html = BeautifulSoup(driver.page_source, "html.parser")
            industryspan = profile_html.find("span", string="Industry")
            industry =  industryspan.find_next_siblings("span")[0].string
        except Exception as E:
            print(E,"errorr")
            industry=""

        telephone_tags = profile_html.find_all("a",  class_ = "C($linkColor)")
        company_phone =""
        for tel in telephone_tags:
            if "tel:" in str(tel):
                company_phone  = tel.string
        return{"ticker":ticker,"revenue":revenue.replace(",","")+"000","revenue_range":lowest_revenue +" - " +revenue,"industry":[industry],"company_phone":company_phone }
    else:
        print("company not on yahoo finance")
        return {"ticker":"","revenue":"","revenue_range":"","industry":"","company_phone":'' }


