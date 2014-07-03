# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reposelector.ui'
#
# Created: Thu Jul 03 11:29:43 2014
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

class Ui_RepoSelectorDialog(object):
    def setupUi(self, RepoSelectorDialog):
        RepoSelectorDialog.setObjectName(_fromUtf8("RepoSelectorDialog"))
        RepoSelectorDialog.resize(677, 526)
        self.verticalLayout_5 = QtGui.QVBoxLayout(RepoSelectorDialog)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.addButton = QtGui.QToolButton(RepoSelectorDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/add-repo-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon)
        self.addButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.addButton.setAutoRaise(True)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.filterBox = QtGui.QLineEdit(RepoSelectorDialog)
        self.filterBox.setObjectName(_fromUtf8("filterBox"))
        self.verticalLayout_3.addWidget(self.filterBox)
        self.repoTree = QtGui.QTreeWidget(RepoSelectorDialog)
        self.repoTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.repoTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.repoTree.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.repoTree.setObjectName(_fromUtf8("repoTree"))
        self.repoTree.headerItem().setText(0, _fromUtf8("1"))
        self.repoTree.header().setVisible(False)
        self.verticalLayout_3.addWidget(self.repoTree)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.repoDescription = QtGui.QTextBrowser(RepoSelectorDialog)
        self.repoDescription.setEnabled(True)
        self.repoDescription.setFrameShape(QtGui.QFrame.Box)
        self.repoDescription.setFrameShadow(QtGui.QFrame.Plain)
        self.repoDescription.setObjectName(_fromUtf8("repoDescription"))
        self.verticalLayout_4.addWidget(self.repoDescription)
        self.openOrCloneRepoButton = QtGui.QToolButton(RepoSelectorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openOrCloneRepoButton.sizePolicy().hasHeightForWidth())
        self.openOrCloneRepoButton.setSizePolicy(sizePolicy)
        self.openOrCloneRepoButton.setMinimumSize(QtCore.QSize(0, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/push-repo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openOrCloneRepoButton.setIcon(icon1)
        self.openOrCloneRepoButton.setIconSize(QtCore.QSize(32, 32))
        self.openOrCloneRepoButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.openOrCloneRepoButton.setAutoRaise(False)
        self.openOrCloneRepoButton.setObjectName(_fromUtf8("openOrCloneRepoButton"))
        self.verticalLayout_4.addWidget(self.openOrCloneRepoButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.retranslateUi(RepoSelectorDialog)
        QtCore.QMetaObject.connectSlotsByName(RepoSelectorDialog)

    def retranslateUi(self, RepoSelectorDialog):
        RepoSelectorDialog.setWindowTitle(_translate("RepoSelectorDialog", "Select Repository", None))
        self.addButton.setText(_translate("RepoSelectorDialog", "Add repository", None))
        self.filterBox.setPlaceholderText(_translate("RepoSelectorDialog", "[Enter text to filter repository list]", None))
        self.openOrCloneRepoButton.setText(_translate("RepoSelectorDialog", "Open repository", None))

import geogitclient_resources_rc
