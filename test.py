#!/usr/bin/python3

from selenium import webdriver # Allows you to launch/initialise a browser.
from selenium.webdriver.common.by import By # Allows you to search for things using specific parameters.
from selenium.webdriver.support import expected_conditions as EC # Specify what you are looking for to determine that the webpage has loaded.
from selenium.webdriver.support.ui import WebDriverWait # Allows you to wait for a page to load.

import time
import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

url="file:///home/jcall/vw-scrape/kengarffvw.html"; filename="test.csv"; dealer="TEST"
#url="https://www.vwsouthtowne.com/new-vehicles/atlas/"; filename="vwsouthtowne.csv"; dealer="VWST"
#url="https://www.kengarffvw.com/new-vehicles/atlas/" ; filename="kengarff.csv"; dealer="KGVW"

today = datetime.datetime.now().strftime("%Y-%m-%d")
f = open(filename,'w',encoding='utf-8')

options = webdriver.ChromeOptions()
options.add_argument("incognito")
#mobile_emulation = { "deviceName": "Pixel 2" }
#options.add_experimental_option("mobileEmulation", mobile_emulation)

PROXY = "127.0.0.1:3128"
options.add_argument('--proxy-server=%s' % PROXY)

driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=options)
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')
x = soup.find('table', attrs={"class" : "results_table"})
for row in x.find_all('tr', attrs={"class" : "hidden-xs"}):
    #print(row.find('div', {'class' : 'vinstock'}).get_text(",", strip=True))
    for string in row.find('div', {'class' : 'vinstock'}).stripped_strings:
        print(string)
    print(row.find('div', {'class' : 'price-block our-price real-price'}).get_text(":", strip=True))
    print('Trim: ' + row.find("div",{"class": "vehicle list-view new-vehicle publish"}).get("data-trim"))
    for detail in row.find("div",{"class": "options"}).find_all("span"):
        if detail.string in ["Exterior:", "Interior:"]:
            print(detail.get_text() + detail.find_next_sibling().get_text())
    print('Dealer: ' + dealer + '\n' + 'Date: ' + today)
    #f.write(row.find('div', {'class' : 'vinstock'}).get_text(":", strip=True))
    #print(' ', end="", file=f)
    #f.write(row.find('div', {'class' : 'price-block our-price real-price'}).get_text(":", strip=True))
    #print(' Dealer: ' + dealer + ' Date: ' + today + '\n', end="", file=f)
    print()

    # VIN: 1V2NR2CA8JC588837:Stock #: 81416 Price:$51,525
    # VIN: 1V2AP2CA1JC595746:Stock #: 2W80638 GarffEase Price:$30,115

print("Finished while True: loop")
driver.quit()





#filter_element = driver.find_element_by_xpath("//a[@title='3.6L V6 SEL Premium']")

#raw=driver.page_source
#file = open('raw.source','w',encoding='utf-8')
#file.write(raw)
#file.close()

        # Several terrible ideas to wait for the next page to load before looking for results
        #try:
        #    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "cn-pk-user")))
        #except TimeoutException:
        #    print("Timed out waiting for element to load...")
        #    driver.quit()
        #    quit()

        #driver.until(ExpectedConditions.jsReturnsValue("return document.readyState==\"complete\";"))
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #driver.execute_script("window.scrollTo(0, 0);")
