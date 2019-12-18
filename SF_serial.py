#-*- coding:utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
from PyQt4 import *
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
import PyQt4
import time
import thread
import serial
import copy

reload(sys)
sys.setdefaultencoding('utf-8')

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



class SerialOnThread():
    def __init__(self, serialOption1, serialOption2):
        self.hostSerial = serialOption1
        self.remoteSerial = serialOption2
        self.isStop = False
        None    

    def StartSerial(self, MainWindow):
        self.isStop = False
        self.hostSerial['connect'] = self.ConnectSerial(MainWindow, self.hostSerial)
        self.remoteSerial['connect'] = self.ConnectSerial(MainWindow, self.remoteSerial)
        
        if(self.hostSerial['connect'] and self.remoteSerial['connect']): 
            self.hostSerial['thread'] = thread.start_new_thread(self.MessageHandler, (MainWindow, self.hostSerial, self.remoteSerial))  
            self.remoteSerial['thread'] = thread.start_new_thread(self.MessageHandler, (MainWindow, self.remoteSerial, self.hostSerial))  
            
        else:
            MainWindow.AppandTextSignal.emit([_fromUtf8("All connections must be successful.. Please Check Serial Option"), QtGui.QColor(255, 0, 0)])


    def StopSerial(self, MainWindow):
        MainWindow.AppandTextSignal.emit([_fromUtf8("Close Serial Session."), QtGui.QColor(255, 0, 0)])
        self.isStop = True
        
        if(self.hostSerial['connect']): 
            self.hostSerial['connect'].close()
        if(self.remoteSerial['connect']): 
            self.remoteSerial['connect'].close()    
   
   
    def ConnectSerial(self, MainWindow, SerialOption):
        if str(SerialOption['flow']) == 'hardware': rtscts = 1
        else: rtscts = 0     
    
        try:
            connect = serial.Serial()
            connect.port = str(SerialOption['port'])
            connect.baudrate = SerialOption['rate']
            connect.rtscts = rtscts
            connect.open()
            MainWindow.AppandTextSignal.emit([_fromUtf8(SerialOption['name'] + " Connect SUCCESS: " + connect.port), QtGui.QColor(255, 0, 0)])
            return connect
        except:
            MainWindow.AppandTextSignal.emit([_fromUtf8("Connect FAIL: " + connect.port), QtGui.QColor(255, 0, 0)])
            return


    def MessageHandler(self, MainWindow, own, peer):
        message = ""
        
        while not self.isStop:
            try:
                if own['connect'].readable():
                    message = own['connect'].readline()
                    if len(message) > 0:
                        peer['connect'].write(message)
                        MainWindow.AppandTextSignal.emit([_fromUtf8(own['name'] + ": " + message.strip('\r\n')), own['color']])

            except:
                    break
                 
        MainWindow.AppandTextSignal.emit([_fromUtf8(own['name'] + " is Closed."), QtGui.QColor(255, 0, 0)])

               
    def SendMessage(self, MainWindow, name, message):
        data = str(message) + "\r\n"
        
        try:
            if(self.hostSerial['name'] == name):
                self.hostSerial['connect'].write(data)
            else:
                self.remoteSerial['connect'].write(data)
        except:
            MainWindow.AppandTextSignal.emit([_fromUtf8("Console Message Send Fail. Check Connection"), QtGui.QColor(255, 0, 0)])
            





