#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from PyQt4 import QtCore, QtGui
from PyQt4 import *
import signal
import SF_ui_window
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

if __name__=='__main__':  
    app = QtGui.QApplication(sys.argv)
    ui = SF_ui_window.Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
    

	
	
	