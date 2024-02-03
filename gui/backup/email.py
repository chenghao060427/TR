from PyQt5.QtWidgets import QFormLayout,QTableWidget,QLabel,QLineEdit,QWidget,QPushButton,QVBoxLayout,\
    QHBoxLayout,QApplication,QAbstractItemView,QHeaderView,QTableWidgetItem,QFileDialog
from PyQt5.QtCore import QThread,pyqtSignal,QMutex,QModelIndex
import sys
from model.email_backup import email_backup
import pandas as pd
import time,re
from gui.process_window import process_window
from threads.backup import import_email_backup_thread,check_email_backup_thread

class email_window(QWidget):

    def __init__(self,p_win=None):
        super().__init__()
        self.email_backup_model=None
        self.email_table=None
        self.p_win=p_win
        #绑定控制器
        self.init_ui()
        self.connect_action()
    def init_ui(self):

        self.resize(300,80)
        self.import_btn = QPushButton('导入数据')
        self.reflesh_btn = QPushButton('验证操作')
        self.clear_btn = QPushButton('清空操作')


        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.import_btn,stretch=1)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.reflesh_btn,stretch=1)
        btn_layout.addStretch(1)

        btn_layout.addWidget(self.clear_btn,stretch=1)
        btn_layout.addStretch(1)

        self.v_layout = QVBoxLayout()
        # v_layout.addLayout(formlayout)
        self.v_layout.addLayout(btn_layout)

        self.v_layout.addWidget(self.init_email_table())
        # v_layout.addStretch(1)
        self.setLayout(self.v_layout)
        # self.center()
        #设置按钮
    def init_email_table(self):
        email_list = self.get_email_list()
        # print(email_list)
        if(self.email_table==None):
            self.email_table = QTableWidget()
            self.email_table.cellClicked.connect(self.delete_email)
        self.email_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.email_table.setRowCount(len(email_list))
        self.email_table.setColumnCount(len(self.email_backup_model.fillable)+1)
        self.email_table.setHorizontalHeaderLabels(self.email_backup_model.fillable+['操作'])
        self.email_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for row in range(len(email_list)):
            print(email_list[row])
            item = QTableWidgetItem(str(email_list[row]['email']))
            self.email_table.setItem(row,0,item)
            self.email_table.setItem(row, 1, QTableWidgetItem(str(email_list[row]['email_pwd'])))
            status = '未使用'
            if(email_list[row]['status']!=1):status='已使用'
            self.email_table.setItem(row, 2, QTableWidgetItem(status))

            item = QTableWidgetItem('删除')
            item.id=email_list[row]['id']
            self.email_table.setItem(row,3,item)
        return self.email_table
        pass
    def delete_email(self,row,col):

        # print(row)
        if(col==3):
            item = self.email_table.item(row,col)
            self.email_backup_model.delete(condition=['id','=',item.id])
            self.email_table.removeRow(row)
        # print(col)

    def get_email_list(self):
        if(self.email_backup_model==None):
            self.email_backup_model = email_backup()

        return self.email_backup_model.select()
        pass
    def connect_action(self):
        # print(1231)
        self.import_btn.clicked.connect(self.show_user_form)
        self.clear_btn.clicked.connect(self.clear_all)
        self.reflesh_btn.clicked.connect(self.reflesh_email)
    def reflesh_email(self):
        self.pro_win = process_window()
        self.reflesh_thread = check_email_backup_thread(pro_win=self.pro_win)
        self.reflesh_thread.start()

    def show_user_form(self):
        try:
            fname,_ = QFileDialog.getOpenFileName(self,'选择文件','C:\\','*.txt')
            if(_):
                self.import_email_infor(fname)
            else:
                return 
        except:
            return
    def clear_all(self):
        self.email_backup_model.delete()
        self.init_email_table()
        self.update()
    def import_email_infor(self,filename):
        self.pro_win = process_window(p_win=self,f_sig=1)
        self.thread=import_email_backup_thread(filename=filename,pro_win=self.pro_win)
        self.thread.start()
    def finish_thread(self,sig=None):
        # self.v_layout.removeWidget(self.email_table)
        self.init_email_table()
        # self.v_layout.addWidget(self.email_table)
        self.v_layout.update()
        self.update()
        pass
    def reflesh_window(self):
        self.init_email_table()
        self.v_layout.update()
        self.update()

    #显示表单


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = email_window()
    m.show()
    sys.exit(app.exec_())