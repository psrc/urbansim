# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from qgis.gui import *
from misc.map_toolbar import *
import re, math, copy
from gui.misc.errors import *
from gui.results_menu.results_preprocessor import *
from gui.misc.dbf import *
from numpy.random import randint
from database.createDBConnection import createDBC
from collections import defaultdict
from math import ceil

class QWizardValidatePage(QWizardPage):
    def __init__(self, complete=False, parent=None):
        super(QWizardValidatePage, self).__init__(parent)
        self.complete = complete

    def isComplete(self):
        if self.complete:
            return True
        else:
            return False

class ComboBoxFolder(QComboBox):
    def __init__(self, parent=None):
        super(ComboBoxFolder, self).__init__(parent)

    def browseFolder(self, index):
        if index  == self.count()-1:
            location = QFileDialog.getExistingDirectory(self, QString("Project Location"), "/home", QFileDialog.ShowDirsOnly)
            if not location.isEmpty():
                indexOfFolder = self.isPresent(location)
                if indexOfFolder is None:
                    self.insertItem(0, QString(location))
                    self.setCurrentIndex(0)
                else:
                    self.setCurrentIndex(indexOfFolder)
            else:
                self.setCurrentIndex(0)

    def isPresent(self, location):
        for i in range(self.count()):
            if location == self.itemText(i):
                return i
        return None

class ComboBoxFile(QComboBox):
    def __init__(self, parent=None):
        super(ComboBoxFile, self).__init__(parent)

    def browseFile(self, index):
        if index == self.count()-1:
            file = QFileDialog.getOpenFileName(self, QString("Browse to select file"), "/home", "Data Files (*.dat *.csv)")
            if not file.isEmpty():
                indexOfFile = self.isPresent(file)
                if indexOfFile is None:
                    self.insertItem(1, QString(file))
                    self.setCurrentIndex(1)
                else:
                    self.setCurrentIndex(indexOfFile)
            else:
                self.setCurrentIndex(0)

    def isPresent(self, file):
        for i in range(self.count()):
            if file == self.itemText(i):
                return i
        return None

    def findAndSet(self, text):
        for i in range(self.count()):
            if self.itemText(i) == ('%s' %text):
                self.setCurrentIndex(i)
                return True
        else:
            return False


class DisplayLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(DisplayLineEdit, self).__init__(parent)
        self.setEnabled(False)


class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)

    def check(self, text):
        text = self.text()
        try:
            if len(text) == 0:
                raise TextError, "Enter a non-empty string"
            if not re.match("[A-Za-z]",text[0]):
                text = text[1:]
                raise TextError, "First character has to be a alphabet"

            for i in text[1:]:
                if not re.match("[A-Za-z_0-9]", i):
                    text.replace(i, '')
                    raise TextError, "Name can only comprise of alphabets and an underscore (_)"
        except TextError, e:
            QMessageBox.information(self, "Warning",
                                    "%s" %e,
                                    QMessageBox.Ok)
            self.setText(text)
            self.selectAll()
            self.setFocus()
        return True

