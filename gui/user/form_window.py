from PyQt5.QtWidgets import QFormLayout,QPushButton,QWidget,QHBoxLayout,QVBoxLayout,QLabel,QComboBox,QSpinBox,QApplication
import sys
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = form_wind()
    m.show()
    sys.exit(app.exec_())