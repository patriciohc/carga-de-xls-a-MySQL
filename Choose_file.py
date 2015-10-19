# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Choose_file.ui'
#
# Created: Sat Oct 17 15:55:19 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(524, 146)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 501, 81))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.txtFile = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.txtFile.setObjectName(_fromUtf8("txtFile"))
        self.horizontalLayout_2.addWidget(self.txtFile)
        self.btChooseFile = QtGui.QPushButton(self.verticalLayoutWidget)
        self.btChooseFile.setObjectName(_fromUtf8("btChooseFile"))
        self.horizontalLayout_2.addWidget(self.btChooseFile)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btClose = QtGui.QPushButton(self.verticalLayoutWidget)
        self.btClose.setObjectName(_fromUtf8("btClose"))
        self.horizontalLayout.addWidget(self.btClose)
        self.btLoadFile = QtGui.QPushButton(self.verticalLayoutWidget)
        self.btLoadFile.setObjectName(_fromUtf8("btLoadFile"))
        self.horizontalLayout.addWidget(self.btLoadFile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 524, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "File", None))
        self.btChooseFile.setText(_translate("MainWindow", "Choose", None))
        self.btClose.setText(_translate("MainWindow", "Cerrar", None))
        self.btLoadFile.setText(_translate("MainWindow", "Cargar Archivo", None))

