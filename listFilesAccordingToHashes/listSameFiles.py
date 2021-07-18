
import subprocess
import os
from os.path import isdir
from _myGui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore 
from PyQt5 import QtGui 
import sys
from time import sleep
import datetime
import ctypes

isRunnable = False
myDict = {}
ctypes.windll.kernel32.SetConsoleTitleW("List same files - console")

def convert(seconds): 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    if minutes < 10:
        if seconds < 10:
            return f"{hour}:0{minutes}:0{seconds}"
        else:
            return f"{hour}:0{minutes}:{seconds}"
    else:
        if seconds < 10:
            return f"{hour}:{minutes}:0{seconds}"
        else:
            return f"{hour}:{minutes}:{seconds}"

class updatePb(QThread):
    sig2 = pyqtSignal(int)
    def run(self):
        global isRunnable
        while isRunnable:
            sleep(0.5)
            self.sig2.emit(1)

class BGworker(QThread):
    sig1 = pyqtSignal(str)
    sig3 = pyqtSignal(str)
    def run(self):
        global isRunnable
        global myDict
        i = 1
        self.sig3.emit("Scanning files")
        print("Scanning files")
        fileNames = os.listdir(".") # current directory
        numFiles = len(fileNames)
        self.sig3.emit("Calculating hashes")
        print("Calculating hashes") 

        for i, fileName in enumerate(fileNames):
            while not isRunnable: # wait
                self.sig3.emit("Paused")
                sleep(0.01)
            
            self.sig3.emit("Calculating hashes")
            self.sig1.emit(f"{i+1}/{numFiles}")
            if isdir(".\\" + fileName):
                print(" [directory]", end="")
            else:
                pShell1 = subprocess.Popen(['powershell.exe', f'$hashVar = Get-FileHash ".\\{fileName}" -Algorithm SHA384\n\r $hashVar.hash'], stdout=subprocess.PIPE)
                hash = pShell1.stdout.read().strip()
                pShell1.terminate()
                if hash in myDict:
                    myDict[hash].append(fileName)
                else:
                    myDict.update({hash: [fileName]})
            
        self.sig3.emit("Listing hashes")
        print("\n" + "="*70 + "\n")
        i = 1
        for hash in myDict:
            print("")
            print(f"{i}-> ".rjust(6) + str(hash)[2:-1])
            j = 1
            for file in myDict[hash]:
                print(f"{j}-> ".rjust(12) + file)
                j += 1
            i += 1
            print("")
        self.sig3.emit("Finished")

class myWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('img.png'))
        self.setWindowTitle("List same files")
        self.ui.btnStart.clicked.connect(self.onStartClick)
        self.ui.btnPause.clicked.connect(self.onPauseClick)
        self.msgRan = False
        self.pbWhereIWas = 0
        self.pbWhereIAm = 0
        self.pbMax = 0
        self.firstStart = True

    def onStartClick(self):
        global isRunnable
        isRunnable = True

        # adjust btn visibilities
        self.ui.btnStart.setEnabled(False)
        self.ui.btnPause.setEnabled(True)

        self.startTime = datetime.datetime.now()
        self.startTime = datetime.datetime.timestamp(self.startTime)

        self.worker2 = updatePb()
        self.worker2.sig2.connect(self.sig2Received)
        self.worker2.start()

        if self.firstStart:
            # init background workers
            self.worker = BGworker()
            self.worker.sig1.connect(self.sig1Received)
            self.worker.sig3.connect(self.sig3Received)
            self.worker.start()
            self.firstStart = False
        else:
            print("Continueing")
            
    def onPauseClick(self):
        global isRunnable
        self.ui.btnStart.setText("Continue")
        isRunnable = False
        self.ui.btnStart.setEnabled(True)
        self.ui.btnPause.setEnabled(False)
        self.pbWhereIWas = self.pbWhereIAm
        print("Paused")
        
    def sig1Received(self, val):
        self.pbWhereIAm = int(val.split("/")[0])
        self.pbMax = int(val.split("/")[1])
        self.ui.label.setText(val)

        if(self.ui.progressBar.value() != self.ui.progressBar.maximum()):
            self.calcRemaining(self.calcElapsed())
        elif not self.msgRan:
            self.msgFinished()
            
    def sig2Received(self, val):
        self.ui.progressBar.setMaximum(self.pbMax)
        self.ui.progressBar.setValue(self.pbWhereIAm)

    def sig3Received(self, val):
        self.ui.label_2.setText(val)

    def calcElapsed(self, mode="standalone"):
        now = datetime.datetime.timestamp(datetime.datetime.now())
        et = now - self.startTime
        et = round(et)

        self.ui.labelET.setText(convert(et))
        return et

        # if(mode == "standalone"):
        #     self.ui.labelET.setText(convert(et))
        # if (mode == "returnEnabled"):
        #     return et

    def calcRemaining(self, elapsedTime):
        if self.pbWhereIAm != self.pbWhereIWas:
            remaining = elapsedTime * (self.pbMax - self.pbWhereIAm) / (self.pbWhereIAm - self.pbWhereIWas)
            remaining = round(remaining)
            self.ui.labelTR.setText(convert(remaining))
        else:
            self.ui.labelTR.setText("infinity")

    def msgFinished(self):
        msg = QMessageBox()
        msg.setWindowTitle("Finished")
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText("Please see console output")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.msgRan = True
    
    
def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myWindow()
    win.show()
    sys.exit(app.exec_())

app()