from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread,QObject,Qt,pyqtSignal,pyqtSlot


class MainWindows(QtWidgets.QWidget):
    mainThreadSignal =  pyqtSignal()
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
        startTestButton.clicked.connect(lambda:self.mainThreadSignal.emit())
        self.setStyleSheet("font-size:20px")
        
        
    def StartButton_Click_Handler(self):
        print(f"主執行緒{QThread.currentThread()}")
        self.qthread = QThread()
        self.work = Work()
        self.work.moveToThread(self.qthread)
        self.work.subThreadSignal.connect(self.Main_Thread_Print)
        self.mainThreadSignal.connect(self.work.test)
        self.qthread.started.connect(self.work.Sub_Thread_Print)
        self.qthread.start()   

      
    def Main_Thread_Print(self):
       print(f"執行執行緒{QThread.currentThread()}")


class Work(QObject):
    subThreadSignal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
    def test(self):
        print("主執行緒觸發歸屬主執行緒的訊號，槽函式歸屬子執行緒")
        print(f"執行執行緒{QThread.currentThread()}")
        for i  in range(3):
            print(f"準備...{i}")
        print("子執行緒觸發歸屬子執行緒的訊號，槽函式歸屬主執行緒")
        self.subThreadSignal.emit()
                
    def Sub_Thread_Print(self):
        print(f"子執行緒{QThread.currentThread()}")
        

app = QtWidgets.QApplication([])
mainWindows = MainWindows()
mainWindows.show()
app.exec()

#結果
"""
主執行緒<PyQt6.QtCore.QThread object at 0x000001D9E6B5C410>
子執行緒<PyQt6.QtCore.QThread object at 0x000001D9E6B5C550>
主執行緒觸發歸屬主執行緒的訊號，槽函式歸屬子執行緒
執行執行緒<PyQt6.QtCore.QThread object at 0x000001D9E6B5C550>
準備...0
準備...1
準備...2
子執行緒觸發歸屬子執行緒的訊號，槽函式歸屬主執行緒
執行執行緒<PyQt6.QtCore.QThread object at 0x000001D9E6B5C410>
"""