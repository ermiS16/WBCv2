from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import time
import datetime
import sys
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

    dest = "../Output/AldiNord/"
    date = datetime.datetime.now()
    #currentDate = date.strftime("%Y%m%d%H%M%S%f")
    currentDate = date.strftime("%Y%m%d%H%M%S")

    filename = dest + currentDate + extension
    return filename


def saveSrcAsCSV(arr):
    print("Save as CSV")
    fileName = generateFileName(".csv")
    print("Filename: " + str(fileName) + "\n")
    # print("Label: " + str(arr[0]))

    idx = 0
    arr_length = len(arr)
    printProgressBar(idx, arr_length, prefix='Progress:', suffix='Complete', length=50)

    output_list = ";"
    for line in arr:
        # print(str(line))
        file = open(fileName, "a")
        file.write(output_list.join(line) + "\n")
        file.close()
        time.sleep(0.1)
        printProgressBar(idx+1, arr_length, prefix='Progress:', suffix='Complete', length=50)
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
                print(item.get_attribute("href"))
                url_list.append(item.get_attribute("href"))
        except:
            throwException()

    print("Sum Distinct: " + str(len(url_list)))
    return url_list



option = Options()
#activate if browser shall be headless
option.add_argument('--headless')

driver = webdriver.Firefox(options=option)


driver.get("https://www.aldi-nord.de/sortiment/neu/linsen-chips-1003041-0-0.article.html")
elem = driver.find_elements_by_xpath("//div[@class='page__content']")
print(len(elem))
print(elem[0].text)

p_arr = []
labels = ["Name", "Price", "Currency", "Description"]
p_arr.append(labels)



# saveSrcAsCSV(p_arr)
# saveSrcAsXML(p_arr)
#time.sleep(120)
driver.close()
print("Finished")
