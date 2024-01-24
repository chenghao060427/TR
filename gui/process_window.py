from PyQt5.QtWidgets import QWidget,QApplication,QProgressBar,QTextEdit,QDesktopWidget,QVBoxLayout,QPushButton
import sys
class process_window(QWidget):
    def __init__(self,p_win=None,f_sig=None):
        super().__init__()
        self.p_win=p_win
        self.f_sig=f_sig
        self.init_ui()
        #初始化界面
    def init_ui(self):

        self.center()
        self.setWindowTitle('程序运行中...')

        #控制窗口显示在屏幕中心的方法
        v_layout = QVBoxLayout()
        self.process_bar = QProgressBar()
        self.process_bar.setValue(0)

        self.message_window = QTextEdit()

        # self.message_window.resize(50,100)
        self.message_window.setReadOnly(True)

        self.finish_btn = QPushButton('完成', self)
        self.finish_btn.clicked.connect(self.finish_event)
        v_layout.addWidget(self.process_bar)
        v_layout.addWidget(self.message_window)
        v_layout.addWidget(self.finish_btn)
        # v_layout.addStretch(1)

        self.setLayout(v_layout)
        self.resize(500, 400)
        self.show()
    def finish_event(self):
        if(self.p_win):
            self.p_win.finish_thread(self.f_sig)
        self.close()
    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add_msg(self,message=''):
        if(message!=''):
            self.message_window.insertPlainText(message+"\n")
    def process_set(self,width=0):
        self.process_bar.setValue(width)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = process_window()
    sys.exit(app.exec_())