class Separator(QFrame):
    def __init__(self, parent=None):
        super(Separator, self).__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class NameDialog(QDialog):
    def __init__(self,  title, parent=None):
        super(NameDialog, self).__init__(parent)

        self.setMinimumSize(200, 100)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("./images/modifydata.png"))

        nameLabel = QLabel("Name of the table")
        self.nameLineEdit = LineEdit()
        nameLabel.setBuddy(self.nameLineEdit)
        hLayout = QHBoxLayout()
        hLayout.addWidget(nameLabel)
        hLayout.addWidget(self.nameLineEdit)

        dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        copyWarning = QLabel("""<font color = blue>Enter a name for the table</font> """)

        vLayout = QVBoxLayout()
        vLayout.addLayout(hLayout)
        vLayout.addWidget(copyWarning)
        vLayout.addWidget(dialogButtonBox)

        self.setLayout(vLayout)

        self.connect(dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.connect(self.nameLineEdit, SIGNAL("textChanged(const QString&)"), self.checkName)

    def checkName(self, text):
        try:
            self.nameLineEdit.check(text)
            self.check = True
        except TextError, e:
            QMessageBox.warning(self, "Table Name", "TextError: %s" %e, QMessageBox.Ok)
            self.check = False

    def accept(self):
        if self.check:
            QDialog.accept(self)
        else:
            QMessageBox.warning(self, "Table Name", "Enter a valid table name", QMessageBox.Ok)


class VariableSelectionDialog(QDialog):
    def __init__(self, variableDict, defaultVariables=[], title="", icon="", warning="", parent=None):
        super(VariableSelectionDialog, self).__init__(parent)

        self.defaultVariables = defaultVariables
        self.variableDict = variableDict
        self.variables = self.variableDict.keys()

        self.checkDefaultVariables()

        self.setStatusTip("Dummy String")
        self.setFixedSize(QSize(500,300))

        if len(defaultVariables) == 0:
            dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Reset| QDialogButtonBox.Cancel| QDialogButtonBox.Ok)
        else:
            dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Reset| QDialogButtonBox.RestoreDefaults| QDialogButtonBox.Cancel| QDialogButtonBox.Ok)
        layout = QVBoxLayout()

        selectButton = QPushButton('Select>>')
        unselectButton = QPushButton('<<Deselect')
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(selectButton)
        buttonLayout.addWidget(unselectButton)

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("./images/%s.png"%(icon)))

        self.oriVariables = self.variables

        self.variableListWidget = ListWidget(self.variables)
        self.variableListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.selectedVariableListWidget = ListWidget([])
        self.selectedVariableListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.variableDescLabel = QLabel("Description of the variables")
        warning = QLabel("<font color = blue>%s</font>" %warning)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.variableListWidget)
        hLayout.addLayout(buttonLayout)
        hLayout.addWidget(self.selectedVariableListWidget)

        layout.addLayout(hLayout)
        layout.addWidget(self.variableDescLabel)
        layout.addWidget(warning)
        layout.addWidget(dialogButtonBox)

        self.setLayout(layout)

        self.variableListWidget.populate()


        self.connect(dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.connect(dialogButtonBox, SIGNAL("clicked(QAbstractButton *)"), self.resetandrestore)
        self.connect(selectButton, SIGNAL("clicked()"), self.moveSelected)
        self.connect(unselectButton, SIGNAL("clicked()"), self.moveUnselected)
        self.connect(self.variableListWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.moveSelected)
        self.connect(self.variableListWidget, SIGNAL("currentRowChanged(int)"), self.displayVariableDescription)
        self.connect(self.selectedVariableListWidget, SIGNAL("currentRowChanged(int)"), self.displaySelectedVariableDescription)


    def accept(self):

        QDialog.accept(self)




    def displayVariableDescription(self, row):
        if row is not -1:
            self.variableDescLabel.setText('%s'%self.variableDict['%s'%self.variableListWidget.item(row).text()])

    def displaySelectedVariableDescription(self, row):
        if row is not -1:
            self.variableDescLabel.setText('%s'%self.variableDict['%s'%self.selectedVariableListWidget.item(row).text()])



    def checkDefaultVariables(self):
        diff = [var for var in self.defaultVariables if var not in self.variables]
        if len(diff) >0 :
            raise FileError, "The default variable list contains variable names that are not in the variable list. "


    def resetandrestore(self, button):
        if button.text() == 'Restore Defaults':
            # Moving the selected variable list to the unselected list
            for i in self.selectedVariableListWidget.variables:
                self.variableListWidget.variables.append(i)
            self.variableListWidget.populate()
            # Emptying the selected variable list
            self.selectedVariableListWidget.variables = []
            self.selectedVariableListWidget.populate()

            # Removing default variables from the unselected list
            for i in self.defaultVariables:
                self.variableListWidget.variables.remove(i)
            self.variableListWidget.populate()

            # Populating the selected variable list with the default variables
            import copy
            self.selectedVariableListWidget.variables = copy.deepcopy(self.defaultVariables)
            self.selectedVariableListWidget.populate()

        if button.text() == 'Reset':
            for i in self.selectedVariableListWidget.variables:
                self.variableListWidget.variables.append(i)

            self.selectedVariableListWidget.variables = []
            self.selectedVariableListWidget.populate()
            self.variableListWidget.populate()

    def moveSelected(self):
        selectedItems = self.variableListWidget.selectedItems()
        for i in selectedItems:
            self.variableListWidget.variables.remove(i.text())
            self.selectedVariableListWidget.variables.append(i.text())

        self.variableListWidget.populate()
        self.selectedVariableListWidget.populate()

    def moveUnselected(self):
        unselectedItems = self.selectedVariableListWidget.selectedItems()
        for i in unselectedItems:
            self.selectedVariableListWidget.variables.remove(i.text())
            self.variableListWidget.variables.append(i.text())

        self.variableListWidget.populate()
        self.selectedVariableListWidget.populate()

class ListWidget(QListWidget):
    def __init__(self, variables=None, parent=None):
        super(ListWidget, self).__init__(parent)
        self.variables = variables

    def populate(self):
        self.clear()
        if len(self.variables) > 0:
            self.addItems(self.variables)

        self.sortItems()

    def remove(self):
        self.takeItem(self.currentRow())
        

    def removeList(self, items):
        for i in items:
            self.setCurrentItem(i)
            self.remove()

    def addList(self, items):
        for i in items:
            self.addItem(i.text())

    def rowOf(self, text):
        for i in range(self.count()):
            if self.item(i).text() == text:
                
                return i
        return -1

class RecodeDialog(QDialog):
    def __init__(self, project, parentText, tablename, title="", icon="", parent=None):
        super(RecodeDialog, self).__init__(parent)

        self.icon = icon

        self.setWindowTitle(title + ' - %s' %tablename)
        self.setWindowIcon(QIcon("./images/%s.png" %icon))

        self.tablename = tablename
        self.variableDict = {}
        self.project = project

        if parentText == 'Project Tables':
            database = self.project.name
        elif parentText == 'Scenario Tables':
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)               

        self.projectDBC = createDBC(self.project.db, database)
        self.projectDBC.dbc.open()

        self.setWindowTitle(title)

        self.setFixedSize(QSize(500, 300))
        self.setWindowTitle(title)

        self.variables = self.variablesInTable()

        self.variableList = QListWidget()

        self.populate()

        oldLabel = QLabel("Variable name to be recoded:")
        self.variableOldEdit = QLineEdit()
        self.variableOldEdit.setEnabled(False)
        newLabel = QLabel("New variable name after recoding:")
        self.variableNewEdit = QLineEdit()
        self.variableNewEdit.setEnabled(False)

        self.oldNewButton = QPushButton("Old and New Values")
        self.oldNewButton.setEnabled(False)

        recodeWarning = QLabel("""<font color = blue>Note: Select the variable whose categories will be """
                               """transformed by double-clicking on the variable. """
                               """ Enter a new variable name for the variable that will contain the transformed categories """
                               """in the <b>New variable name after recoding:</b> line edit box. Then click on """
                               """<b>Old and New Values </b> to define the transformations.</font>""")

        recodeWarning.setWordWrap(True)
        vlayout1 = QVBoxLayout()
        vlayout1.addWidget(self.variableList)

        vlayout2 = QVBoxLayout()
        vlayout2.addWidget(oldLabel)
        vlayout2.addWidget(self.variableOldEdit)
        vlayout2.addWidget(newLabel)
        vlayout2.addWidget(self.variableNewEdit)
        vlayout2.addItem(QSpacerItem(10, 200))
        vlayout2.addWidget(self.oldNewButton)

        hlayout = QHBoxLayout()
        hlayout.addLayout(vlayout1)
        hlayout.addLayout(vlayout2)

        dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)

        layout = QVBoxLayout()
        layout.addLayout(hlayout)
        layout.addWidget(recodeWarning)
        layout.addWidget(dialogButtonBox)

        self.setLayout(layout)

        self.connect(self.variableList, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.moveSelectedVar)
        self.connect(self.variableNewEdit, SIGNAL("textChanged(const QString&)"), self.checkNewVarName)
        self.connect(dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.connect(self.oldNewButton, SIGNAL("clicked()"), self.relationOldNew)

    def accept(self):
        QDialog.accept(self)
        self.projectDBC.dbc.close()    

    def accept(self):
        QDialog.reject(self)
        self.projectDBC.dbc.close()    

    def checkNewVarName(self, name):

        import copy
        variables = copy.deepcopy(self.variables)

        variables = [('%s'%i).lower() for i in variables]

        name = ('%s'%name).lower()

        try:
            variables.index(name)
            self.oldNewButton.setEnabled(False)
        except:
            if len(name)>0:
                if not re.match("[A-Za-z]",name[0]):
                    self.oldNewButton.setEnabled(False)
                else:
                    self.oldNewButton.setEnabled(True)
                    if len(name)>1:
                        for i in name[1:]:
                            if not re.match("[A-Za-z_0-9]", i):
                                self.oldNewButton.setEnabled(False)
                            else:
                                self.oldNewButton.setEnabled(True)
            else:
                self.oldNewButton.setEnabled(False)

    def relationOldNew(self):
        variablename = self.variableOldEdit.text()
        varcats = self.variableDict['%s' %variablename]
        newvariablename = self.variableNewEdit.text()


        dia = OldNewRelation(variablename, varcats, icon = self.icon)
        if dia.exec_():
            self.variables.append(newvariablename)
            self.runRecodeCrit(variablename, newvariablename, dia.recodeCrit)
            self.resetDialog()

    def runRecodeCrit(self, variablename, newvariablename, recodeCrit):
        query = QSqlQuery(self.projectDBC.dbc)

        self.addColumn(newvariablename)

        for crit in recodeCrit:
            if not query.exec_("""update %s set %s = %s where %s = %s"""
                               %(self.tablename,
                                 newvariablename,
                                 crit[1],
                                 variablename,
                                 crit[0])):
                raise FileError, query.lastError().text()


    def addColumn(self, variablename):
        query = QSqlQuery(self.projectDBC.dbc)


        if not query.exec_("""alter table %s add column %s text""" %(self.tablename, variablename)):
            raise FileError, query.lastError().text()

    def resetDialog(self):
        self.variableNewEdit.clear()
        self.variableOldEdit.clear()
        self.variableList.clear()
        self.populate()




    def populate(self):
        self.variableList.clear()
        self.variableList.addItems(self.variables)


    def moveSelectedVar(self, listItem):
        self.variableOldEdit.clear()
        varname = listItem.text()
        self.variableOldEdit.setText(varname)
        varCats = self.categories(varname)
        self.variableDict['%s' %varname] = varCats
        self.variableNewEdit.setEnabled(True)

    def variablesInTable(self):
        variables = []
        query = QSqlQuery(self.projectDBC.dbc)
        if not query.exec_("""desc %s""" %self.tablename):
            raise FileError, query.lastError().text()

        FIELD = 0

        while query.next():
            field = query.value(FIELD).toString()
            variables.append(field)

        return variables



    def categories(self, varname):
        cats = []

        query = QSqlQuery(self.projectDBC.dbc)
        if not query.exec_("""select %s from %s group by %s""" %(varname, self.tablename, varname)):
            raise FileError, query.lastError().text()

        CATEGORY = 0

        while query.next():
            cat = unicode(query.value(CATEGORY).toString())
            #try:
            #    cat = query.value(CATEGORY).toInt()[0]
            #except:
            #    cat = query.value(CATEGORY).toString()[0]
            cats.append(cat)

        return cats

class OldNewRelation(QDialog):
    def __init__(self, variablename, varcats, icon, parent=None):
        super(OldNewRelation, self).__init__(parent)

        self.setWindowTitle("Old and New Values")
        self.setWindowIcon(QIcon("./images/%s.png" %icon))

        self.variablename = variablename
        self.varcats = varcats
        self.recCritDict = {}

        varCatsLabel = QLabel("Categories in the variable:")
        self.varCatsList = ListWidget()
        self.varCatsList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        newCatLabel = QLabel("Value of the new category:")
        self.newCatEdit = QLineEdit()

        recodeCritLabel = QLabel("Transformation(s)")
        self.recodeCritList = ListWidget()

        self.addRecCrit = QPushButton("Add")
        self.addRecCrit.setEnabled(False)

        self.removeRecCrit = QPushButton("Remove")
        self.removeRecCrit.setEnabled(False)

        self.copyOldCrit = QPushButton("Copy Old Values")
        self.copyOldCrit.setEnabled(False)

        oldnewWarning = QLabel("""<font color = blue>Note: Highlight the old category from the <b>Categories in the variable</b>"""
                               """ list box and enter a new category value in the <b>Value of the new category</b> """
                               """ line edit box. Click on <b>Add</b> to add a transformation, <b>Remove</b> """
                               """to remove a transformation and <b>Copy Old Values</b> to copy old categories.</font>""")
        oldnewWarning.setWordWrap(True)

        vLayout2 = self.vLayout([varCatsLabel, self.varCatsList, newCatLabel, self.newCatEdit])

        vLayout3 = self.vLayout([self.addRecCrit, self.removeRecCrit, self.copyOldCrit])
        vLayout3.addItem(QSpacerItem(10,100))

        vLayout4 = self.vLayout([recodeCritLabel, self.recodeCritList])


        hLayout = self.hLayout([vLayout2, vLayout3, vLayout4])

        dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Reset| QDialogButtonBox.Cancel| QDialogButtonBox.Ok)

        layout = QVBoxLayout()
        layout.addLayout(hLayout)
        layout.addWidget(oldnewWarning)
        layout.addWidget(dialogButtonBox)

        self.setLayout(layout)

        self.populate()

        self.connect(dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.connect(dialogButtonBox, SIGNAL("clicked(QAbstractButton *)"), self.reset)
        self.connect(self.varCatsList, SIGNAL("itemSelectionChanged()"), self.enableAddCrit)
        self.connect(self.varCatsList, SIGNAL("itemSelectionChanged()"), self.enableCopyOldCrit)
        self.connect(self.newCatEdit, SIGNAL("textChanged(const QString&)"), self.enableAddCrit)
        self.connect(self.recodeCritList, SIGNAL("itemSelectionChanged()"), self.enableRemoveCrit)

        self.connect(self.addRecCrit, SIGNAL("clicked()"), self.addRecCritList)
        self.connect(self.removeRecCrit, SIGNAL("clicked()"), self.removeRecCritList)
        self.connect(self.copyOldCrit, SIGNAL("clicked()"), self.addCopyOldCritList)


    def accept(self):
        self.recodeCrit = []

        if not self.recodeCritList.count() < 1:
            for i in range(self.recodeCritList.count()):
                itemText = self.recodeCritList.item(i).text()
                old, new = self.parse(itemText)

                self.recodeCrit.append([old,new])
                QDialog.accept(self)
        else:
            reply = QMessageBox.question(self, "PopGen: Display and Modify Data",
                                         QString("No recode criterion set. Do you wish to continue?"),
                                         QMessageBox.Yes| QMessageBox.No)
            if reply == QMessageBox.Yes:
                QDialog.accept(self)



    def parse(self, text):
        parsed = text.split(',')
        return int(parsed[0]), int(parsed[1])


    def reset(self):
        pass

    def enableAddCrit(self):
        try:
            int(self.newCatEdit.text())
            if len(self.varCatsList.selectedItems())>0:
                self.addRecCrit.setEnabled(True)
            else:
                self.addRecCrit.setEnabled(False)
        except Exception, e:
            self.addRecCrit.setEnabled(False)

    def enableCopyOldCrit(self):
        if len(self.varCatsList.selectedItems())>0:
            self.copyOldCrit.setEnabled(True)
        else:
            self.copyOldCrit.setEnabled(False)



    def enableRemoveCrit(self):
        if len(self.recodeCritList.selectedItems())>0:
            self.removeRecCrit.setEnabled(True)
        else:
            self.removeRecCrit.setEnabled(False)


    def addCopyOldCritList(self):
        items = self.varCatsList.selectedItems()
        recCrit = []

        for i in items:
            crit = '%s' %i.text() + ',' + '%s' %i.text()
            recCrit.append(crit)
            self.recCritDict[crit] = i.text()

        self.recodeCritList.addItems(recCrit)
        self.recodeCritList.sortItems()
        self.varCatsList.removeList(items)
        self.newCatEdit.clear()


    def addRecCritList(self):
        items = self.varCatsList.selectedItems()
        recCrit = []

        newCat = int(self.newCatEdit.text())

        for i in items:
            crit = '%s' %i.text() + ',' + '%s' %newCat
            recCrit.append(crit)
            self.recCritDict[crit] = i.text()

        self.recodeCritList.addItems(recCrit)
        self.recodeCritList.sortItems()
        self.varCatsList.removeList(items)
        self.newCatEdit.clear()


    def removeRecCritList(self):
        items = self.recodeCritList.selectedItems()

        for i in items:
            self.varCatsList.addItem(self.recCritDict['%s' %i.text()])
        self.varCatsList.sortItems()

        self.recodeCritList.removeList(items)


    def populate(self):

        catString = ['%s' %i for i in self.varcats]
        self.varCatsList.addItems(catString)
        self.varCatsList.sortItems()

    def hLayout(self, widgetList):
        layout = QHBoxLayout()
        for i in widgetList:
            layout.addLayout(i)
        return layout

    def vLayout(self, widgetList):
        layout = QVBoxLayout()
        for i in widgetList:
            layout.addWidget(i)
        return layout


class CreateVariable(QDialog):
    def __init__(self, project, database, tablename, variableTypeDict, title="", icon="", parent=None):
        super(CreateVariable, self).__init__(parent)

        self.setWindowTitle(title + " - %s" %tablename)
        self.setWindowIcon(QIcon("./images/%s.png" %icon))
        self.tablename = tablename
        self.project = project

        self.projectDBC = createDBC(self.project.db, database)
        self.projectDBC.dbc.open()

        self.variableDict = {}
        self.variables = variableTypeDict.keys()

        newVarLabel = QLabel("New Variable Name")
        self.newVarNameEdit = QLineEdit()
        variableListLabel = QLabel("Variables in Table")
        self.variableListWidget = ListWidget()
        variableCatsListLabel = QLabel("Categories")
        self.variableCatsListWidget = ListWidget()

        formulaLabel = QLabel("Expression")
        self.formulaEdit = QPlainTextEdit()
        formulaEgLabel = QLabel("<font color = brown>Eg. (1) Var1 + Var2; (2) 11 </font>")
        self.formulaEdit.setEnabled(False)
        whereLabel = QLabel("Filter Expression")
        self.whereEdit = QPlainTextEdit()
        dummy = "Eg. (1) Var1 > 10; (2) Var1 > 5 and var1 = 2; (3) var1 != 3"
        whereEgLabel = QLabel("<font color = brown>%s</font>" %dummy)
        self.whereEdit.setEnabled(False)

        createVarWarning = QLabel("""<font color = blue>Note: Enter the name of the new variable in <b>New Variable Name</b> """
                                  """line edit box, type the mathematical expression that defines the new variable in the """
                                  """<b>Expression</b> text edit box, and add any mathematical filter expression in the """
                                  """<b>Filter Expression</b> text edit box to create a new variable. """
                                  """The dialog also allows users to check the """
                                  """categories under any variable by clicking the variable in the """
                                  """<b>Variables in Table</b> list box.</font>""")

        createVarWarning.setWordWrap(True)
        vLayout2 = QVBoxLayout()
        vLayout2.addWidget(newVarLabel)
        vLayout2.addWidget(self.newVarNameEdit)

        hLayout1 = QHBoxLayout()
        vLayout3 = QVBoxLayout()
        vLayout3.addWidget(variableListLabel)
        vLayout3.addWidget(self.variableListWidget)
        vLayout4 = QVBoxLayout()
        vLayout4.addWidget(variableCatsListLabel)
        vLayout4.addWidget(self.variableCatsListWidget)
        hLayout1.addLayout(vLayout3)
        hLayout1.addLayout(vLayout4)
        vLayout2.addLayout(hLayout1)

        vLayout1 = QVBoxLayout()
        vLayout1.addWidget(formulaLabel)
        vLayout1.addWidget(formulaEgLabel)
        vLayout1.addWidget(self.formulaEdit)

        vLayout1.addWidget(whereLabel)
        vLayout1.addWidget(whereEgLabel)
        vLayout1.addWidget(self.whereEdit)


        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout2)
        hLayout.addLayout(vLayout1)

        dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)

        layout = QVBoxLayout()
        layout.addLayout(hLayout)
        layout.addWidget(createVarWarning)
        layout.addWidget(dialogButtonBox)

        self.setLayout(layout)
        self.populate()

        self.connect(self.newVarNameEdit, SIGNAL("textChanged(const QString&)"), self.checkNewVarName)
        self.connect(self.variableListWidget, SIGNAL("itemSelectionChanged()"), self.displayCats)
        self.connect(dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))


    def displayCats(self):
        varname = self.variableListWidget.currentItem().text()
        varCats = self.categories(varname)
        self.variableDict['%s' %varname] = varCats

        cats = ['%s' %i for i in self.variableDict['%s' %varname]]

        self.variableCatsListWidget.clear()
        self.variableCatsListWidget.addItems(cats)


    def checkNewVarName(self, name):

        import copy
        variables = copy.deepcopy(self.variables)

        variables = [('%s'%i).lower() for i in variables]

        name = ('%s'%name).lower()

        try:
            variables.index(name)
            self.enable(False)
        except:
            if len(name)>0:
                if not re.match("[A-Za-z]",name[0]):
                    self.enable(False)
                else:
                    self.enable(True)
                    if len(name)>1:
                        for i in name[1:]:
                            if not re.match("[A-Za-z_0-9]", i):
                                self.enable(False)
                            else:
                                self.enable(True)
            else:
                self.enable(False)


    def enable(self, value):
        self.formulaEdit.setEnabled(value)
        self.whereEdit.setEnabled(value)

    def populate(self):
        self.variables.sort()
        self.variableListWidget.addItems(self.variables)


    def categories(self, varname):
        cats = []

        query = QSqlQuery(self.projectDBC.dbc)
        query.exec_("""select %s from %s group by %s""" %(varname, self.tablename, varname))

        CATEGORY = 0

        while query.next():
            cat = unicode(query.value(CATEGORY).toString())
            #try:
            #    cat = query.value(CATEGORY).toInt()[0]
            #except:
            #    cat = query.value(CATEGORY).toString()
            #    print cat
            cats.append(cat)


        return cats



