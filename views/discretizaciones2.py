# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'discretizaciones.ui'
#
# Created: Mon Feb 20 23:59:56 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(372, 305)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 351, 121))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 30, 161, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 171, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.txt_nix = QtGui.QLineEdit(self.groupBox)
        self.txt_nix.setGeometry(QtCore.QRect(210, 30, 113, 20))
        self.txt_nix.setObjectName(_fromUtf8("txt_nix"))
        self.txt_niy = QtGui.QLineEdit(self.groupBox)
        self.txt_niy.setGeometry(QtCore.QRect(210, 60, 113, 20))
        self.txt_niy.setObjectName(_fromUtf8("txt_niy"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(30, 90, 201, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(210, 90, 111, 21))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 140, 351, 121))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(30, 30, 141, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(30, 60, 141, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.txt_ti = QtGui.QLineEdit(self.groupBox_2)
        self.txt_ti.setGeometry(QtCore.QRect(210, 30, 113, 20))
        self.txt_ti.setObjectName(_fromUtf8("txt_ti"))
        self.txt_tf = QtGui.QLineEdit(self.groupBox_2)
        self.txt_tf.setGeometry(QtCore.QRect(210, 60, 113, 20))
        self.txt_tf.setObjectName(_fromUtf8("txt_tf"))
        self.txt_nit = QtGui.QLineEdit(self.groupBox_2)
        self.txt_nit.setGeometry(QtCore.QRect(210, 90, 113, 20))
        self.txt_nit.setObjectName(_fromUtf8("txt_nit"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(30, 80, 171, 31))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.btn_Aceptar = QtGui.QPushButton(Dialog)
        self.btn_Aceptar.setGeometry(QtCore.QRect(10, 270, 75, 23))
        self.btn_Aceptar.setObjectName(_fromUtf8("btn_Aceptar"))
        self.btn_Cancelar = QtGui.QPushButton(Dialog)
        self.btn_Cancelar.setGeometry(QtCore.QRect(290, 270, 75, 23))
        self.btn_Cancelar.setObjectName(_fromUtf8("btn_Cancelar"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Ingreso de valores para discretizaciones", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Discretizacion Espacial", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Número de intervalos para x:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Número de intervaloes para y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Tiempo final para observaciones:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "Lineal", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "Logarítmica", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Discretizacion Temporal", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Tiempo inicial de simulación:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Tiempó final de simulación:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Número de intervaloes de tiempo:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_Aceptar.setText(QtGui.QApplication.translate("Dialog", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_Cancelar.setText(QtGui.QApplication.translate("Dialog", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
