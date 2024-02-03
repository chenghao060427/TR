import time

from PyQt5.QtCore import QThread,pyqtSignal
from actions.ads_browser import ads_browser,browserException
from model.user import user
class account_check_thread(QThread):
    msg_sig = pyqtSignal(str)
    pro_sig = pyqtSignal(int)
    def __init__(self,pro_win=None):
        super().__init__()
        self.pro_win = pro_win
        self.msg_sig.connect(self.pro_win.add_msg)
        self.pro_sig.connect(self.pro_win.process_set)
    def run(self):
        browser = ads_browser()
        user_model = user()
        account_list = browser.search_account(query={'group_id': '3492708', 'page_size': 100})
        count = len(account_list)
        if(count==0):
            self.msg_sig.emit('暂无账号')
            self.pro_sig.emit(100)
        d_ids=[]
        i=0
        for a in account_list:
            if(user_model.count(condition=[['status','=',1],['browser_account','=',a['user_id']]])==0):
                d_ids.append(a['user_id'])
                self.msg_sig.emit('账号：{}可以删除'.format(a['user_id']))
            else:
                self.msg_sig.emit('账号：{}正在使用'.format(a['user_id']))
            i+=1
            self.pro_sig.emit(i * 100 / count)
        # print(d_ids)
        if(len(d_ids)):
            browser.del_account(user_infor=d_ids)
            self.msg_sig.emit('删除{}个账号'.format(len(d_ids)))

