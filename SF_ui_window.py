#-*- coding:utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
import time, threading, sys, serial, glob
import SF_serial

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)

except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


# get com port list
def getSerialPortList():
    if sys.platform.startswith('win'):
        ports = [ 'COM%s' % (i + 1) for i in range(256) ]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    return result



class Ui_MainWindow(QtGui.QMainWindow):
    AppandTextSignal = QtCore.pyqtSignal(list)
    PaintButtonSignal = QtCore.pyqtSignal(object)
    serial
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setSerialPort(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(958, 952)
        self.centralwidget = QtGui.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(10)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox_host = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_host.setGeometry(QtCore.QRect(40, 10, 341, 271))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(10)
        self.groupBox_host.setFont(font)
        self.groupBox_host.setObjectName(_fromUtf8("groupBox_host"))
        self.comboBox_host_port = QtGui.QComboBox(self.groupBox_host)
        self.comboBox_host_port.setGeometry(QtCore.QRect(120, 20, 201, 31))
        self.comboBox_host_port.setObjectName(_fromUtf8("comboBox_host_port"))
        self.comboBox_host_port.addItem(_fromUtf8(""))
        self.comboBox_host_rate = QtGui.QComboBox(self.groupBox_host)
        self.comboBox_host_rate.setGeometry(QtCore.QRect(120, 60, 201, 31))
        self.comboBox_host_rate.setObjectName(_fromUtf8("comboBox_host_rate"))
        self.comboBox_host_rate.addItem(_fromUtf8(""))
        self.comboBox_host_rate.addItem(_fromUtf8(""))
        self.comboBox_host_rate.addItem(_fromUtf8(""))
        self.comboBox_host_rate.addItem(_fromUtf8(""))
        self.comboBox_host_rate.addItem(_fromUtf8(""))
        self.comboBox_host_rate.addItem(_fromUtf8(""))
        self.comboBox_host_parity = QtGui.QComboBox(self.groupBox_host)
        self.comboBox_host_parity.setGeometry(QtCore.QRect(120, 140, 201, 31))
        self.comboBox_host_parity.setObjectName(_fromUtf8("comboBox_host_parity"))
        self.comboBox_host_parity.addItem(_fromUtf8(""))
        self.comboBox_host_parity.addItem(_fromUtf8(""))
        self.comboBox_host_parity.addItem(_fromUtf8(""))
        self.comboBox_host_parity.addItem(_fromUtf8(""))
        self.comboBox_host_parity.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(self.groupBox_host)
        self.label.setGeometry(QtCore.QRect(20, 30, 101, 18))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox_host)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 91, 18))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox_host)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 101, 18))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox_host)
        self.label_4.setGeometry(QtCore.QRect(20, 190, 101, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.groupBox_host)
        self.label_5.setGeometry(QtCore.QRect(20, 227, 101, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.comboBox_host_stopbit = QtGui.QComboBox(self.groupBox_host)
        self.comboBox_host_stopbit.setGeometry(QtCore.QRect(120, 180, 201, 31))
        self.comboBox_host_stopbit.setObjectName(_fromUtf8("comboBox_host_stopbit"))
        self.comboBox_host_stopbit.addItem(_fromUtf8(""))
        self.comboBox_host_stopbit.addItem(_fromUtf8(""))
        self.comboBox_host_stopbit.addItem(_fromUtf8(""))
        self.comboBox_host_flow = QtGui.QComboBox(self.groupBox_host)
        self.comboBox_host_flow.setGeometry(QtCore.QRect(120, 220, 201, 31))
        self.comboBox_host_flow.setObjectName(_fromUtf8("comboBox_host_flow"))
        self.comboBox_host_flow.addItem(_fromUtf8(""))
        self.comboBox_host_flow.addItem(_fromUtf8(""))
        self.comboBox_host_flow.addItem(_fromUtf8(""))
        self.comboBox_host_data = QtGui.QComboBox(self.groupBox_host)
        self.comboBox_host_data.setGeometry(QtCore.QRect(120, 100, 201, 31))
        self.comboBox_host_data.setObjectName(_fromUtf8("comboBox_host_data"))
        self.comboBox_host_data.addItem(_fromUtf8(""))
        self.comboBox_host_data.addItem(_fromUtf8(""))
        self.label_6 = QtGui.QLabel(self.groupBox_host)
        self.label_6.setGeometry(QtCore.QRect(20, 110, 101, 18))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.textEdit_console = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_console.setGeometry(QtCore.QRect(40, 310, 881, 531))
        self.textEdit_console.setObjectName(_fromUtf8("textEdit_console"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 860, 511, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton_send = QtGui.QPushButton(self.centralwidget)
        self.pushButton_send.setGeometry(QtCore.QRect(730, 860, 191, 31))
        self.pushButton_send.setObjectName(_fromUtf8("pushButton_send"))
        self.pushButton_send.clicked.connect(self.onClickSendMessage)
    
        self.groupBox_remote = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_remote.setGeometry(QtCore.QRect(400, 10, 341, 271))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(10)
        self.groupBox_remote.setFont(font)
        self.groupBox_remote.setObjectName(_fromUtf8("groupBox_remote"))
        self.comboBox_remote_port = QtGui.QComboBox(self.groupBox_remote)
        self.comboBox_remote_port.setGeometry(QtCore.QRect(120, 20, 201, 31))
        self.comboBox_remote_port.setObjectName(_fromUtf8("comboBox_remote_port"))
        self.comboBox_remote_port.addItem(_fromUtf8(""))
        self.comboBox_remote_rate = QtGui.QComboBox(self.groupBox_remote)
        self.comboBox_remote_rate.setGeometry(QtCore.QRect(120, 60, 201, 31))
        self.comboBox_remote_rate.setObjectName(_fromUtf8("comboBox_remote_rate"))
        self.comboBox_remote_rate.addItem(_fromUtf8(""))
        self.comboBox_remote_rate.addItem(_fromUtf8(""))
        self.comboBox_remote_rate.addItem(_fromUtf8(""))
        self.comboBox_remote_rate.addItem(_fromUtf8(""))
        self.comboBox_remote_rate.addItem(_fromUtf8(""))
        self.comboBox_remote_rate.addItem(_fromUtf8(""))
        self.comboBox_remote_parity = QtGui.QComboBox(self.groupBox_remote)
        self.comboBox_remote_parity.setGeometry(QtCore.QRect(120, 140, 201, 31))
        self.comboBox_remote_parity.setObjectName(_fromUtf8("comboBox_remote_parity"))
        self.comboBox_remote_parity.addItem(_fromUtf8(""))
        self.comboBox_remote_parity.addItem(_fromUtf8(""))
        self.comboBox_remote_parity.addItem(_fromUtf8(""))
        self.comboBox_remote_parity.addItem(_fromUtf8(""))
        self.comboBox_remote_parity.addItem(_fromUtf8(""))
        self.label_7 = QtGui.QLabel(self.groupBox_remote)
        self.label_7.setGeometry(QtCore.QRect(20, 30, 101, 18))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.groupBox_remote)
        self.label_8.setGeometry(QtCore.QRect(20, 70, 91, 18))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.groupBox_remote)
        self.label_9.setGeometry(QtCore.QRect(20, 150, 101, 18))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(self.groupBox_remote)
        self.label_10.setGeometry(QtCore.QRect(20, 190, 101, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.groupBox_remote)
        self.label_11.setGeometry(QtCore.QRect(20, 227, 101, 21))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.comboBox_remote_stopbit = QtGui.QComboBox(self.groupBox_remote)
        self.comboBox_remote_stopbit.setGeometry(QtCore.QRect(120, 180, 201, 31))
        self.comboBox_remote_stopbit.setObjectName(_fromUtf8("comboBox_remote_stopbit"))
        self.comboBox_remote_stopbit.addItem(_fromUtf8(""))
        self.comboBox_remote_stopbit.addItem(_fromUtf8(""))
        self.comboBox_remote_stopbit.addItem(_fromUtf8(""))
        self.comboBox_remote_flow = QtGui.QComboBox(self.groupBox_remote)
        self.comboBox_remote_flow.setGeometry(QtCore.QRect(120, 220, 201, 31))
        self.comboBox_remote_flow.setObjectName(_fromUtf8("comboBox_remote_flow"))
        self.comboBox_remote_flow.addItem(_fromUtf8(""))
        self.comboBox_remote_flow.addItem(_fromUtf8(""))
        self.comboBox_remote_flow.addItem(_fromUtf8(""))
        self.comboBox_remote_data = QtGui.QComboBox(self.groupBox_remote)
        self.comboBox_remote_data.setGeometry(QtCore.QRect(120, 100, 201, 31))
        self.comboBox_remote_data.setObjectName(_fromUtf8("comboBox_remote_data"))
        self.comboBox_remote_data.addItem(_fromUtf8(""))
        self.comboBox_remote_data.addItem(_fromUtf8(""))
        self.label_12 = QtGui.QLabel(self.groupBox_remote)
        self.label_12.setGeometry(QtCore.QRect(20, 110, 101, 18))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.pushButton_connect = QtGui.QPushButton(self.centralwidget)
        self.pushButton_connect.setGeometry(QtCore.QRect(760, 20, 161, 81))
        self.pushButton_connect.setObjectName(_fromUtf8("pushButton_connect"))
        self.pushButton_connect.clicked.connect(self.onClickConnect)
        
        self.comboBox_select = QtGui.QComboBox(self.centralwidget)
        self.comboBox_select.setGeometry(QtCore.QRect(570, 860, 151, 31))
        self.comboBox_select.setObjectName(_fromUtf8("comboBox_select"))
        self.comboBox_select.addItem(_fromUtf8(""))
        self.comboBox_select.addItem(_fromUtf8(""))
        self.pushButton_clear = QtGui.QPushButton(self.centralwidget)
        self.pushButton_clear.setGeometry(QtCore.QRect(760, 200, 161, 81))
        self.pushButton_clear.setObjectName(_fromUtf8("pushButton_clear"))
        self.pushButton_clear.clicked.connect(self.onClickClearConsole)
        self.pushButton_disconnect = QtGui.QPushButton(self.centralwidget)
        self.pushButton_disconnect.setGeometry(QtCore.QRect(760, 110, 161, 81))
        self.pushButton_disconnect.setObjectName(_fromUtf8("pushButton_disconnect"))
        self.pushButton_disconnect.clicked.connect(self.onClickDisConnect)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 958, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.AppandTextSignal.connect(self.onAppandText)
        self.PaintButtonSignal.connect(self.onPaintButton)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Serial Forwarding", None))
        self.groupBox_host.setTitle(_translate("MainWindow", "Host", None))
        self.comboBox_host_port.setItemText(0, _translate("MainWindow", "PORT", None))
        self.comboBox_host_rate.setItemText(0, _translate("MainWindow", "115200", None))
        self.comboBox_host_rate.setItemText(1, _translate("MainWindow", "9600", None))
        self.comboBox_host_rate.setItemText(2, _translate("MainWindow", "14400", None))
        self.comboBox_host_rate.setItemText(3, _translate("MainWindow", "19200", None))
        self.comboBox_host_rate.setItemText(4, _translate("MainWindow", "38400", None))
        self.comboBox_host_rate.setItemText(5, _translate("MainWindow", "57600", None))
        self.comboBox_host_parity.setItemText(0, _translate("MainWindow", "none", None))
        self.comboBox_host_parity.setItemText(1, _translate("MainWindow", "odd", None))
        self.comboBox_host_parity.setItemText(2, _translate("MainWindow", "even", None))
        self.comboBox_host_parity.setItemText(3, _translate("MainWindow", "mark", None))
        self.comboBox_host_parity.setItemText(4, _translate("MainWindow", "space", None))
        self.label.setText(_translate("MainWindow", "Port : ", None))
        self.label_2.setText(_translate("MainWindow", "Speed :", None))
        self.label_3.setText(_translate("MainWindow", "Parity :", None))
        self.label_4.setText(_translate("MainWindow", "StopBit :", None))
        self.label_5.setText(_translate("MainWindow", "Flow Contorl :", None))
        self.comboBox_host_stopbit.setItemText(0, _translate("MainWindow", "1 bit", None))
        self.comboBox_host_stopbit.setItemText(1, _translate("MainWindow", "1.5 bit", None))
        self.comboBox_host_stopbit.setItemText(2, _translate("MainWindow", "2 bit", None))
        self.comboBox_host_flow.setItemText(0, _translate("MainWindow", "none", None))
        self.comboBox_host_flow.setItemText(1, _translate("MainWindow", "Xon/Xoff", None))
        self.comboBox_host_flow.setItemText(2, _translate("MainWindow", "hardware", None))
        self.comboBox_host_data.setItemText(0, _translate("MainWindow", "8 bit", None))
        self.comboBox_host_data.setItemText(1, _translate("MainWindow", "7 bit", None))
        self.label_6.setText(_translate("MainWindow", "Data :", None))
        self.pushButton_send.setText(_translate("MainWindow", "Send", None))
        self.groupBox_remote.setTitle(_translate("MainWindow", "Remote", None))
        self.comboBox_remote_port.setItemText(0, _translate("MainWindow", "PORT", None))
        self.comboBox_remote_rate.setItemText(0, _translate("MainWindow", "115200", None))
        self.comboBox_remote_rate.setItemText(1, _translate("MainWindow", "9600", None))
        self.comboBox_remote_rate.setItemText(2, _translate("MainWindow", "14400", None))
        self.comboBox_remote_rate.setItemText(3, _translate("MainWindow", "19200", None))
        self.comboBox_remote_rate.setItemText(4, _translate("MainWindow", "38400", None))
        self.comboBox_remote_rate.setItemText(5, _translate("MainWindow", "57600", None))
        self.comboBox_remote_parity.setItemText(0, _translate("MainWindow", "none", None))
        self.comboBox_remote_parity.setItemText(1, _translate("MainWindow", "odd", None))
        self.comboBox_remote_parity.setItemText(2, _translate("MainWindow", "even", None))
        self.comboBox_remote_parity.setItemText(3, _translate("MainWindow", "mark", None))
        self.comboBox_remote_parity.setItemText(4, _translate("MainWindow", "space", None))
        self.label_7.setText(_translate("MainWindow", "Port :", None))
        self.label_8.setText(_translate("MainWindow", "Speed :", None))
        self.label_9.setText(_translate("MainWindow", "Parity :", None))
        self.label_10.setText(_translate("MainWindow", "StopBit :", None))
        self.label_11.setText(_translate("MainWindow", "Flow Control :", None))
        self.comboBox_remote_stopbit.setItemText(0, _translate("MainWindow", "1 bit", None))
        self.comboBox_remote_stopbit.setItemText(1, _translate("MainWindow", "1.5 bit", None))
        self.comboBox_remote_stopbit.setItemText(2, _translate("MainWindow", "2 bit", None))
        self.comboBox_remote_flow.setItemText(0, _translate("MainWindow", "none", None))
        self.comboBox_remote_flow.setItemText(1, _translate("MainWindow", "Xon/Xoff", None))
        self.comboBox_remote_flow.setItemText(2, _translate("MainWindow", "hardware", None))
        self.comboBox_remote_data.setItemText(0, _translate("MainWindow", "8 bit", None))
        self.comboBox_remote_data.setItemText(1, _translate("MainWindow", "7 bit", None))
        self.label_12.setText(_translate("MainWindow", "Data :", None))
        self.pushButton_connect.setText(_translate("MainWindow", "Connect", None))
        self.comboBox_select.setItemText(0, _translate("MainWindow", "host", None))
        self.comboBox_select.setItemText(1, _translate("MainWindow", "remote", None))
        self.pushButton_clear.setText(_translate("MainWindow", "Clear Console", None))
        self.pushButton_disconnect.setText(_translate("MainWindow", "DisConnect", None))

    def setSerialPort(self, MainWindow):
        serialPorts = getSerialPortList()
        if len(serialPorts) == 0:
            self.comboBox_host_port.setEnabled(False)
            self.comboBox_remote_port.setEnabled(False)
        else:
            self.comboBox_host_port.clear()
            self.comboBox_remote_port.clear()
            for port in serialPorts:
                self.comboBox_host_port.addItem(port)
                self.comboBox_remote_port.addItem(port)
        return


    def onAppandText(self, list):
        try:
            self.textEdit_console.setTextColor(list[1])
        except:
            self.textEdit_console.setTextColor(QtGui.QColor(0, 0, 0))
        finally:
            self.textEdit_console.append(list[0])
            self.textEdit_console.moveCursor(QtGui.QTextCursor.End)
            self.textEdit_console.moveCursor(QtGui.QTextCursor.StartOfLine)


    def onPaintButton(self, true):
        if(true): self.pushButton_connect.setStyleSheet("font:bold; font-family:Agency FB; font-size: 20px; background-color: greenyellow")
        else: self.pushButton_connect.setStyleSheet("font:bold; font-family:Agency FB; font-size: 20px; background-color: lightcoral")


    def onClickClearConsole(self):
        self.textEdit_console.clear()

    def onClickConnect(self):
        hostSerialOption = {}
        hostSerialOption['name'] = "host"
        hostSerialOption['color'] = QtGui.QColor(0, 0, 0)
        hostSerialOption['port'] = self.comboBox_host_port.currentText()
        hostSerialOption['rate'] = self.comboBox_host_rate.currentText()
        hostSerialOption['data'] = self.comboBox_host_data.currentText()
        hostSerialOption['parity'] = self.comboBox_host_parity.currentText()
        hostSerialOption['stopbit'] = self.comboBox_host_stopbit.currentText()
        hostSerialOption['flow'] = self.comboBox_host_flow.currentText()
        
        remoteSerialOption = {}
        remoteSerialOption['name'] = "remote"
        remoteSerialOption['color'] = QtGui.QColor(0, 0, 255)
        remoteSerialOption['port'] = self.comboBox_remote_port.currentText()
        remoteSerialOption['rate'] = self.comboBox_remote_rate.currentText()
        remoteSerialOption['data'] = self.comboBox_remote_data.currentText()
        remoteSerialOption['parity'] = self.comboBox_remote_parity.currentText()
        remoteSerialOption['stopbit'] = self.comboBox_remote_stopbit.currentText()
        remoteSerialOption['flow'] = self.comboBox_remote_flow.currentText()      
        
        self.serial = SF_serial.SerialOnThread(hostSerialOption, remoteSerialOption)
        self.serial.StartSerial(self)


    def onClickDisConnect(self):
        self.serial.StopSerial(self)


    def onClickSendMessage(self):
        self.serial.SendMessage(self, self.comboBox_select.currentText(), self.lineEdit.text())














