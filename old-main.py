# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sat Apr  9 09:19:54 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

import sys

from PyQt4 import QtCore, QtGui

from makepkl import similarity

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
        MainWindow.resize(890, 697)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 60, 200, 200))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(340, 50, 200, 200))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 290, 103, 32))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(280, 80, 20, 181))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(630, 50, 200, 200))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(570, 80, 20, 181))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(350, 370, 200, 200))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(290, 400, 20, 181))
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(640, 370, 200, 200))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(60, 370, 200, 200))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.line_4 = QtGui.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(580, 400, 20, 181))
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 290, 103, 32))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 890, 28))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        QtCore.QObject.connect(
            self.pushButton,
            QtCore.SIGNAL("clicked()"), self.choseDoc
            )

        QtCore.QObject.connect(
            self.pushButton_2,
            QtCore.SIGNAL("clicked()"), self.add_images
            )


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Original image", None))
        # self.label.setPixmap(QtGui.QPixmap(_fromUtf8("0.jpg")))
        self.label_2.setText(_translate("MainWindow", "Image 1", None))
        self.pushButton.setText(_translate("MainWindow", "Browse", None))
        self.label_3.setText(_translate("MainWindow", "Image 2", None))
        self.label_4.setText(_translate("MainWindow", "Image 4", None))
        self.label_5.setText(_translate("MainWindow", "Image 5", None))
        self.label_6.setText(_translate("MainWindow", "Image 3", None))
        self.pushButton_2.setText(_translate("MainWindow", "Start", None))

    def choseDoc(self):
        # Adding '/' so that we get 'doc/' not 'doc'
        self.origin = QtGui.QFileDialog.getOpenFileName()
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(self.origin)))
        print str(self.origin)

    def add_images(self):
        top5 = similarity(self.origin)
        print top5
        images = [img[0] for img in top5]
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(sys.argv[1]+images[0])))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8(sys.argv[1]+images[1])))
        self.label_4.setPixmap(QtGui.QPixmap(_fromUtf8(sys.argv[1]+images[2])))
        self.label_5.setPixmap(QtGui.QPixmap(_fromUtf8(sys.argv[1]+images[3])))
        self.label_6.setPixmap(QtGui.QPixmap(_fromUtf8(sys.argv[1]+images[4])))


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
