import requests,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

ads_id = "2cb99d93dd220ad4b3950db9976544a5"
ads_id = "jcxetpn"
open_url = "http://local.adspower.net:50325/api/v1/browser/start?open_tabs=1&ip_tab=0&user_id=" + ads_id
close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id

resp = requests.get(open_url).json()
if resp["code"] != 0:
    print(resp["msg"])
    print("please check ads_id")
    sys.exit()
print(resp)
# time.sleep(10)
# requests.get(close_url)
# exit(1)
chrome_driver = resp["data"]["webdriver"]
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

driver.get("https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResultDetail?inquirytype=EntityName&directionType=ForwardList&searchNameOrder=VERACRUZGROUP%20L230003067520&aggregateId=flal-l23000306752-4a164814-2f19-4f5e-a109-83fb87d12fd9&searchTerm=VERA%20COPPORATION&listNameOrder=VERACRUZGROUP%20L230003067520")
with open('detail.html','w') as f:
    f.write(driver.page_source)

time.sleep(200)
driver.quit()
requests.get(close_url)
                  