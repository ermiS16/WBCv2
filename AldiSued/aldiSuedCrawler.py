from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


import time
import datetime
import sys



def throwException():
    print("Exception", sys.exc_info()[0], "occured.")
    print("Detail:", sys.exc_info()[1])


def generateFileName(extension):

    dest = "../Output/AldiSued/"
    date = datetime.datetime.now()
    #currentDate = date.strftime("%Y%m%d%H%M%S%f")
    currentDate = date.strftime("%Y%m%d%H%M%S")

    filename = dest + currentDate + extension
    return filename


def saveSrcAsCSV(arr):
    print("Save as CSV...")
    fileName = generateFileName(".csv")
    print("Filename: " + fileName + "\n")
    print("Label: " + str(arr[0]))

    output_list = ";"
    line_idx = 1
    for line in arr:
        print("Line " + str(line_idx) + ": " + str(line))
        file = open(fileName, "a")
        file.write(output_list.join(line) + "\n")
        file.close()
        line_idx += 1

    print("\n")


def getURLList(arr):
    print("Get URL List...")
    url_list = []
    print("Sum All: " + str(len(arr)))
    for item in arr:
        if item.get_attribute("href") not in url_list:
            print(item.get_attribute("href"))
            url_list.append(item.get_attribute("href"))
    print("Sum Distinct: " + str(len(url_list)) + "\n")
    return url_list


def removeModal():
    try:
        js_script = 'var c_modal = document.getElementById("c-modal");' \
                    'c_modal.style.display = "none";' \
                    'c_modal.setAttribute("tabindex", "0");' \
                    'var modal_backdrop_show = document.getElementsByClassName("modal-backdrop show");' \
                    'modal_backdrop_show[0].remove();' \
                    'return 0'
        result = driver.execute_script(js_script)
        # print("Eval Result: " + str(result))

    except:
        throwException()


option = Options()
#activate if browser shall be headless
option.add_argument('--headless')

driver = webdriver.Firefox(options=option)


driver.get("https://www.aldi-sued.de/de/produkte.html")

xPath = "//a[contains(@href, '/de/produkte/produktsortiment/')]"

elem = driver.find_elements_by_xpath(xPath)

print("Get Product Categories...")
url_list = getURLList(elem)

next_page_url = url_list[3]
driver.get(str(next_page_url))
delay = 3

removeModal()
try:
    btn_show_more = driver.find_element_by_id("showMore")
    btn_style = btn_show_more.get_attribute("style")
    # print(str(btn_style))

    if(btn_style != 'display:none'):
        # print("Show more...")
        #ActionChains(driver).click(btn_show_more).perform()
        #driver.action.click(btn_show_more)
        btn_show_more.click()

        while btn_style != "display: none;":
            # print("Show more...")
            btn_show_more.click()
            btn_style = btn_show_more.get_attribute("style")
            # print(str(btn_style))
except:
    throwException()


print("Get Product Sites...")

xPath = "//a[contains(@href, '/de/p.')]"
elem = driver.find_elements_by_xpath(xPath)
product_url_list = getURLList(elem)
#product_url_list = ['https://www.aldi-sued.de/de/p.bbq-laugenbaguette-mit--kraeuterbutter--g.490000000000039910.html']
#product_url_list = ['https://www.aldi-sued.de/de/p.meine-kuchenwelt-frischei-waffeln--g.490100000000055521.html']

print("Extract Data...")
w, h = 4, (len(product_url_list)+1)
p_arr = [[0 for x in range(w)] for y in range(h)]

labels = ["Name", "Price", "Currency", "Description"]
p_arr[0] = labels
idx = 1
for url in product_url_list:
    print(str(url))
    #next_page_url = product_url_list[0]
    #driver.get(str(next_page_url))
    driver.get(str(url))

    removeModal()
    try:
        product_data = driver.execute_script('var data = document.querySelectorAll("[data-product-name],'
                                        '[data-price],'
                                        '[data-currency],'
                                        '[data-description]");'
                                        'console.log(data);'
                                        'return data;'
                                     )
    except:
        throwException()

    #time.sleep(90)
    # try:
    #     print(product_data[0].text)
    #     print(product_data[1].text)
    #     print(product_data[3].text)
    # except:
    #     throwException()

    try:
        p_name = product_data[0].get_attribute('data-product-name')
        p_price = product_data[1].text.split(" ")[1]
        p_currency = product_data[1].text.split(" ")[0]
        p_description = ""

        for idx_desc in range(len(product_data)):
            if(idx_desc > 1):
                p_description += product_data[idx_desc].text.replace("\n", ", ")
    except:
        p_description = "NULL"
        throwException()

    # print("Name: " + p_name)
    # print("Price: " + p_price)
    # print("Currency: " + p_currency)
    # print("Description" + p_description)

    line = [str(p_name), str(p_price), str(p_currency), str(p_description)]
    p_arr[idx] = line
    idx += 1

    #print(labels)
    print(line)
    print("\n")

saveSrcAsCSV(p_arr)

# for item in product_data:
#    print(str(item.text))
#time.sleep(90)


#w, h = 7, 3
#test_arr = [[0 for y in range(w)] for y in range(h)]

#labels = ["Category", "Name", "Weight", "Volume", "Price", "Currency", "MwSt", "Discount", "Description"]
#test_arr[0] = labels

#line = ["Bread", "Roggen", "500g", "1.49", "7%", "0", "N/A"]
#test_arr[1] = line
#line = ["Bread", "Schwarzbrot", "500g", "1.79", "7%", "0", "N/A"]
#test_arr[2] = line

#saveSrcAsCSV(test_arr)

# time.sleep(90)
driver.close()

# async def main():
#     debug = False
#     if len(sys.argv) > 1:
#         runs = int(sys.argv[1])
#         print("Debug: " + str(debug))
#     if len(sys.argv) > 2:
#         prog = str(sys.argv[2])