import time,re

from PyQt5.QtCore import QThread,pyqtSignal,QMutex
import pandas as pd
from urllib.parse import urljoin
from model.comany_keyword import comany_keyword
from func.search_xpath import get_company_list,get_company_detail
from actions.ads_browser import ads_browser
import random
import os
class import_keyword_thread(QThread):
    #表格和数据库字典

    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,filename=None,pro_win=None):
        super().__init__()
        self.filename=filename
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.keyword_db=comany_keyword()
    def run(self):
        with open(self.filename) as f:
            keyword_list = []
            for i in f:
                keyword_list.append(i.replace('\n','').replace('\t',' '))

            total = len(keyword_list)
            print(keyword_list)
            if(total==0):total=1
            i=0
            for keyword in keyword_list:

                data={'value':keyword}
                print(self.keyword_db.count(condition=['value','=',str(keyword)]))
                if(self.keyword_db.count(condition=['value','=',keyword])==0):
                #     print(keyword)
                    if(self.keyword_db.create(data)):
                        self.msg_sig.emit('第{}条数据导入成功'.format(i+1))
                        self.pro_sig.emit(int((i+1)*100/total))
                        i+=1
                    else:
                        self.msg_sig.emit('第{}条数据导入失败'.format(i+1))

class get_comany_thread(QThread):
    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,count=0,pro_win=None):
        super().__init__()
        self.count=count
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.keyword_db=comany_keyword()
    def run(self):

        # log_file = 'output/company'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+'.csv'
        try:
            browser = ads_browser()
            driver = browser.get_driver('jdc1ree')
            base_url = 'https://search.sunbiz.org/'
            log_file = 'output/company'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+'.csv'
            total_times=self.count
            company_list=[]

            f_start_url = "https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults/EntityName/{}/Page1?searchNameOrder={}"

            keyword_model = comany_keyword()
            name_list = keyword_model.select(order='id asc')
            random.shuffle(name_list)

            # name = f.readline()
            # n = re.sub(r'\s?','',name)
            # n = n.upper()
            for name in name_list:
                if(total_times<=0):
                    break
                times=10
                n = re.sub(r'\s?','',name['value'])
                n = n.upper()
                start_url=f_start_url.format(n,n)
                while (times > 0):
                    driver.get(start_url)
                    time.sleep(random.randint(1,2))
                    # 分析页面内容
                    href_list, next_href = get_company_list(driver.page_source)
                    for h in href_list:
                        time.sleep(1)
                        driver.get(urljoin(base_url, h))
                        company = get_company_detail(driver.page_source)
                        if (re.match(r'^\d{2}-\d{7}$', company['ein'])):
                            times -= 1
                            total_times -= 1
                            print(times)
                            print(total_times)
                            company_list.append(company)
                            self.msg_sig.emit('第{}条信息采集成功'.format(self.count-total_times))
                            self.pro_sig.emit(int((self.count-total_times) * 100 / self.count))
                    start_url = urljoin(base_url, next_href)

        finally:
            # print(company_list)
            driver.close()
            self.msg_sig.emit('公司信息采集完成，共采集到{}条公司信息,保存到{}'.format((self.count-total_times),log_file))
            df = pd.DataFrame(company_list)
            df.to_csv(log_file)
            os.startfile(log_file.replace('/','\\'))

        pass