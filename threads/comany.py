import time,re

from PyQt5.QtCore import QThread,pyqtSignal
import pandas as pd
from urllib.parse import urljoin
from model.company_keyword import company_keyword
from func.search_xpath import get_company_list,get_company_detail
from actions.ads_browser import ads_browser
import random
import os
from model.company_used import company_used
import threading


class threadsafe_generator:
    """Takes an generator and makes it thread-safe by
    serializing call to the `next` method of given generator.
    """
    def __init__(self, gen):
        self.gen = gen
        self.lock = threading.Lock()

    def __iter__(self):

        return self

    def __next__(self):
        # print(60)
        with self.lock:
            return self.gen.__next__()



class get_company_dispatch(QThread):
    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,company_num =0,pro_win=None):
        super().__init__()
        self.company_num=company_num
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.keyword_db=company_keyword()
        self.thread_list = []
        self.company_list = []
        self.success_num=0
    def run(self):
        self.keyword_iter = threadsafe_generator(self.chose_keyword(int(self.company_num/10)+1))
        # for index,k in keyword_iter:
            # print(k)
        # return
        log_file = 'output/company' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.csv'
        browser = ads_browser()
        bro_user_list = browser.search_account(query={'group_id':'3492708','page_size':100})
        d_ids = []
        for a in bro_user_list:
            d_ids.append(a['user_id'])
        if(len(d_ids)>0):
            browser.del_account(user_infor=d_ids)
        thread_count = int(self.company_num/600)+1
        for i in range(thread_count):
            account_infor = {
                'name': '公司信息采集{}'.format(i),
                'domain_name': 'https://search.sunbiz.org/',
                'username': 'account{}'.format(i),
                'password': 'pwd{}'.format(i),
                'group_id': '3492708',
                'country': 'us',
                'regin': 'new york',
                'user_proxy_config': {
                    "proxy_soft":"other",
                    "proxy_type":"http",
                    "proxy_host":"na.ad940239e17dbd86.ipmars.vip",
                    "proxy_port":"4900",
                    "proxy_user":"igSkDT0mOS-zone-mars-region-US",
                    "proxy_password":"45959743"
                },
                'fingerprint_config': {
                    'automatic_timezone': 1,
                    'webrtc': 'proxy',
                    'location_switch': 1,
                    'language': ["en-US", "en"],
                    'browser_kernel_config': {"version": "120", "type": "chrome"}
                }
            }
            bro_account = browser.create_account(account_infor)
            t = get_comany_thread(keyword_iter= self.keyword_iter,
                                  pro_win = self.pro_win,
                                  bro_account=bro_account,
                                  count=self.company_num,
                                  log_file=log_file,
                                  save_list=self.company_list,
                                  p_thread=self
                                  )
            self.thread_list.append(t)
            t.start()
        pass

    def chose_keyword(self,num=0):
        min_times = self.keyword_db.select(colunm='min(times)');
        current_times = min_times[0]['min(times)']
        keyword_list = []
        total_num = num
        last_num = num
        while (total_num > len(keyword_list)):
            re_keyword_list = self.keyword_db.select(condition=['times', '=', current_times])
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
            current_times += 1

        for index in range(num):
            yield index, keyword_list[index]

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
        self.keyword_db=company_keyword()
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
    def __init__(self,keyword_iter=[],pro_win=None,bro_account=None,count=0,log_file='',save_list=[],p_thread=None):
        super().__init__()
        self.count = count
        self.keyword_iter=keyword_iter
        self.pro_win = pro_win
        self.bro_account=bro_account
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.log_file = log_file
        self.save_list=save_list
        self.keyword_db = company_keyword()
        self.p_thread = p_thread
    def run(self):

        # log_file = 'output/company'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+'.csv'
        try:
            browser = ads_browser()
            driver = browser.get_driver(self.bro_account)
            base_url = 'https://search.sunbiz.org/'
            log_file = 'output/company'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+'.csv'
            total_times=self.count


            f_start_url = "https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults/EntityName/{}/Page1?searchNameOrder={}"

            company_used_model = company_used()
            # name = f.readline()
            # n = re.sub(r'\s?','',name)
            # n = n.upper()
            # print(148)
            for index,name in self.keyword_iter:
                # print(name)
                print(index)
                # continue

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
                        company['address']=re.sub(r'\s+',' ',company['address'])
                        # print(company)
                        # print(type(company['name']))
                        # print(type(company['address']))
                        # exit(1)
                        if (re.match(r'^\d{2}-\d{7}$', company['ein']) and company_used_model.count(condition=['ein','=',company['ein']])==0):
                            times -= 1
                            total_times -= 1
                            # print(times)
                            # print(total_times)
                            self.save_list.append(company)

                            company_used_model.create(company)
                            self.p_thread.success_num+=1
                            self.msg_sig.emit('第{}条信息采集成功'.format(self.p_thread.success_num))
                            self.pro_sig.emit(int(self.p_thread.success_num * 100 / self.count))
                    start_url = urljoin(base_url, next_href)
                self.keyword_db.update(data={'tiems':int(name['times'])+1},condition=['id','=',name['id']])
                df = pd.DataFrame(self.save_list)
                df.to_csv(self.log_file)
        except Exception as e:
            print(e)
        finally:
            # print(company_list)
            driver.close()
            self.msg_sig.emit('公司信息采集完成，共采集到{}条公司信息,保存到{}'.format((self.count-total_times),log_file))
            df = pd.DataFrame(self.save_list)
            df.to_csv(self.log_file)
            # os.startfile(self.log_file.replace('/','\\'))

        pass