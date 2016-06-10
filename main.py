# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Wed Jun  8 22:34:17 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys

from theano_imports import dA
import functs
from functs import searchImage

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
        MainWindow.resize(958, 747)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 60, 244, 244))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 330, 131, 32))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(320, 80, 20, 201))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 330, 131, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(360, 60, 244, 244))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(630, 80, 20, 201))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(680, 60, 244, 244))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 410, 244, 244))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(320, 430, 20, 201))
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(360, 410, 244, 244))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.line_4 = QtGui.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(630, 430, 20, 201))
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(680, 410, 244, 244))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 958, 34))
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
        self.label.setText(_translate("MainWindow", "Image originale", None))
        self.pushButton.setText(_translate("MainWindow", "Parcourir", None))
        self.pushButton_2.setText(_translate("MainWindow", "Chercher", None))
        self.label_2.setText(_translate("MainWindow", "Image 1", None))
        self.label_3.setText(_translate("MainWindow", "Image 2", None))
        self.label_4.setText(_translate("MainWindow", "Image 3", None))
        self.label_5.setText(_translate("MainWindow", "Image 4", None))
        self.label_6.setText(_translate("MainWindow", "Image 5", None))

    def choseDoc(self):
        # Adding '/' so that we get 'doc/' not 'doc'
        self.origin = QtGui.QFileDialog.getOpenFileName()
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(self.origin)))
        self.label.setScaledContents(True)
        print str(self.origin)

    def add_images(self):
        print(self.origin)
        top5 = searchImage(str(self.origin), functs.model)
        print top5
        images = [img[0] for img in top5]
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(images[0])))
        self.label_2.setScaledContents(True)
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8(images[1])))
        self.label_3.setScaledContents(True)
        self.label_4.setPixmap(QtGui.QPixmap(_fromUtf8(images[2])))
        self.label_4.setScaledContents(True)
        self.label_5.setPixmap(QtGui.QPixmap(_fromUtf8(images[3])))
        self.label_5.setScaledContents(True)
        self.label_6.setPixmap(QtGui.QPixmap(_fromUtf8(images[4])))
        self.label_6.setScaledContents(True)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
