# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reposelector.ui'
#
# Created: Tue Jun 10 10:58:54 2014
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
        self.newUjoRepoButton = QtGui.QToolButton(RepoSelectorDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/ujo-24.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newUjoRepoButton.setIcon(icon1)
        self.newUjoRepoButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.newUjoRepoButton.setAutoRaise(True)
        self.newUjoRepoButton.setObjectName(_fromUtf8("newUjoRepoButton"))
        self.horizontalLayout.addWidget(self.newUjoRepoButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.loggedAsLabel = QtGui.QLabel(RepoSelectorDialog)
        self.loggedAsLabel.setObjectName(_fromUtf8("loggedAsLabel"))
        self.horizontalLayout.addWidget(self.loggedAsLabel)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.filterBox = QtGui.QLineEdit(RepoSelectorDialog)
        self.filterBox.setObjectName(_fromUtf8("filterBox"))
        self.horizontalLayout_3.addWidget(self.filterBox)
        self.advancedSearchButton = QtGui.QPushButton(RepoSelectorDialog)
        self.advancedSearchButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.advancedSearchButton.setFlat(True)
        self.advancedSearchButton.setObjectName(_fromUtf8("advancedSearchButton"))
        self.horizontalLayout_3.addWidget(self.advancedSearchButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/push-repo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openOrCloneRepoButton.setIcon(icon2)
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
        self.addButton.setText(_translate("RepoSelectorDialog", "Add Repo", None))
        self.newUjoRepoButton.setText(_translate("RepoSelectorDialog", "New Ujo Repo", None))
        self.loggedAsLabel.setText(_translate("RepoSelectorDialog", "Logged as XXX. Log out", None))
        self.filterBox.setPlaceholderText(_translate("RepoSelectorDialog", "[Enter text to filter repository list]", None))
        self.advancedSearchButton.setText(_translate("RepoSelectorDialog", "...", None))
        self.openOrCloneRepoButton.setText(_translate("RepoSelectorDialog", "Open repository", None))

import geogitclient_resources_rc