class DeleteRows(QDialog):
    def __init__(self, project, parentText, tablename, variableTypeDict, title="", icon="", parent=None):
        super(DeleteRows, self).__init__(parent)

        self.setWindowTitle(title + " - %s" %tablename)
        self.setWindowIcon(QIcon("./images/%s.png" %icon))
        self.tablename = tablename
        self.project = project

        if parentText == 'Project Tables':
            database = self.project.name
        elif parentText == 'Scenario Tables':
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)            

        self.projectDBC = createDBC(self.project.db, database)
        self.projectDBC.dbc.open()
        self.variableDict = {}
        self.variables = variableTypeDict.keys()

        variableListLabel = QLabel("Variables in Table")
        self.variableListWidget = ListWidget()
        variableCatsListLabel = QLabel("Categories")
        self.variableCatsListWidget = ListWidget()

        dummy = "Eg. Var1 > 10"
        whereLabel = QLabel("Filter Expression    " + "<font color = brown>%s</font>" %dummy)
        self.whereEdit = QPlainTextEdit()

        createVarWarning = QLabel("""<font color = blue>Note: Enter a mathematical filter expression in the """
                                  """<b>Filter Expression</b> text edit box to delete rows. """
                                  """The dialog also allows users to check the """
                                  """categories under any variable by selecting the variable in the """
                                  """<b>Variables in Table</b> list box.</font>""")

        createVarWarning.setWordWrap(True)
        vLayout2 = QVBoxLayout()

        hLayout1 = QHBoxLayout()
        vLayout3 = QVBoxLayout()
        vLayout3.addWidget(variableListLabel)
        vLayout3.addWidget(self.variableListWidget)
        vLayout4 = QVBoxLayout()
        vLayout4.addWidget(variableCatsListLabel)
        vLayout4.addWidget(self.variableCatsListWidget)
        hLayout1.addLayout(vLayout3)
        hLayout1.addLayout(vLayout4)
        vLayout2.addLayout(hLayout1)

        vLayout1 = QVBoxLayout()
        vLayout1.addWidget(whereLabel)
        vLayout1.addWidget(self.whereEdit)


        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout2)
        hLayout.addLayout(vLayout1)

        dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)

        layout = QVBoxLayout()
        layout.addLayout(hLayout)
        layout.addWidget(createVarWarning)
        layout.addWidget(dialogButtonBox)

        self.setLayout(layout)
        self.populate()

        self.connect(self.variableListWidget, SIGNAL("itemSelectionChanged()"), self.displayCats)
        self.connect(dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))

    def displayCats(self):
        varname = self.variableListWidget.currentItem().text()
        varCats = self.categories(varname)
        self.variableDict['%s' %varname] = varCats

        cats = ['%s' %i for i in self.variableDict['%s' %varname]]

        self.variableCatsListWidget.clear()
        self.variableCatsListWidget.addItems(cats)



    def populate(self):
        self.variableListWidget.addItems(self.variables)


    def categories(self, varname):
        cats = []

        query = QSqlQuery(self.projectDBC.dbc)
        query.exec_("""select %s from %s group by %s""" %(varname, self.tablename, varname))

        CATEGORY = 0

        while query.next():
            cat = unicode(query.value(CATEGORY).toString())
            cats.append(cat)
        return cats

