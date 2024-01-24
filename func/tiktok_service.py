from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import imapclient
import re
from selenium.webdriver.common.by import By
import time
import random
import requests

class tiktok_service():
    month_n_e={
        1:'January',
        2:'February',
        3:'March',
        4:'April',
        5:'May',
        6:'June',
        7:'July',
        8:'August',
        9:'September',
        10:'October',
        11:'November',
        12:'December'
    }
    str_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',"Q",'R','S','T','U','V','W','X','Y','Z']

    def __init__(self,user,driver):
        self.user=user
        self.driver = driver
        pass
    #注册tiktok用户
    def register(self):
        self.driver.get('https://seller-us-accounts.tiktok.com/account/register/form')
        # self.driver.get('https://seller-us.tiktok.com/settle/verification?is_new_connect=0&shop_region=US')

        self.write_input(by=By.ID,condition='phone_email_input',value=self.user['邮箱'])
        self.driver.implicitly_wait(1)

        #点击按钮
        self.btn_click(by=By.CLASS_NAME,condition='index__RedButton--xEvbb')

        time.sleep(10)
        repeat_times=4
        try:
            while (repeat_times>0):
                code = self.get_register_code(email=self.user['邮箱'],password=self.user['邮箱密码'],end_time=int(time.time())-36000)
                if(code):
                    for i in range(0,6):
                        self.write_input(by=By.ID,condition='verificationInput-{}'.format(i),value=code[i])
                    break
                else:
                    print('获取验证码失败，重新获取，剩余次数：{}'.format(repeat_times))
                    repeat_times-=1
                    time.sleep(2)
        except:
            print('获取验证码失败，需人工干预')
            self.driver.implicitly_wait(300)
        #切换
        self.btn_click(by=By.CLASS_NAME,condition='mt-60')
        #输入密码
        self.write_input(by=By.XPATH,condition='//input[@type="password"]',value=self.user['账户密码'])
        self.write_input(by=By.ID,condition='repeat_password_input',value=self.user['账户密码'])
        self.btn_click(by=By.CLASS_NAME,condition='mt-60')

        self.btn_click(by=By.XPATH,condition='//div[contains(text(),"Corporation")]')
        self.btn_click(by=By.XPATH,condition='//span[text()="Next"]')

        self.write_company_infor()
        self.write_business_infor()
        self.write_shop_infor()
        time.sleep(2)
        self.write_tax_infor()
        # for window in self.driver.window_handles:
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(10)
        self.driver.close()
        return True
    #填写公司信息
    def write_company_infor(self):
        wait = WebDriverWait(self.driver,100)
        wait.until(EC.presence_of_element_located((By.XPATH,'//input[@placeholder="Enter the business name"]')))

        self.write_input(by=By.XPATH,condition='//input[@placeholder="Enter the business name"]',value=self.user['公司名称'])
        #EIN码
        ein_num = self.user['EIN码'].split('-')
        if(len(ein_num)==2):
            self.write_input(by=By.XPATH,condition='//input[@placeholder="XX"]',value=ein_num[0])
            self.write_input(by=By.XPATH,condition='//input[@placeholder="XXXXXXX"]',value=ein_num[1])
        else:
            print('Ein码读取失败，需人工干预')
            self.driver.implicitly_wait(300)
        self.btn_click(by=By.XPATH,condition='//div[contains(text(),"Yes, this business has at least 1 beneficial owner")]')
        self.write_input(by=By.XPATH,condition='//input[@placeholder="Street address"]',value=self.user['公司地址'])

        self.btn_click(by=By.XPATH,condition='//div[@id="theme-arco-select-popup-0"]/div/div/li[1]')
        checked = self.driver.find_element(by=By.XPATH,value='//input[@type="checkbox"]')
        if(checked.get_attribute('checked')==None):
            self.btn_click(by=By.XPATH,condition='//span[contains(text(),"I certify that I do not have a business address and only")]')
        self.btn_click(by=By.XPATH,condition='//div[text()="No"]')
        self.btn_click(by=By.XPATH,condition='//span[text()="Next"]')
        print('公司信息输入完成')
        pass
    #填写商家信息
    def write_business_infor(self):
        wait = WebDriverWait(self.driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'//div[text()="Business representative"]')))
        try:
            self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-icon-only")]',type=2)
        except:
            pass
        checked = self.driver.find_element(by=By.XPATH,value='//input[@value="director"]')
        if(checked.get_attribute('checked')==None):
            self.btn_click(by=By.XPATH,condition='//div[text()="Business representative"]')
        name_list = self.user['名字'].split(' ')
        self.write_input(by=By.XPATH,condition='//input[@placeholder="First name"]',value=name_list[0])
        self.write_input(by=By.XPATH,condition='//input[@placeholder="Last name"]',value=name_list[1])
        #出生日期1981-12-19
        birth = str(self.user['生日'])[0:10]
        if(re.search(r'\d{4}-\d{1,2}-\d{1,2}',birth)):
            birth_list = birth.split('-')
        else:
            birth_list = [2024-random.randint(20,40),random.randint(1,12),random.randint(1,28)]
        print(birth_list)
        birth_select = self.driver.find_elements(by=By.XPATH,value='//span[contains(@class,"theme-arco-select-view-value")]')
        # print(birth_select)
        self.driver.execute_script("arguments[0].click();", birth_select[0])
        # birth_select[0].click()
        self.select_action(by=By.XPATH,condition='//span[contains(text(),"{}")]'.format(self.month_n_e[int(birth_list[1])]))
        # time.sleep(2)
        birth_select[1].click()
        self.select_action(by=By.XPATH,condition='//span[contains(text(),"{}")]'.format(int(birth_list[2])))

        # birth_select[2].click()
        if(birth_select[2].get_property('textContent').isdigit()):
            start_year = int(birth_select[2].get_property('textContent'))
        else:
            start_year=2024

        select_year = int(birth_list[0])
        while 1:
            try:
                print(start_year)
                birth_select[2].click()
                self.select_action(by=By.XPATH,condition='//span[contains(text(),"{}")]'.format(start_year))
                # y.click()
                time.sleep(0.1)
                if (start_year == select_year):
                    break
                elif(start_year<select_year):
                    start_year +=1
                else:
                    start_year-=1
            except:
                print(2)
        self.write_input(by=By.XPATH,condition='//input[@placeholder="Street address"]',value=self.user['地址'])
        self.btn_click(by=By.XPATH,condition='//div[@id="theme-arco-select-popup-7"]/div/div/li[1]')
        self.write_input(by=By.XPATH,condition='//input[@placeholder="XXXX"]',value=str(self.user['SSN'])[-4:])
        self.btn_click(by=By.XPATH,condition='//span[text()="Next"]')


        pass
    #填写商店信息
    def write_shop_infor(self):
        wait = WebDriverWait(self.driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'//div[text()="Shop name"]')))
        company_list = re.findall(r'[a-z|A-Z]+',self.user['公司名称'])
        company_name= (''.join(company_list))
        if(len(company_list)==0):
            company_name=''
            for i in range(len(self.user['公司名称'])):
                company_name=company_name+self.str_list[random.randint(0,25)]
        self.write_input(by=By.XPATH,condition='//input[contains(@placeholder,"shop name")]',value=company_name)
        try:
            service_type_input = self.driver.find_element(by=By.XPATH,value='//span[@class="theme-arco-select-view-value"]')
            service_type_input.click()
            self.select_action(by=By.XPATH,condition='//span[text()="Fashion Accessories"]')
        except:
            service_type_input = self.driver.find_element(by=By.XPATH,value='//input[@placeholder="Choose the primary product/service type"]')
            if(service_type_input.get_attribute('value')):
                service_type_input.send_keys(Keys.CONTROL + "a")
                service_type_input.send_keys(Keys.DELETE)
            service_type_input.click()
            self.select_action(by=By.XPATH,condition='//span[text()="Fashion Accessories"]')
        try:
            self.driver.find_element(by=By.XPATH,value='//div[text()="Use below"]')
        except:
            s=self.user['电话号码']
            mobie,sms_url = s.split('----')
            self.write_input(by=By.XPATH,condition='//input[@name="mobile"]',value=mobie[2:])
            resend_times=5
            while(resend_times>0):

                self.btn_click(by=By.XPATH,condition='//div[text()="Resend code" or text()="Send code"]')
                time.sleep(5)

                sms_result = requests.get(sms_url)
                # print(sms_result.text)
                sms_content = sms_result.text
                code_search = re.search(r'Your verification code is (\d{4})',sms_content)
                if(code_search):
                    sms_code = code_search.group(1)
                    self.write_input(by=By.XPATH,condition='//input[@placeholder="Enter the verification code"]',value=sms_code)
                    break
                else:
                    resend_times-=1
                    print('无法获取短信验证码，稍后重新获取，剩余尝试次数：{}'.format(resend_times))
                    time.sleep(60)
        # time.sleep(5)
        # exit(13)
        # while 1:
        #     try:
        #         self.driver.find_element(by=By.XPATH, value='//div[text()="Use below"]')
        #         break
        #     except:
        #         print('请手动输入验证码')
        self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-default")]',type=2)
        time.sleep(5)
        self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-default")]',type=2)

        self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-large")]',type=2)

        #https://seller-us.tiktok.com/homepage
        pass
    #填写相关文字信息
    def write_tax_infor(self):
        self.driver.get('https://seller-us.tiktok.com/homepage?shop_region=US')
        self.btn_click(by=By.XPATH,condition='//p[text()="Add tax information"]/../../following-sibling::*[1]/button',type=2)
        time.sleep(1)
        while 1:
            # if(len(self.driver.window_handles)==2):
            #     break
            for window in self.driver.window_handles:
                self.driver.switch_to.window(window)
                if(re.search(r'https://seller-us.tiktok.com/settle/tax-staged',self.driver.current_url)):
                    break
            if (re.search(r'https://seller-us.tiktok.com/settle/tax-staged', self.driver.current_url)):
                break
            # exit(1)
        # self.driver.switch_to.window(self.driver.window_handles[1])

        self.btn_click(by=By.XPATH,condition='//div[text()="Non individual / Entity"]')
        self.btn_click(by=By.XPATH,condition='//input[@placeholder="Select the U.S federal tax classification"]')
        self.select_action(by=By.XPATH,condition='//div[contains(text(),"Sole proprietor")]')
        # exit(13)
        try:
            self.btn_click(by=By.XPATH,condition='//label[contains(@class,"theme-arco-checkbox theme-m4b-checkbox")]/descendant::div[contains(text(),"I confirm that I have reviewed the generated tax documents")]')
            self.btn_click(by=By.XPATH,condition='//label[contains(@class,"theme-arco-checkbox theme-m4b-checkbox")]/descendant::div[contains(text(),"I have read the Consent and agree to accept the paperless")]')
        except:
            print('点击失败')
            pass
        self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn theme-arco-btn-primary")]',type=2)

        self.write_input(by=By.XPATH,condition='//input[@name="signature"]',value=self.user['名字'])
        self.btn_click(by=By.XPATH,condition='//div[contains(@class,"ModalContainer-sc-1erxb43-2 fUveFc")]/descendant::button[contains(@class,"theme-arco-btn-primary")]',type=2)
        time.sleep(5)
        self.driver.close()

    def write_input(self,by,condition,value):
        wait = WebDriverWait(self.driver, 60)
        wait.until(EC.presence_of_element_located((by, condition)))
        input = self.driver.find_element(by=by, value=condition)
        if (input.get_attribute('value')):
            input.send_keys(Keys.CONTROL + "a")
            input.send_keys(Keys.DELETE)
        input.send_keys(value)
        pass
    #选择选项
    def select_action(self,by,condition):
        self.btn_click(by,condition)
        pass
    #点击事件
    def btn_click(self,by,condition,type=1):
        wait = WebDriverWait(self.driver, 60)
        wait.until(EC.presence_of_element_located((by, condition)))
        btn = self.driver.find_element(by=by, value=condition)
        if(type==1):
            self.driver.execute_script("arguments[0].click();", btn)
        else:
            btn.click()
        pass

    #获取邮箱验证码
    def get_register_code(self,email='', password='', end_time=''):
        client = imapclient.IMAPClient('outlook.office365.com', port=993)
        # print(email)
        # print(password)
        client.login(email, password)
        folders = client.list_folders()
        # print(folders)
        # exit(11)
        client.select_folder(folder='Junk')

        messages = client.search(['FROM', 'register@account.tiktok.com'])
        # print(messages)
        messages.reverse()
        for _sm in messages:
            msgdict = client.fetch(_sm, ['INTERNALDATE', 'ENVELOPE'])  # 获取邮件内容
            # mailbody = msgdict[_sm][b'BODY[]']
            print(msgdict[_sm])
            if (end_time <= int(msgdict[_sm][b'INTERNALDATE'].timestamp())):
                s = re.search(r'\d{6}', msgdict[_sm][b'ENVELOPE'].subject.decode())
                if (s != None):
                    print(s.group())
                    return s.group()
            return None
        return None
    #登录tiktok
    def login_user(self):
        self.driver.get('https://seller-us-accounts.tiktok.com/account/login')

        pass
    #登出tiktok
    def logout(self):
                        # 'https://seller-us.tiktok.com/passport/web/logout/?next=https%3A%2F%2Fseller-us-accounts.tiktok.com%2Faccount%2Flogin'
        self.driver.get('https://business-sso.us.tiktok.com/logout/?service=https%3A%2F%2Fseller-us.tiktok.com%2Fpassport%2Fweb%2Flogout%2F%3Fnext%3Dhttps%253A%252F%252Fseller-us-accounts.tiktok.com%252Faccount%252Flogin')
        pass
    def get_shop_register_status(self,email='', password='', end_time=''):
        client = imapclient.IMAPClient('outlook.office365.com', port=993)
        # print(email)
        # print(password)
        client.login(email, password)
        folders = client.list_folders()
        # print(folders)
        # exit(11)
        client.select_folder(folder='Inbox')

        messages = client.search(['FROM', 'sellersupport@shop.tiktok.com'])
        # print(messages)
        messages.reverse()
        for _sm in messages:
            msgdict = client.fetch(_sm, ['INTERNALDATE', 'ENVELOPE'])  # 获取邮件内容
            # mailbody = msgdict[_sm][b'BODY[]']
            # print(msgdict[_sm])
            if (end_time <= int(msgdict[_sm][b'INTERNALDATE'].timestamp())):
                return msgdict[_sm][b'ENVELOPE'].subject.decode()
                # s = re.search(r'\d{6}', msgdict[_sm][b'ENVELOPE'].subject.decode())
                # if (s != None):
                #     print(s.group())
                #     return s.group()
            return None
        return None
        pass