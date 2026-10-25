from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread,QObject,Qt,pyqtSignal,pyqtSlot


class MainWindows(QtWidgets.QWidget):
    mainThreadSignal =  pyqtSignal()
    subThreadSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.resize(450,250)
        self.setWindowTitle("控制面板")
        #開始子事件迴圈按鈕
        startButton = QtWidgets.QPushButton("啟動子事件迴圈",self)
        startButton.setGeometry(30, 50, 170, 50)
        startButton.clicked.connect(self.StartButton_Click_Handler)
        #開始測試按鈕
        startTestButton = QtWidgets.QPushButton("開始測試",self)
        startTestButton.setGeometry(210, 50, 100, 50)
        startTestButton.clicked.connect(self.startTestButton_Click_Handler)
        self.setStyleSheet("font-size:20px")
        
        
    def StartButton_Click_Handler(self):
        print(f"主執行緒{QThread.currentThread()}")
        self.qthread = QThread()
        self.work = Work()
        self.work.moveToThread(self.qthread)
        self.subThreadSignal.connect(MainWindows.Main_Thread_Print)
        self.mainThreadSignal.connect(Work.test)
        self.qthread.started.connect(self.work.Sub_Thread_Print)
        self.qthread.start()   

    def startTestButton_Click_Handler(self):
        self.mainThreadSignal.emit()
    
    @staticmethod
    def Main_Thread_Print():
        print(f"執行執行緒{QThread.currentThread()}")    


class Work(QObject):
    def __init__(self):
        super().__init__()
    
                
    def Sub_Thread_Print(self):
        print(f"子執行緒{QThread.currentThread()}")
    
    @staticmethod
    def test():
        print("主執行緒觸發歸屬主執行緒的訊號，槽函式staticmethod定義在子執行緒")
        print(f"執行執行緒{QThread.currentThread()}")
        for i  in range(3):
            print(f"準備...{i}")
        print("子執行緒觸發歸屬主執行緒的訊號，槽函式staticmethod定義在主執行緒")
        mainWindows.subThreadSignal.emit()






app = QtWidgets.QApplication([])
mainWindows = MainWindows()
mainWindows.show()
app.exec()

#結果
"""
主執行緒<PyQt6.QtCore.QThread object at 0x00000287854E18B0>
子執行緒<PyQt6.QtCore.QThread object at 0x00000287854E19F0>
主執行緒觸發歸屬主執行緒的訊號，槽函式staticmethod定義在子執行緒
執行執行緒<PyQt6.QtCore.QThread object at 0x00000287854E1B30>
準備...0
準備...1
準備...2
子執行緒觸發歸屬主執行緒的訊號，槽函式staticmethod定義在主執行緒
執行執行緒<PyQt6.QtCore.QThread object at 0x00000287854E1B30>
"""