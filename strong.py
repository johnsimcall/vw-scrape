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

url="https://www.strongvw.com/new-volkswagen-atlas-salt-lake-city-ut"; filename="STNG-"; dealer="STNG"

today = datetime.datetime.now().strftime("%Y-%m-%d")
filename = "ALL.csv"
###filename += today + ".csv"
f = open(filename,'a',encoding='utf-8')

def setup():
    global f
    f = open(filename,'a',encoding='utf-8')
    options = webdriver.ChromeOptions()
    options.add_argument("incognito")
    global driver
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=options)
    driver.get(url)

def scrape():
    soup = BeautifulSoup(driver.page_source, 'lxml')
    x = soup.find('div', attrs={"class" : "vehicle-page", "data-page" : str(pagenum)})
    for row in x.find_all('div', attrs={"class" : "vehicle"}):
        print('VIN:' + row.find('meta', {'itemprop' : 'serialNumber'}).get("content"), end=":", file=f)
        print('Stock #:' + row.get("id"), end=":", file=f)
        try:
            print('Price:' + row.find('meta', {'itemprop' : 'price'}).get("content"), end=":", file=f)
        except AttributeError:
            print('Price:     ', end=":", file=f)
        print('Dealer:' + dealer + ':Date:' + today, end=":", file=f)
        print('Trim:' + row.find('meta', {'itemprop': 'name'}).get("content"), end=":", file=f)
        print('Color:' + row.find('meta', {'itemprop': 'color'}).get("content") + ':', file=f)

setup()
pagenum = 1
print("Using " + filename + " for " + url)
print("Scraping page " + str(pagenum)) ; scrape()

while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        xpath='//div[@data-page="' + str(pagenum + 1) + '"]'
        next_page_element = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        print("Reached last page, quitting...")
        break
    else:
        pagenum += 1
        print("Going to page " + str(pagenum))
        time.sleep(4)
        scrape()
print("Finished while True: loop")

driver.quit()
f.close()

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://seleniumhq.github.io/selenium/docs/api/py/api.html
# https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72
# https://medium.freecodecamp.org/better-web-scraping-in-python-with-selenium-beautiful-soup-and-pandas-d6390592e251
# sudo dnf install chromedriver python3-selenium python3-beautifulsoup4
#
#mobile_emulation = { "deviceName": "Pixel 2" }
#options.add_experimental_option("mobileEmulation", mobile_emulation)



# Can I just grab this array?
#//<![CDATA[
#var daObjects = daObjects || {}; daObjects['vehicleListDaObjects'] = {"25306217":{"VUID":"25306217","IsNew":1,"YearFrom":"2018","YearTo":"2018","Make":"Volkswagen","Model":"Atlas","Trim":"SE 4Motion","StandardBody":"4 Door Wagon","PriceFrom":"34030","PriceTo":"34030"},"25654114":{"VUID":"25654114","IsNew":1,"YearFrom":"2018","YearTo":"2018","Make":"Volkswagen","Model":"Atlas","Trim":"SE 4Motion","StandardBody":"4 Door Wagon","PriceFrom":"34030","PriceTo":"34030"}};
#//]]>

#{
#  "25306217": {
#    "VUID": "25306217",
#    "IsNew": 1,
#    "YearFrom": "2018",
#    "YearTo": "2018",
#    "Make": "Volkswagen",
#    "Model": "Atlas",
#    "Trim": "SE 4Motion",
#    "StandardBody": "4 Door Wagon",
#    "PriceFrom": "34030",
#    "PriceTo": "34030"
#  },
#  "25654114": {
#    "VUID": "25654114",
#    "IsNew": 1,
#    "YearFrom": "2018",
#    "YearTo": "2018",
#    "Make": "Volkswagen",
#    "Model": "Atlas",
#    "Trim": "SE 4Motion",
#    "StandardBody": "4 Door Wagon",
#    "PriceFrom": "34030",
#    "PriceTo": "34030"
#  }
#}
