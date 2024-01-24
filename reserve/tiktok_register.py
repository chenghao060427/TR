import requests,time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import sys
import pandas as pd
from func.reserve_email import get_register_code
def get_user_infor(path='input/user.xlsx'):
    user_list = pd.read_excel(path)
    for i,user in user_list.iterrows():
        yield user

user_iter = get_user_infor('input/user.xlsx')

#打开Tik Tok Seller 注册网站
ads_key='54b535e7fde791a6648a1481f5049735'
ads_id = "jd0d6ca"
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

driver.get('https://seller-us-accounts.tiktok.com/account/register/form')
wait = WebDriverWait(driver,10)
wait.until(EC.presence_of_element_located((By.ID,'phone_email_input')))
input = driver.find_element(by=By.ID,value='phone_email_input')
input.send_keys(user_email)
driver.implicitly_wait(1)
#点击按钮
button = driver.find_element(by=By.CLASS_NAME,value='index__RedButton--xEvbb')
button.click()
#监听页面地址变化
wait = WebDriverWait(driver,20)
wait.until(EC.presence_of_element_located((By.ID,'verificationInput-0')))
current_stamp=int(time.time())
time.sleep(5)
#获取验证码
code = get_register_code(email=user_email,password=email_password,end_time=current_stamp)
if(code):
    for i in range(0,6):
        c_input = driver.find_element(by=By.ID,value='verificationInput-{}'.format(i))
        c_input.send_keys(code[i])
wait = WebDriverWait(driver,20)
wait.until(EC.presence_of_element_located((By.CLASS_NAME,'mt-60')))

button = driver.find_element(by=By.CLASS_NAME,value='mt-60')
button.click()
#输入密码
wait = WebDriverWait(driver,10)
wait.until(EC.presence_of_element_located((By.XPATH,'//input[@type="password"]')))
password = driver.find_element(by=By.XPATH,value='//input[@type="password"]')
password.send_keys(re_password)
'repeat_password_input'
re_passwd = driver.find_element(by=By.ID,value='repeat_password_input')
re_passwd.send_keys(re_passwd)
#点击确认
wait = WebDriverWait(driver,20)
wait.until(EC.presence_of_element_located((By.CLASS_NAME,'mt-60')))
button = driver.find_element(by=By.CLASS_NAME,value='mt-60')
button.click()
#验证信息
wait = WebDriverWait(driver,20)
wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"Corporation")')))
check_div = driver.find_element(by=By.XPATH,value='//div[contains(text(),"Corporation")')
check_div.click()
#点击确认
wait = WebDriverWait(driver,20)
wait.until(EC.presence_of_element_located((By.CLASS_NAME,'theme-arco-btn-primary')))
button = driver.find_element(by=By.CLASS_NAME,value='theme-arco-btn-primary')
#公司信息输入

