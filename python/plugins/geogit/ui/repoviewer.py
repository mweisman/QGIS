# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'repoviewer.ui'
#
# Created: Wed Apr 23 13:41:15 2014
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

class Ui_GeoGitSimpleViewer(object):
    def setupUi(self, GeoGitSimpleViewer):
        GeoGitSimpleViewer.setObjectName(_fromUtf8("GeoGitSimpleViewer"))
        GeoGitSimpleViewer.resize(471, 794)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GeoGitSimpleViewer.sizePolicy().hasHeightForWidth())
        GeoGitSimpleViewer.setSizePolicy(sizePolicy)
        GeoGitSimpleViewer.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/geogit-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        GeoGitSimpleViewer.setWindowIcon(icon)
        GeoGitSimpleViewer.setToolTip(_fromUtf8(""))
        GeoGitSimpleViewer.setAutoFillBackground(False)
        GeoGitSimpleViewer.setStyleSheet(_fromUtf8("QDockWidget {\n"
"  color: white;\n"
"}\n"
"QDockWidget::title {\n"
"  font-size: 12px;\n"
"  font-weight: bold;\n"
"  color: #FFFFFF;\n"
"  text-align: left;\n"
"  padding-left: 10px;  \n"
"  background-color:  #28728D;\n"
"\n"
"}\n"
"QDockWidget::close-button {\n"
"    subcontrol-position: top right;\n"
"    subcontrol-origin: margin;\n"
"    position: absolute;\n"
"    top: 0px; right: 2px; bottom: 0px;\n"
"    width: 20px;\n"
"}\n"
"QDockWidget::float-button {\n"
"   subcontrol-position: top right;\n"
"    subcontrol-origin: margin;\n"
"    position: absolute;\n"
"    top: 0px; right: 28px; bottom: 0px;\n"
"    width: 20px;\n"
"}\n"
"\n"
"#toolbarFrame {\n"
"border: none;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #a6a6a6, stop: 0.08 #7f7f7f,\n"
"stop: 0.39999 #717171, stop: 0.4 #626262,\n"
"stop: 0.9 #4c4c4c, stop: 1 #333333);\n"
"}"))
        GeoGitSimpleViewer.setFloating(False)
        GeoGitSimpleViewer.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.toolbarFrame = QtGui.QFrame(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolbarFrame.sizePolicy().hasHeightForWidth())
        self.toolbarFrame.setSizePolicy(sizePolicy)
        self.toolbarFrame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.toolbarFrame.setStyleSheet(_fromUtf8("#toolbarFrame {\n"
"border: 1px solid #e5e5e5;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #ffffff, stop: 0.08 #ffffff,\n"
"stop: 0.39999 #f6f6f6, stop: 0.4 #f6f6f6,\n"
"stop: 0.9 #e5e5e5, stop: 1 #e5e5e5);\n"
"}\n"
"\n"
""))
        self.toolbarFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.toolbarFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.toolbarFrame.setObjectName(_fromUtf8("toolbarFrame"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.toolbarFrame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.importExportButton = QtGui.QToolButton(self.toolbarFrame)
        self.importExportButton.setMaximumSize(QtCore.QSize(130, 16777215))
        self.importExportButton.setStyleSheet(_fromUtf8("#importExportButton {\n"
"border: 0;\n"
"color: #666;\n"
"}\n"
"\n"
"#importExportButton:pressed {\n"
"background: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 2, stop: 0 #ffffff, stop: 0.08 #f6f6f6,\n"
"stop: 0.9 #eeeeee, stop: 0.4 #d6d6d6,\n"
"stop: 0.9 #aaaaaa, stop: 1 #999999);\n"
"border-left: 1px solid #ccc;\n"
"border-right: 1px solid #ccc;\n"
"color: #333;\n"
"}\n"
""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/importExport-repo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.importExportButton.setIcon(icon1)
        self.importExportButton.setIconSize(QtCore.QSize(60, 24))
        self.importExportButton.setAutoRepeatDelay(3000)
        self.importExportButton.setAutoRepeatInterval(3000)
        self.importExportButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.importExportButton.setAutoRaise(False)
        self.importExportButton.setObjectName(_fromUtf8("importExportButton"))
        self.horizontalLayout.addWidget(self.importExportButton)
        self.commitRepoButton = QtGui.QToolButton(self.toolbarFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commitRepoButton.sizePolicy().hasHeightForWidth())
        self.commitRepoButton.setSizePolicy(sizePolicy)
        self.commitRepoButton.setMaximumSize(QtCore.QSize(130, 16777215))
        self.commitRepoButton.setAutoFillBackground(False)
        self.commitRepoButton.setStyleSheet(_fromUtf8("#commitRepoButton {\n"
"border: none;\n"
"color: #666;\n"
"}\n"
"\n"
"#commitRepoButton:pressed {\n"
"background: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 2, stop: 0 #ffffff, stop: 0.08 #f6f6f6,\n"
"stop: 0.9 #eeeeee, stop: 0.4 #d6d6d6,\n"
"stop: 0.9 #aaaaaa, stop: 1 #999999);\n"
"border-left: 1px solid #ccc;\n"
"color: #333;\n"
"}\n"
""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/commit-repo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commitRepoButton.setIcon(icon2)
        self.commitRepoButton.setIconSize(QtCore.QSize(60, 24))
        self.commitRepoButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.commitRepoButton.setAutoRaise(True)
        self.commitRepoButton.setObjectName(_fromUtf8("commitRepoButton"))
        self.horizontalLayout.addWidget(self.commitRepoButton)
        self.mergeButton = QtGui.QToolButton(self.toolbarFrame)
        self.mergeButton.setMaximumSize(QtCore.QSize(130, 16777215))
        self.mergeButton.setStyleSheet(_fromUtf8("#mergeButton {\n"
"border: none;\n"
"color: #666;\n"
"}\n"
"\n"
"#commitRepoButton:pressed {\n"
"background: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 2, stop: 0 #ffffff, stop: 0.08 #f6f6f6,\n"
"stop: 0.9 #eeeeee, stop: 0.4 #d6d6d6,\n"
"stop: 0.9 #aaaaaa, stop: 1 #999999);\n"
"border-left: 1px solid #ccc;\n"
"color: #333;\n"
"}\n"
""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/merge-24.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mergeButton.setIcon(icon3)
        self.mergeButton.setIconSize(QtCore.QSize(60, 24))
        self.mergeButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.mergeButton.setAutoRaise(True)
        self.mergeButton.setObjectName(_fromUtf8("mergeButton"))
        self.horizontalLayout.addWidget(self.mergeButton)
        self.syncRepoButton = QtGui.QToolButton(self.toolbarFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.syncRepoButton.sizePolicy().hasHeightForWidth())
        self.syncRepoButton.setSizePolicy(sizePolicy)
        self.syncRepoButton.setMaximumSize(QtCore.QSize(130, 16777215))
        self.syncRepoButton.setAutoFillBackground(False)
        self.syncRepoButton.setStyleSheet(_fromUtf8("#syncRepoButton {\n"
"border: none;\n"
"color: #666;\n"
"}\n"
"\n"
"#syncRepoButton:pressed {\n"
"background: qlineargradient(x1: 1, y1: 0, x2: 1, y2: 2, stop: 0 #ffffff, stop: 0.08 #f6f6f6,\n"
"stop: 0.9 #eeeeee, stop: 0.4 #d6d6d6,\n"
"stop: 0.9 #aaaaaa, stop: 1 #999999);\n"
"border-left: 1px solid #ccc;\n"
"border-right: 1px solid #ccc;\n"
"color: #333;\n"
"}\n"
"\n"
"\n"
""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/sync-repo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.syncRepoButton.setIcon(icon4)
        self.syncRepoButton.setIconSize(QtCore.QSize(60, 24))
        self.syncRepoButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.syncRepoButton.setAutoRaise(True)
        self.syncRepoButton.setObjectName(_fromUtf8("syncRepoButton"))
        self.horizontalLayout.addWidget(self.syncRepoButton)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.toolbarFrame)
        self.splitter = QtGui.QSplitter(self.dockWidgetContents)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.selectRepoFrame = QtGui.QFrame(self.layoutWidget)
        self.selectRepoFrame.setMinimumSize(QtCore.QSize(0, 47))
        self.selectRepoFrame.setStyleSheet(_fromUtf8("#selectRepoFrame {\n"
" border: 1px solid #999999;\n"
" background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #606c88, stop: 0.08 #606c88,\n"
"stop: 0.9 #3f4c6b, stop: 1 #3f4c6b);\n"
"\n"
"}"))
        self.selectRepoFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.selectRepoFrame.setFrameShadow(QtGui.QFrame.Plain)
        self.selectRepoFrame.setObjectName(_fromUtf8("selectRepoFrame"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.selectRepoFrame)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.repoNameLabel = QtGui.QLabel(self.selectRepoFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.repoNameLabel.sizePolicy().hasHeightForWidth())
        self.repoNameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.repoNameLabel.setFont(font)
        self.repoNameLabel.setAutoFillBackground(False)
        self.repoNameLabel.setStyleSheet(_fromUtf8("#selectRepoFrameLabel {\n"
"    color: #fff;\n"
" border-bottom: 1px #666;\n"
"}"))
        self.repoNameLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.repoNameLabel.setObjectName(_fromUtf8("repoNameLabel"))
        self.horizontalLayout_5.addWidget(self.repoNameLabel)
        self.changeRepoButton = QtGui.QToolButton(self.selectRepoFrame)
        self.changeRepoButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.changeRepoButton.setAutoRaise(True)
        self.changeRepoButton.setObjectName(_fromUtf8("changeRepoButton"))
        self.horizontalLayout_5.addWidget(self.changeRepoButton)
        self.verticalLayout_3.addWidget(self.selectRepoFrame)
        self.repoDetailsFrame = QtGui.QFrame(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.repoDetailsFrame.sizePolicy().hasHeightForWidth())
        self.repoDetailsFrame.setSizePolicy(sizePolicy)
        self.repoDetailsFrame.setStyleSheet(_fromUtf8("#repoDetailsFrame {\n"
"  background-color: #eeeeee;\n"
"  border: 0;\n"
"}"))
        self.repoDetailsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.repoDetailsFrame.setFrameShadow(QtGui.QFrame.Plain)
        self.repoDetailsFrame.setObjectName(_fromUtf8("repoDetailsFrame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.repoDetailsFrame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.repoTitle = QtGui.QLabel(self.repoDetailsFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.repoTitle.sizePolicy().hasHeightForWidth())
        self.repoTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.repoTitle.setFont(font)
        self.repoTitle.setText(_fromUtf8(""))
        self.repoTitle.setObjectName(_fromUtf8("repoTitle"))
        self.horizontalLayout_6.addWidget(self.repoTitle)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.syncLabel = QtGui.QLabel(self.repoDetailsFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.syncLabel.sizePolicy().hasHeightForWidth())
        self.syncLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.syncLabel.setFont(font)
        self.syncLabel.setStyleSheet(_fromUtf8(""))
        self.syncLabel.setText(_fromUtf8(""))
        self.syncLabel.setObjectName(_fromUtf8("syncLabel"))
        self.horizontalLayout_6.addWidget(self.syncLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.repoStatusLabel = QtGui.QLabel(self.repoDetailsFrame)
        self.repoStatusLabel.setStyleSheet(_fromUtf8("color:rgb(255, 85, 0)"))
        self.repoStatusLabel.setText(_fromUtf8(""))
        self.repoStatusLabel.setObjectName(_fromUtf8("repoStatusLabel"))
        self.verticalLayout.addWidget(self.repoStatusLabel)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.commitCountLabel = QtGui.QLabel(self.repoDetailsFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commitCountLabel.sizePolicy().hasHeightForWidth())
        self.commitCountLabel.setSizePolicy(sizePolicy)
        self.commitCountLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.commitCountLabel.setFont(font)
        self.commitCountLabel.setStyleSheet(_fromUtf8("#repoHistoryFrameLabel {\n"
"    color: #666666;\n"
"}"))
        self.commitCountLabel.setObjectName(_fromUtf8("commitCountLabel"))
        self.horizontalLayout_8.addWidget(self.commitCountLabel)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.branchLabel = QtGui.QLabel(self.repoDetailsFrame)
        self.branchLabel.setText(_fromUtf8(""))
        self.branchLabel.setObjectName(_fromUtf8("branchLabel"))
        self.horizontalLayout_8.addWidget(self.branchLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.commitsFilterBox = QtGui.QLineEdit(self.repoDetailsFrame)
        self.commitsFilterBox.setObjectName(_fromUtf8("commitsFilterBox"))
        self.horizontalLayout_2.addWidget(self.commitsFilterBox)
        spacerItem2 = QtGui.QSpacerItem(5, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.diffSelectedButton = QtGui.QToolButton(self.repoDetailsFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.diffSelectedButton.sizePolicy().hasHeightForWidth())
        self.diffSelectedButton.setSizePolicy(sizePolicy)
        self.diffSelectedButton.setMinimumSize(QtCore.QSize(110, 32))
        self.diffSelectedButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.diffSelectedButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.diffSelectedButton.setStyleSheet(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/diff-selected.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.diffSelectedButton.setIcon(icon5)
        self.diffSelectedButton.setIconSize(QtCore.QSize(24, 24))
        self.diffSelectedButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.diffSelectedButton.setAutoRaise(True)
        self.diffSelectedButton.setObjectName(_fromUtf8("diffSelectedButton"))
        self.horizontalLayout_2.addWidget(self.diffSelectedButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.commitsList = QtGui.QListWidget(self.repoDetailsFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commitsList.sizePolicy().hasHeightForWidth())
        self.commitsList.setSizePolicy(sizePolicy)
        self.commitsList.setMinimumSize(QtCore.QSize(0, 0))
        self.commitsList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.commitsList.setFrameShape(QtGui.QFrame.NoFrame)
        self.commitsList.setAlternatingRowColors(True)
        self.commitsList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.commitsList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.commitsList.setResizeMode(QtGui.QListView.Adjust)
        self.commitsList.setObjectName(_fromUtf8("commitsList"))
        self.verticalLayout.addWidget(self.commitsList)
        self.verticalLayout_3.addWidget(self.repoDetailsFrame)
        self.commitHistoryFrame = QtGui.QFrame(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commitHistoryFrame.sizePolicy().hasHeightForWidth())
        self.commitHistoryFrame.setSizePolicy(sizePolicy)
        self.commitHistoryFrame.setStyleSheet(_fromUtf8("#commitHistoryFrame {\n"
"  background-color: #eeeeee;\n"
" border: 0;\n"
"}"))
        self.commitHistoryFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.commitHistoryFrame.setFrameShadow(QtGui.QFrame.Plain)
        self.commitHistoryFrame.setObjectName(_fromUtf8("commitHistoryFrame"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.commitHistoryFrame)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.splitter_2 = QtGui.QSplitter(self.commitHistoryFrame)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.layoutWidget1 = QtGui.QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.commitHistoryFrameLabel = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commitHistoryFrameLabel.sizePolicy().hasHeightForWidth())
        self.commitHistoryFrameLabel.setSizePolicy(sizePolicy)
        self.commitHistoryFrameLabel.setMinimumSize(QtCore.QSize(0, 16))
        self.commitHistoryFrameLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.commitHistoryFrameLabel.setFont(font)
        self.commitHistoryFrameLabel.setStyleSheet(_fromUtf8("#commitHistoryFrameLabel {\n"
"    color: #666666;\n"
"    background: #ccc;\n"
"}"))
        self.commitHistoryFrameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.commitHistoryFrameLabel.setObjectName(_fromUtf8("commitHistoryFrameLabel"))
        self.verticalLayout_2.addWidget(self.commitHistoryFrameLabel)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.commitDetailText = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commitDetailText.sizePolicy().hasHeightForWidth())
        self.commitDetailText.setSizePolicy(sizePolicy)
        self.commitDetailText.setMinimumSize(QtCore.QSize(0, 50))
        self.commitDetailText.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.commitDetailText.setText(_fromUtf8(""))
        self.commitDetailText.setObjectName(_fromUtf8("commitDetailText"))
        self.horizontalLayout_3.addWidget(self.commitDetailText)
        self.commitDiffButton = QtGui.QToolButton(self.layoutWidget1)
        self.commitDiffButton.setMinimumSize(QtCore.QSize(0, 32))
        self.commitDiffButton.setMaximumSize(QtCore.QSize(16777215, 32))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/diff-details.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commitDiffButton.setIcon(icon6)
        self.commitDiffButton.setIconSize(QtCore.QSize(32, 32))
        self.commitDiffButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.commitDiffButton.setAutoRaise(True)
        self.commitDiffButton.setObjectName(_fromUtf8("commitDiffButton"))
        self.horizontalLayout_3.addWidget(self.commitDiffButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.commitMessageText = QtGui.QTextBrowser(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        self.commitMessageText.setFont(font)
        self.commitMessageText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.commitMessageText.setReadOnly(True)
        self.commitMessageText.setObjectName(_fromUtf8("commitMessageText"))
        self.verticalLayout_2.addWidget(self.commitMessageText)
        self.treeList = QtGui.QListWidget(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeList.sizePolicy().hasHeightForWidth())
        self.treeList.setSizePolicy(sizePolicy)
        self.treeList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.treeList.setObjectName(_fromUtf8("treeList"))
        self.verticalLayout_4.addWidget(self.splitter_2)
        self.verticalLayout_5.addWidget(self.splitter)
        GeoGitSimpleViewer.setWidget(self.dockWidgetContents)

        self.retranslateUi(GeoGitSimpleViewer)
        QtCore.QMetaObject.connectSlotsByName(GeoGitSimpleViewer)

    def retranslateUi(self, GeoGitSimpleViewer):
        GeoGitSimpleViewer.setWindowTitle(_translate("GeoGitSimpleViewer", "GeoGit Plugin", None))
        self.importExportButton.setToolTip(_translate("GeoGitSimpleViewer", "Import or export data to other formats", None))
        self.importExportButton.setText(_translate("GeoGitSimpleViewer", "Import/Export", None))
        self.commitRepoButton.setToolTip(_translate("GeoGitSimpleViewer", "Commit recent changes to this repo", None))
        self.commitRepoButton.setText(_translate("GeoGitSimpleViewer", "Commit Edits", None))
        self.mergeButton.setText(_translate("GeoGitSimpleViewer", "Merge", None))
        self.syncRepoButton.setToolTip(_translate("GeoGitSimpleViewer", "Synchronize selected repo", None))
        self.syncRepoButton.setText(_translate("GeoGitSimpleViewer", "Sync Repo", None))
        self.repoNameLabel.setText(_translate("GeoGitSimpleViewer", "REPOSITORY:", None))
        self.changeRepoButton.setText(_translate("GeoGitSimpleViewer", "Change...", None))
        self.commitCountLabel.setText(_translate("GeoGitSimpleViewer", "Commits:", None))
        self.commitsFilterBox.setPlaceholderText(_translate("GeoGitSimpleViewer", "[enter text or date in dd/mm/yyyy format to filter history]", None))
        self.diffSelectedButton.setToolTip(_translate("GeoGitSimpleViewer", "Select 1 commit to diff with parent, 2 to diff those 2.", None))
        self.diffSelectedButton.setText(_translate("GeoGitSimpleViewer", "Diff Selected", None))
        self.commitHistoryFrameLabel.setText(_translate("GeoGitSimpleViewer", "Details of Selected Commit:", None))
        self.commitDiffButton.setText(_translate("GeoGitSimpleViewer", "Diff details", None))

import geogitclient_resources_rc
