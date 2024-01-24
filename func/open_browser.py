import requests,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import re
import random
import sys
# str_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',"Q",'R','S','T','U','V','W','X','Y','Z']
# num = '226276018'
# s=''
# for i in range(len(num)):
#    s=s+str_list[random.randint(0,25)]
#
# print(s)
'''
104.160.21.98:40000
104.160.21.98:40001
'''
result = requests.get('http://104.160.21.98:9049/v1/ips?num=2&country=US&state=newyork&city=all&zip=all&t=txt&port=40000&isp=all&start=&end=')
print(result.text)
exit()
# company_list = re.findall(r'[a-z|A-Z]+','PATRICIA LONG, INC.')
ads_id = "2cb99d93dd220ad4b3950db9976544a5"
ads_id = "jd0d6ca"
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
driver.get('https://wwww.baidu.com')
print(driver.current_url)


# print(''.join(company_list))

def t_yield():
   for i in range(6):
      yield i
for i in t_yield():
   print(i)
# print(re.findall(r'[a-z|A-Z]+','PATRICIA LONG, INC.'))
# birth_list = [2024-random.randint(20,40),random.randint(1,12),random.randint(1,28)]
# print(birth_list)
# birth = '198/2/9'
# print(re.search(r'\d{4}/\d{1,2}/\d{1,2}',birth))
# s='+13305003509----https://good999.vip/api/smsCode/ad7b77999ae048278978a9361d97a5d1'
# mobie,sms_url = s.split('----')
#
# print(mobie[2:])
# # sms_result = requests.get(sms_url)
# # print(sms_result.text)
# sms_content = 'true|[TikTok] Your verification code is 2992, it will expire in 5 minutes. Do not share it with anyone.|2024-03-05 23:00:00'
# code_search = re.search(r'Your verification code is (\d{4})',sms_content)
# print(code_search.group(1))
# class test():/
    # a=111

# t = test()
# print(t.a)