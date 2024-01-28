import time

from actions.tiktok import tiktok_service

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import pandas as pd
import requests
from model.user import user
# r = requests.get('https://p16-rc-captcha-sg.ibyteimg.com/tos-alisg-i-749px8mig0-sg/3d_2385_248c0f3b3b9cd8db273c6706f25ab5d98882403a_1.jpg~tplv-749px8mig0-2.jpeg')
# print(r)
# exit(1)
def get_user_infor(path='input/user.xlsx'):
    user_list = pd.read_excel(path)
    for i,user in user_list.iterrows():
        yield user

user_iter = get_user_infor('input/user.xlsx')

#打开Tik Tok Seller 注册网站
ads_key='54b535e7fde791a6648a1481f5049735'
ads_id = "jdopcsb"
open_url = "http://local.adspower.net:50325/api/v1/browser/start?open_tabs=1&ip_tab=0&user_id=" + ads_id
close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id

resp = requests.get(open_url).json()
if resp["code"] != 0:
    print(resp["msg"])
    print("please check ads_id")
    sys.exit()
'''
https://p16-rc-captcha-sg.ibyteimg.com/tos-alisg-i-749px8mig0-sg/3d_2385_cd0c84b28b70f5fcfabd920efb0a5f45f777ad05_1.jpg~tplv-749px8mig0-2.jpeg
https://p16-rc-captcha-sg.ibyteimg.com/tos-alisg-i-749px8mig0-sg/3d_2385_a3262a335d3610fb43f10bd55355eb68c47f98fe_1.jpg~tplv-749px8mig0-2.jpeg
https://p19-rc-captcha-sg.ibyteimg.com/tos-alisg-i-749px8mig0-sg/3d_2385_960917fe9e3c596c875eb6a8e2139d5c2bef0d0b_1.jpg~tplv-749px8mig0-2.jpeg
https://p19-rc-captcha-sg.ibyteimg.com/tos-alisg-i-749px8mig0-sg/3d_2385_c8395460b62cd82c07f1ed7acc9e03abcc417cff_1.jpg~tplv-749px8mig0-2.jpeg
'''
chrome_driver = resp["data"]["webdriver"]
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
driver = webdriver.Chrome(chrome_options,service=Service(chrome_driver))
driver.get('https://seller-us.tiktok.com/settle/verification?is_new_connect=0&shop_region=US')
# print(driver.get_log('driver'))
driver.implicitly_wait(100)
icon_img= driver.find_element(by=By.XPATH,value='//img[@id="captcha-verify-image"]')
icon_img.screenshot('2.png')

# driver.close()
exit(11)
t_service = tiktok_service(user='',driver=driver)
user_model = user()
user_list = user_model.select(condition=['status','=',1])
for user in user_list:
    t_service.user=user
    result = t_service.register_by_phone()
    if(result==True):
        print('{}注册成功'.user['realname'])
