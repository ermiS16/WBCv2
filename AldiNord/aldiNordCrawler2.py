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


def generateFileName(extension, category_url):
    category = getCategory(category_url)
    date = datetime.datetime.now()
    currentDate = date.strftime("%Y%m%d")
    try:
        dest = f"../Output/AldiNord2/{currentDate}/"
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
        tree.write(f, xml_declaration=True)
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
                # print(item.get_attribute("href"))
                url_list.append(item.get_attribute("href"))
        except:
            throwException()

    print("Sum Distinct: " + str(len(url_list)))
    return url_list



option = Options()
#activate if browser shall be headless
option.add_argument('--headless')

driver = webdriver.Firefox(options=option)

print("Get Product Categories")

url_list = []
filename = "URL_List.txt"
if not os.path.isfile(filename):
    print ("File does not exists")
else:
    with open(filename) as f:
        urlContent = f.readlines()
        #print(urlContent)


for line in urlContent:
    #print(line)
    line = line.replace("\n", "")
    url_list.append(line)


url_list = ['https://www.aldi-nord.de/sortiment/kaffee-tee-kakao/kaffee.html',
            'https://www.aldi-nord.de/sortiment/backwaren-aufstriche-cerealien/ofenfrische-backwaren.html']

url_list_length = len(url_list)
url_list_idx = 1
for category_url in url_list:
    idx = 0
    p_arr = []
    print(f'\rGet Products From: {category_url} ( {url_list_idx} / {url_list_length} )')
    driver.get(str(category_url))

    print("Get Product Sites")
    xPath = f"//a[contains(@href, '/sortiment/')]"
    elem = driver.find_elements_by_xpath(xPath)
    product_url_list = getURLList(elem)


    print("Start Extract Data")
    if(len(product_url_list) > 0):
        printProgressBar(idx, len(product_url_list), prefix='Progress:', suffix='Complete', length=50)

    for url in product_url_list:
        # print(str(url))
        driver.get(str(url))
        html_body = driver.find_elements_by_xpath("/html/body")
        product_info = html_body[0].text
        product_info = product_info.replace("\n", "; ")
        print(product_info + "\n")

        p_arr.append(product_info)
        time.sleep(0.1)
        idx += 1
        printProgressBar(idx, len(product_url_list), prefix='Progress:', suffix='Complete', length=50)
    print("Extract Data Done!\n")

    url_list_idx += 1
    saveSrcAsXML(p_arr, category_url)

#time.sleep(120)
driver.close()
print("Finished")
