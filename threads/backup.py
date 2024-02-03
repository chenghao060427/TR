from PyQt5.QtCore import QThread,pyqtSignal
from model.phone_backup import phone_backup
from model.email_backup import email_backup
from func.reserve_email import email_check
class import_phone_backup_thread(QThread):
    #表格和数据库字典

    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,filename=None,pro_win=None):
        super().__init__()
        self.filename=filename
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.phone_model=phone_backup()
    def run(self):
        with open(self.filename) as f:
            infor_list = []
            for i in f:
                infor_list.append(i.replace('\n','').replace('\t',' '))

            total = len(infor_list)
            print(infor_list)
            if(total==0):total=1
            i=0
            for infor in infor_list:
                phone,sms_url = infor.split('----')
                data={'phone':phone,'sms_url':sms_url,'status':1}

                if(self.phone_model.count(condition=['phone','=',phone])==0):
                #     print(keyword)
                    if(self.phone_model.create(data)):
                        self.msg_sig.emit('第{}条数据导入成功'.format(i+1))
                        self.pro_sig.emit(int((i+1)*100/total))
                        i+=1
                    else:
                        self.msg_sig.emit('第{}条数据导入失败'.format(i+1))
class import_email_backup_thread(QThread):
    #表格和数据库字典

    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,filename=None,pro_win=None):
        super().__init__()
        self.filename=filename
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.email_model=email_backup()
    def run(self):
        with open(self.filename) as f:
            infor_list = []
            for i in f:
                infor_list.append(i.replace('\n','').replace('\t',' '))

            total = len(infor_list)
            print(infor_list)
            if(total==0):total=1
            i=0
            for infor in infor_list:
                email,email_pwd = infor.split('----')
                data={'email':email,'email_pwd':email_pwd,'status':1}

                if(self.email_model.count(condition=['email','=',email])==0 and (email_check(data['email'],data['email_pwd']))):
                #     print(keyword)
                    if(self.email_model.create(data)):
                        self.msg_sig.emit('第{}条数据导入成功'.format(i+1))
                        self.pro_sig.emit(int((i+1)*100/total))
                        i+=1
                    else:
                        self.msg_sig.emit('第{}条数据导入失败'.format(i+1))
class check_email_backup_thread(QThread):
    #表格和数据库字典

    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,pro_win=None):
        super().__init__()
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
        self.email_model=email_backup()
    def run(self):
        email_list= self.email_model.select(condition=['status','=',1])

        total = len(email_list)
        print(email_list)
        if(total==0):total=1
        i=0
        for email in email_list:

            if(email_check(email['email'],email['email_pwd'])):
            #     print(keyword)
                self.msg_sig.emit('邮箱：{}可以使用'.format(email['email']))
            else:
                self.msg_sig.emit('邮箱：{}登录失败'.format(email['email']))
                self.email_model.update(data={'status':3},condition=['id','=',email['id']])
            i += 1
            self.pro_sig.emit(int((i + 1) * 100 / total))