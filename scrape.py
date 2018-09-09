#!/usr/bin/python3
# https://seleniumhq.github.io/selenium/docs/api/py/api.html
# https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72
# https://medium.freecodecamp.org/better-web-scraping-in-python-with-selenium-beautiful-soup-and-pandas-d6390592e251
# sudo dnf install chromedriver python3-selenium python3-beautifulsoup4

from selenium import webdriver # Allows you to launch/initialise a browser.
from selenium.webdriver.common.by import By # Allows you to search for things using specific parameters.
from selenium.webdriver.support import expected_conditions as EC # Specify what you are looking for to determine that the webpage has loaded.
from selenium.webdriver.support.ui import WebDriverWait # Allows you to wait for a page to load.

import time
import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

url="https://www.kengarffvw.com/new-vehicles/atlas/" ; filename="TEST-"; dealer="TEST"
#url="https://www.vwsouthtowne.com/new-vehicles/atlas/"; filename="TEST-"; dealer="TEST"

#url="https://www.vwsouthtowne.com/new-vehicles/atlas/"; filename="VWST-"; dealer="VWST"
#url="https://www.kengarffvw.com/new-vehicles/atlas/" ; filename="KGVW-"; dealer="KGVW"

today = datetime.datetime.now().strftime("%Y-%m-%d")
filename += today + ".csv"
f = open(filename,'w',encoding='utf-8')

options = webdriver.ChromeOptions()
options.add_argument("incognito")
#mobile_emulation = { "deviceName": "Pixel 2" }
#options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=options)
driver.get(url)

def scrape():
    soup = BeautifulSoup(driver.page_source, 'lxml')
    x = soup.find('table', attrs={"class" : "results_table"})
    for row in x.find_all('tr', attrs={"class" : "hidden-xs"}):
        print(row.find('div', {'class' : 'vinstock'}).get_text(":", strip=True), end=":", file=f)
        print(row.find('div', {'class' : 'price-block our-price real-price'}).get_text(":", strip=True), end=":", file=f)
        print('Dealer:' + dealer + ':Date:' + today, end=":", file=f)
        for detail in row.find("div",{"class": "options"}).find_all("span"):
            if detail.string in ["Exterior:", "Interior:"]:
                print(detail.get_text() + detail.find_next_sibling().get_text(), end=":", file=f)
        trim = row.find("div",{"class": "vehicle list-view new-vehicle publish"}).get("data-trim")
        print('Trim:' + trim, file=f)

scrape()

while True:
    try:
        next_page_element = driver.find_element_by_xpath("//a[@class='next']")
    except NoSuchElementException:
        #print("Reached last page, quitting...")
        f.close()
        driver.quit()
        quit()
    else:
        #print("Going to next page...")
        next_page_element.click()
        time.sleep(2)
        scrape()

print("Finished while True: loop")
driver.quit()
f.close()
