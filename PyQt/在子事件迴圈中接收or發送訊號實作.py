from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread,QObject,QTimer,pyqtSignal,pyqtSlot


class MainWindows(QtWidgets.QWidget):
    #會由子執行緒觸發
    updateOverTimeSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.resize(450,250)
        self.setWindowTitle("控制面板")
        #開始子事件迴圈按鈕
        self.startButton = QtWidgets.QPushButton("啟動子事件迴圈",self)
        self.startButton.setGeometry(30, 50, 170, 50)
        self.startButton.clicked.connect(self.StartButton_Click_Handler)
        #停止子件迴圈按鈕
        self.stopButton = QtWidgets.QPushButton("停止子事件迴圈",self)
        self.stopButton.setGeometry(30, 130, 170, 50)
        self.stopButton.clicked.connect(self.StopButton_Click_Handler)
        #開始計時按鈕
        self.startTimingButton = QtWidgets.QPushButton("開始計時",self)
        self.startTimingButton.setGeometry(210, 50, 100, 50)
        self.startTimingButton.clicked.connect(self.StartTimingButton_Click_Handler)
        #停止計時按鈕
        self.stopTimingButton = QtWidgets.QPushButton("停止計時",self)
        self.stopTimingButton.setGeometry(320, 50, 100, 50)
        self.stopTimingButton.clicked.connect(self.StopTimingButton_Click_Handler)
        #標題
        title = QtWidgets.QLabel("經過秒數:",self)
        title.setGeometry(220, 130, 90, 50)
        #title.setStyleSheet("background-color:red")
        #內容
        self.content = QtWidgets.QLabel("0",self)
        self.content.setGeometry(310, 130, 50, 50)
        self.content.setStyleSheet("background-color:white")
        self.setStyleSheet("font-size:20px")
        #slot連接
        self.updateOverTimeSignal.connect(self.UpdateOverTime)
        
        
    def StartButton_Click_Handler(self):
        self.subThread = QThread()
        self.work = Work()
        self.work.updateOverTimeSignal = self.updateOverTimeSignal
        #將繼承QObject的物件，指定它的執行緒歸屬
        self.work.moveToThread(self.subThread)
        self.subThread.start()
        print("成功啟動子事件迴圈")
        
        
    def StopButton_Click_Handler(self):
        # 1. 告訴子執行緒退出事件迴圈
        self.subThread.quit()   
        # 2. 阻塞主執行緒，直到子執行緒完全關閉並釋放
        self.subThread.wait()
        self.content.setText("0")
        print("成功停止子事件迴圈")


    def StartTimingButton_Click_Handler(self):
        self.work.startTimerSignal.emit()
      
        
    def StopTimingButton_Click_Handler(self):
        self.work.stopTimerSignal.emit()
        self.content.setText("0")

    
    @pyqtSlot()
    def UpdateOverTime(self):
        print("更新觸發")
        now = int(self.content.text())
        new = now+1
        self.content.setText(str(new))


class Work(QObject):
    #會由主執行緒觸發
    startTimerSignal = pyqtSignal()
    stopTimerSignal = pyqtSignal()
    def __init__(self):
        super().__init__() 
        self.startTimerSignal.connect(self.StartTimer)
        self.stopTimerSignal.connect(self.stopTimer)
        #self.timer = QTimer()  
        #不能在這裡建立，因為還在主執行緒中，執行緒歸屬會變主執行緒
        
        
    @pyqtSlot()    
    def StartTimer(self):
        #指定QTimer的父物件為此QObject物件
        #這樣做的好處，當此QObject物件被銷毀(手動銷毀、歸屬的執行緒結束或者重新建立時）
        #Qt 的 C++ 底層會自動幫你釋放QTimer的記憶體
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:self.updateOverTimeSignal.emit())
        self.timer.start(1000)
        print("計時器啟動")
        
        
    @pyqtSlot()    
    def stopTimer(self):
        self.timer.stop()
        print("計時器停止")


app = QtWidgets.QApplication([])
mainWindows = MainWindows()
mainWindows.show()
app.exec()