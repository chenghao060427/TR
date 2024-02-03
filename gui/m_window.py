import sys
from PyQt5.QtWidgets import QMainWindow , QApplication
from PyQt5.QtWidgets import QAction,QLineEdit,QFormLayout,QVBoxLayout,QHBoxLayout,QLabel
from PyQt5.QtWidgets import QMainWindow,QDesktopWidget,QApplication,QInputDialog,QStatusBar,QPushButton,QWidget
from .user.window import user_window
from .company.window import keyword_window
from .process_window import process_window
from threads.comany import get_comany_thread
from threads.ads_browser import account_check_thread
from .backup.phone import phone_window
from .backup.email import email_window
import json
class m_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_action()
        self.connect_action()
        self.show()
        self.user_win=None,
        self.keyword_win=None

    def init_ui(self):
        self.resize(1200, 800)
        #控制窗口显示在屏幕中心的方法
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('TikTok管理系统1.0')
        pass
    #
    def init_action(self):
        #公司信息菜单栏
        bar = self.menuBar()
        company_menu = bar.addMenu('公司信息管理')
        self.com_keywords_action = QAction('关键词管理',self)
        self.com_infor_action=QAction('获取公司信息',self)
        company_menu.addActions([self.com_keywords_action,self.com_infor_action])
        #用户信息管理
        user_menu = bar.addMenu('用户信息管理')
        self.user_infor_action = QAction('用户信息',self)
        self.ads_reflash_action=QAction('ads浏览器账号释放',self)
        user_menu.addActions([self.user_infor_action,self.ads_reflash_action])
        #备份信息
        backup_menu = bar.addMenu('备份信息管理')
        self.phone_backup_action = QAction('手机号备份')
        self.email_backup_action = QAction('邮箱备份')
        self.config_action = QAction('运行信息设置')
        backup_menu.addActions([self.phone_backup_action,self.email_backup_action,self.config_action])


        pass
    #绑定动作
    def connect_action(self):
        self.user_infor_action.triggered.connect(self.show_user_window)
        self.ads_reflash_action.triggered.connect(self.ads_reflash)
        self.com_keywords_action.triggered.connect(self.show_keyword_window)
        self.com_infor_action.triggered.connect(self.show_comany_dialog)
        self.phone_backup_action.triggered.connect(self.show_phone_backup)
        self.email_backup_action.triggered.connect(self.show_email_backup)
        self.config_action.triggered.connect(self.show_config_form)
        pass
    def ads_reflash(self):
        self.pro_win = process_window(p_win=self, f_sig=1)
        self.af_thread = account_check_thread(pro_win=self.pro_win)
        self.af_thread.start()

    def show_phone_backup(self):
        window = phone_window(p_win=self)
        self.setCentralWidget(window)
        pass
    def show_email_backup(self):
        window = email_window(p_win=self)
        self.setCentralWidget(window)
        pass
    def show_comany_dialog(self):
        num, ok = QInputDialog.getInt(self, "新注册用户数", "输入数量", value=600, min=0, max=600)
        if ok:
            self.pro_win = process_window(p_win=self, f_sig=1)
            self.gc_thread = get_comany_thread(count=num, pro_win=self.pro_win)
            self.gc_thread.start()
    def show_user_window(self):

        # if(self.user_win==None):
        self.user_win = user_window(p_win=self)
        self.setCentralWidget(self.user_win)
    def show_keyword_window(self):

        # if(self.keyword_win==None):
        self.keyword_win = keyword_window(p_win=self)

        self.setCentralWidget(self.keyword_win)
    def finish_thread(self,f_sig):
        pass
    def show_config_form(self):
        self.con_win = config_form(self)
        pass
class config_form(QWidget):

    def __init__(self,p_window=None):
        self.p_win =p_window
        super().__init__()
        self.resize(400,100)
        self.config = json.load(open('.env', 'r', encoding='utf-8'))
        self.setWindowTitle("运行环境信息编辑")
        keys =self.config.keys()
        formlayout = QFormLayout()
        for key in self.config.keys():
            input = QLineEdit()
            input.setText(self.config[key])
            exec(f'self.{key} = input')
            exec(f'formlayout.addRow(QLabel("{key}"),self.{key})')
            print(self.config[key])

        vlayout = QVBoxLayout(self)
        vlayout.addLayout(formlayout)

        s_btn = QPushButton('保存')
        s_btn.setFixedWidth(100)
        c_btn = QPushButton('取消')
        c_btn.setFixedWidth(100)
        hlayout = QHBoxLayout(self)
        hlayout.addWidget(s_btn,stretch=0)
        hlayout.addWidget(c_btn,stretch=0)
        vlayout.addLayout(hlayout,stretch=1)
        s_btn.clicked.connect(self.sure)
        c_btn.clicked.connect(self.cancle)
        self.show()
    def cancle(self):
        self.close()
    def sure(self):
        for key in self.config.keys():
            # print(f'self.config[{key}]= self.{key}.text()')
            exec(f'self.config["{key}"]= self.{key}.text()')
        json.dump(self.config,open('.env', 'w', encoding='utf-8'))
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = m_window()
    main.show()
    sys.exit(app.exec_())