import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def get_urls_google_scraping(search_keywords):
    options = webdriver.ChromeOptions()
    options.headless = True
    # options.add_argument("--headless")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options = options)
    driver.get("https://www.google.com")
    time.sleep(1)
    search_box = driver.find_element(By.NAME, 'q')

    search_box.send_keys(search_keywords )
    print("google search on {}".format(search_keywords))
    search_box.send_keys(Keys.RETURN)
    time.sleep(1)
    base_soup = BeautifulSoup(driver.page_source, "html.parser")
    results = base_soup.find_all("div", {"class": "tF2Cxc"})
    linkedInUrlArr = []
    try:
        for result in results:
            try:
                all_links = result.find_all("a")
                for link in all_links:
                    url = link['href']
                    print(url)
                    if "linkedin.com/in/" in url:
                        url_split = url.split('linkedin.com/in/')[1].split('/')
                    if "linkedin.com/company/" in url:
                        url_split = url.split('linkedin.com/company/')[1].split('/')
                    if len(url_split) == 1:
                        if url not in linkedInUrlArr:
                            linkedInUrlArr.append(url_split)
            except Exception as E:
                print(E,"===1==")
        return linkedInUrlArr[0]
    except Exception as E:
        print(E,"==2===")
        return
    # print("After processing we found out that linked in url is ",linkedInUrlArr[0])