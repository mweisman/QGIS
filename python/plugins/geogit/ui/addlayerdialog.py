# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addlayerdialog.ui'
#
# Created: Wed Apr 09 12:39:33 2014
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_GeoGitLayerDialog(object):
    def setupUi(self, GeoGitLayerDialog):
        GeoGitLayerDialog.setObjectName(_fromUtf8("GeoGitLayerDialog"))
        GeoGitLayerDialog.resize(504, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(GeoGitLayerDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(GeoGitLayerDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.repoBox = QtGui.QComboBox(self.groupBox)
        self.repoBox.setObjectName(_fromUtf8("repoBox"))
        self.verticalLayout.addWidget(self.repoBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.connectButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectButton.sizePolicy().hasHeightForWidth())
        self.connectButton.setSizePolicy(sizePolicy)
        self.connectButton.setObjectName(_fromUtf8("connectButton"))
        self.horizontalLayout.addWidget(self.connectButton)
        self.newLocalRepoButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newLocalRepoButton.sizePolicy().hasHeightForWidth())
        self.newLocalRepoButton.setSizePolicy(sizePolicy)
        self.newLocalRepoButton.setObjectName(_fromUtf8("newLocalRepoButton"))
        self.horizontalLayout.addWidget(self.newLocalRepoButton)
        self.deleteButton = QtGui.QPushButton(self.groupBox)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout.addWidget(self.deleteButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.label = QtGui.QLabel(GeoGitLayerDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.layersList = QtGui.QListWidget(GeoGitLayerDialog)
        self.layersList.setObjectName(_fromUtf8("layersList"))
        self.verticalLayout_2.addWidget(self.layersList)
        self.buttonBox = QtGui.QDialogButtonBox(GeoGitLayerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(GeoGitLayerDialog)
        QtCore.QMetaObject.connectSlotsByName(GeoGitLayerDialog)

    def retranslateUi(self, GeoGitLayerDialog):
        GeoGitLayerDialog.setWindowTitle(_translate("GeoGitLayerDialog", "Add layer from GeoGit repository", None))
        self.groupBox.setTitle(_translate("GeoGitLayerDialog", "Repository", None))
        self.connectButton.setText(_translate("GeoGitLayerDialog", "Connect", None))
        self.newLocalRepoButton.setText(_translate("GeoGitLayerDialog", "New local repo", None))
        self.deleteButton.setText(_translate("GeoGitLayerDialog", "Delete", None))
        self.label.setText(_translate("GeoGitLayerDialog", "Layers", None))

