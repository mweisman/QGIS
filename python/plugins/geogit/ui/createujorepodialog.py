# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createujorepodialog.ui'
#
# Created: Wed Jun 11 10:23:06 2014
#      by: PyQt4 UI code generator 4.11
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

class Ui_CreateUjoRepoDialog(object):
    def setupUi(self, CreateUjoRepoDialog):
        CreateUjoRepoDialog.setObjectName(_fromUtf8("CreateUjoRepoDialog"))
        CreateUjoRepoDialog.resize(400, 279)
        self.verticalLayout = QtGui.QVBoxLayout(CreateUjoRepoDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(CreateUjoRepoDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.titleBox = QtGui.QLineEdit(CreateUjoRepoDialog)
        self.titleBox.setObjectName(_fromUtf8("titleBox"))
        self.verticalLayout.addWidget(self.titleBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(CreateUjoRepoDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.nameWarningLabel = QtGui.QLabel(CreateUjoRepoDialog)
        self.nameWarningLabel.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.nameWarningLabel.setObjectName(_fromUtf8("nameWarningLabel"))
        self.horizontalLayout.addWidget(self.nameWarningLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelUrl = QtGui.QLabel(CreateUjoRepoDialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.labelUrl.setFont(font)
        self.labelUrl.setObjectName(_fromUtf8("labelUrl"))
        self.horizontalLayout_3.addWidget(self.labelUrl)
        self.nameBox = QtGui.QLineEdit(CreateUjoRepoDialog)
        self.nameBox.setObjectName(_fromUtf8("nameBox"))
        self.horizontalLayout_3.addWidget(self.nameBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_2 = QtGui.QLabel(CreateUjoRepoDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.descriptionBox = QtGui.QTextEdit(CreateUjoRepoDialog)
        self.descriptionBox.setObjectName(_fromUtf8("descriptionBox"))
        self.verticalLayout.addWidget(self.descriptionBox)
        self.buttonBox = QtGui.QDialogButtonBox(CreateUjoRepoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CreateUjoRepoDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateUjoRepoDialog)

    def retranslateUi(self, CreateUjoRepoDialog):
        CreateUjoRepoDialog.setWindowTitle(_translate("CreateUjoRepoDialog", "Create Ujo Repository", None))
        self.label.setText(_translate("CreateUjoRepoDialog", "Title", None))
        self.label_3.setText(_translate("CreateUjoRepoDialog", "URL name", None))
        self.nameWarningLabel.setText(_translate("CreateUjoRepoDialog", "URL name can only contain ASCII characters and numbers", None))
        self.labelUrl.setText(_translate("CreateUjoRepoDialog", "http://ujo.com/", None))
        self.label_2.setText(_translate("CreateUjoRepoDialog", "Description", None))

