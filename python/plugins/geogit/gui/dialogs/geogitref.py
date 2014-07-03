from PyQt4 import QtGui, QtCore
from geogitpy.commitish import Commitish
from geogitpy.commit import Commit
from geogitpy import geogit
from geogitpy.geogitexception import GeoGitException
import datetime
import os
import time

class RefWidget(QtGui.QWidget):
    
    def __init__(self, repo):
        super(RefWidget, self).__init__()
        self.repo = repo
        self.initGui()

    def initGui(self):                    
        verticalLayout = QtGui.QVBoxLayout()
        verticalLayout.setSpacing(2)
        verticalLayout.setMargin(0)
        
        verticalLayout2 = QtGui.QVBoxLayout()
        verticalLayout2.setSpacing(2)
        verticalLayout2.setMargin(15)
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(10)
        horizontalLayout.setMargin(0)        
        self.branchRadio = QtGui.QRadioButton('Branch', self)        
        self.branchRadio.toggled.connect(self.branchRadioClicked)        
        horizontalLayout.addWidget(self.branchRadio)
        self.comboBranch = QtGui.QComboBox()
        for branch in self.repo.branches:
            self.comboBranch.addItem(branch)
        self.comboBranch.setMaximumWidth(200)
        self.comboBranch.setMinimumWidth(200)            
        horizontalLayout.addWidget(self.comboBranch)        
        verticalLayout2.addLayout(horizontalLayout)
        
        horizontalLayout2 = QtGui.QHBoxLayout()
        horizontalLayout2.setSpacing(10)
        horizontalLayout2.setMargin(0)
        self.tagRadio = QtGui.QRadioButton('Tag', self)
        self.tagRadio.toggled.connect(self.tagRadioClicked)
        horizontalLayout2.addWidget(self.tagRadio)
        self.comboTag = QtGui.QComboBox()
        for tag in self.repo.tags:
            self.comboTag.addItem(tag)
        self.comboTag.setMaximumWidth(200)
        self.comboTag.setMinimumWidth(200)            
        horizontalLayout2.addWidget(self.comboTag)
        verticalLayout2.addLayout(horizontalLayout2)
        
        horizontalLayout3 = QtGui.QHBoxLayout()
        horizontalLayout3.setSpacing(10)
        horizontalLayout3.setMargin(0)
        self.commitRadio = QtGui.QRadioButton('Commit', self)
        self.commitRadio.toggled.connect(self.commitRadioClicked)   
        horizontalLayout3.addWidget(self.commitRadio)
        self.comboCommit = QtGui.QComboBox() 
        self.comboCommit.setEditable(True)  
        self.comboCommit.setMaximumWidth(200)
        self.comboCommit.setMinimumWidth(200)
        log = self.repo.log()
        for commit in log[:min(100, len(log))]:
            self.comboCommit.addItem(commit.message.split("\n")[0], commit)     
        horizontalLayout3.addWidget(self.comboCommit)
        verticalLayout2.addLayout(horizontalLayout3)
        
        horizontalLayout4 = QtGui.QHBoxLayout()
        horizontalLayout4.setSpacing(10)
        horizontalLayout4.setMargin(0)        
        self.dateRadio = QtGui.QRadioButton('Date', self)        
        self.dateRadio.toggled.connect(self.dateRadioClicked)        
        horizontalLayout4.addWidget(self.dateRadio)
        self.dateBox = QtGui.QDateTimeEdit()
        now = datetime.datetime.now()
        self.dateBox.setDate(now)
        #self.dateBox.setPlaceholderText("MM/DD/YYYY")
        self.dateBox.setMaximumWidth(200)
        self.dateBox.setMinimumWidth(200)
        horizontalLayout4.addWidget(self.dateBox)        
        verticalLayout2.addLayout(horizontalLayout4)        
        
        groupBox = QtGui.QGroupBox("Reference")
        groupBox.setLayout(verticalLayout2)
        
        verticalLayout.addWidget(groupBox)
        self.setLayout(verticalLayout)
        
        self.branchRadio.setChecked(True)
            
    def commitRadioClicked(self):
        self.comboBranch.setEnabled(False)
        self.comboTag.setEnabled(False)
        self.comboCommit.setEnabled(True)
        self.dateBox.setEnabled(False)
        
    def tagRadioClicked(self):
        self.comboBranch.setEnabled(False)
        self.comboCommit.setEnabled(False)
        self.comboTag.setEnabled(True)
        self.dateBox.setEnabled(False)
        
    def branchRadioClicked(self):
        self.comboCommit.setEnabled(False)
        self.comboTag.setEnabled(False)
        self.comboBranch.setEnabled(True)
        self.dateBox.setEnabled(False)    
        
    def dateRadioClicked(self):
        self.comboCommit.setEnabled(False)
        self.comboTag.setEnabled(False)
        self.comboBranch.setEnabled(False)
        self.dateBox.setEnabled(True)
          
    def getref(self):
        if self.branchRadio.isChecked():
            return Commitish(self.repo, self.comboBranch.currentText())
        elif self.tagRadio.isChecked():
            return Commitish(self.repo, self.comboTag.currentText())
        elif self.dateRadio.isChecked():                    
            date = self.dateBox.dateTime().toPyDateTime()
            return self.repo.commitatdate(date)                    
        else:
            idx = self.comboCommit.currentIndex()
            commit = self.comboCommit.itemData(idx)
            ref = self.comboCommit.currentText()
            if commit.message != ref:                                
                try:
                    return Commit.fromref(self.repo, ref)
                except GeoGitException, e:
                    raise GeoGitException("The provided reference does not exist: " + ref)
            else:
                return self.comboCommit.itemData(idx)
    
    def setref(self, ref):
        if ref is not None:
            self.commitRadio.setChecked(True)
            self.comboCommit.setEditText(ref)
        
