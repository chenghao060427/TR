import requests,time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
import re
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

driver.get('https://seller-us.tiktok.com/settle/verification')

# wait = WebDriverWait(driver,10)
# wait.until(EC.presence_of_element_located((By.XPATH,'//input[@type="password"]')))
# email= driver.find_element(by=By.XPATH,value='//input[@type="email"]')
# email.send_keys('rfednyvds@hotmail.com')
# password = driver.find_element(by=By.XPATH,value='//input[@type="password"]')
# password.send_keys('Nbmlz5574#')

wait = WebDriverWait(driver,100)
wait.until(EC.presence_of_element_located((By.XPATH,'//input[@placeholder="Enter the business name"]')))
#公司名称
business_input = driver.find_element(by=By.XPATH,value='//input[@placeholder="Enter the business name"]')
business_input.send_keys(Keys.CONTROL + "a")
business_input.send_keys(Keys.DELETE)
business_input.send_keys('bussnisess name')

ein_xx = driver.find_element(by=By.XPATH,value='//input[@placeholder="XX"]')
ein_xx.send_keys(Keys.CONTROL + "a")
ein_xx.send_keys(Keys.DELETE)
ein_xx.send_keys('20')

ein_xxx = driver.find_element(by=By.XPATH,value='//input[@placeholder="XXXXXXX"]')
ein_xxx.send_keys(Keys.CONTROL + "a")
ein_xxx.send_keys(Keys.DELETE)
ein_xxx.send_keys('3891737')

owner_div = driver.find_element(by=By.XPATH,value='//div[contains(text(),"Yes, this business has at least 1 beneficial owner")]')
owner_div.click()

addres_input = driver.find_element(by=By.XPATH,value='//input[@placeholder="Street address"]')
addres_input.send_keys(Keys.CONTROL + "a")
addres_input.send_keys(Keys.DELETE)
addres_input.send_keys('520 BRICKELL KEY DR A900 MIAMI, FL 33131')
# addres_input.click()
wait = WebDriverWait(driver,15)
wait.until(EC.presence_of_element_located((By.ID,'theme-arco-select-popup-0')))
select_div = driver.find_element(By.XPATH,'//div[@id="theme-arco-select-popup-0"]/div[1]')
driver.execute_script("arguments[0].click();", select_div)

"I certify that I do not have a business address and only have a residential address or a combined business and residential address. If TikTok becomes aware that you have provided a false certification, you will have 10 days to consent to the disclosure of your address prior to account suspension."
checked = driver.find_element(by=By.XPATH,value='//input[@type="checkbox"]')
if(checked.get_attribute('checked')==None):
    address_span = driver.find_element(by=By.XPATH,value='//span[contains(text(),"I certify that I do not have a business address and only")]')
    driver.execute_script("arguments[0].click();", address_span)

company_radio = driver.find_element(by=By.XPATH,value='//div[text()="No"]')
driver.execute_script("arguments[0].click();", company_radio)

next_btn = driver.find_element(by=By.XPATH,value='//span[text()="Next"]')
driver.execute_script("arguments[0].click();", next_btn)

# driver.switch_to_alert().accept()
#Primary business person页面填写
wait = WebDriverWait(driver,30)
wait.until(EC.presence_of_element_located((By.XPATH,'//div[text()="Business representative"]')))

#根据按钮判断页面是否可编辑
show_btn =driver.find_element(by=By.XPATH,value='//button[contains(@class,"theme-arco-btn-icon-only")]')
if(show_btn):
    show_btn.click()
time.sleep(1)
checked = driver.find_element(by=By.XPATH,value='//input[@value="director"]')
if(checked.get_attribute('checked')==None):
    business_div = driver.find_element(by=By.XPATH,value='//div[text()="Business representative"]')
    driver.execute_script("arguments[0].click();", business_div)


first_name_input= driver.find_element(by=By.XPATH,value='//input[@placeholder="First name"]')
if(first_name_input.get_attribute('value')!=''):
    first_name_input.send_keys(Keys.CONTROL + "a")
    first_name_input.send_keys(Keys.DELETE)
first_name_input.send_keys('Howard')

last_name_input= driver.find_element(by=By.XPATH,value='//input[@placeholder="Last name"]')
if(last_name_input.get_attribute('value')!=''):
    last_name_input.send_keys(Keys.CONTROL + "a")
    last_name_input.send_keys(Keys.DELETE)
last_name_input.send_keys('Farley')

month_select = driver.find_elements(by=By.XPATH,value='//span[@class="theme-arco-select-view-value"]')
print(month_select)
# print(month_select.get_attribute('text'))
# exit()
# last_name_input.send_keys(Keys.CONTROL + "a")
# last_name_input.send_keys(Keys.DELETE)
month_select[0].click()
# 'span'
month_select_span = driver.find_element(by=By.XPATH,value='//span[contains(text(),"January")]')
month_select_span.click()

