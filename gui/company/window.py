from PyQt5.QtWidgets import QFormLayout,QTableWidget,QLabel,QLineEdit,QWidget,QPushButton,QVBoxLayout,\
    QHBoxLayout,QApplication,QAbstractItemView,QHeaderView,QTableWidgetItem,QFileDialog
from PyQt5.QtCore import QThread,pyqtSignal,QMutex
import sys
from model.company_keyword import company_keyword
import pandas as pd
import time,re
from gui.process_window import process_window
from threads.comany import import_keyword_thread

class keyword_window(QWidget):

    def __init__(self,p_win=None):
        super().__init__()
        self.keyword_model=None
        self.keyword_table=None
        self.p_win=p_win
        #绑定控制器
        self.init_ui()
        self.connect_action()
    def init_ui(self):

        self.resize(300,80)
        self.import_btn = QPushButton('导入关键词')
        self.reflesh_btn = QPushButton('清空关键词')


        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.import_btn,stretch=1)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.reflesh_btn,stretch=1)
        btn_layout.addStretch(1)

        self.v_layout = QVBoxLayout()
        # v_layout.addLayout(formlayout)
        self.v_layout.addLayout(btn_layout)

        self.v_layout.addWidget(self.init_keyword_table())
        # v_layout.addStretch(1)
        self.setLayout(self.v_layout)
        # self.center()
        #设置按钮
    def init_keyword_table(self):
        keyword_list = self.get_keyword_list()
        print(keyword_list)
        if(self.keyword_table==None):
            self.keyword_table = QTableWidget()
        self.keyword_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.keyword_table.setRowCount(len(keyword_list))
        self.keyword_table.setColumnCount(len(self.keyword_model.fillable)+1)
        self.keyword_table.setHorizontalHeaderLabels(self.keyword_model.fillable+['操作'])
        self.keyword_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for row in range(len(keyword_list)):
            item = QTableWidgetItem(str(keyword_list[row]['value']))
            self.keyword_table.setItem(row,0,item)
            item = QTableWidgetItem(str('删除'))
            self.keyword_table.setItem(row,1,item)
        return self.keyword_table
        pass

    def get_keyword_list(self):
        if(self.keyword_model==None):
            self.keyword_model = company_keyword()

        return self.keyword_model.select()
        pass
    def connect_action(self):
        # print(1231)
        self.import_btn.clicked.connect(self.show_user_form)
    def show_user_form(self):
        try:
            fname,_ = QFileDialog.getOpenFileName(self,'选择文件','C:\\','*.txt')
            print(fname)
            self.import_keyword_infor(fname)
        except:
            return
    def import_keyword_infor(self,filename):
        self.pro_win = process_window(p_win=self,f_sig=1)
        self.thread=import_keyword_thread(filename=filename,pro_win=self.pro_win)
        self.thread.start()
    def finish_thread(self,sig=None):
        # self.v_layout.removeWidget(self.keyword_table)
        self.init_keyword_table()
        # self.v_layout.addWidget(self.keyword_table)
        self.v_layout.update()
        self.update()
        pass

    #显示表单


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = keyword_window()
    m.show()
    sys.exit(app.exec_())