class DisplayMapsDlg(QDialog):
    def __init__(self, project, tablename, title="", icon="", parent=None):


        self.tablename = tablename
        self.project = project
        self.fromTableToTable()
        self.check = self.isValid()
        


        if self.check < 0:
            super(DisplayMapsDlg, self).__init__(parent)
            self.setMinimumSize(QSize(950, 500))
            
            self.setWindowTitle(title)
            self.setWindowIcon(QIcon("./images/%s.png" %icon))



            scenarioDatabase = '%s%s%s' %(project.name, 'scenario', project.scenario)
            self.projectDBC = createDBC(self.project.db, scenarioDatabase)
            self.projectDBC.dbc.open()

            self.query = QSqlQuery(self.projectDBC.dbc)
            self.variableDict = {}
            self.variableTypeDict = self.populateVariableTypeDictionary(self.tablename)
            self.variables = self.variableTypeDict.keys()
            
            variableListLabel = QLabel("Variables in Table")
            self.variableListWidget = ListWidget()
            variableCatsListLabel = QLabel("Categories")
            self.variableCatsListWidget = ListWidget()
            self.variableListWidget.setMaximumWidth(200)
            self.variableCatsListWidget.setMaximumWidth(100)
        
            self.legendTable = QTableWidget()



            self.legendTable.setMaximumWidth(335)
            self.legendTable.setMaximumHeight(255)
        
            legendString = QLabel("Legend")
            self.legendTable.setHorizontalHeaderLabels(['Lower Limit', 'Upper Limit', 'Color'])
        

        # Displaying the thematic map
            self.canvas = QgsMapCanvas()
            self.canvas.setCanvasColor(QColor(255,255,255))
            self.canvas.enableAntiAliasing(True)
            self.canvas.useQImageToRender(False)

            if self.project.resolution == "County":
                self.res_prefix = "co"
            if self.project.resolution == "Tract":
                self.res_prefix = "tr"
            if self.project.resolution == "Blockgroup":
                self.res_prefix = "bg"

            self.stateCode = self.project.stateCode[self.project.state]
            resultfilename = self.res_prefix+self.stateCode+"_selected"
            self.resultsloc = self.project.location + os.path.sep + self.project.name + os.path.sep + "results"
        
            self.resultfileloc = os.path.realpath(self.resultsloc+os.path.sep+resultfilename+".shp")
            self.dbffileloc = os.path.realpath(self.resultsloc+os.path.sep+resultfilename+".dbf")

            layerName = self.project.name + '-' + self.project.resolution
            layerProvider = "ogr"
            self.layer = QgsVectorLayer(self.resultfileloc, layerName, layerProvider)

            renderer = self.layer.renderer()
            renderer.setSelectionColor(QColor(255,255,0))

            symbol = renderer.symbols()[0]
            symbol.setFillColor(QColor(153,204,0))

            if not self.layer.isValid():
                return
            QgsMapLayerRegistry.instance().addMapLayer(self.layer)
            self.canvas.setExtent(self.layer.extent())
            cl = QgsMapCanvasLayer(self.layer)
            layers = [cl]
        #self.canvas.setLayerSet(layers)

            self.toolbar = Toolbar(self.canvas, self.layer)
            self.toolbar.hideDragTool()
            self.toolbar.hideSelectTool()
        

            mapLabel = QLabel("Thematic Map")

        


            
            createVarWarning = QLabel("""<font color = blue>Note: Select a variable and category to view"""
                                      """ a thematic map displaying the proportion of the synthetic population"""
                                      """ belonging to a particular category of the selected variable """
                                      """ within each geography"""
                                      """</font>""")
            
            createVarWarning.setWordWrap(True)
            vLayout2 = QVBoxLayout()
            
            hLayout1 = QHBoxLayout()
            vLayout3 = QVBoxLayout()
            vLayout3.addWidget(variableListLabel)
            vLayout3.addWidget(self.variableListWidget)
            vLayout4 = QVBoxLayout()
            vLayout4.addWidget(variableCatsListLabel)
            vLayout4.addWidget(self.variableCatsListWidget)
            hLayout1.addLayout(vLayout3)
            hLayout1.addLayout(vLayout4)
            vLayout2.addLayout(hLayout1)
            
            vLayout5 = QVBoxLayout()
            vLayout5.addWidget(legendString)
            vLayout5.addWidget(self.legendTable)
            
            hLayout5 = QHBoxLayout()
            hLayout5.addLayout(vLayout5)
        
            vLayout2.addLayout(hLayout5)
            
            vLayout1 = QVBoxLayout()
            vLayout1.addWidget(mapLabel)
            vLayout1.addWidget(self.toolbar)
            vLayout1.addWidget(self.canvas)


            hLayout = QHBoxLayout()
            hLayout.addLayout(vLayout2)
            hLayout.addLayout(vLayout1)

            dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)
            
            layout = QVBoxLayout()
            layout.addLayout(hLayout)
            layout.addWidget(createVarWarning)
            layout.addWidget(dialogButtonBox)
        
            self.setLayout(layout)
            self.populate()
        
            self.connect(self.variableListWidget, SIGNAL("itemSelectionChanged()"), self.displayCats)
            self.connect(dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
            self.connect(dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
            self.connect(self.variableCatsListWidget, SIGNAL("itemSelectionChanged()"), self.displayMap)
            self.connect(self, SIGNAL("updateLimits()"), self.updateCatLimits)


    def updateCatLimits(self):
        #print 'minimum prop', self.minProp, 'maximum prop', self.maxProp
        self.updateColumnHeaders()
        if self.minProp <> 0 and self.maxProp <> 0:
            if self.minProp <> self.maxProp:
                for i in range(5):
                    itemMin = QTableWidgetItem('%.4f' %(self.minProp + i * self.intervalLength), 1000)
                    itemMax = QTableWidgetItem('%.4f' %(self.minProp + (i+ 1) * self.intervalLength), 1000)
                    self.legendTable.setItem(i, 0, itemMin)
                    self.legendTable.setItem(i, 1, itemMax)
            else:
                itemMin = QTableWidgetItem('%.4f' %(self.minProp), 1000)
                itemMax = QTableWidgetItem('%.4f' %(self.minProp), 1000)
                self.legendTable.setItem(0,0,itemMin)
                self.legendTable.setItem(0,1,itemMax)


    def updateColumnHeaders(self):
        item = QTableWidgetItem('Minimum', 1000)
        self.legendTable.setHorizontalHeaderItem(0, item)
        
        item = QTableWidgetItem('Maximum', 1000)
        self.legendTable.setHorizontalHeaderItem(1, item)
        
        item = QTableWidgetItem('Color', 1000)
        self.legendTable.setHorizontalHeaderItem(2, item)
            
        

    def isValid(self):
        retval = -1
        if not self.isResolutionValid():
            retval = 1
            return retval
        elif not self.isLayerValid():
            retval = 2
            return retval
        elif not self.isPopSyn():
            retval = 3
            return retval
        else:
            return retval

    def isResolutionValid(self):
        return self.project.resolution != "TAZ"

    def isLayerValid(self):
        res = ResultsGen(self.project)
        return res.create_hhmap()

    def isPopSyn(self):
        self.getGeographies()
        return len(self.geolist)>0

    def getGeographies(self):
        self.geolist = []
        for geo in self.project.synGeoIds.keys():
            geostr = str(geo[0]) + "," + str(geo[1]) + "," + str(geo[3]) + "," + str(geo[4])
            self.geolist.append(geostr)


    def accept(self):
        self.projectDBC.dbc.close()
        QDialog.accept(self)

    def reject(self):
        self.projectDBC.dbc.close()
        QDialog.reject(self)



    def makeTempTables(self, varname):
        query = QSqlQuery(self.projectDBC.dbc)
        query.exec_(""" DROP TABLE IF EXISTS %s""" %(self.toTable))
        if not query.exec_("""CREATE TABLE %s SELECT %s.*,%s FROM %s"""
                            """ LEFT JOIN %s using (serialno)""" %(self.toTable, self.fromTable, varname, self.fromTable, self.tablename)):
            raise FileError, query.lastError().text()


    def fromTableToTable(self):
        if self.tablename == 'hhld_sample':
            self.fromTable = 'housing_synthetic_data'
            self.toTable = 'temphhld'
        elif self.tablename == 'gq_sample':
            self.fromTable = 'housing_synthetic_data'
            self.toTable = 'tempgq'
        else:
            self.fromTable = 'person_synthetic_data'
            self.toTable = 'temp'



    def extractTotalsByCat(self, cat):
        query = QSqlQuery(self.projectDBC.dbc)
        varstr = self.variableListWidget.currentItem().text()
        if not query.exec_("""select state, county, tract, bg, sum(frequency) from %s where %s = %s """
                           """group by state, county, tract, bg"""
                           %(self.toTable, varstr, cat)):
            raise FileError, query.lastError().text()

        distDict = {}

        while query.next():
            state = str(query.value(0).toString())
            county = str(query.value(1).toString())
            tract = str(query.value(2).toString())
            bg = str(query.value(3).toString())

            value = query.value(4).toInt()[0]

            key = (state, county, tract, bg)
            
            distDict[key] = value

        return distDict        
        

    
    def displayMap(self):

        cat = int(self.variableCatsListWidget.currentItem().text())

        numDistDict = self.distDictList[cat-1]
        
        totalDistDict = {}
        distDict = {}

        varname = self.variableListWidget.currentItem().text()
        varCats = self.categories(varname)

        for i in numDistDict.keys():
            total = 0
            for j in varCats:
                try:
                    total = total + self.distDictList[int(j)-1][i]
                except:
                    total = total + 0
            totalDistDict[i] = total
            if total == 0:
                distDict[i] = 0
            else:
                distDict[i] = float(numDistDict[i])/total


        try:
            self.minProp = min(distDict.values())
            self.maxProp = max(distDict.values())
        # assuming 5 categories
            self.intervalLength = (self.maxProp - self.minProp)/5

            for i in distDict.keys():
                if distDict[i] == self.minProp:
                    distDict[i] = 1.0
                else:
                    distDict[i] = ceil((distDict[i]-self.minProp)/self.intervalLength)


            if self.minProp == self.maxProp:
                self.legendTable.clear()
                self.legendTable.setColumnCount(3)
                self.legendTable.setRowCount(1)
                item = QTableWidgetItem(1000)
                item.setBackgroundColor(QColor(255, 205, 205))
                self.legendTable.setItem(0, 2, item)
            else:
                self.legendTable.clear()
                self.legendTable.setColumnCount(3)
                self.legendTable.setRowCount(5)
                for i in range(6):
                    item = QTableWidgetItem(1000)
                    item.setBackgroundColor(QColor(255, 255- (50 * i), 255 - (50 * i)))
                    if i > 0:
                        self.legendTable.setItem(i-1,2,item)

        # proportions calculated, categories calculated
        # TO DO - append to the shapefile? show the colors?
                
        except Exception, e:
            print e
            self.minProp = 0
            self.maxProp = 0
            self.intervalLength = 0
            if len(distDict) == 0:
                QMessageBox.warning(self, "Thematic Map", """No population for variable - %s and category - %s """
                                    """present in the geographies"""
                                    """ synthesized so far""" %(varname, cat), QMessageBox.Ok)
        

        self.stateCode = self.project.stateCode[self.project.state]
        resultfilename = self.res_prefix+self.stateCode+"_selected"
        self.resultsloc = self.project.location + os.path.sep + self.project.name + os.path.sep + "results"
        
        self.resultfileloc = os.path.realpath(self.resultsloc+os.path.sep+resultfilename+".shp")
        self.dbffileloc = os.path.realpath(self.resultsloc+os.path.sep+resultfilename+".dbf")

        layerName = self.project.name + '-' + self.project.resolution
        layerProvider = "ogr"
        self.layer = QgsVectorLayer(self.resultfileloc, layerName, layerProvider)

        # Generating a random number field to the shape files database
        var =  'freq'
        f = open(self.dbffileloc, 'rb')
        db = list(dbfreader(f))
        f.close()
        fieldnames, fieldspecs, records = db[0], db[1], db[2:]
        if var not in fieldnames:
            fieldnames.append(var)
            fieldspecs.append(('N',11,0))
            freqidx = -1
        else:
            freqidx = fieldnames.index("freq")
        for rec in records:
            state = '%s' %int(rec[fieldnames.index("STATE")])
            if self.res_prefix == "co":
                coidx = fieldnames.index("COUNTY")
                compid = state, '%s' %int(rec[coidx].strip()),'0','0'
            elif self.res_prefix == "tr":
                coidx = fieldnames.index("COUNTY")
                tridx = fieldnames.index("TRACT")
                compid = state,'%s' %int(rec[coidx].strip()), ('%s' %int((rec[tridx].strip()).ljust(6,'0'))),'0'
            elif self.res_prefix == "bg":
                coidx = fieldnames.index("COUNTY")
                tridx = fieldnames.index("TRACT")
                bgidx = fieldnames.index("BLKGROUP")
                compid = state, '%s' %int(rec[coidx].strip()) , ('%s' %int((rec[tridx].strip()).ljust(6,'0'))) , '%s' %int(rec[bgidx].strip())
                
            if compid in distDict:
                if freqidx > 0:
                    rec[freqidx] = distDict[compid]
                else:
                    rec.append(distDict[compid])
            else:
                if freqidx > 0:
                    rec[freqidx] = 0
                else:
                    rec.append(0)
                    
        f = open(self.dbffileloc, 'wb')
        dbfwriter(f, fieldnames, fieldspecs, records)
        f.close()

        self.layer.setRenderer(QgsUniqueValueRenderer(self.layer.vectorType()))

        self.layer.setRenderer(QgsContinuousColorRenderer(self.layer.vectorType()))
        r = self.layer.renderer()
        provider = self.layer.getDataProvider()
        idx = provider.indexFromFieldName(var)

        r.setClassificationField(idx)
        #minval = provider.minValue(idx).toString()
        #maxval = provider.maxValue(idx).toString()
        minval = '0'
        maxval = '5'
        minsymbol = QgsSymbol(self.layer.vectorType(), minval, "","")
        minsymbol.setBrush(QBrush(QColor(255,255,255)))
        maxsymbol = QgsSymbol(self.layer.vectorType(), maxval, "","")
        maxsymbol.setBrush(QBrush(QColor(255,5,5)))
        #maxsymbol.setBrush(QBrush(QColor(0,0,0)))
        r.setMinimumSymbol(minsymbol)
        r.setMaximumSymbol(maxsymbol)
        r.setSelectionColor(QColor(255,255,0))
        r.setDrawPolygonOutline(True)
        
        QgsMapLayerRegistry.instance().addMapLayer(self.layer)
        self.canvas.setExtent(self.layer.extent())

        cl = QgsMapCanvasLayer(self.layer)
        layers = [cl]
        self.canvas.setLayerSet(layers)

        self.canvas.refresh()

        self.emit(SIGNAL("updateLimits()"))
        


    def populateVariableTypeDictionary(self, tablename):

        variableTypeDictionary = {}
        self.query.exec_("""desc %s""" %tablename)

        FIELD, TYPE, NULL, KEY, DEFAULT, EXTRA = range(6)

        while self.query.next():
            field = '%s' %self.query.value(FIELD).toString()
            type = self.query.value(TYPE).toString()
            null = self.query.value(NULL).toString()
            key = self.query.value(KEY).toString()
            default = self.query.value(DEFAULT).toString()
            extra = self.query.value(EXTRA).toString()

            unanalyVars = ['state', 'pumano', 'hhid', 
                         'serialno', 'pnum', 'hhlduniqueid', 
                         'personuniqueid', 'gquniqueid', 'hhtype']


            if not field in unanalyVars:
                variableTypeDictionary['%s' %field] = type

        return variableTypeDictionary


    def displayCats(self):
        varname = self.variableListWidget.currentItem().text()
        varCats = self.categories(varname)
        self.variableDict['%s' %varname] = varCats

        cats = ['%s' %i for i in self.variableDict['%s' %varname]]

        self.variableCatsListWidget.clear()
        self.variableCatsListWidget.addItems(cats)

        self.makeTempTables(varname)

        self.distDictList = []
        for cat in varCats:
            distDict = self.extractTotalsByCat(cat)
            self.distDictList.append(distDict)
            
        layers = []
        self.canvas.setLayerSet(layers)
        self.canvas.refresh()

        


    def populate(self):
        self.variableListWidget.addItems(self.variables)


    def categories(self, varname):
        cats = []

        self.query.exec_("""select %s from %s group by %s""" %(varname, self.tablename, varname))

        CATEGORY = 0

        while self.query.next():
            cat = unicode(self.query.value(CATEGORY).toString())
            cats.append(cat)
        return cats


class ChangeMargsDlg(DisplayMapsDlg):
    def __init__(self, project, tabletype, title="", icon="", parent=None):
        super(DisplayMapsDlg, self).__init__(parent)

        self.setMinimumSize(QSize(1100, 700))

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("./images/%s.png"%icon))

        self.tabletype = tabletype
        self.tablename = "%s_sample" %tabletype
        self.mtablename = "%s_marginals" %tabletype

        self.project = project
        
        check = self.isValid()
        
        if check:
            self.emit(SIGNAL("rejected()"))
            

        self.projectDBC = createDBC(self.project.db, self.project.name)
        self.projectDBC.dbc.open()
        self.query = QSqlQuery(self.projectDBC.dbc)
        self.variableDict = {}
        self.variableTypeDict = self.populateVariableTypeDictionary(self.tablename)
        self.variables = self.variableTypeDict.keys()

        self.totalControl = 0
        self.totalAdj = 0

        self.adjDict = defaultdict(dict)

        geographyLabel = QLabel("Geography ID")
        self.geographyComboBox = QComboBox()
        geoids = self.allGeographyids().keys()
        geoids.sort()
        self.geographyComboBox.addItems(geoids)
        
        


        variableListLabel = QLabel("Variables in Table")
        self.variableListWidget = ListWidget()
        self.variableListWidget.setMaximumWidth(200)

        self.totalDisplay = TotalLabelBox()
        

        self.sliderSpace = QWidget()
        sliderSpaceLabel = QLabel("Modify")
        self.sliderSpace.setMinimumSize(QSize(650, 475))

        
        self.listWidget = ListWidget()
        #addScenarioButton = QPushButton("Add Scenario")
        #delScenarioButton = QPushButton("Delete Scenario")

        changeMargsLabel = QLabel("""<font color = blue>Select a geography ID from the <b>Geography ID</b> drop down menu"""
                                  """ and select a household variable from the <b>Variables in Table</b> list box"""
                                  """ to modify the marginals distribution for the variable. """
                                  """ Marginals can be modified by using the slider or the spin box. Note that"""
                                  """ the modified marginals total and the actual total should remain the same."""
                                  """ After modifying the marginals, click on <b>Add to Scenario</b> to use the """
                                  """ modified marginals for the selected geography. Note that if you modify """
                                  """ household marginals here and also choose to adjust/modify the household control variable distributions """
                                  """ in the Set Correspondence Variables option, the modified marginals from the later option """
                                  """ will be used. However for groupquarter and person control variable distributions the modified marginals"""
                                  """ from this option are used.</font> """)
        changeMargsLabel.setWordWrap(True)
        

        addToScenarioButton = QPushButton("Add to Scenario")
        delFromScenarioButton = QPushButton("Delete from Scenario")
        

        hLayout2 = QHBoxLayout()
        #hLayout2.addWidget(addScenarioButton)
        #hLayout2.addWidget(delScenarioButton)
        hLayout2.addItem(QSpacerItem(100, 10))
        hLayout2.addWidget(addToScenarioButton)
        hLayout2.addWidget(delFromScenarioButton)
        hLayout2.addItem(QSpacerItem(100, 10))
        


        vLayout4 = QVBoxLayout()
        vLayout4.addWidget(sliderSpaceLabel)
        vLayout4.addWidget(self.sliderSpace)

        vLayout2 = QVBoxLayout()

        hLayout1 = QHBoxLayout()
        vLayout3 = QVBoxLayout()
        
        vLayout3.addWidget(geographyLabel)
        vLayout3.addWidget(self.geographyComboBox)
        vLayout3.addWidget(variableListLabel)
        vLayout3.addWidget(self.variableListWidget)
        vLayout3.addWidget(self.totalDisplay)

        hLayout1.addLayout(vLayout3)
        vLayout2.addLayout(hLayout1)


        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout2)
        hLayout.addLayout(vLayout4)
        dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)

        layout = QVBoxLayout()
        layout.addLayout(hLayout)
        layout.addLayout(hLayout2)
        layout.addWidget(self.listWidget)
        layout.addWidget(changeMargsLabel)
        layout.addWidget(dialogButtonBox)

        self.sliders = []

        self.setLayout(layout)
        self.populate()
        self.displaySliders()

        #self.variableListWidget.setItemSelected(self.variableListWidget.item(0), True)


        self.connect(self.variableListWidget, SIGNAL("itemSelectionChanged()"), self.unhideSliders)
        self.connect(self.geographyComboBox, SIGNAL("currentIndexChanged(int)"), self.unhideSliders)
        self.connect(dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))

        for j in range(len(self.sliders)):
            self.connect(self.sliders[j].sliderAdj.slider, SIGNAL("sliderMoved(int)"), self.updateTotals)
            self.connect(self.sliders[j].sliderAdj.valueBox, SIGNAL("valueChanged(int)"), self.updateTotals)


        self.connect(addToScenarioButton, SIGNAL("clicked()"), self.addToScenario)
        self.connect(delFromScenarioButton, SIGNAL("clicked()"), self.delFromScenario)


    def addToScenario(self):
        if self.checkTotals():
            if self.controlDistribution == self.controlDistributionAdj:
                QMessageBox.information(self, "Modify Control Variable Distributions", 
                                        """No changes made to the control Variable Distributions for the selected"""
                                        """ geography.""", QMessageBox.Ok)
            else:
                selGeography = '%s' %self.geographyComboBox.currentText()
                selVar = '%s' %self.variableListWidget.currentItem().text()
                adjText = "%s;%s-%s-->%s" %(selGeography, selVar, self.controlDistribution, self.controlDistributionAdj) 
                
                if selVar in self.adjDict[selGeography].keys():
                    reply = QMessageBox.question(self, "Modify Control Variable Distributions",
                                                 """Adjustment for the Control Variable Distributions already exists"""
                                                 """ for geography - %s. Do you wish to replace?""" %(selGeography),
                                                 QMessageBox.Yes|QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        adjToRemove = self.adjDict[selGeography][selVar]
                        textToRemove = "%s;%s-%s-->%s" %(selGeography, selVar, adjToRemove[0], adjToRemove[1])
                        row = self.listWidget.rowOf(textToRemove)
                        self.listWidget.takeItem(row)
                        self.adjDict[selGeography][selVar] = [self.controlDistribution, self.controlDistributionAdj]
                        self.listWidget.addItem(adjText)
                else:
                    self.adjDict[selGeography][selVar] = [self.controlDistribution, self.controlDistributionAdj]
                    self.listWidget.addItem(adjText)

    def delFromScenario(self):
        try:
            removeText = self.listWidget.currentItem().text()
            row = self.listWidget.rowOf(removeText)
            self.listWidget.takeItem(row)
            splitRemoveText = re.split("[;\-\>]", removeText)
            selGeography = ('%s' %splitRemoveText[0])
            selVar = ('%s' %splitRemoveText[1])
            del(self.adjDict[selGeography][selVar])
        except Exception, e:
            QMessageBox.warning(self, "Modify Control Variable Distributions",
                                """No changes selected. Select a change to the marginal distribution and then press Delete from Scenario""", QMessageBox.Ok)


    def accept(self):
        self.projectDBC.dbc.close()
        QDialog.accept(self)
        #print 'adjusted dictionary', self.adjDict
        if self.tabletype == 'hhld':
            self.project.adjControlsDicts.hhld = self.adjDict
        elif self.tabletype == 'gq':
            self.project.adjControlsDicts.gq = self.adjDict
        elif self.tabletype == 'person':
            self.project.adjControlsDicts.person = self.adjDict

        self.project.save()


    def reject(self):
        self.projectDBC.dbc.close()
        QDialog.reject(self)


    def checkTotals(self):
        if len(self.variableListWidget.selectedItems())>0:
            if self.totalControl == self.totalAdj:
                return True
            else:
                #QMessageBox.warning(self, "Modify Control Variable Distributions", 
                #                    """The adjusted control variable distribution total must be equal to """
                #                    """the actual control variable distribution total.""",
                #                    QMessageBox.Ok)                        
                #return False
                QMessageBox.warning(self, "Modify Control Variable Distributions", 
                                    """The adjusted control variable distribution total is different from """
                                    """the actual control variable distribution total. Please note that if you wish """
                                    """to modify the totals please make appropriate changes to the other """
                                    """control varaibles of interest to avoid inconsistency in the totals obtained """
                                    """from the marginal distributions of the variables.""",
                                    QMessageBox.Ok)                        
                return True

        else:
            QMessageBox.warning(self, "Modify Control Variable Distributions", 
                                """Select a variable, modify the control variable distribution and then press """
                                """Add to Scenario.""",
                                QMessageBox.Ok)                        
            return False


    def unhideSliders(self):

        if len(self.variableListWidget.selectedItems()) > 0:

            self.varname = self.variableListWidget.selectedItems()[0].text()
            self.selVarCategories = self.categories(self.varname)
            
            self.controlDistribution = self.retrieveControlDistribution()
            self.controlDistributionAdj = self.controlDistribution
            self.totalControl = sum(self.controlDistribution)
            
        # Trying to get the layout for the sliders
            self.numCategories = len(self.selVarCategories)
            
            if self.numCategories > 10:
                QMessageBox.warning(self, "Modify Control Variable Distributions", 
                                    """Only control variable distributions of variables with 10 or fewer """
                                    """categories can be modified. Select another variable.""",
                                    QMessageBox.Ok)
                self.variableListWidget.clearSelection()
                self.variableListWidget.clearFocus()
                
                self.variableListWidget.setItemSelected(self.variableListWidget.item(0), True)
                return

            for j in range(self.numCategories):
                self.sliders[j].sliderGiven.slider.setRange(0, self.totalControl)
                self.sliders[j].sliderGiven.valueBox.setRange(0, self.totalControl)
                
                self.sliders[j].sliderAdj.slider.setRange(0, self.totalControl)
                self.sliders[j].sliderAdj.valueBox.setRange(0, self.totalControl)
                
                self.sliders[j].sliderGiven.slider.setValue(self.controlDistribution[j])
                self.sliders[j].sliderGiven.valueBox.setValue(self.controlDistribution[j])
                
                self.sliders[j].sliderAdj.slider.setValue(self.controlDistribution[j])
                self.sliders[j].sliderAdj.valueBox.setValue(self.controlDistribution[j])
                
                self.sliders[j].setHidden(False)
                self.sliders[j].labelWidget.setText('Category - %s' %self.selVarCategories[j])
                
            for j in range(10 - self.numCategories):
                self.sliders[j+self.numCategories].setHidden(True)
        

    def updateTotals(self):
        self.totalDisplay.actualTotal.setText("Actual Total - %s" %self.totalControl)
        
        self.totalAdj = 0
        self.controlDistributionAdj = []

        for j in range(self.numCategories):
            dummy = self.sliders[j].sliderAdj.slider.value()
            self.totalAdj = self.totalAdj + dummy
            self.controlDistributionAdj.append(dummy)
        
        self.totalDisplay.adjustedTotal.setText("Adjusted Total - %s" %self.totalAdj)


    def retrieveControlDistribution(self):
        marginals = []
        selGeoidText = self.geographyComboBox.currentText()
        
        self.selGeoid = re.split("[,]", selGeoidText)

        state, county, tract, bg = self.selGeoid
        for j in self.selVarCategories:
            catText = '%s, Category %s' %(self.varname, j)
            corrControlVar = self.variablesCorrDict['%s' %self.varname][catText]

            if not self.query.exec_("""select %s from %s where state = %s and county = %s """
                                       """and tract = %s and bg = %s""" 
                                       %(corrControlVar, self.mtablename, state, county, tract, bg)):
                raise FileError, self.query.lastError().text()
            while self.query.next():
                marginalVal = self.query.value(0).toInt()[0]

            marginals.append(marginalVal)

        return marginals
            

        

    def displaySliders(self):
        # Trying to get the layout for the sliders
        cols = 5
        rows = 2
        
        hLayout = QHBoxLayout()
        for j in range(cols):
            vLayout = QVBoxLayout()
            for i in range(rows):
                slider = self.slider()
                self.sliders.append(slider)
                vLayout.addWidget(slider)
                slider.setHidden(True)
            hLayout.addLayout(vLayout)
        self.sliderSpace.setLayout(hLayout)

    def slider(self, category=None):
        # we also need a label and list box at the bottom
        # they should be attached to each other so that if one changes the other reflects the change
        return SliderBoxCombo(category)

    def populate(self):
        if self.tabletype == 'hhld':
            self.variablesCorrDict = self.project.selVariableDicts.hhld
            self.adjDict = copy.deepcopy(self.project.adjControlsDicts.hhld)
        elif self.tabletype == 'gq':
            self.variablesCorrDict = self.project.selVariableDicts.gq
            self.adjDict = copy.deepcopy(self.project.adjControlsDicts.gq)
        elif self.tabletype == 'person':
            self.variablesCorrDict = self.project.selVariableDicts.person
            self.adjDict = copy.deepcopy(self.project.adjControlsDicts.person)

        self.variables = self.variablesCorrDict.keys()
        self.variableListWidget.addItems(self.variables)

        for i in self.adjDict.keys():
            for j in self.adjDict[i].keys():
                
                geography = i
                selVar = j
                controlDistribution = self.adjDict[i][j][0]
                controlDistributionAdj = self.adjDict[i][j][1]
                text = "%s;%s-%s-->%s" %(geography, selVar, controlDistribution, controlDistributionAdj)
                
                self.listWidget.addItem(text)


    def categories(self, varname):
        cats = []

        self.query.exec_("""select %s from %s group by %s""" %(varname, self.tablename, varname))

        CATEGORY = 0

        while self.query.next():
            cat = unicode(self.query.value(CATEGORY).toString())
            cats.append(cat)
        return cats 

    def allGeographyids(self):

        allGeoids = {}
        for i in self.project.region.keys():
            countyName = i
            stateName = self.project.region[i]
            countyText = '%s,%s' %(countyName, stateName)
            countyCode = self.project.countyCode[countyText]
            stateCode = self.project.stateCode[stateName]

            if self.project.resolution == 'County':
                if not self.query.exec_("""select state, county from geocorr where state = %s and county = %s"""
                                   """ group by state, county"""
                                   %(stateCode, countyCode)):
                    raise FileError, self.query.lastError().text()
            elif self.project.resolution == 'Tract':
                if not self.query.exec_("""select state, county, tract from geocorr where state = %s and county = %s"""
                                   """ group by state, county, tract"""
                                   %(stateCode, countyCode)):
                    raise FileError, self.query.lastError().text()
            else:
                if not self.query.exec_("""select state, county, tract, bg from geocorr where state = %s and county = %s"""
                                   """ group by state, county, tract, bg"""
                                   %(stateCode, countyCode)):
                    raise FileError, self.query.lastError().text()
        #return a dictionary of all VALID geographies

            STATE, COUNTY, TRACT, BG = range(4)


            tract = 0
            bg = 0

            while self.query.next():
                state = self.query.value(STATE).toInt()[0]
                county = self.query.value(COUNTY).toInt()[0]

                if self.project.resolution == 'Tract' or self.project.resolution == 'Blockgroup' or self.project.resolution == 'TAZ':
                    tract = self.query.value(TRACT).toInt()[0]
                if self.project.resolution == 'Blockgroup' or self.project.resolution == 'TAZ':
                    bg = self.query.value(BG).toInt()[0]

                id = '%s,%s,%s,%s' %(state, county, tract, bg)
                idText = 'State - %s, County - %s, Tract - %s, Block Group - %s' %(state, county, tract, bg)

                allGeoids[id] = idText

        return allGeoids


class TotalLabelBox(QWidget):
    def __init__(self, parent=None):
        super(TotalLabelBox, self).__init__(parent)
        
        self.actualTotal = QLabel()
        self.adjustedTotal = QLabel()

        groupBox = QGroupBox()
        
        layout = QVBoxLayout()
        layout.addWidget(self.actualTotal)
        layout.addWidget(self.adjustedTotal)
        groupBox.setLayout(layout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(groupBox)
        
        self.setLayout(hLayout)
        


class ScenarioTab(QTabWidget):
    def __init__(self, label, parent=None):
        super(ScenarioTab, self).__init__(parent)

        




class SliderBoxCombo(QWidget):
    def __init__(self, label, parent=None):
        super(SliderBoxCombo, self).__init__(parent)
        
        self.labelWidget = QLabel()
        self.sliderGiven = SliderBox('Act')
        self.sliderGiven.slider.setEnabled(False)
        self.sliderGiven.valueBox.setEnabled(False)
        
        self.sliderAdj = SliderBox('Adj')

        groupBox = QGroupBox()

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.sliderGiven)
        hLayout.addWidget(self.sliderAdj)
        
        groupBox.setLayout(hLayout)
        
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.labelWidget)
        vLayout.addWidget(groupBox)

        self.setMaximumSize(200, 235)

        self.setLayout(vLayout)


class SliderBox(QWidget):
    def __init__(self, label, parent=None):
        super(SliderBox, self).__init__(parent)

        self.setMaximumWidth(75)
        self.setMinimumHeight(125)

        sliderLabel = QLabel(label)
        self.slider = QSlider()
        self.valueBox = QSpinBox()

        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(self.slider)
        
        vLayout1 = QVBoxLayout()
        vLayout1.addWidget(sliderLabel)
        vLayout1.addLayout(hLayout1)
        vLayout1.addWidget(self.valueBox)
        
        self.setLayout(vLayout1)

        self.connect(self.slider, SIGNAL("sliderMoved(int)"), self.sliderMoved)
        self.connect(self.valueBox, SIGNAL("valueChanged(int)"), self.valueChanged)

    def sliderMoved(self, value):
        self.valueBox.setValue(value)
        
    def valueChanged(self, value):
        self.slider.setValue(value)
        
        


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    var = {}
    var['first'] = [1,2,3,4,-99]
    var['second'] = [3,4,1,-1]

    dia = CreateVariable(var)
    dia.show()
    app.exec_()


