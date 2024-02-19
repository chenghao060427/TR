import time

from actions.ads_browser import ads_browser,browserException
import model.user
from model.company_keyword import company_keyword
from actions.tiktok import tiktok_service
from actions.ads_browser import ads_browser
import random
import logging
import os
import subprocess
from retry import retry
import _thread
import pandas as pd
import json
from model.company_used import company_used
from model.user import user
from threads.comany import get_comany_thread
import re
# j = {'code': 0, 'message': '', 'data': {'captchaId': '2301-66cca14b-c52a-422f-84fd-11f736b38617', 'captchaType': '2301', 'recognition': '175,171|85,168'}}
# pos1,pos2 = j['data']['recognition'].split('|')
# pos1_x,pos1_y = pos1.split(',')
# pos2_x,pos2_y = pos2.split(',')
# print(j['code'])
# print(type(json.dumps(j)))
# comany_u = company_used()
# comany_u.count(condition=['ein','=','0'])
# exit()
# config = json.load(open('.env','r',encoding='utf-8'))
# print(config)
# user = model.user.user()
# user.select(condition='status in  (15,17)')
# # t_list = [1,2,3,4]
# # del(t_list[-2:])
# # print(t_list)
# # exit(1)
# user_list = pd.read_excel('input/0122-01.xls')
# user_list.reset_index()
# if('Unnamed: 12' in user_list.columns):
#     user_list['名字']=user_list['名字']+user_list['Unnamed: 12']
# print(user_list['名字'])
# exit(1)
# d = list(range(100,80,-1))
# print(d)
# exit(91)
from threading import Thread
import threading
r = re.sub(r'\s+',' ','5400 Volunteer Road             Southwest Ranches, FL 33330 ')
print(r)
exit(111)
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
class c_y(Thread):
    d = list(range(100,80,-1))
    def __init__(self):
        Thread.__init__(self)
        self.thread_list=[]
    def run(self):

        self.it = threadsafe_generator(self.t_yield(20))
        # for i in self.it:
            # print(i)
        # return
        for i in range(3):
            ct = t(y=self.it)
            ct.start()
            self.thread_list.append(ct)

    def t_yield(self,count=1):
        for i in range(count):
            yield i,self.d[i]
    # def get_regitser_user_iter(self,num=1):
    #     print(93)
    #     index = 0
    #     self.user_model = user()
    #     user_list = self.user_model.select(condition=['status', '=', 1], limit='0,{}'.format(str(num)))
    #     print(user_list)
    #     self.count = len(user_list)
    #     for u in user_list:
    #         index+=1
    #         yield u,index
class t(Thread):

    def __init__(self,y):
        Thread.__init__(self)  # 必须步骤
        self.y= y
    def run(self):
        for i,k in self.y:
            time.sleep(random.randint(0,4))
            print(i)
            self.test('steer')
            print(k)
    def test(self,s):
        print(s)
#
# # try:
c_y = c_y()
c_y.start()
# y=c_y.get_regitser_user_iter(20)
# t1 = t(y=y)
# t2 = t(y=y)
# t1.start()
# t2.start()
# except:
#     print("Error: unable to start thread")
# exit(123)
while 1:
    pass
# # class r:
# #     @retry(tries=3,delay=1)
# #     def test(self):
# #         print(1312)
# #         raise Exception
# #
# # r1 = r()
# # r1.test()
# # path =os.path.join('output','company2024-01-03-14-40-44.csv')
# # print(path)
# # os.startfile(path)
# exit()
# #
# # keyword_model = comany_keyword()
# # name_list = keyword_model.select(order='id asc')
# # random.shuffle(name_list)
# # print(name_list)
# # exit()
# user = model.user.user()
# browser = ads_browser()
#
# user_list = user.select(condition=['status', '=', 1], limit='0,1')
# for u in user_list:
#     # try:
#     if (u['browser_account'] == None):
#         account_infor = {
#             'name': u['email'],
#             'domain_name': 'https://seller-us.tiktok.com',
#             'username': u['email'],
#             'password': u['email_pwd'],
#             'group_id': '3492708',
#             'country': 'us',
#             'regin': 'new york',
#             'user_proxy_config': {"proxy_soft": "922S5"},
#             'fingerprint_config': {
#                 'automatic_timezone': 1,
#                 'webrtc': 'proxy',
#                 'location_switch': 1,
#                 'language': ["en-US", "en"],
#             }
#         }
#         print(u)
#         u['browser_account'] = browser.create_account(account_infor=account_infor)
#         user.update(data=u, condition=['id', '=', u['id']])
#     driver = browser.get_driver(u['browser_account'])
#     t_service = tiktok_service(user=u, driver=driver)
#     result = t_service.register()
# # print(user_list)
# # print(browser.search_group(query=''))  https://seller-us.tiktok.com/settle/landing/
# i = 0
# total = len(user_list)
# if (total == 0): total = 1
# for u in user_list:
#     u['browser_account']='jdbd88g'
#     user.update(data=u, condition=['id', '=', u['id']])
#     exit(1)
#     try:
#         if (u['browser_account'] == None):
#             account_infor = {
#                 'name': u['email'],
#                 'domain_name': 'https://seller-us.tiktok.com',
#                 'username': u['email'],
#                 'password': u['email_pwd'],
#                 'group_id': '3492708',
#                 'country':'us',
#                 'user_proxy_config': {"proxy_soft": "922S5"},
#                 'fingerprint_config': {
#                     'automatic_timezone': 1,
#                     'webrtc': 'proxy',
#                     'location_switch': 1,
#                     'language': ["en-US", "en"],
#                 }
#             }
#             u['browser_account'] = browser.create_account(account_infor=account_infor)
#             user.update(data=u, condition=['id', '=', u['id']])
#         driver = browser.get_driver(u['browser_account'])
#         t_service = tiktok_service(user=u, driver=driver)
#         result = t_service.register()
#         if (result == True):
#             i += 1
#         # if(u[''])
#     except browserException as e:
#         print(e.message)
#     except Exception as e:
#         print(e)
#     finally:
#         continue