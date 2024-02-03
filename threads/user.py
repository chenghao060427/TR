import random
import time,re
import imapclient
from PyQt5.QtCore import QThread,pyqtSignal
import pandas as pd
from model.user import user
from model.email_backup import email_backup
from actions.ads_browser import ads_browser,browserException
from actions.tiktok import tiktok_service
from func.reserve_email import check_account_status,email_check

class import_user_thread(QThread):
    #表格和数据库字典
    dk_xk_dir={
        'email':'邮箱',
        'email_pwd':'邮箱密码',
        'backup_email':'备用邮箱',
        'backup_email_url':'备用邮箱链接',
        'realname':'名字',
        'pwd':'账户密码',
        'birth':'生日',
        'address':'地址',
        'ssn':'SSN',
        'comany_name':'公司名称',
        'ein':'EIN码',
        'comnay_addr':'公司地址',

    }
    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,filename=None,pro_win=None):
        super().__init__()
        self.filename=filename
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.user=user()
    def run(self):
        i_user_list = pd.read_excel(self.filename)
        i_user_list.reset_index()
        if('Unnamed: 12' in i_user_list.columns):
            i_user_list['名字']=i_user_list['名字']+' '+i_user_list['Unnamed: 12'].apply(str)
        total = len(i_user_list)

        if(total==0):total=1

        for i,user in i_user_list.iterrows():
            data={}
            for k in self.dk_xk_dir:
                data[k]=str(user[self.dk_xk_dir[k]])

            data['birth']=str(data['birth'])
            data['address']=re.sub(r'[ \xa0]+',' ',data['address'])
            data['ssn'] = re.sub('-','',data['ssn'])
            data['comnay_addr']=re.sub(r'[ \xa0]+',' ',data['comnay_addr'])
            phone,sms_url = user['电话号码'].split('----')
            data['phone']=phone
            data['sms_url']=sms_url
            data['status']=1
            data['created_at']= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data['updated_at']= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            if(self.user.create(data)):
                self.msg_sig.emit('第{}条数据导入成功'.format(i+1))
                self.pro_sig.emit(int((i+1)*100/total))
            else:
                self.msg_sig.emit('第{}条数据导入失败'.format(i+1))
class register_user_thread_dispatch(QThread):
    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,r_type='',count=0,pro_win=None,thread_count=1):
        super().__init__()
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.user_model = user()
        self.count = count
        self.r_type = r_type
        self.thread_count=thread_count
        self.thread_list = []
        self.user_iter = self.get_regitser_user_iter(num=int(self.count))
        print(777)
    def run(self):
        if(self.count==0):
            self.msg_sig.emit('0用户注册')
            self.pro_sig.emit(100)
            return

        for i in range(self.thread_count):
            t = register_user_thread(r_type=self.r_type,count=self.count,pro_win=self.pro_win,user_iter=self.user_iter)
            self.thread_list.append(t)
            t.start()

    def get_regitser_user_iter(self,num=1):
        print(93)
        index = 0
        user_list = self.user_model.select(condition=['status', '=', 1], limit='0,{}'.format(str(num)))
        print(user_list)
        # self.msg_sig.emit('共获取到{}个用户信息'.format(len(user_list)))
        self.count = len(user_list)
        for u in user_list:
            index+=1
            yield u,index
