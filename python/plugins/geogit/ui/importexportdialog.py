# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importexportdialog.ui'
#
# Created: Wed Jun 11 13:04:26 2014
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

class Ui_ImportExportDialog(object):
    def setupUi(self, ImportExportDialog):
        ImportExportDialog.setObjectName(_fromUtf8("ImportExportDialog"))
        ImportExportDialog.resize(470, 638)
        ImportExportDialog.setMinimumSize(QtCore.QSize(0, 540))
        ImportExportDialog.setMaximumSize(QtCore.QSize(900, 967))
        ImportExportDialog.setStyleSheet(_fromUtf8("#ImportExportDialog {\n"
"  background-color: #eeeeee;\n"
"}"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(ImportExportDialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.importExportTabWidget = QtGui.QTabWidget(ImportExportDialog)
        self.importExportTabWidget.setObjectName(_fromUtf8("importExportTabWidget"))
        self.importTab = QtGui.QWidget()
        self.importTab.setObjectName(_fromUtf8("importTab"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.importTab)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.importTypeWidget = QtGui.QTabWidget(self.importTab)
        self.importTypeWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.importTypeWidget.setStyleSheet(_fromUtf8(" #importTypeWidget::pane { \n"
"     border: 1px solid #C2C7CB;\n"
"     position: absolute;\n"
"     margin-top: 5px;  \n"
"     top: -1em;\n"
"     background: #eaeaea;\n"
"     \n"
"}\n"
"\n"
"  #importTypeWidget::tab-bar {\n"
"     alignment: center;\n"
" }\n"
"\n"
"  #importTypeWidget QTabBar::tab {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #d0d0d0, stop: 0.4 #cccccc,\n"
"                                 stop: 0.5 #c7c7c7, stop: 1.0 #c2c2c2);\n"
"     border: 1px solid #b3b3b2;\n"
"     border-bottom-color: #b2b6ba; \n"
"     min-width: 8ex;\n"
"     padding: 2px 6px;\n"
" }\n"
"\n"
"  #importTypeWidget QTabBar::tab:selected, QTabBar::tab:hover {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #fafafa, stop: 0.4 #e5e5e5,\n"
"                                 stop: 0.5 #e5e5e5, stop: 1.0 #fafafa);\n"
" }\n"
"\n"
"  #importTypeWidget QTabBar::tab:selected {\n"
"     border-color: #9B9B9B;\n"
"     border-bottom-color: #C2C7CB;\n"
"     outline: 0;s\n"
" }"))
        self.importTypeWidget.setTabPosition(QtGui.QTabWidget.North)
        self.importTypeWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.importTypeWidget.setUsesScrollButtons(False)
        self.importTypeWidget.setObjectName(_fromUtf8("importTypeWidget"))
        self.vectorLayer = QtGui.QWidget()
        self.vectorLayer.setObjectName(_fromUtf8("vectorLayer"))
        self.verticalLayout = QtGui.QVBoxLayout(self.vectorLayer)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.fileBrowserLabel = QtGui.QLabel(self.vectorLayer)
        self.fileBrowserLabel.setMinimumSize(QtCore.QSize(0, 30))
        self.fileBrowserLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.fileBrowserLabel.setFont(font)
        self.fileBrowserLabel.setObjectName(_fromUtf8("fileBrowserLabel"))
        self.horizontalLayout_17.addWidget(self.fileBrowserLabel)
        spacerItem1 = QtGui.QSpacerItem(40, 30, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_17)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.importLayerComboBox = QtGui.QComboBox(self.vectorLayer)
        self.importLayerComboBox.setEditable(True)
        self.importLayerComboBox.setObjectName(_fromUtf8("importLayerComboBox"))
        self.horizontalLayout.addWidget(self.importLayerComboBox)
        self.selectLayerFileButton = QtGui.QToolButton(self.vectorLayer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectLayerFileButton.sizePolicy().hasHeightForWidth())
        self.selectLayerFileButton.setSizePolicy(sizePolicy)
        self.selectLayerFileButton.setMinimumSize(QtCore.QSize(0, 0))
        self.selectLayerFileButton.setMaximumSize(QtCore.QSize(16777215, 26))
        self.selectLayerFileButton.setObjectName(_fromUtf8("selectLayerFileButton"))
        self.horizontalLayout.addWidget(self.selectLayerFileButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_15 = QtGui.QLabel(self.vectorLayer)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_8.addWidget(self.label_15)
        self.featureIdBox = QtGui.QLineEdit(self.vectorLayer)
        self.featureIdBox.setObjectName(_fromUtf8("featureIdBox"))
        self.horizontalLayout_8.addWidget(self.featureIdBox)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.importTypeWidget.addTab(self.vectorLayer, _fromUtf8(""))
        self.osm = QtGui.QWidget()
        self.osm.setObjectName(_fromUtf8("osm"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.osm)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        spacerItem3 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem3)
        self.horizontalLayout_20 = QtGui.QHBoxLayout()
        self.horizontalLayout_20.setObjectName(_fromUtf8("horizontalLayout_20"))
        self.fileBrowserLabel_2 = QtGui.QLabel(self.osm)
        self.fileBrowserLabel_2.setMinimumSize(QtCore.QSize(0, 30))
        self.fileBrowserLabel_2.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.fileBrowserLabel_2.setFont(font)
        self.fileBrowserLabel_2.setObjectName(_fromUtf8("fileBrowserLabel_2"))
        self.horizontalLayout_20.addWidget(self.fileBrowserLabel_2)
        spacerItem4 = QtGui.QSpacerItem(40, 30, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem4)
        self.verticalLayout_6.addLayout(self.horizontalLayout_20)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.osmFileBox = QtGui.QLineEdit(self.osm)
        self.osmFileBox.setMinimumSize(QtCore.QSize(250, 0))
        self.osmFileBox.setMaximumSize(QtCore.QSize(16777215, 26))
        self.osmFileBox.setText(_fromUtf8(""))
        self.osmFileBox.setObjectName(_fromUtf8("osmFileBox"))
        self.horizontalLayout_2.addWidget(self.osmFileBox)
        self.selectOsmFileButton = QtGui.QToolButton(self.osm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectOsmFileButton.sizePolicy().hasHeightForWidth())
        self.selectOsmFileButton.setSizePolicy(sizePolicy)
        self.selectOsmFileButton.setMinimumSize(QtCore.QSize(0, 0))
        self.selectOsmFileButton.setMaximumSize(QtCore.QSize(16777215, 26))
        self.selectOsmFileButton.setObjectName(_fromUtf8("selectOsmFileButton"))
        self.horizontalLayout_2.addWidget(self.selectOsmFileButton)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        spacerItem5 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem5)
        self.horizontalLayout_27 = QtGui.QHBoxLayout()
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(_fromUtf8("horizontalLayout_27"))
        spacerItem6 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_27.addItem(spacerItem6)
        self.optionalLabel = QtGui.QLabel(self.osm)
        self.optionalLabel.setStyleSheet(_fromUtf8("#optionalLabel {\n"
"     color: #666;\n"
"}"))
        self.optionalLabel.setObjectName(_fromUtf8("optionalLabel"))
        self.horizontalLayout_27.addWidget(self.optionalLabel)
        self.mappingFileBox = QtGui.QLineEdit(self.osm)
        self.mappingFileBox.setMinimumSize(QtCore.QSize(0, 0))
        self.mappingFileBox.setObjectName(_fromUtf8("mappingFileBox"))
        self.horizontalLayout_27.addWidget(self.mappingFileBox)
        self.mappingFileButton = QtGui.QToolButton(self.osm)
        self.mappingFileButton.setMinimumSize(QtCore.QSize(0, 0))
        self.mappingFileButton.setStyleSheet(_fromUtf8("#fileImportHelp {\n"
"   color: blue;\n"
"}"))
        self.mappingFileButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.mappingFileButton.setObjectName(_fromUtf8("mappingFileButton"))
        self.horizontalLayout_27.addWidget(self.mappingFileButton)
        self.verticalLayout_6.addLayout(self.horizontalLayout_27)
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem7)
        self.importTypeWidget.addTab(self.osm, _fromUtf8(""))
        self.postgis = QtGui.QWidget()
        self.postgis.setObjectName(_fromUtf8("postgis"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.postgis)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        spacerItem8 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem8)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.label_3 = QtGui.QLabel(self.postgis)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_13.addWidget(self.label_3)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem9)
        self.verticalLayout_5.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.label_4 = QtGui.QLabel(self.postgis)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_14.addWidget(self.label_4)
        self.pgImportHostBox = QtGui.QLineEdit(self.postgis)
        self.pgImportHostBox.setText(_fromUtf8(""))
        self.pgImportHostBox.setObjectName(_fromUtf8("pgImportHostBox"))
        self.horizontalLayout_14.addWidget(self.pgImportHostBox)
        self.label_5 = QtGui.QLabel(self.postgis)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_14.addWidget(self.label_5)
        self.pgImportPortBox = QtGui.QLineEdit(self.postgis)
        self.pgImportPortBox.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pgImportPortBox.setText(_fromUtf8(""))
        self.pgImportPortBox.setObjectName(_fromUtf8("pgImportPortBox"))
        self.horizontalLayout_14.addWidget(self.pgImportPortBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_18 = QtGui.QHBoxLayout()
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.label_6 = QtGui.QLabel(self.postgis)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_18.addWidget(self.label_6)
        self.pgImportUserBox = QtGui.QLineEdit(self.postgis)
        self.pgImportUserBox.setText(_fromUtf8(""))
        self.pgImportUserBox.setObjectName(_fromUtf8("pgImportUserBox"))
        self.horizontalLayout_18.addWidget(self.pgImportUserBox)
        self.label_7 = QtGui.QLabel(self.postgis)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_18.addWidget(self.label_7)
        self.pgImportPasswordBox = QtGui.QLineEdit(self.postgis)
        self.pgImportPasswordBox.setText(_fromUtf8(""))
        self.pgImportPasswordBox.setObjectName(_fromUtf8("pgImportPasswordBox"))
        self.horizontalLayout_18.addWidget(self.pgImportPasswordBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_19 = QtGui.QHBoxLayout()
        self.horizontalLayout_19.setObjectName(_fromUtf8("horizontalLayout_19"))
        self.label_9 = QtGui.QLabel(self.postgis)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_19.addWidget(self.label_9)
        self.pgImportDatabaseBox = QtGui.QLineEdit(self.postgis)
        self.pgImportDatabaseBox.setText(_fromUtf8(""))
        self.pgImportDatabaseBox.setObjectName(_fromUtf8("pgImportDatabaseBox"))
        self.horizontalLayout_19.addWidget(self.pgImportDatabaseBox)
        self.label_8 = QtGui.QLabel(self.postgis)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_19.addWidget(self.label_8)
        self.pgImportSchemaBox = QtGui.QLineEdit(self.postgis)
        self.pgImportSchemaBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pgImportSchemaBox.setText(_fromUtf8(""))
        self.pgImportSchemaBox.setObjectName(_fromUtf8("pgImportSchemaBox"))
        self.horizontalLayout_19.addWidget(self.pgImportSchemaBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_21 = QtGui.QHBoxLayout()
        self.horizontalLayout_21.setObjectName(_fromUtf8("horizontalLayout_21"))
        self.label_10 = QtGui.QLabel(self.postgis)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_21.addWidget(self.label_10)
        self.pgImportTablesBox = QtGui.QLineEdit(self.postgis)
        self.pgImportTablesBox.setText(_fromUtf8(""))
        self.pgImportTablesBox.setObjectName(_fromUtf8("pgImportTablesBox"))
        self.horizontalLayout_21.addWidget(self.pgImportTablesBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout_21)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem10)
        self.horizontalLayout_22 = QtGui.QHBoxLayout()
        self.horizontalLayout_22.setObjectName(_fromUtf8("horizontalLayout_22"))
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem11)
        self.importTestConnectionButton = QtGui.QPushButton(self.postgis)
        self.importTestConnectionButton.setMinimumSize(QtCore.QSize(0, 32))
        self.importTestConnectionButton.setMaximumSize(QtCore.QSize(16777215, 32))
        self.importTestConnectionButton.setObjectName(_fromUtf8("importTestConnectionButton"))
        self.horizontalLayout_22.addWidget(self.importTestConnectionButton)
        self.importListFeatureTypesButton = QtGui.QPushButton(self.postgis)
        self.importListFeatureTypesButton.setMinimumSize(QtCore.QSize(0, 32))
        self.importListFeatureTypesButton.setMaximumSize(QtCore.QSize(16777215, 32))
        self.importListFeatureTypesButton.setObjectName(_fromUtf8("importListFeatureTypesButton"))
        self.horizontalLayout_22.addWidget(self.importListFeatureTypesButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_22)
        self.importTypeWidget.addTab(self.postgis, _fromUtf8(""))
        self.verticalLayout_8.addWidget(self.importTypeWidget)
        self.addCheckBox = QtGui.QCheckBox(self.importTab)
        self.addCheckBox.setObjectName(_fromUtf8("addCheckBox"))
        self.verticalLayout_8.addWidget(self.addCheckBox)
        self.horizontalLayout_25 = QtGui.QHBoxLayout()
        self.horizontalLayout_25.setObjectName(_fromUtf8("horizontalLayout_25"))
        self.label_2 = QtGui.QLabel(self.importTab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_25.addWidget(self.label_2)
        self.destTreeBox = QtGui.QLineEdit(self.importTab)
        self.destTreeBox.setObjectName(_fromUtf8("destTreeBox"))
        self.horizontalLayout_25.addWidget(self.destTreeBox)
        self.verticalLayout_8.addLayout(self.horizontalLayout_25)
        self.forceCheckBox = QtGui.QCheckBox(self.importTab)
        self.forceCheckBox.setObjectName(_fromUtf8("forceCheckBox"))
        self.verticalLayout_8.addWidget(self.forceCheckBox)
        spacerItem12 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_8.addItem(spacerItem12)
        self.line_3 = QtGui.QFrame(self.importTab)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout_8.addWidget(self.line_3)
        self.progressBarImport = QtGui.QProgressBar(self.importTab)
        self.progressBarImport.setProperty("value", 0)
        self.progressBarImport.setObjectName(_fromUtf8("progressBarImport"))
        self.verticalLayout_8.addWidget(self.progressBarImport)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem13 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem13)
        self.importButtonBox = QtGui.QDialogButtonBox(self.importTab)
        self.importButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.importButtonBox.setObjectName(_fromUtf8("importButtonBox"))
        self.horizontalLayout_4.addWidget(self.importButtonBox)
        self.verticalLayout_8.addLayout(self.horizontalLayout_4)
        self.importExportTabWidget.addTab(self.importTab, _fromUtf8(""))
        self.exportTab = QtGui.QWidget()
        self.exportTab.setObjectName(_fromUtf8("exportTab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.exportTab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.label = QtGui.QLabel(self.exportTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_15.addWidget(self.label)
        spacerItem14 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem14)
        self.verticalLayout_4.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_13 = QtGui.QLabel(self.exportTab)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_5.addWidget(self.label_13)
        self.exportSnapshotWidget = QtGui.QWidget(self.exportTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportSnapshotWidget.sizePolicy().hasHeightForWidth())
        self.exportSnapshotWidget.setSizePolicy(sizePolicy)
        self.exportSnapshotWidget.setObjectName(_fromUtf8("exportSnapshotWidget"))
        self.horizontalLayout_5.addWidget(self.exportSnapshotWidget)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_14 = QtGui.QLabel(self.exportTab)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_7.addWidget(self.label_14)
        self.layersList = QtGui.QListWidget(self.exportTab)
        self.layersList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.layersList.setObjectName(_fromUtf8("layersList"))
        self.horizontalLayout_7.addWidget(self.layersList)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.line = QtGui.QFrame(self.exportTab)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_4.addWidget(self.line)
        spacerItem15 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem15)
        self.horizontalLayout_32 = QtGui.QHBoxLayout()
        self.horizontalLayout_32.setObjectName(_fromUtf8("horizontalLayout_32"))
        self.label_19 = QtGui.QLabel(self.exportTab)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.horizontalLayout_32.addWidget(self.label_19)
        spacerItem16 = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_32.addItem(spacerItem16)
        self.verticalLayout_4.addLayout(self.horizontalLayout_32)
        self.exportTypeWidget = QtGui.QTabWidget(self.exportTab)
        self.exportTypeWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.exportTypeWidget.setStyleSheet(_fromUtf8(" #importTypeWidget::pane { \n"
"     border: 1px solid #C2C7CB;\n"
"     position: absolute;\n"
"     margin-top: 5px;  \n"
"     top: -1em;\n"
"     background: #eaeaea;\n"
"     \n"
"}\n"
"\n"
"  #importTypeWidget::tab-bar {\n"
"     alignment: center;\n"
" }\n"
"\n"
"  #importTypeWidget QTabBar::tab {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #d0d0d0, stop: 0.4 #cccccc,\n"
"                                 stop: 0.5 #c7c7c7, stop: 1.0 #c2c2c2);\n"
"     border: 1px solid #b3b3b2;\n"
"     border-bottom-color: #b2b6ba; \n"
"     min-width: 8ex;\n"
"     padding: 2px 6px;\n"
" }\n"
"\n"
"  #importTypeWidget QTabBar::tab:selected, QTabBar::tab:hover {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #fafafa, stop: 0.4 #e5e5e5,\n"
"                                 stop: 0.5 #e5e5e5, stop: 1.0 #fafafa);\n"
" }\n"
"\n"
"  #importTypeWidget QTabBar::tab:selected {\n"
"     border-color: #9B9B9B;\n"
"     border-bottom-color: #C2C7CB;\n"
" }"))
        self.exportTypeWidget.setTabPosition(QtGui.QTabWidget.North)
        self.exportTypeWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.exportTypeWidget.setUsesScrollButtons(False)
        self.exportTypeWidget.setObjectName(_fromUtf8("exportTypeWidget"))
        self.shapefile_2 = QtGui.QWidget()
        self.shapefile_2.setObjectName(_fromUtf8("shapefile_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.shapefile_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem17 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem17)
        self.fileBrowserLabel_3 = QtGui.QLabel(self.shapefile_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileBrowserLabel_3.sizePolicy().hasHeightForWidth())
        self.fileBrowserLabel_3.setSizePolicy(sizePolicy)
        self.fileBrowserLabel_3.setMinimumSize(QtCore.QSize(0, 0))
        self.fileBrowserLabel_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.fileBrowserLabel_3.setFont(font)
        self.fileBrowserLabel_3.setObjectName(_fromUtf8("fileBrowserLabel_3"))
        self.verticalLayout_2.addWidget(self.fileBrowserLabel_3)
        self.horizontalLayout_29 = QtGui.QHBoxLayout()
        self.horizontalLayout_29.setObjectName(_fromUtf8("horizontalLayout_29"))
        self.exportFileBox = QtGui.QLineEdit(self.shapefile_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportFileBox.sizePolicy().hasHeightForWidth())
        self.exportFileBox.setSizePolicy(sizePolicy)
        self.exportFileBox.setMinimumSize(QtCore.QSize(250, 0))
        self.exportFileBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.exportFileBox.setInputMask(_fromUtf8(""))
        self.exportFileBox.setText(_fromUtf8(""))
        self.exportFileBox.setObjectName(_fromUtf8("exportFileBox"))
        self.horizontalLayout_29.addWidget(self.exportFileBox)
        self.selectExportFileButton = QtGui.QToolButton(self.shapefile_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectExportFileButton.sizePolicy().hasHeightForWidth())
        self.selectExportFileButton.setSizePolicy(sizePolicy)
        self.selectExportFileButton.setMinimumSize(QtCore.QSize(0, 0))
        self.selectExportFileButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.selectExportFileButton.setObjectName(_fromUtf8("selectExportFileButton"))
        self.horizontalLayout_29.addWidget(self.selectExportFileButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_29)
        spacerItem18 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem18)
        self.exportTypeWidget.addTab(self.shapefile_2, _fromUtf8(""))
        self.spatialite_2 = QtGui.QWidget()
        self.spatialite_2.setObjectName(_fromUtf8("spatialite_2"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.spatialite_2)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        spacerItem19 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_10.addItem(spacerItem19)
        self.horizontalLayout_36 = QtGui.QHBoxLayout()
        self.horizontalLayout_36.setObjectName(_fromUtf8("horizontalLayout_36"))
        self.label_17 = QtGui.QLabel(self.spatialite_2)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_36.addWidget(self.label_17)
        self.spatialiteFileBox = QtGui.QLineEdit(self.spatialite_2)
        self.spatialiteFileBox.setMinimumSize(QtCore.QSize(0, 0))
        self.spatialiteFileBox.setObjectName(_fromUtf8("spatialiteFileBox"))
        self.horizontalLayout_36.addWidget(self.spatialiteFileBox)
        self.verticalLayout_10.addLayout(self.horizontalLayout_36)
        self.horizontalLayout_37 = QtGui.QHBoxLayout()
        self.horizontalLayout_37.setObjectName(_fromUtf8("horizontalLayout_37"))
        self.label_18 = QtGui.QLabel(self.spatialite_2)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_37.addWidget(self.label_18)
        self.spatialiteUserBox = QtGui.QLineEdit(self.spatialite_2)
        self.spatialiteUserBox.setMinimumSize(QtCore.QSize(0, 0))
        self.spatialiteUserBox.setObjectName(_fromUtf8("spatialiteUserBox"))
        self.horizontalLayout_37.addWidget(self.spatialiteUserBox)
        self.verticalLayout_10.addLayout(self.horizontalLayout_37)
        spacerItem20 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem20)
        self.exportTypeWidget.addTab(self.spatialite_2, _fromUtf8(""))
        self.postgis_2 = QtGui.QWidget()
        self.postgis_2.setObjectName(_fromUtf8("postgis_2"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.postgis_2)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        spacerItem21 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_11.addItem(spacerItem21)
        self.horizontalLayout_40 = QtGui.QHBoxLayout()
        self.horizontalLayout_40.setObjectName(_fromUtf8("horizontalLayout_40"))
        self.label_12 = QtGui.QLabel(self.postgis_2)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_40.addWidget(self.label_12)
        self.pgExportHostBox = QtGui.QLineEdit(self.postgis_2)
        self.pgExportHostBox.setText(_fromUtf8(""))
        self.pgExportHostBox.setObjectName(_fromUtf8("pgExportHostBox"))
        self.horizontalLayout_40.addWidget(self.pgExportHostBox)
        self.label_20 = QtGui.QLabel(self.postgis_2)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.horizontalLayout_40.addWidget(self.label_20)
        self.pgExportPortBox = QtGui.QLineEdit(self.postgis_2)
        self.pgExportPortBox.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pgExportPortBox.setText(_fromUtf8(""))
        self.pgExportPortBox.setObjectName(_fromUtf8("pgExportPortBox"))
        self.horizontalLayout_40.addWidget(self.pgExportPortBox)
        self.verticalLayout_11.addLayout(self.horizontalLayout_40)
        self.horizontalLayout_41 = QtGui.QHBoxLayout()
        self.horizontalLayout_41.setObjectName(_fromUtf8("horizontalLayout_41"))
        self.label_21 = QtGui.QLabel(self.postgis_2)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.horizontalLayout_41.addWidget(self.label_21)
        self.pgExportUserBox = QtGui.QLineEdit(self.postgis_2)
        self.pgExportUserBox.setText(_fromUtf8(""))
        self.pgExportUserBox.setObjectName(_fromUtf8("pgExportUserBox"))
        self.horizontalLayout_41.addWidget(self.pgExportUserBox)
        self.label_22 = QtGui.QLabel(self.postgis_2)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.horizontalLayout_41.addWidget(self.label_22)
        self.pgExportPasswordBox = QtGui.QLineEdit(self.postgis_2)
        self.pgExportPasswordBox.setText(_fromUtf8(""))
        self.pgExportPasswordBox.setObjectName(_fromUtf8("pgExportPasswordBox"))
        self.horizontalLayout_41.addWidget(self.pgExportPasswordBox)
        self.verticalLayout_11.addLayout(self.horizontalLayout_41)
        self.horizontalLayout_42 = QtGui.QHBoxLayout()
        self.horizontalLayout_42.setObjectName(_fromUtf8("horizontalLayout_42"))
        self.label_23 = QtGui.QLabel(self.postgis_2)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.horizontalLayout_42.addWidget(self.label_23)
        self.pgExportDatabaseBox = QtGui.QLineEdit(self.postgis_2)
        self.pgExportDatabaseBox.setText(_fromUtf8(""))
        self.pgExportDatabaseBox.setObjectName(_fromUtf8("pgExportDatabaseBox"))
        self.horizontalLayout_42.addWidget(self.pgExportDatabaseBox)
        self.label_24 = QtGui.QLabel(self.postgis_2)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.horizontalLayout_42.addWidget(self.label_24)
        self.pgExportSchemaBox = QtGui.QLineEdit(self.postgis_2)
        self.pgExportSchemaBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pgExportSchemaBox.setText(_fromUtf8(""))
        self.pgExportSchemaBox.setObjectName(_fromUtf8("pgExportSchemaBox"))
        self.horizontalLayout_42.addWidget(self.pgExportSchemaBox)
        self.verticalLayout_11.addLayout(self.horizontalLayout_42)
        self.horizontalLayout_43 = QtGui.QHBoxLayout()
        self.horizontalLayout_43.setObjectName(_fromUtf8("horizontalLayout_43"))
        self.label_25 = QtGui.QLabel(self.postgis_2)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.horizontalLayout_43.addWidget(self.label_25)
        self.pgExportTableBox = QtGui.QLineEdit(self.postgis_2)
        self.pgExportTableBox.setText(_fromUtf8(""))
        self.pgExportTableBox.setPlaceholderText(_fromUtf8(""))
        self.pgExportTableBox.setObjectName(_fromUtf8("pgExportTableBox"))
        self.horizontalLayout_43.addWidget(self.pgExportTableBox)
        self.verticalLayout_11.addLayout(self.horizontalLayout_43)
        self.horizontalLayout_44 = QtGui.QHBoxLayout()
        self.horizontalLayout_44.setObjectName(_fromUtf8("horizontalLayout_44"))
        spacerItem22 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_44.addItem(spacerItem22)
        self.exportTestConnectionButton = QtGui.QPushButton(self.postgis_2)
        self.exportTestConnectionButton.setMinimumSize(QtCore.QSize(0, 32))
        self.exportTestConnectionButton.setMaximumSize(QtCore.QSize(16777215, 32))
        self.exportTestConnectionButton.setObjectName(_fromUtf8("exportTestConnectionButton"))
        self.horizontalLayout_44.addWidget(self.exportTestConnectionButton)
        self.exportListFeatureTypesButton = QtGui.QPushButton(self.postgis_2)
        self.exportListFeatureTypesButton.setMinimumSize(QtCore.QSize(0, 32))
        self.exportListFeatureTypesButton.setMaximumSize(QtCore.QSize(16777215, 32))
        self.exportListFeatureTypesButton.setObjectName(_fromUtf8("exportListFeatureTypesButton"))
        self.horizontalLayout_44.addWidget(self.exportListFeatureTypesButton)
        self.verticalLayout_11.addLayout(self.horizontalLayout_44)
        self.exportTypeWidget.addTab(self.postgis_2, _fromUtf8(""))
        self.verticalLayout_4.addWidget(self.exportTypeWidget)
        spacerItem23 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem23)
        self.openLayerCheckbox = QtGui.QCheckBox(self.exportTab)
        self.openLayerCheckbox.setObjectName(_fromUtf8("openLayerCheckbox"))
        self.verticalLayout_4.addWidget(self.openLayerCheckbox)
        self.line_4 = QtGui.QFrame(self.exportTab)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.verticalLayout_4.addWidget(self.line_4)
        self.progressBarExport = QtGui.QProgressBar(self.exportTab)
        self.progressBarExport.setProperty("value", 0)
        self.progressBarExport.setObjectName(_fromUtf8("progressBarExport"))
        self.verticalLayout_4.addWidget(self.progressBarExport)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem24 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem24)
        self.exportButtonBox = QtGui.QDialogButtonBox(self.exportTab)
        self.exportButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.exportButtonBox.setObjectName(_fromUtf8("exportButtonBox"))
        self.horizontalLayout_6.addWidget(self.exportButtonBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.importExportTabWidget.addTab(self.exportTab, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.importExportTabWidget)

        self.retranslateUi(ImportExportDialog)
        self.importExportTabWidget.setCurrentIndex(0)
        self.importTypeWidget.setCurrentIndex(0)
        self.exportTypeWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ImportExportDialog)

    def retranslateUi(self, ImportExportDialog):
        ImportExportDialog.setWindowTitle(_translate("ImportExportDialog", "Import or Export Data to a Repo", None))
        self.importExportTabWidget.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.fileBrowserLabel.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.fileBrowserLabel.setText(_translate("ImportExportDialog", "Layer to Import (select layer or enter vector layer filename):", None))
        self.selectLayerFileButton.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.selectLayerFileButton.setText(_translate("ImportExportDialog", "...", None))
        self.label_15.setText(_translate("ImportExportDialog", "Attribute for feature id", None))
        self.featureIdBox.setPlaceholderText(_translate("ImportExportDialog", "[Leave empty to use feature index (not recommended)]", None))
        self.importTypeWidget.setTabText(self.importTypeWidget.indexOf(self.vectorLayer), _translate("ImportExportDialog", "Vector layer/ file", None))
        self.fileBrowserLabel_2.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.fileBrowserLabel_2.setText(_translate("ImportExportDialog", "File to Import:", None))
        self.osmFileBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.osmFileBox.setPlaceholderText(_translate("ImportExportDialog", "Enter an .osm file location", None))
        self.selectOsmFileButton.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.selectOsmFileButton.setText(_translate("ImportExportDialog", "...", None))
        self.optionalLabel.setText(_translate("ImportExportDialog", "(Optional) Custom Mapping File:", None))
        self.mappingFileButton.setText(_translate("ImportExportDialog", "...", None))
        self.importTypeWidget.setTabText(self.importTypeWidget.indexOf(self.osm), _translate("ImportExportDialog", "OSM file", None))
        self.label_3.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_3.setText(_translate("ImportExportDialog", "PostGIS database to Import from:", None))
        self.label_4.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_4.setText(_translate("ImportExportDialog", "host:", None))
        self.pgImportHostBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgImportHostBox.setPlaceholderText(_translate("ImportExportDialog", "localhost", None))
        self.label_5.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_5.setText(_translate("ImportExportDialog", "port:", None))
        self.pgImportPortBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgImportPortBox.setPlaceholderText(_translate("ImportExportDialog", "5432", None))
        self.label_6.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_6.setText(_translate("ImportExportDialog", "user:", None))
        self.pgImportUserBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgImportUserBox.setPlaceholderText(_translate("ImportExportDialog", "postgres", None))
        self.label_7.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_7.setText(_translate("ImportExportDialog", "password:", None))
        self.pgImportPasswordBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgImportPasswordBox.setPlaceholderText(_translate("ImportExportDialog", "postgres", None))
        self.label_9.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_9.setText(_translate("ImportExportDialog", "database:", None))
        self.pgImportDatabaseBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgImportDatabaseBox.setPlaceholderText(_translate("ImportExportDialog", "database", None))
        self.label_8.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_8.setText(_translate("ImportExportDialog", "schema:", None))
        self.pgImportSchemaBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgImportSchemaBox.setPlaceholderText(_translate("ImportExportDialog", "public", None))
        self.label_10.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_10.setText(_translate("ImportExportDialog", "table:", None))
        self.pgImportTablesBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgImportTablesBox.setPlaceholderText(_translate("ImportExportDialog", "<all tables>", None))
        self.importTestConnectionButton.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.importTestConnectionButton.setText(_translate("ImportExportDialog", "Test Connection", None))
        self.importListFeatureTypesButton.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.importListFeatureTypesButton.setText(_translate("ImportExportDialog", "List Feature Types", None))
        self.importTypeWidget.setTabText(self.importTypeWidget.indexOf(self.postgis), _translate("ImportExportDialog", "PostGIS", None))
        self.addCheckBox.setText(_translate("ImportExportDialog", "Add imported data (do not overwrite destination layer)", None))
        self.label_2.setText(_translate("ImportExportDialog", "Destination layer", None))
        self.destTreeBox.setPlaceholderText(_translate("ImportExportDialog", "Leave empty to use origin name", None))
        self.forceCheckBox.setText(_translate("ImportExportDialog", "Force import if imported data has a different attribute schema", None))
        self.line_3.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.progressBarImport.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.importExportTabWidget.setTabText(self.importExportTabWidget.indexOf(self.importTab), _translate("ImportExportDialog", "Import", None))
        self.label.setText(_translate("ImportExportDialog", "Export from:", None))
        self.label_13.setText(_translate("ImportExportDialog", "Snapshot:", None))
        self.label_14.setText(_translate("ImportExportDialog", "Layer", None))
        self.label_19.setText(_translate("ImportExportDialog", "Export to:", None))
        self.fileBrowserLabel_3.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.fileBrowserLabel_3.setText(_translate("ImportExportDialog", "Filename:", None))
        self.exportFileBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.exportFileBox.setPlaceholderText(_translate("ImportExportDialog", "Enter a file location", None))
        self.selectExportFileButton.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.selectExportFileButton.setText(_translate("ImportExportDialog", "...", None))
        self.exportTypeWidget.setTabText(self.exportTypeWidget.indexOf(self.shapefile_2), _translate("ImportExportDialog", "Shapefile", None))
        self.label_17.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_17.setText(_translate("ImportExportDialog", "database:", None))
        self.spatialiteFileBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.spatialiteFileBox.setPlaceholderText(_translate("ImportExportDialog", "database.sqlite", None))
        self.label_18.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_18.setText(_translate("ImportExportDialog", "user:", None))
        self.spatialiteUserBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.spatialiteUserBox.setPlaceholderText(_translate("ImportExportDialog", "user", None))
        self.exportTypeWidget.setTabText(self.exportTypeWidget.indexOf(self.spatialite_2), _translate("ImportExportDialog", "SpatiaLite", None))
        self.label_12.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_12.setText(_translate("ImportExportDialog", "host:", None))
        self.pgExportHostBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgExportHostBox.setPlaceholderText(_translate("ImportExportDialog", "localhost", None))
        self.label_20.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_20.setText(_translate("ImportExportDialog", "port:", None))
        self.pgExportPortBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgExportPortBox.setPlaceholderText(_translate("ImportExportDialog", "5432", None))
        self.label_21.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_21.setText(_translate("ImportExportDialog", "user:", None))
        self.pgExportUserBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgExportUserBox.setPlaceholderText(_translate("ImportExportDialog", "postgres", None))
        self.label_22.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_22.setText(_translate("ImportExportDialog", "password:", None))
        self.pgExportPasswordBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgExportPasswordBox.setPlaceholderText(_translate("ImportExportDialog", "postgres", None))
        self.label_23.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_23.setText(_translate("ImportExportDialog", "database:", None))
        self.pgExportDatabaseBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgExportDatabaseBox.setPlaceholderText(_translate("ImportExportDialog", "database", None))
        self.label_24.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_24.setText(_translate("ImportExportDialog", "schema:", None))
        self.pgExportSchemaBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.pgExportSchemaBox.setPlaceholderText(_translate("ImportExportDialog", "public", None))
        self.label_25.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.label_25.setText(_translate("ImportExportDialog", "table:", None))
        self.pgExportTableBox.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.exportTestConnectionButton.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.exportTestConnectionButton.setText(_translate("ImportExportDialog", "Test Connection", None))
        self.exportListFeatureTypesButton.setStyleSheet(_translate("ImportExportDialog", "#fileImportHelp {\n"
"   color: blue;\n"
"}", None))
        self.exportListFeatureTypesButton.setText(_translate("ImportExportDialog", "List Feature Types", None))
        self.exportTypeWidget.setTabText(self.exportTypeWidget.indexOf(self.postgis_2), _translate("ImportExportDialog", "PostGIS", None))
        self.openLayerCheckbox.setText(_translate("ImportExportDialog", "Open in QGIS after exporting", None))
        self.importExportTabWidget.setTabText(self.importExportTabWidget.indexOf(self.exportTab), _translate("ImportExportDialog", "Export", None))

