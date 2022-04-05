from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


import time
import datetime
import sys
import os
import psycopg

__DBNAME__ = "forex"
__DBUSER__ = "eric"

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
    currentDate = date.strftime("%Y-%m-%d, %H:%M:%S")
    return currentDate

def generateFileName(extension):
    date = datetime.datetime.now()
    currentDate = date.strftime("%Y%m%d")
    try:
        dest = f"Output/EURUSD/"
        os.mkdir(dest)
    except:
        throwException()

    try:
        dest = f"Output/EURUSD/{currentDate}/"
        os.mkdir(dest)
    except:
        throwException()

    #currentDate = date.strftime("%Y%m%d")
    filename = dest + "EURUSD" + currentDate + extension
    return filename


def getScriptNameWithoutExt():
    return os.path.basename(__file__)[:-3]

def getFileName(path):
    path_parts = path.split("/")
    return path_parts[-1]

def getFilePath(path):
    path_parts = path.split("/")

    return "/".join(path_parts[:-1])

def saveAsCSV(arr):
    print("Save as XML")
    file = generateFileName(".csv")

    filename = getFileName(file)
    filepath = getFilePath(file)
    head = True

    if filename in list(os.listdir(filepath)):
        head = False

    head_line = "timestamp;ask;bid\n"
    content = ""
    for entry in arr:
        timestamp = entry.get('timestamp')
        ask = entry.get('ask')
        bid = entry.get('bid')

        line = timestamp + ";" + ask + ";" + bid + "\n"

        if head:
            content = head_line + line
            head = False
        else:
            content = content + line

    with open(file, 'a') as f:
        f.write(content)
    f.close()
    print("Filename: " + str(file) + "\n")

def saveToDB(arr):
    # test_arr = [
    #                 {'timestamp': '2022-04-05 16:08:02', 'ask': '1.08789', 'bid': '1.08786'},
    #                 {'timestamp': '2022-04-05 16:08:04', 'ask': '1.05123', 'bid': '1.05126'},
    #                 {'timestamp': '2022-04-05 16:08:06', 'ask': '1.07645', 'bid': '1.07642'}
    #             ]
    query_values = []
    print("Save to DB")
    sql_insert_stmt = "INSERT INTO eurusd(ask, bid, crawl_ts) VALUES"
    sql_value_stmt = "(%s, %s, %s),"

    for entry in arr:
        sql_insert_stmt = sql_insert_stmt + sql_value_stmt
        ts = entry.get('timestamp')
        ask = entry.get('ask')
        bid = entry.get('bid')
        query_values.append(ask)
        query_values.append(bid)
        query_values.append(ts)

    sql_insert_stmt = sql_insert_stmt[:-1]
    #print(sql_insert_stmt)

    with psycopg.connect(f"dbname={__DBNAME__} user={__DBUSER__}") as conn:
        with conn.cursor() as cur:
            cur.execute(sql_insert_stmt, query_values)

            #cur.execute("SELECT * FROM eurusd")
            #res = cur.fetchone()
            #print(res)

            conn.commit()

#saveToDB(['test'])
#sys.exit()

# file = generateFileName(".csv")
# filepath = getFilePath(file)
# filename = getFileName(file)
# print(file)
# print(filename)
# print(filepath)




option = Options()
#activate if browser shall be headless
option.add_argument('--headless')

driver = webdriver.Firefox(options=option)

# class: dfx-singleInstrument__price
# data-symbol = "EURUSD"
# data-type = "bid" | "ask"
# data-value = "x.x"

xPatch = ""


#time.sleep(10)
script = '''
    function get_price(){
        var dict = [];
        var data = {};
        var li = [];
        var eur_usd = {"bid": 0, "ask": 0};
        var fx = document.getElementsByClassName("dfx-singleInstrument__price");
        console.log(fx);
        ts = Date.now();
        date = new Date();
        crawl_ts = date.getFullYear() + "-" + String((date.getMonth()+1)).padStart(2, '0') + "-" + String(date.getDate()).padStart(2, '0') + " " + String(date.getHours()).padStart(2, '0') + ":" + String(date.getMinutes()) + ":" + String(date.getSeconds()).padStart(2, '0');
        data['timestamp'] = crawl_ts;
        for(var i=0; i<fx.length;i++){
            console.log(fx[i].innerText);
            elem = fx[i]
            if(elem.getAttribute("data-symbol") == "EURUSD"){
                data_type = String(elem.getAttribute("data-type"));
                data_value = String(elem.getAttribute("data-value"));
                data[data_type] = data_value;
            }
        }
        
        dict.push(data);
        console.log(dict);
        return data;    
    }
    
    return get_price();
'''
url = "https://www.dailyfx.com/forex-rates"
print(f"Get URL: {url}")

valid = False
driver = webdriver.Firefox(options=option)
while not valid:
    driver.get(url)
    result = driver.execute_script(script)

    if result.get('ask') != "---" and result.get('bid') != '---':
        valid = True
        print("Site valid")
    else:
        time.sleep(5)
        print("Fetch again")
        driver.close()
        driver = webdriver.Firefox(options=option)


print("Start fetch period")
res_list = []
finished = False
t_max = 1800
t = 0
t1 = 0
while not finished:
    t = t+1
    if t >= t_max:
        finished = True

    result = driver.execute_script(script)
    #print(result)

    res_list.append(result)

    #ask = result.get('ask')
    #bid = result.get('bid')
    #ts = result.get('timestamp')



    #print("Ask: ", ask)
    #print("Bid: ", bid)
    #print("TS: ", ts)

    time.sleep(1)
    t1 = t1 + 1
    if t1 % 60 == 0:
        print(t1)
    #print("Minute:", str(t))

#print(res_list)
saveToDB(res_list)
#saveAsCSV(res_list)

#time.sleep(10)

# fx = driver.find_elements(By.CLASS_NAME, "dfx-singleInstrument__price")
# eur_usd = [elem for elem in fx if elem.get_attribute("data-symbol") == "EURUSD"]
#
# print(eur_usd)
#
# for elem in eur_usd:
#     data_type = elem.get_attribute("data-type")
#     data_val = elem.get_attribute("data-value")
#
#     print("Type: ", data_type)
#     print("Val: ", data_val)
#     print()

#time.sleep(30)

driver.close()
print("Finished")