# day_select = driver.find_element(by=By.XPATH,value='//span[contains(text(),"Day")]')
month_select[1].click()
# 'span'
day_select_span = driver.find_element(by=By.XPATH,value='//span[contains(text(),"26")]')
day_select_span.click()

year_select = month_select[2]
current_year = int(year_select.get_property('textContent'))
if(current_year==0):
    start_year=2024
else:
    start_year=current_year
select_year=2003
# year_select.click()
while 1:
    try:
        print(start_year)
        year_select.click()
        y = driver.find_element(by=By.XPATH,value='//span[contains(text(),"{}")]'.format(start_year))
        y.click()
        time.sleep(0.1)
        if (start_year == select_year):
            break
        elif(start_year<select_year):
            start_year+=1
        else:
            start_year-=1
    except:
        print(2)

# wait = WebDriverWait(driver,20)
# wait.until(EC.presence_of_element_located((By.XPATH,'//span[contains(text(),"2003")]')))
# 'span'
# year_select_span = driver.find_element(by=By.XPATH,value='//span[contains(text(),"2003")]')
# year_select_span.click()

addres_input = driver.find_element(by=By.XPATH,value='//input[@placeholder="Street address"]')
if(addres_input.get_attribute('value')):
    addres_input.send_keys(Keys.CONTROL + "a")
    addres_input.send_keys(Keys.DELETE)
addres_input.send_keys('520 BRICKELL KEY DR A900 MIAMI, FL 33131')
# addres_input.click()
wait = WebDriverWait(driver,15)
wait.until(EC.presence_of_element_located((By.ID,'theme-arco-select-popup-7')))
select_div = driver.find_element(By.XPATH,'//div[@id="theme-arco-select-popup-7"]/div/div/li[1]')
driver.execute_script("arguments[0].click();", select_div)

ssn_div = driver.find_element(by=By.XPATH,value='//div[text()="Social security number (SSN)"]')
driver.execute_script("arguments[0].click();", ssn_div)

ssn_xxx = driver.find_element(by=By.XPATH,value='//input[@placeholder="XXXX"]')
if(ssn_xxx.get_attribute('value')):
    ssn_xxx.send_keys(Keys.CONTROL + "a")
    ssn_xxx.send_keys(Keys.DELETE)
ssn_xxx.send_keys('1456')

next_btn = driver.find_element(by=By.XPATH,value='//span[text()="Next"]')
driver.execute_script("arguments[0].click();", next_btn)

#Shop information
wait = WebDriverWait(driver,30)
wait.until(EC.presence_of_element_located((By.XPATH,'//div[text()="Shop name"]')))

shopname_input = driver.find_element(by=By.XPATH,value='//input[contains(@placeholder,"shop name")]')
if(shopname_input.get_attribute('value')):
    shopname_input.send_keys(Keys.CONTROL + "a")
    shopname_input.send_keys(Keys.DELETE)
shopname_input.send_keys('ABCD')

service_type_input = driver.find_element(by=By.XPATH,value='//input[@placeholder="Choose the primary product/service type"]')
if(service_type_input.get_attribute('value')):
    service_type_input.send_keys(Keys.CONTROL + "a")
    service_type_input.send_keys(Keys.DELETE)
service_type_input.click()

service_select_span = driver.find_element(by=By.XPATH,value='//span[text()="Fashion Accessories"]')
service_select_span.click()

s='+13305003509----https://good999.vip/api/smsCode/ad7b77999ae048278978a9361d97a5d1'
mobie,sms_url = s.split('----')


mobile_input = driver.find_element(by=By.XPATH,value='//input[@name="mobile"]')
if(mobile_input.get_attribute('value')):
    mobile_input.send_keys(Keys.CONTROL + "a")
    mobile_input.send_keys(Keys.DELETE)
mobile_input.send_keys(mobie[2:])

send_btn = driver.find_element(by=By.XPATH,value='//div[text()="Resend code" or text()="Send code"]')
driver.execute_script("arguments[0].click();", send_btn)
time.sleep(5)

# sms_result = requests.get(sms_url)
# print(sms_result.text)
sms_content = 'true|[TikTok] Your verification code is 2992, it will expire in 5 minutes. Do not share it with anyone.|2024-03-05 23:00:00'
code_search = re.search(r'Your verification code is (\d{4})',sms_content)
print(code_search.group(1))
code_input = driver.find_element(by=By.XPATH,value='//input[@placeholder="Enter the verification code"]')
if(code_input.get_attribute('value')):
    code_input.send_keys(Keys.CONTROL + "a")
    code_input.send_keys(Keys.DELETE)
code_input.send_keys(code_search.group(1))