class RefDialog(QtGui.QDialog):
    
    def __init__(self, repo, parent = None):
        super(RefDialog, self).__init__(parent)
        self.repo = repo
        self.ref = None
        self.initGui()

        
    def initGui(self):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)
        self.refwidget = RefWidget(self.repo)
        layout.addWidget(self.refwidget)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(400,180)
        self.setWindowTitle("Reference")
             

    def okPressed(self):
        try:
            self.ref = self.refwidget.getref()
        except GeoGitException, e:
            QtGui.QMessageBox.warning(self, 'Wrong reference',
                        str(e),
                        QtGui.QMessageBox.Ok)
            return
        self.close()

    def cancelPressed(self):
        self.ref = None
        self.close()      


class CommitListItem(QtGui.QListWidgetItem):
    
    icon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui", "resources", "person.png"))
    
    def __init__(self, commit):
        QtGui.QListWidgetItem.__init__(self)
        self.commit = commit  
        epoch = time.mktime(commit.committerdate.timetuple())
        offset = datetime.datetime.fromtimestamp (epoch) - datetime.datetime.utcfromtimestamp (epoch)
        d = commit.committerdate + offset             
        self.setText("%s %s" % (d.strftime("[%m/%d/%y %H:%M]"), commit.message.splitlines()[0]))
        self.setIcon(self.icon)      
        
                
class CommitSelectDialog(QtGui.QDialog):
    
    def __init__(self, repo, parent = None):
        super(CommitSelectDialog, self).__init__()
        self.repo = repo
        self.ref = None
        self.initGui()
        
    def initGui(self):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)
        self.filterBox = QtGui.QLineEdit()
        self.filterBox.setPlaceholderText("[enter text or date in dd/mm/yyyy format to filter history]")
        self.filterBox.textChanged.connect(self.filterCommits)
        self.list = QtGui.QListWidget()
        self.list.setAlternatingRowColors(True)
        self.list.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.list.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        log = self.repo.log()
        for commit in log:
            item = CommitListItem(commit)                    
            self.list.addItem(item)
        layout.addWidget(self.filterBox)
        layout.addWidget(self.list)        
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(500,400)
        self.setWindowTitle("Select commit")
        
        
    def filterCommits(self):
        text = self.filterBox.text().strip()
        try:
            t = datetime.datetime.strptime(text, "%d/%m/%Y")
            found = False
            for i in xrange(self.list.count()):
                item = self.list.item(i)
                if found:
                    item.setHidden(True)
                else:                    
                    delta = item.commit.committerdate - t               
                    found = delta.days < 0
                    item.setHidden(not found) 
                    
        except ValueError, e:            
            for i in xrange(self.list.count()):
                item = self.list.item(i)
                msg = item.commit.message            
                item.setHidden(text != "" and text not in msg) 
                            

    def okPressed(self):
        selected = self.list.selectedItems()
        if len(selected) == 0:
            QtGui.QMessageBox.warning(self, 'No commit selected',
                    "Select 1 commits from the commit list.", 
                    QtGui.QMessageBox.Ok)
        else:
            self.ref = selected[0].commit
            self.close()

    def cancelPressed(self):
        self.ref = None
        self.close()      
  
        
class RefPanel(QtGui.QWidget):
    
    refChanged = QtCore.pyqtSignal()

    def __init__(self, repo, ref = None, onlyCommits = True):
        super(RefPanel, self).__init__(None)
        self.repo = repo  
        self.ref = ref      
        self.onlyCommits = onlyCommits
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)        
        self.text = QtGui.QLineEdit()  
        self.text.setEnabled(False)      
        if ref is not None:
            self.text.setText(ref.humantext())
        self.text.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.horizontalLayout.addWidget(self.text)
        self.pushButton = QtGui.QToolButton()
        self.pushButton.setText("...")    
        self.pushButton.clicked.connect(self.showSelectionDialog)
        self.pushButton.setEnabled(self.repo is not None)
        self.horizontalLayout.addWidget(self.pushButton)
        self.setLayout(self.horizontalLayout)        

    def showSelectionDialog(self):
        if self.onlyCommits:
            dialog = CommitSelectDialog(self.repo, self)
        else:
            dialog = RefDialog(self.repo, self)        
        dialog.exec_()
        ref = dialog.ref 
        if ref:
            self.setRef(ref)            
            
    def setRepo(self, repo):        
        self.repo = repo
        self.pushButton.setEnabled(True)
        self.setRef(Commitish(repo, geogit.HEAD))

    def setRef(self, ref):
        self.ref = ref        
        self.text.setText(ref.humantext())
        self.refChanged.emit()

    def getRef(self):
        return self.ref
        
