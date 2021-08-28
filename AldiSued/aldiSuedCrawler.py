from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

Options.set_headless = True
driver = webdriver.Firefox()
#driver.get("https://www.aldi-sued.de/de/homepage.html")
driver.get("https://www.aldi-sued.de/de/produkte.html")
#assert "Pr0gramm" in driver.title

#xPath = "//a[@href='/de/produkte/produktsortiment/brot-aufstrich-und-cerealien.html']"
xPath = "//a[contains(@href, '/de/produkte/produktsortiment/')]"

elem = driver.find_elements_by_xpath(xPath)
print (len(elem))
for item in elem:
    print (item.get_attribute("href"))
time.sleep(2)
driver.close()

