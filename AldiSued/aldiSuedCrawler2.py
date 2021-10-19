from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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

def generateFileName(extension, category_url):
    category = getCategory(category_url)
    date = datetime.datetime.now()
    currentDate = date.strftime("%Y%m%d")
    try:
        dest = f"../Output/AldiSued2/{currentDate}/"
        os.mkdir(dest)
    except:
        throwException()
    currentDate = date.strftime("%Y%m%d%H%M%S")
    filename = dest + currentDate + "_" + category + extension
    return filename


def getScriptNameWithoutExt():
    return os.path.basename(__file__)[:-3]



def saveSrcAsXML(arr, category_url):
    print("Save as XML")
    fileName = generateFileName(".xml", category_url)
    print("Filename: " + str(fileName) + "\n")
    # print("Label: " + str(arr[0]))
    root = Element('Products')
    tree = ElementTree(root)
    arr_length = len(arr)

    idx=0
    for info_text in arr:
        # print(str(line))
        product = SubElement(root, 'Product')
        product.set('processed', 'false')
        description = SubElement(product, 'p_info')
        description.text = str(info_text)
        time.sleep(0.1)

    with open(fileName, 'wb') as f:
        tree.write(f, encoding='UTF-8', xml_declaration=True)
    print("Save Done!\n")


def getCategory(category_url):
    category = ""
    for i in range(len(category_url)):
        if i > 0:
            c = category_url[-i]
            if(c != '/'):
                category = c + category
            else:
                break
    category = category[:-5]
    print("Category: " + str(category))
    return category


def getURLList(arr):
    print("Get URL List")
    url_list = []
    print("Sum All: " + str(len(arr)))
    for item in arr:
        try:
            if item.get_attribute("href") not in url_list:
                url_list.append(item.get_attribute("href"))
                # print(item.get_attribute("href"))
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
#elem = driver.find_elements_by_xpath(xPath)
elem = driver.find_elements(By.XPATH, xPath)
url_list = getURLList(elem)
#url_list = ['https://www.aldi-sued.de/de/produkte/produktsortiment/brot-aufstrich-und-cerealien.html']
#url_list = ['https://www.aldi-sued.de/de/produkte/produktsortiment/haushalt.html']

url_list_length = len(url_list)
url_list_idx = 1

for category_url in url_list:
    p_arr = []
    print(f'\rGet Products From: {category_url} ( {url_list_idx} / {url_list_length} )')
    driver.get(str(category_url))

    removeModal()
    try:
        # btn_show_more = driver.find_element_by_id("showMore")
        btn_show_more = driver.find_element(By.ID, "showMore")
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
    #elem = driver.find_elements_by_xpath(xPath)
    elem = driver.find_elements(By.XPATH, xPath)
    product_url_list = getURLList(elem)

    print("Start Extract Data")
    idx = 0
    product_url_list_length = len(product_url_list)
    printProgressBar(idx, product_url_list_length, prefix='Progress:', suffix='Complete', length=50)
    for url in product_url_list:
        # print(str(url))
        driver.get(str(url))
        removeModal()

        # html_body = driver.find_elements_by_xpath("/html/body")
        html_body = driver.find_elements(By.XPATH, "/html/body")
        product_info = html_body[0].text
        product_info = product_info.replace("\n", "; ")
        p_arr.append(product_info)

        time.sleep(0.1)
        printProgressBar(idx+1, product_url_list_length, prefix='Progress:', suffix='Complete', length=50)
        idx += 1
    url_list_idx += 1
    print("Extract Data Done!\n")
    saveSrcAsXML(p_arr, category_url)

driver.close()
print("Finished")
