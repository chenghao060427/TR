from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import imapclient
import re
from selenium.webdriver.common.by import By
import time
import random
import requests
from model.user import user as user_model
from retry import retry
class tiktok_service():
    __instans = None
    def __new__(cls, *args, **kwargs):
        if(cls.__instans is None):
            cls.__instans = super().__new__(cls)
            return cls.__instans
        else:
            return cls.__instans
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
        self.user_model = user_model()
        self.driver = driver
        pass
    #注册tiktok用户（用邮箱）
    def register(self):
        # self.driver.get('https://seller-us-accounts.tiktok.com/account/register/form')
        self.driver.get('https://seller-us.tiktok.com/settle/verification?is_new_connect=0&shop_region=US')
        print('填写邮箱')
        self.write_input(by=By.ID,condition='phone_email_input',value=self.user['email'])
        self.driver.implicitly_wait(1)

        #点击按钮
        self.btn_click(by=By.CLASS_NAME,condition='index__RedButton--xEvbb')

        self.driver.implicitly_wait(10)
        repeat_time=5
        try:
            while(repeat_time>0):
                if(self.check_ele_exit(by=By.ID,condition='verificationInput-0')):
                    code = self.get_register_code(email=self.user['email'],password=self.user['email_pwd'],end_time=int(time.time())-36000)
                    if(code):
                        for i in range(0,6):
                            self.write_input(by=By.ID,condition='verificationInput-{}'.format(i),value=code[i])
                        break
                    else:
                        repeat_time-=1
                        print('获取验证码失败,尝试重新获取，剩余重复次数：{}'.format(repeat_time))
                        time.sleep(10)
            raise
        except:
            print('获取验证码失败，需人工干预')
        self.driver.implicitly_wait(300)
        #切换
        self.btn_click(by=By.CLASS_NAME,condition='mt-60')
        #输入密码
        self.write_input(by=By.XPATH,condition='//input[@type="password"]',value=self.user['pwd'])
        self.write_input(by=By.ID,condition='repeat_password_input',value=self.user['pwd'])
        self.btn_click(by=By.CLASS_NAME,condition='mt-60')
        try:
            self.skip_start_page()
        except:
            pass

        self.btn_click(by=By.XPATH,condition='//div[contains(text(),"Corporation")]')
        self.btn_click(by=By.XPATH,condition='//span[text()="Next"]')

        self.user['status'] = 3
        self.user_model.update(data={'status':self.user['status']},condition=['id','=',self.user['id']])


        self.write_company_infor()
        self.user['status'] = 5
        self.user_model.update(data={'status':self.user['status']}, condition=['id', '=', self.user['id']])
        self.write_business_infor()
        self.user['status'] = 7
        self.user_model.update(data={'status':self.user['status']}, condition=['id', '=', self.user['id']])
        self.write_shop_infor()
        self.user['status'] = 9
        self.user_model.update(data={'status':self.user['status']}, condition=['id', '=', self.user['id']])
        self.write_tax_infor()
        self.user['status'] = 11
        self.user_model.update(data={'status':self.user['status']}, condition=['id', '=', self.user['id']])
        return True

    # 注册tiktok用户（用手机号）
    def register_by_phone(self):
        self.driver.get('https://seller-us.tiktok.com/settle/verification?is_new_connect=0&shop_region=US')
        print('填写邮箱')
        ele = self.write_input(by=By.ID,condition='phone_email_input',value=self.user['phone'])
        self.driver.execute_script("arguments[0].blur();", ele)
        self.driver.implicitly_wait(1)
        self.btn_click(by=By.XPATH,condition='//div[@class="theme-arco-checkbox-mask"]')
        self.driver.implicitly_wait(1)
        #点击按钮
        self.btn_click(by=By.CLASS_NAME,condition='index__RedButton--xEvbb')
        self.driver.implicitly_wait(10)
        try:
            repeat_time=5
            while (repeat_time > 0):

                sms_result = requests.get(self.user['sms_url'])
                print(sms_result.text)
                sms_content = sms_result.text
                code_search = re.search(r'(\d{4}) is your verification code', sms_content)
                if (code_search):
                    sms_code = code_search.group(1)
                    if (sms_code):
                        for i in range(0, 4):
                            self.write_input(by=By.ID, condition='verificationInput-{}'.format(i), value=sms_code[i])
                        break
                    break
                else:
                    repeat_time -= 1
                    print('无法获取短信验证码，稍后重新获取，剩余尝试次数：{}'.format(repeat_time))
                    time.sleep(60)
        except:
            print('无法获取短信验证码，需人工干预')
        self.driver.implicitly_wait(300)
        # 切换
        self.btn_click(by=By.CLASS_NAME, condition='mt-60')
        # 输入密码
        self.write_input(by=By.XPATH, condition='//input[@type="password"]', value=self.user['pwd'])
        self.write_input(by=By.ID, condition='repeat_password_input', value=self.user['pwd'])
        self.btn_click(by=By.CLASS_NAME, condition='mt-60')

        try:
            self.skip_start_page()
        except:
            pass

        self.btn_click(by=By.XPATH, condition='//div[contains(text(),"Corporation")]')
        self.btn_click(by=By.XPATH, condition='//span[text()="Next"]')

        self.user['status'] = 3
        self.user_model.update(data={'status': self.user['status']}, condition=['id', '=', self.user['id']])

        self.write_company_infor()
        self.user['status'] = 5
        self.user_model.update(data={'status': self.user['status']}, condition=['id', '=', self.user['id']])
        self.write_business_infor()
        self.user['status'] = 7
        self.user_model.update(data={'status': self.user['status']}, condition=['id', '=', self.user['id']])
        return
        self.write_shop_infor_by_phone()
        self.user['status'] = 9
        self.user_model.update(data={'status': self.user['status']}, condition=['id', '=', self.user['id']])
        self.write_tax_infor()
        self.user['status'] = 11
        self.user_model.update(data={'status': self.user['status']}, condition=['id', '=', self.user['id']])
        return True
    #跳过当前页
    def skip_start_page(self):
        print('自动跳转执行')
        wait = WebDriverWait(self.driver,20)
        wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(@class,"w-[350px]")]')))
        # if(re.search(r'https://seller-us.tiktok.com/settle/landing/',self.driver.current_url)):
        self.btn_click(by=By.XPATH,condition='//button[contains(@class,"w-[350px]")]',type=2)

    #填写公司信息
    def write_company_infor(self):
        wait = WebDriverWait(self.driver,100)
        wait.until(EC.presence_of_element_located((By.XPATH,'//input[@placeholder="Enter the business name"]')))
        # self.doownload_html(filename='output/company_infor.html')
        self.write_input(by=By.XPATH,condition='//input[@placeholder="Enter the business name"]',value=self.user['comany_name'])
        #EIN码
        ein_num = self.user['ein'].split('-')
        if(len(ein_num)==2):
            self.write_input(by=By.XPATH,condition='//input[@placeholder="XX"]',value=ein_num[0])
            self.driver.implicitly_wait(random.randint(1,3))
            self.write_input(by=By.XPATH,condition='//input[@placeholder="XXXXXXX"]',value=ein_num[1])
            self.driver.implicitly_wait(random.randint(1,3))

        else:
            print('Ein码读取失败，需人工干预')
            self.driver.implicitly_wait(300)
        self.btn_click(by=By.XPATH,condition='//div[contains(text(),"Yes, this business has at least 1 beneficial owner")]')
        self.driver.implicitly_wait(random.randint(1, 3))

        self.write_input(by=By.XPATH,condition='//input[@placeholder="Street address"]',value=self.user['comnay_addr'])
        self.driver.implicitly_wait(0.5)

        self.btn_click(by=By.XPATH,condition='//div[@id="theme-arco-select-popup-0"]/div/div/li[1]')
        checked = self.driver.find_element(by=By.XPATH,value='//input[@type="checkbox"]')
        if(checked.get_attribute('checked')==None):
            self.btn_click(by=By.XPATH,condition='//span[contains(text(),"I certify that I do not have a business address and only")]')
        self.btn_click(by=By.XPATH,condition='//div[text()="No"]')

        self.driver.implicitly_wait(random.randint(2,5))
        self.btn_click(by=By.XPATH,condition='//span[text()="Next"]')
        print('公司信息输入完成')

        pass
    #填写商家信息
    def write_business_infor(self):
        print('等待页面变化')
        wait = WebDriverWait(self.driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'//div[text()="Business representative"]')))
        print('等待页面变化结束')
        # self.doownload_html(filename='output/business_infor.html')

        print('检查按钮是否存在')

        # if(self.check_ele_exit(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-icon-only")]')):
        #     self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-icon-only")]',type=2)
        #     print('检查按钮存在结束')
        # else:
        #     print('检查按钮不存在')
        #     pass
        print('选择Business representative')
        checked = self.driver.find_element(by=By.XPATH,value='//input[@value="director"]')
        if(checked.get_attribute('checked')==None):
            self.btn_click(by=By.XPATH,condition='//div[text()="Business representative"]')
        print('选择Business representative结束，开始填写姓名')
        self.driver.implicitly_wait(random.randint(1, 3))

        name_list = self.user['realname'].split(' ')
        self.write_input(by=By.XPATH,condition='//input[@placeholder="First name"]',value=name_list[0])
        self.driver.implicitly_wait(1)

        self.write_input(by=By.XPATH,condition='//input[@placeholder="Last name"]',value=name_list[1])
        self.driver.implicitly_wait(random.randint(1, 3))

        print('填写姓名结束，开始填写出生日期')
        birth = str(self.user['birth'])[0:10]
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
                # print(start_year)
                birth_select[2].click()
                self.select_action(by=By.XPATH,condition='//span[contains(text(),"{}")]'.format(start_year))
                # y.click()
                time.sleep(0.1)
                if (start_year == select_year):
                    break
                elif(start_year<select_year):
                    start_year+=1
                else:
                    start_year-=1
            except:
                print(2)
        print('填写出生日期')
        self.driver.implicitly_wait(random.randint(1, 3))

        self.write_input(by=By.XPATH,condition='//input[@placeholder="Street address"]',value=self.user['address'])
        self.driver.implicitly_wait(random.randint(1, 3))

        print('填写地址')
        self.btn_click(by=By.XPATH,condition='//div[@id="theme-arco-select-popup-7"]/div/div/li[1]')
        print('填写SSN')
        self.driver.implicitly_wait(random.randint(1, 3))

        self.write_input(by=By.XPATH,condition='//input[@placeholder="XXXX"]',value=str(self.user['ssn'])[-4:])
        self.driver.implicitly_wait(random.randint(1, 3))

        self.btn_click(by=By.XPATH,condition='//span[text()="Next"]')

        print('商务信息输入完成')
        pass

    def check_ele_exit(self,by,condition):
        try:
            self.driver.find_element(by=by,value=condition)
            return True
        except:
            return False
    # 填写商店信息
    def write_shop_infor(self):
        wait = WebDriverWait(self.driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'//div[text()="Shop name"]')))
        # self.doownload_html(filename='output/shop_infor.html')
        company_list = re.findall(r'[a-z|A-Z]+',self.user['comany_name'])
        company_name= (''.join(company_list))
        if(len(company_list)==0):
            company_name=''
            for i in range(len(self.user['comany_name'])):
                company_name=company_name+self.str_list[random.randint(0,25)]
        self.write_input(by=By.XPATH,condition='//input[contains(@placeholder,"shop name")]',value=company_name)
        self.driver.implicitly_wait(random.randint(1, 3))
        try:
            print('选择店铺类型')
            self.driver.find_element(by=By.XPATH,value='//span[@theme-arco-select-view-selector"]')
            self.btn_click(by=By.XPATH,condition='//span[@class="theme-arco-select-view-selector"]',type=2)
            self.select_action(by=By.XPATH, condition='//span[text()="Fashion Accessories"]')
            print('选择店铺类型结束')
        except:
            print('选择店铺类型异常处理')
            service_type_input = self.driver.find_element(by=By.XPATH,value='//input[@placeholder="Choose the primary product/service type"]')
            if(service_type_input.get_attribute('value')):
                service_type_input.send_keys(Keys.CONTROL + "a")
                service_type_input.send_keys(Keys.DELETE)
            service_type_input.click()
            self.select_action(by=By.XPATH,condition='//span[text()="Fashion Accessories"]')
            print('选择结束')
        # try:
        #     self.driver.find_element(by=By.XPATH,value='//div[text()="Use below"]')
        # except:
        if(re.match(r'Use below',self.driver.page_source)==None):
            print('填写手机号')
            mobie=self.user['phone']
            sms_url = self.user['sms_url']
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
            self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-default")]')
            self.driver.implicitly_wait(7)
            if(self.check_ele_exit(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-large")]')):
                self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-large")]')
            else:
                self.btn_click(by=By.XPATH,
                               condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-default")]')
                self.btn_click(by=By.XPATH,
                               condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-large")]')

        print("店铺信息输入完成")
        #https://seller-us.tiktok.com/homepage
        pass
    # 填写商店信息(手机注册)
    def write_shop_infor_by_phone(self):
        wait = WebDriverWait(self.driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,'//div[text()="Shop name"]')))
        # self.doownload_html(filename='output/shop_infor.html')
        company_list = re.findall(r'[a-z|A-Z]+',self.user['comany_name'])
        company_name= (''.join(company_list))
        if(len(company_list)==0):
            company_name=''
            for i in range(len(self.user['comany_name'])):
                company_name=company_name+self.str_list[random.randint(0,25)]
        self.write_input(by=By.XPATH,condition='//input[contains(@placeholder,"shop name")]',value=company_name)
        self.driver.implicitly_wait(random.randint(1, 3))
        try:
            print('选择店铺类型')
            self.driver.find_element(by=By.XPATH,value='//span[@theme-arco-select-view-selector"]')
            self.btn_click(by=By.XPATH,condition='//span[@class="theme-arco-select-view-selector"]',type=2)
            self.select_action(by=By.XPATH, condition='//span[text()="Fashion Accessories"]')
            print('选择店铺类型结束')
        except:
            print('选择店铺类型异常处理')
            service_type_input = self.driver.find_element(by=By.XPATH,value='//input[@placeholder="Choose the primary product/service type"]')
            if(service_type_input.get_attribute('value')):
                service_type_input.send_keys(Keys.CONTROL + "a")
                service_type_input.send_keys(Keys.DELETE)
            service_type_input.click()
            self.select_action(by=By.XPATH,condition='//span[text()="Fashion Accessories"]')
            print('选择结束')
        # try:
        #     self.driver.find_element(by=By.XPATH,value='//div[text()="Use below"]')
        # except:

        self.driver.implicitly_wait(random.randint(1,3))

        if(re.match(r'Use below',self.driver.page_source)==None):
            print('填写邮箱')

            self.write_input(by=By.XPATH,condition='//input[@placeholder="Enter your email address"]',value=self.user['email'])
            self.driver.implicitly_wait(random.randint(1,3))

            resend_times=5
            while(resend_times>0):

                self.btn_click(by=By.XPATH,condition='//div[text()="Resend code" or text()="Send code"]')
                time.sleep(5)

                code = self.get_verfication_code_by_email(end_time=time.time()-3600)
                if(code):
                    self.write_input(by=By.XPATH,condition='//input[@placeholder="Enter the verification code"]',value=code)
                    break
                else:
                    resend_times-=1
                    print('无法获取邮箱验证码，稍后重新获取，剩余尝试次数：{}'.format(resend_times))
                    time.sleep(60)
            self.driver.implicitly_wait(random.randint(1,3))
            self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-default")]')
            self.driver.implicitly_wait(7)
            if(self.check_ele_exit(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-large")]')):
                self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-large")]')
            else:
                self.btn_click(by=By.XPATH,
                               condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-default")]')
                self.btn_click(by=By.XPATH,
                               condition='//button[contains(@class,"theme-arco-btn-primary theme-arco-btn-size-large")]')

        print("店铺信息输入完成")
        #https://seller-us.tiktok.com/homepage
        pass
    #填写相关文字信息
    def write_tax_infor(self):
        print('开始输入税务信息')
        # self.driver.get('https://seller-us.tiktok.com/homepage?shop_region=US')
        self.btn_click(by=By.XPATH,condition='//p[text()="Add tax information"]/../../following-sibling::*[1]/button',type=2)
        time.sleep(1)
        while 1:
            if(len(self.driver.window_handles)==2):
                break
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.btn_click(by=By.XPATH,condition='//div[text()="Non individual / Entity"]')
        self.btn_click(by=By.XPATH,condition='//input[@placeholder="Select the U.S federal tax classification"]')
        self.select_action(by=By.XPATH,condition='//div[text()="Sole proprietor / Single-member LLC"]')
        try:
            self.btn_click(by=By.XPATH,condition='//label[contains(@class,"theme-arco-checkbox theme-m4b-checkbox")]/descendant::div[contains(text(),"I confirm that I have reviewed the generated tax documents")]')
            self.btn_click(by=By.XPATH,condition='//label[contains(@class,"theme-arco-checkbox theme-m4b-checkbox")]/descendant::div[contains(text(),"I have read the Consent and agree to accept the paperless")]')
        except:
            print('点击失败')
            pass
        self.btn_click(by=By.XPATH,condition='//div[contains(@class,"SubmitBar__ButtonArea-sc-1fu192b-0")]/button[contains(@class,"theme-arco-btn theme-arco-btn-primary")]',type=2)
        self.write_input(by=By.XPATH,condition='//input[@name="signature"]',value=self.user['realname'])
        self.driver.implicitly_wait(3)
        print('提交保存按钮点击')
        self.btn_click(by=By.XPATH,condition='//div[contains(@class,"button-area")]/button[contains(@class,"theme-arco-btn-primary")]')
        self.driver.implicitly_wait(5)
        if(re.match(r'signature',self.driver.page_source)):
            print('重复提交保存按钮点击')
            self.write_input(by=By.XPATH,condition='//input[@name="signature"]',value=self.user['realname'])
            self.btn_click(by=By.XPATH,condition='//button[contains(@class,"theme-arco-btn-primary")]')
    @retry(tries=5,delay=4)
    def write_input(self,by,condition,value):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((by, condition)))
        input = self.driver.find_element(by=by, value=condition)
        if (input.get_attribute('value')):
            input.send_keys(Keys.CONTROL + "a")
            input.send_keys(Keys.DELETE)
        input.send_keys(value)
        return input
        pass
    #选择选项
    def select_action(self,by,condition):
        return self.btn_click(by,condition)
        pass
    #点击事件
    @retry(tries=3, delay=4)
    def btn_click(self,by,condition,type=1):
        print('点击按钮事件处理')
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((by, condition)))
        btn = self.driver.find_element(by=by, value=condition)
        if(type==1):
            self.driver.execute_script("arguments[0].click();", btn)
        else:
            btn.click()
        return btn
        pass
    #验证邮箱
    def get_verfication_code_by_email(self,end_time=0):
        client = imapclient.IMAPClient('outlook.office365.com', port=993)

        client.login(email = self.user['email'], password = self.user['email_pwd'])
        folders = client.list_folders()
        # print(folders)
        # exit(11)
        for f in ['INBOX','Junk']:
            client.select_folder(folder=f)

            messages = client.search(['FROM', 'sellersupport@shop.tiktok.com'])
            # print(messages)
            messages.reverse()
            for _sm in messages:
                msgdict = client.fetch(_sm, ['INTERNALDATE', 'ENVELOPE'])  # 获取邮件内容
                # mailbody = msgdict[_sm][b'BODY[]']
                # print(msgdict[_sm])
                if (end_time <= int(msgdict[_sm][b'INTERNALDATE'].timestamp())):
                    s = re.match(r'([a-z|A-Z|\d]{6}) is your verification code', msgdict[_sm][b'ENVELOPE'].subject.decode())
                    # s = re.search(r'\d{6}', msgdict[_sm][b'ENVELOPE'].subject.decode())
                    if (s != None):
                        print(s.group(1))
                        return s.group(1)

        return None

    #获取邮箱验证码
    def get_register_code(self,email='', password='', end_time=''):
        client = imapclient.IMAPClient('outlook.office365.com', port=993)
        # print(email)
        # print(password)
        client.login(email, password)
        folders = client.list_folders()
        # print(folders)
        # exit(11)
        for f in ['INBOX','Junk']:
            client.select_folder(folder=f)

            messages = client.search(['FROM', 'register@account.tiktok.com'])
            # print(messages)
            messages.reverse()
            for _sm in messages:
                msgdict = client.fetch(_sm, ['INTERNALDATE', 'ENVELOPE'])  # 获取邮件内容
                # mailbody = msgdict[_sm][b'BODY[]']
                # print(msgdict[_sm])
                if (end_time <= int(msgdict[_sm][b'INTERNALDATE'].timestamp())):
                    s = re.search(r'\d{6}', msgdict[_sm][b'ENVELOPE'].subject.decode())
                    if (s != None):
                        print(s.group())
                        return s.group()

        return None
    #登录tiktok
    def login_user(self):
        self.driver.get('https://seller-us-accounts.tiktok.com/account/login')

        pass
    #登出tiktok
    def logout(self):
        self.driver.get('https://seller-us.tiktok.com/passport/web/logout/?next=https%3A%2F%2Fseller-us-accounts.tiktok.com%2Faccount%2Flogin')
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
                # return msgdict[_sm][b'ENVELOPE'].subject.decode()
                s = re.search(r'\d{6}', msgdict[_sm][b'ENVELOPE'].subject.decode())
                if (s != None):
                    print(s.group())
                    return s.group()
            return None
        return None
        pass

    def doownload_html(self,filename=''):
        with open(filename,'w',encoding='utf-8') as f:
            f.write(self.driver.page_source)
            f.close()

