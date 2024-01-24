import sys
from PyQt5.QtWidgets import QMainWindow , QApplication
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMainWindow,QDesktopWidget,QApplication,QInputDialog,QStatusBar
from .user.window import user_window
from .company.window import keyword_window
from .process_window import process_window
from threads.comany import get_comany_thread
import subprocess
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
        self.user_infor_import_action=QAction('用户信息导入',self)
        user_menu.addActions([self.user_infor_action,self.user_infor_import_action])
        #tiktok菜单栏
        tiktok_menu = bar.addMenu('TikTok管理')
        self.tiktok_register_action = QAction('用户注册')
        tiktok_menu.addActions([self.tiktok_register_action])
        pass
    #绑定动作
    def connect_action(self):
        self.user_infor_action.triggered.connect(self.show_user_window)
        self.com_keywords_action.triggered.connect(self.show_keyword_window)
        self.com_infor_action.triggered.connect(self.show_comany_dialog)
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
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = m_window()
    main.show()
    sys.exit(app.exec_())