import re
import requests,time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import sys
from urllib.parse import urljoin
import pandas as pd
from func.search_xpath import get_company_list,get_company_detail
from model.company_keyword import company_keyword
import random
from threads.comany import get_company_dispatch

d = get_company_dispatch(company_num=700,pro_win=None)
d.start()
def chose_keyword(num=0):
    keyword_db = company_keyword()
    min_times = keyword_db.select(colunm='min(times)');
    current_times = min_times[0]['min(times)']
    keyword_list = []
    total_num = num
    last_num = num
    while (total_num > len(keyword_list)):
        re_keyword_list = keyword_db.select(condition=['times', '=', current_times])
        if (last_num > len(re_keyword_list)):
            random.shuffle(re_keyword_list)
            for keyword in re_keyword_list:
                keyword_list.append(keyword)
            last_num -= len(re_keyword_list)
        else:
            random.shuffle(re_keyword_list)
            for keyword in re_keyword_list[0:last_num]:
                keyword_list.append(keyword)
            last_num = 0
        current_times+=1

    for index in  range(num):
        yield index,keyword_list[index]


k_list = chose_keyword(100)
print(k_list)
exit(1333)

# ads_id = "2cb99d93dd220ad4b3950db9976544a5"
ads_id = "jcxetpn"
open_url = "http://local.adspower.net:50325/api/v1/browser/start?open_tabs=1&ip_tab=0&user_id=" + ads_id
close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id

resp = requests.get(open_url).json()
if resp["code"] != 0:
    print(resp["msg"])
    print("please check ads_id")
    sys.exit()
# print(resp)
# time.sleep(10)
# requests.get(close_url)
# exit(1)
chrome_driver = resp["data"]["webdriver"]
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
driver = webdriver.Chrome(chrome_options,service=Service(chrome_driver))

base_url = 'https://search.sunbiz.org/'
log_file = 'output/company'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+'.csv'
total_times=500
company_list=[]

f_start_url = "https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults/EntityName/{}/Page1?searchNameOrder={}"

f = open('output/人名.txt','r')

# name = f.readline()
# n = re.sub(r'\s?','',name)
# n = n.upper()
while(total_times>0):
    times=10
    name = f.readline()
    n = re.sub(r'\s?','',name)
    n = n.upper()
    start_url=f_start_url.format(n,n)
    print(start_url)
    while(times>0):
        driver.get(start_url)
        time.sleep(2)
        #分析页面内容
        href_list,next_href = get_company_list(driver.page_source)
        for h in href_list:
            time.sleep(1)
            driver.get(urljoin(base_url,h))
            company = get_company_detail(driver.page_source)
            if(re.match(r'^\d{2}-\d{7}$',company['ein'])):
                times-=1
                total_times-=1
                print(times)
                print(total_times)
                company_list.append(company)
        start_url = urljoin(base_url,next_href)
print(company_list)
df = pd.DataFrame(company_list)
df.to_csv(log_file)
with open('current_url','w+') as f:
    f.write(start_url)
