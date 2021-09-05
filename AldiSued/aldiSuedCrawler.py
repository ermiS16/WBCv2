from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import time
import datetime
import sys
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix} ( {iteration} / {total} )', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def throwException():
    file = open("../error.log", "a")
    info1 = "Exception " + str(sys.exc_info()[0]) + " occured."
    info2 = "Details: " + str(sys.exc_info()[0])
    file.write("[ " + str(getCurrentDate()) + " ] | " + str(info1) + ", " + str(info2))
    file.write("\n")
    file.close()
    # print("Exception", sys.exc_info()[0], "occured.")
    # print("Detail:", sys.exc_info()[1])


def getCurrentDate():
    date = datetime.datetime.now()
    #currentDate = date.strftime("%Y%m%d%H%M%S%f")
    #currentDate = date.strftime("%Y%m%d%H%M%S")
    currentDate = date.strftime("%Y-%m-%d, %H:%M:%S")
    return currentDate

def generateFileName(extension):

    dest = "../Output/AldiSued/"
    date = datetime.datetime.now()
    #currentDate = date.strftime("%Y%m%d%H%M%S%f")
    currentDate = date.strftime("%Y%m%d%H%M%S")

    filename = dest + os.path.basename(__file__) + "_" + currentDate + extension
    return filename


def saveSrcAsCSV(arr):
    print("Save as CSV")
    fileName = generateFileName(".csv")
    print("Filename: " + str(fileName) + "\n")
    # print("Label: " + str(arr[0]))

    idx = 0
    arr_length = len(arr)
    #printProgressBar(idx, arr_length, prefix='Progress:', suffix='Complete', length=50)

    output_list = ";"
    for line in arr:
        # print(str(line))
        file = open(fileName, "a")
        file.write(output_list.join(line) + "\n")
        file.close()
        time.sleep(0.1)
        #printProgressBar(idx+1, arr_length, prefix='Progress:', suffix='Complete', length=50)
        idx += 1

    print("Save Done!\n")

def saveSrcAsXML(arr):
    print("Save as CSV")
    fileName = generateFileName(".xml")
    print("Filename: " + str(fileName) + "\n")
    # print("Label: " + str(arr[0]))
    root = Element('Products')
    tree = ElementTree(root)
    idx = 0
    arr_length = len(arr)

    #printProgressBar(idx, arr_length, prefix='Progress:', suffix='Complete', length=50)
    output_list = ";"
    for line in arr:
        # print(str(line))
        product = SubElement(root, 'Product')
        name = SubElement(product, 'p_name')
        price = SubElement(product, 'p_price')
        currency = SubElement(product, 'p_currency')
        description = SubElement(product, 'p_description')
        name.text = str(line[0])
        price.text = str(line[1])
        currency.text = str(line[2])
        description.text = str(line[3])
        time.sleep(0.1)
        #printProgressBar(idx+1, arr_length, prefix='Progress:', suffix='Complete', length=50)
        idx += 1

    with open(fileName, 'wb') as f:
        tree.write(f, xml_declaration='UTF-8')
    print("Save Done!\n")


def getURLList(arr):
    print("Get URL List")
    url_list = []
    print("Sum All: " + str(len(arr)))
    for item in arr:
        try:
            if item.get_attribute("href") not in url_list:
                # print(item.get_attribute("href"))
                url_list.append(item.get_attribute("href"))
        except:
            throwException()

    print("Sum Distinct: " + str(len(url_list)))
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

print("Get Product Categories")
elem = driver.find_elements_by_xpath(xPath)
url_list = getURLList(elem)
#url_list = ['https://www.aldi-sued.de/de/produkte/produktsortiment/brot-aufstrich-und-cerealien.html']
#url_list = ['https://www.aldi-sued.de/de/produkte/produktsortiment/haushalt.html']

url_list_length = len(url_list)
url_list_idx = 1
p_arr = []
labels = ["Name", "Price", "Currency", "Description"]
p_arr.append(labels)

for category_url in url_list:
    print(f'\rGet Products From: {category_url} ( {url_list_idx} / {url_list_length} )')
    driver.get(str(category_url))

    removeModal()
    try:
        btn_show_more = driver.find_element_by_id("showMore")
        btn_style = btn_show_more.get_attribute("style")
        if(btn_style != 'display:none'):
            # print("Show more...")
            btn_show_more.click()

            while btn_style != "display: none;":
                # print("Show more...")
                btn_show_more.click()
                btn_style = btn_show_more.get_attribute("style")
    except:
        throwException()


    print("Get Product Sites")
    xPath = "//a[contains(@href, '/de/p.')]"
    elem = driver.find_elements_by_xpath(xPath)
    product_url_list = getURLList(elem)

    print("Start Extract Data")
    idx = 0
    product_url_list_length = len(product_url_list)
    printProgressBar(idx, product_url_list_length, prefix='Progress:', suffix='Complete', length=50)
    for url in product_url_list:
        # print(str(url))
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
        p_arr.append(line)

        time.sleep(0.1)
        printProgressBar(idx+1, product_url_list_length, prefix='Progress:', suffix='Complete', length=50)
        idx += 1
    url_list_idx += 1
    print("Extract Data Done!\n")
saveSrcAsCSV(p_arr)
saveSrcAsXML(p_arr)
driver.close()
print("Finished")
