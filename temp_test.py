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

from threads.comany import get_comany_thread
import re
s = 'j89t7m is your verification code'
r = re.match(r'([a-z|A-Z|\d]{6}) is your verification code',s)
print(r.group(1))
exit(1)
"true|[TikTok] 7397 is your verification code, valid for 5 minutes. To keep your account safe, never forward this code.|过期时间：2024-03-08 23:00:00"
c_t = get_comany_thread(count=10)
c_t.start()
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
# from threading import Thread
# class c_y():
#     def t_yield(self):
#         for i in range(20):
#             yield i
#
# class t(Thread):
#     def __init__(self,y):
#         Thread.__init__(self)  # 必须步骤
#         self.y= y
#     def run(self):
#         for i in self.y:
#             time.sleep(4)
#             print(i)
#
# # try:
# c_y = c_y()
# y=c_y.t_yield()
# t1 = t(y=y)
# t2 = t(y=y)
# t1.start()
# t2.start()
# # except:
# #     print("Error: unable to start thread")
# exit(123)
# while 1:
#     pass
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