class register_user_thread(QThread):
    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,r_type='',count=0,pro_win=None,user_iter=[]):
        super().__init__()
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.user=user()
        self.count=count
        self.r_type=r_type
        self.browser = ads_browser()
        self.user_iter = user_iter

    def run(self):
        if(self.count==0):
            self.msg_sig.emit('0用户注册')
            self.pro_sig.emit(100)
            return
        # user_list = self.user.select(condition=['status','=',1],limit='0,{}'.format(self.count))
        # print(user_list)
        # print(self.browser.search_group(query=''))
        # self.msg_sig.emit('共获取到{}个用户信息'.format(len(user_list)))
        # i=0
        # total = len(user_list)
        # if(total==0):total=1
        # print(127)
        for u,i in self.user_iter:
            try:
                if(self.user_email_check(u)==False):
                    continue
                account_infor = {
                    'name': u['email'],
                    'domain_name': 'https://seller-us.tiktok.com',
                    'username': u['email'],
                    'password': u['email_pwd'],
                    'group_id': '3492708',
                    'country': 'us',
                    'regin': 'new york',
                    'user_proxy_config': {"proxy_soft": "922S5"},
                    'fingerprint_config': {
                        'automatic_timezone': 1,
                        'webrtc': 'proxy',
                        'location_switch': 1,
                        'language': ["en-US", "en"],
                        'browser_kernel_config': {"version": "120", "type": "chrome"}
                    }
                }
                if(len(self.browser.search_account({'group_id':'3492708','page_size':100,'user_id':u['browser_account']}))==0):

                    # print(u)
                    u['browser_account'] = self.browser.create_account(account_infor=account_infor)
                    self.user.update(data=u, condition=['id', '=', u['id']])
                    # u['browser_account'] = 'jdc1ree'
                else:
                    account_infor['user_id']=u['browser_account']
                    self.browser.update_account(account_infor=account_infor)

                driver = self.browser.get_driver(u['browser_account'])
                t_service = tiktok_service(user=u,driver=driver,thr=self)
                if(self.r_type=='邮箱注册'):
                    result = t_service.register()
                else:
                    result = t_service.register_by_phone()
                if(result==True):
                    t_service.logout()
                    self.msg_sig.emit('第{}个用户注册成功'.format(i))
                    self.pro_sig.emit(int((i)*100/self.count))
                # if(u[''])
            except browserException as e:
                print(e.message)
                self.msg_sig.emit(e.message)
            finally:
                self.user.update(data=u,condition=['id','=',u['id']])
                continue
    def user_email_check(self,user):
        if(email_check(user['email'],password=user['email_pwd'])):
            self.msg_sig.emit('用户{}:登录成功'.format(user['email']))
            return True
        else:
            self.msg_sig.emit('用户{}:登录失败,替换邮箱'.format(user['email']))
            b_email_list = email_backup().select(condition=['status','=',1],limit='0,1')
            if(len(b_email_list)):
                user['email']=b_email_list[0]['email']
                user['email_pwd']=b_email_list[0]['email_pwd']
                self.user.update(user,condition=['id','=',user['id']])
                return True

            else:
                self.msg_sig.emit('用户{}:登录失败,替换邮箱失败'.format(user['email']))
                return False

class reflash_user(QThread):
    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,pro_win=None,user_iter=[]):
        super().__init__()
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.user_iter = user_iter
        self.user_model = user()
    def run(self):

        self.msg_sig.emit('共获取到{}个用户信息'.format(len(self.user_iter)))
        i = 0
        print(147)
        total = len(self.user_iter)
        if (total == 0): total = 1
        for u in self.user_iter:
            try:
            # client.login(u['email'], u['email_pwd'])
                result = check_account_status(email=u['email'],password=u['email_pwd'])
                if(result==True):
                    self.user_model.update({'status':13},condition=['id','=',u['id']])
                    self.msg_sig.emit('用户:{}店铺正常'.format(u['email']))
                elif(result==False):
                    self.user_model.update({'status': 17}, condition=['id', '=', u['id']])
                    self.msg_sig.emit('用户:{}店铺关闭'.format(u['email']))
                else:
                    self.msg_sig.emit('用户:{}未收到邮件'.format(u['email']))
                i+=1
            except:
                self.msg_sig.emit('用户:{}登录失败'.format(u['email']))
            finally:
                time.sleep(random.uniform(0.3, 1.1))
                self.pro_sig.emit(int((i) * 100 / total))
                continue
