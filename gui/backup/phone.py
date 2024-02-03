from PyQt5.QtWidgets import QFormLayout,QTableWidget,QLabel,QLineEdit,QWidget,QPushButton,QVBoxLayout,\
    QHBoxLayout,QApplication,QAbstractItemView,QHeaderView,QTableWidgetItem,QFileDialog
from PyQt5.QtCore import QThread,pyqtSignal,QMutex,QModelIndex
import sys
from model.phone_backup import phone_backup
import pandas as pd
import time,re
from gui.process_window import process_window
from threads.backup import import_phone_backup_thread

class phone_window(QWidget):

    def __init__(self,p_win=None):
        super().__init__()
        self.phone_backup_model=None
        self.phone_table=None
        self.p_win=p_win
        #绑定控制器
        self.init_ui()
        self.connect_action()
    def init_ui(self):

        self.resize(300,80)
        self.import_btn = QPushButton('导入数据')
        self.reflesh_btn = QPushButton('清空操作')


        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.import_btn,stretch=1)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.reflesh_btn,stretch=1)
        btn_layout.addStretch(1)

        self.v_layout = QVBoxLayout()
        # v_layout.addLayout(formlayout)
        self.v_layout.addLayout(btn_layout)

        self.v_layout.addWidget(self.init_phone_table())
        # v_layout.addStretch(1)
        self.setLayout(self.v_layout)
        # self.center()
        #设置按钮
    def init_phone_table(self):
        phone_list = self.get_phone_list()
        # print(phone_list)
        if(self.phone_table==None):
            self.phone_table = QTableWidget()
            self.phone_table.cellClicked.connect(self.delete_phone)
        self.phone_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.phone_table.setRowCount(len(phone_list))
        self.phone_table.setColumnCount(len(self.phone_backup_model.fillable)+1)
        self.phone_table.setHorizontalHeaderLabels(self.phone_backup_model.fillable+['操作'])
        self.phone_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for row in range(len(phone_list)):
            print(phone_list[row])
            item = QTableWidgetItem(str(phone_list[row]['phone']))
            self.phone_table.setItem(row,0,item)
            self.phone_table.setItem(row, 1, QTableWidgetItem(str(phone_list[row]['sms_url'])))
            status = '未使用'
            if(phone_list[row]['status']!=1):status='已使用'
            self.phone_table.setItem(row, 2, QTableWidgetItem(status))

            item = QTableWidgetItem('删除')
            item.id=phone_list[row]['id']
            self.phone_table.setItem(row,3,item)
        return self.phone_table
        pass
    def delete_phone(self,row,col):

        # print(row)
        if(col==3):
            item = self.phone_table.item(row,col)
            self.phone_backup_model.delete(condition=['id','=',item.id])
            self.phone_table.removeRow(row)
        # print(col)

    def get_phone_list(self):
        if(self.phone_backup_model==None):
            self.phone_backup_model = phone_backup()

        return self.phone_backup_model.select()
        pass
    def connect_action(self):
        # print(1231)
        self.import_btn.clicked.connect(self.show_user_form)
        self.reflesh_btn.clicked.connect(self.clear_all)
    def show_user_form(self):
        try:
            fname,_ = QFileDialog.getOpenFileName(self,'选择文件','C:\\','*.txt')
            if(_):
                self.import_phone_infor(fname)
            else:
                return
        except:
            return
    def clear_all(self):
        self.phone_backup_model.delete()
        self.init_phone_table()
        self.update()
    def import_phone_infor(self,filename):
        self.pro_win = process_window(p_win=self,f_sig=1)
        self.thread=import_phone_backup_thread(filename=filename,pro_win=self.pro_win)
        self.thread.start()
    def finish_thread(self,sig=None):
        # self.v_layout.removeWidget(self.phone_table)
        self.init_phone_table()
        # self.v_layout.addWidget(self.phone_table)
        self.v_layout.update()
        self.update()
        pass

    #显示表单


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = phone_window()
    m.show()
    sys.exit(app.exec_())