import time

from actions.tiktok import tiktok_service

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import pandas as pd
import requests
from model.user import user
def get_user_infor(path='input/user.xlsx'):
    user_list = pd.read_excel(path)
    for i,user in user_list.iterrows():
        yield user

user_iter = get_user_infor('input/user.xlsx')

#打开Tik Tok Seller 注册网站
ads_key='54b535e7fde791a6648a1481f5049735'
ads_id = "jdtj96n"
open_url = "http://local.adspower.net:50325/api/v1/browser/start?open_tabs=1&ip_tab=0&user_id=" + ads_id
close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id

resp = requests.get(open_url).json()
if resp["code"] != 0:
    print(resp["msg"])
    print("please check ads_id")
    sys.exit()

chrome_driver = resp["data"]["webdriver"]
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
driver = webdriver.Chrome(chrome_options,service=Service(chrome_driver))
driver.get('https://seller-us.tiktok.com/homepage?shop_region=US')
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH,'//p[contains(text(),"Register your business")]/../../../div[1]/img')))
ele = driver.find_element(by=By.XPATH,value='//p[contains(text(),"Register your business")]/../../../div[1]/img')

print(ele.get_attribute('src'))
# driver.switch_to.new_window()
# driver.get('https://www.baidu.com')
# driver.implicitly_wait(20)
time.sleep(20)
# for w in driver.window_handles:
#     driver.switch_to.window(w)
#     driver.close()
exit(11)
t_service = tiktok_service(user='',driver=driver)
user_model = user()
user_list = user_model.select(condition=['status','=',1])
for user in user_list:
    t_service.user=user
    result = t_service.register_by_phone()
    if(result==True):
        print('{}注册成功'.user['realname'])
