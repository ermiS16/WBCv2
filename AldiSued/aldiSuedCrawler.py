from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

option = Options()

#activate if browser shall be headless
#option.add_argument('--headless')

driver = webdriver.Firefox(options=option)

#driver.get("https://www.aldi-sued.de/de/homepage.html")
driver.get("https://www.aldi-sued.de/de/produkte.html")

#xPath = "//a[@href='/de/produkte/produktsortiment/brot-aufstrich-und-cerealien.html']"
xPath = "//a[contains(@href, '/de/produkte/produktsortiment/')]"

elem = driver.find_elements_by_xpath(xPath)
url_list = []
print (len(elem))
for item in elem:
    print (item.get_attribute("href"))
    url_list.append(item.get_attribute("href"))

next_page_url = url_list[0]
driver.get(str(next_page_url))

time.sleep(2)
driver.close()

