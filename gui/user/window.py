from PyQt5.QtWidgets import QFormLayout,QTableWidget,QLabel,QLineEdit,QWidget,QPushButton,QVBoxLayout,\
    QHBoxLayout,QApplication,QAbstractItemView,QHeaderView,QTableWidgetItem,QFileDialog,QInputDialog,QMessageBox,\
    QCheckBox,QComboBox,QSpinBox

from PyQt5.QtCore import QThread,pyqtSignal,QMutex,Qt
import sys
from model.user import user
import pandas as pd
import time,re
from gui.process_window import process_window
from threads.user import import_user_thread,register_user_thread
import copy
class user_window(QWidget):

    def __init__(self,p_win=None):
        super().__init__()
        self.user_model=None
        self.user_table = None
        self.p_win=p_win
        #绑定控制器
        self.init_ui()
        self.connect_action()

    def init_ui(self):

        self.resize(300,80)
        self.import_btn = QPushButton('导入用户信息')
        self.reflesh_btn = QPushButton('刷新用户信息')
        self.register_btn = QPushButton('注册新用户')
        self.delete_btn = QPushButton('删除用户')

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.import_btn,stretch=1)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.reflesh_btn,stretch=1)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.register_btn,stretch=1)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.delete_btn,stretch=1)
        btn_layout.addStretch(1)
        self.v_layout = QVBoxLayout()
        # v_layout.addLayout(formlayout)
        self.v_layout.addLayout(btn_layout)

        self.v_layout.addWidget(self.init_user_table())
        # v_layout.addStretch(1)
        self.setLayout(self.v_layout)
        # self.center()
        #设置按钮
    def init_user_table(self):
        user_list = self.get_user_list()
        # print(user_list)
        if(self.user_table==None):
            # print(12312)
            self.user_table = QTableWidget()
        self.user_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.user_table.setRowCount(len(user_list))
        column_lable = copy.copy(self.user_model.fillable)
        # print(self.user_model.fillable)
        del(column_lable[-2:])
        del(column_lable[2:4])
        self.user_table.setColumnCount(len(column_lable)+1)
        self.user_table.setHorizontalHeaderLabels(['全选']+column_lable)
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.horizontalHeader().sectionClicked.connect(self.check_all_action)
        self.user_table.verticalHeader().setVisible(False)
        # print(self.user_table.horizontalHeaderItem(0).text())
        for row in range(len(user_list)):
            checkbox =  QCheckBox(str(user_list[row]['id']))
            # checkbox.checkStateSet(True)
            checkbox.id = user_list[row]['id']
            self.user_table.setCellWidget(row,0,checkbox)
            # self.user_table.cellWidget()
            col=1
            for k in column_lable:
                # print(k)
                if(k!='status'):
                    item = QTableWidgetItem(str(user_list[row][k]))
                else:
                    item = QTableWidgetItem(self.status_change(user_list[row][k]))
                self.user_table.setItem(row,col,item)
                col+=1
        return self.user_table
        pass
    def check_all_action(self,index):
        # self.user_table.horizontalHeader().
        current_t = self.user_table.horizontalHeaderItem(0).text()
        if(index==0):
            if(current_t=='全选'):
                self.user_table.horizontalHeaderItem(0).setText('全不选')
                for row in range(self.user_table.rowCount()):
                    check_box = self.user_table.cellWidget(row,0)
                    check_box.setChecked(True)
                    pass
                pass
            elif(current_t=='全不选'):
                self.user_table.horizontalHeaderItem(0).setText('全选')
                for row in range(self.user_table.rowCount()):
                    check_box = self.user_table.cellWidget(row,0)
                    check_box.setChecked(False)
                    pass
                pass
            pass

        pass
    def status_change(self,status):
        if(status==1):
            return '未使用'
        elif(status==3):
            return '未填写公司信息'
        elif(status==5):
            return '未填写商务信息'
        elif(status==7):
            return '未填写店铺信息'
        elif(status==9):
            return '未填写税务信息'
        elif(status==11):
            return '待审核'
        elif(status==13):
            return '开通成功'
        elif(status==15):
            return '开通失败'
        elif(status == 17):
            return '店铺已关闭'

        return '未知状态'
        pass
    def get_user_list(self):
        if(self.user_model==None):
            self.user_model = user()
        return self.user_model.select()
        pass
    def connect_action(self):
        # print(1231)
        self.import_btn.clicked.connect(self.show_user_form)
        self.register_btn.clicked.connect(self.show_register_form)
        self.delete_btn.clicked.connect(self.show_delete_form)
    def show_delete_form(self):
        items = ("全部删除","删除失败的账号","删除选中的账号")
        item,ok = QInputDialog.getItem(self,"选择删除的条件","筛选条件",items,0,False)
        if ok and item:
            print(item)
            if item=='全部删除':
                all_ok = QMessageBox.information(self,"警告","确定全部删除用户信息吗",QMessageBox.Yes|QMessageBox.No)
                if(all_ok):
                    self.user_model.delete()
                pass
            elif item=='删除失败的账号':
                self.user_model.delete(condition='status in (15,17)')
                pass
            elif item=='删除选中的账号':
                user_ids=['0']
                for row in range(self.user_table.rowCount()):
                    check_box = self.user_table.cellWidget(row,0)
                    if(check_box.isChecked()):
                        user_ids.append(str(check_box.id))
                self.user_model.delete(condition='id in ({})'.format(','.join(user_ids)))
                pass
            self.reflesh_window()
        pass

    def show_register_form(self):
        unregister_count = self.user_model.count(condition=['status','=',1])
        self.form_wind = form_window(self,unregister_count=unregister_count)

        # try:
        #     num,ok = QInputDialog.getInt(self,"新注册用户数","输入数量",value=unregister_count,min=0,max=unregister_count)
        #     if ok:
        #         self.pro_win = process_window(p_win=self,f_sig=1)
        #         self.r_thread = register_user_thread(count=num,pro_win=self.pro_win)
        #         self.r_thread.start()
        # except:
        #     pass
    def start_register(self,r_type='邮箱注册',num=1):
        self.pro_win = process_window(p_win=self, f_sig=1)
        self.r_thread = register_user_thread(count=num, pro_win=self.pro_win,r_type=r_type)
        self.r_thread.start()
    def show_user_form(self):

        fname,ok = QFileDialog.getOpenFileName(self,'选择文件','C:\\','*.xls')
        if ok:
            self.import_user_infor(fname)
    def import_user_infor(self,filename):
        self.pro_win = process_window(p_win=self,f_sig=1)
        self.thread=import_user_thread(filename=filename,pro_win=self.pro_win)
        self.thread.start()
    def finish_thread(self,sig=None):
        # self.v_layout.removeWidget(self.user_table)
        self.init_user_table()
        # self.v_layout.addWidget(self.user_table)
        self.v_layout.update()
        self.update()
        pass
    def reflesh_window(self):
        self.init_user_table()
        self.v_layout.update()
        self.update()
    #显示表单

class form_window(QWidget):
    def __init__(self,p_window=None,unregister_count=0):
        self.p_win =p_window
        super().__init__()
        self.resize(400,100)

        self.setWindowTitle("注册选项")

        formlayout = QFormLayout()
        lable1 = QLabel("注册方式")

        self.r_type = QComboBox()
        self.r_type.addItems(['邮箱注册','手机号注册'])
        lable2 = QLabel("注册用户数")

        self.c_input= QSpinBox()
        self.c_input.setMaximum(unregister_count)
        self.c_input.setMinimum(1)

        formlayout.addRow(lable1,self.r_type)
        formlayout.addRow(lable2, self.c_input)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(formlayout)

        s_btn = QPushButton('确认')
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
        print(self.r_type.currentText())
        print(self.c_input.text())
        self.p_win.start_register(r_type=self.r_type.currentText(),num=self.c_input.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = user_window()
    m.show()
    sys.exit(app.exec_())