from PyQt5.QtWidgets import QFormLayout,QPushButton,QWidget,QHBoxLayout,QVBoxLayout,QLabel,QComboBox,QSpinBox,QApplication,QLineEdit
import sys
from model.user import user
class form_wind(QWidget):

    def __init__(self,p_window=None):
        super().__init__(p_window)
        self.resize(400,100)

        self.setWindowTitle("注册选项")

        formlayout = QFormLayout()
        lable1 = QLabel("注册方式")

        self.r_type = QComboBox()
        self.r_type.addItems(['邮箱注册','手机号注册'])
        lable2 = QLabel("注册用户数")

        self.c_input= QSpinBox()
        self.c_input.setMaximum(300)
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
    def cancle(self):
        self.close()
    def sure(self):
        print(self.r_type.currentText())
        print(self.c_input.text())
class userinfor_form(QWidget):
    fillable=['email',
              'email_pwd',
              'backup_email',
              'backup_email_url',
              'realname',
              'pwd',
              'birth',
              'address',
              'ssn',
              'phone',
              'sms_url',
              'comany_name',
              'ein',
              'comnay_addr',
              'browser_account',

              ]
    status_dir={
        1:'未使用',
        3:'未填写公司信息',
        5:'未填写商务信息',
        7:'未填写店铺信息',
        9:'未填写税务信息',
        11:'待审核',
        13:'开通成功',
        15:'开通失败',
        17:'店铺已关闭'
    }
    def __init__(self,p_window=None,user_id=0):
        self.p_win =p_window
        super().__init__()
        self.resize(400,100)
        self.model = user()
        self.user_id = user_id
        u = self.model.select(condition=['id','=',user_id])
        u = u[0]
        self.setWindowTitle("注册信息编辑")

        formlayout = QFormLayout()
        for key in self.fillable:
            input = QLineEdit()

            input.setText(str(u[key]))
            exec(f'self.{key} = input')
            exec(f'formlayout.addRow(QLabel(key),self.{key})')
        self.status = QComboBox()
        self.status.addItems(self.status_dir.values())
        current_status = self.status_dir[u['status']]
        self.status.setCurrentText(current_status)
        formlayout.addRow(QLabel('status'),self.status)
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
        data={}
        for key in self.fillable:
            exec(f'data["{key}"]=self.{key}.text()')
        reversed_dict = dict(zip(self.status_dir.values(), self.status_dir.keys()))
        data['status'] = reversed_dict[self.status.currentText()]
        self.model.update(data=data,condition=['id','=',self.user_id])
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = userinfor_form(user_id=336)
    m.show()
    sys.exit(app.exec_())