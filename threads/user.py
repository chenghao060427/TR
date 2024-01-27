import time,re
import imapclient
from PyQt5.QtCore import QThread,pyqtSignal,QMutex
import pandas as pd
from model.user import user
from actions.ads_browser import ads_browser,browserException
from actions.tiktok import tiktok_service
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

class register_user_thread(QThread):
    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,r_type='',count=0,pro_win=None):
        super().__init__()
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.user=user()
        self.count=count
        self.r_type=r_type
        self.browser = ads_browser()
    def run(self):
        if(self.count==0):
            self.msg_sig.emit('0用户注册')
            self.pro_sig.emit(100)
            return
        user_list = self.user.select(condition=['status','=',1],limit='0,{}'.format(self.count))
        print(user_list)
        # print(self.browser.search_group(query=''))
        self.msg_sig.emit('共获取到{}个用户信息'.format(len(user_list)))
        i=0
        total = len(user_list)
        if(total==0):total=1
        for u in user_list:
            try:
                if(u['browser_account']==None):
                    account_infor={
                        'name':u['email'],
                        'domain_name':'https://seller-us.tiktok.com',
                        'username':u['email'],
                        'password':u['email_pwd'],
                        'group_id':'3492708',
                        'country':'us',
                        'regin':'new york',
                        'user_proxy_config':{"proxy_soft":"922S5"},
                        'fingerprint_config':{
                            'automatic_timezone':1,
                            'webrtc':'proxy',
                            'location_switch':1,
                            'language':["en-US","en"],
                        }
                    }
                    print(u)
                    u['browser_account'] = self.browser.create_account(account_infor=account_infor)
                    # u['browser_account'] = 'jdc1ree'

                    self.user.update(data=u, condition=['id', '=', u['id']])
                driver = self.browser.get_driver(u['browser_account'])
                t_service = tiktok_service(user=u,driver=driver)
                if(self.r_type=='邮箱注册'):
                    result = t_service.register()
                else:
                    result = t_service.register_by_phone()
                if(result==True):
                    i+=1
                    t_service.logout()
                    self.msg_sig.emit('第{}个用户注册成功'.format(i))
                    self.pro_sig.emit(int((i)*100/total))
                # if(u[''])
            except browserException as e:
                print(e.message)
                self.msg_sig.emit(e.message)
            finally:
                self.user.update(data=u,condition=['id','=',u['id']])
                continue
class reflash_user(QThread):
    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,pro_win=None,user_iter=[]):
        super().__init__()
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.user_iter = user_iter

    def run(self):
        client = imapclient.IMAPClient('outlook.office365.com', port=993)
        for u in self.user_iter:
            client.login(u['email'], u['email_pwd'])
            #接受邮件判断店铺状态
            for f in ['INBOX','Junk']:
                client.select_folder(folder=f)

                messages = client.search(['FROM', 'register@account.tiktok.com'])
                # client.select_folder(folder='Inbox')

                # messages = client.search(['FROM','sellersupport@shop.tiktok.com'])
                print(messages)
                messages.reverse()
                for _sm in messages:
                    msgdict = client.fetch(_sm, ['INTERNALDATE', 'ENVELOPE'])  # 获取邮件内容
                    # mailbody = msgdict[_sm][b'BODY[]']
                    # print(msgdict[_sm][b'ENVELOPE'])

                    return msgdict[_sm][b'ENVELOPE'].subject.decode()
            client.logout()


