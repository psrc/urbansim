# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

import sys
import re
import numpy

from collections import defaultdict

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *


from database.createDBConnection import createDBC
from gui.misc.widgets import *


class SetCorrDialog(QDialog):
    def __init__(self, project, parent=None):
        super(SetCorrDialog, self).__init__(parent)

        self.setWindowTitle("Corresponding Sample Categories with Marginal Variables")
        self.setWindowIcon(QIcon("./images/varcorr.png"))
        import copy
        self.project = copy.deepcopy(project)
        self.projectDBC = createDBC(self.project.db, self.project.name)
        self.projectDBC.dbc.open()

        self.persControlGroupBox = QGroupBox("""a. Do you wish to match distributions of both Persons """
                                             """and Household attributes of interest?""")
        self.persControlYes = QRadioButton("Yes")
        self.persControlNo = QRadioButton("No")
        self.persControlYes.setChecked(True)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.persControlYes)
        hLayout.addWidget(self.persControlNo)
        self.persControlGroupBox.setLayout(hLayout)
        
        setCorrespondenceLabel = QLabel("""b. Set the correspondence between """
                                        """the sample variable categories and the columns in the Marginals table""")
        self.tabWidget = SetCorrTabWidget(self.project)

        dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)

        correspondenceWarning = QLabel("""<font color = blue>Note: Select household/person/groupquarter variables of interest """
                                       """from the <b>'Sample Variable'</b> that you wish to control. Once these have been selected, """
                                       """create appropriate mapping between the categories of the selected variables and """
                                       """the columns in the marginal tables. To do this, highlight a category from the """
                                       """<b>'Selected Variable Categories'</b> and the corresponding column name under the """
                                       """<b>'Marginal Variables'</b> and click on <b>'Add Correspondence'</b>.</font>""")
        correspondenceWarning.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.persControlGroupBox)
        layout.addWidget(Separator())
        layout.addWidget(setCorrespondenceLabel)
        layout.addWidget(self.tabWidget)
        layout.addWidget(correspondenceWarning)
        layout.addWidget(dialogButtonBox)
        self.setLayout(layout)

        hhldSelVariableDicts = copy.deepcopy(self.project.selVariableDicts.hhld)
        self.populate(hhldSelVariableDicts, self.tabWidget.housingTab)
        if self.tabWidget.personAnalyzed:
            personSelVariableDicts = copy.deepcopy(self.project.selVariableDicts.person)
            self.populate(personSelVariableDicts, self.tabWidget.personTab)
        if self.tabWidget.gqAnalyzed:
            gqSelVariableDicts = copy.deepcopy(self.project.selVariableDicts.gq)
            self.populate(gqSelVariableDicts, self.tabWidget.gqTab)

        self.connect(dialogButtonBox, SIGNAL("accepted()"), self.acceptCheck)
        self.connect(dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
        self.connect(self.persControlYes, SIGNAL("clicked()"), self.persControlYesAction)
        self.connect(self.persControlNo, SIGNAL("clicked()"), self.persControlNoAction)

    def persControlYesAction(self):
        #self.tabWidget.personTab.setEnabled(True)
        self.project.selVariableDicts.persControl = True




    def persControlNoAction(self):
        #self.tabWidget.personTab.setEnabled(False)
        self.project.selVariableDicts.persControl = False
        

    def populate(self, selVariable, tab):
        for i in selVariable.keys():

            tab.selSampleVarListWidget.addItem(i)
            row = tab.sampleVarListWidget.rowOf(i)
            tab.sampleVarListWidget.setCurrentRow(row)
            tab.sampleVarListWidget.remove()
            cats = []
            for j in selVariable[i].keys():

                varCatString = j

                dummy = ('%s' %j).split()

                sampleVarCat = dummy[-1]
                varName = i
                controlVar = selVariable[i][varCatString]

                relation = '%s -  %s' %(varCatString, controlVar)

                tab.selVarCatStrings[varCatString] = varName
                tab.relationStrings[relation] = varName
                tab.selVariables = selVariable

                tab.selSampleVarCatListWidget.addItem(varCatString)
                tab.relationsListWidget.addItem(relation)

                cats.append(sampleVarCat)
            tab.sampleVarsDict[i] = cats

        if self.tabWidget.personAnalyzed:
            if self.project.selVariableDicts.persControl:
                #self.tabWidget.personTab.setEnabled(True)
                self.persControlYes.setChecked(True)
            else:
                #self.tabWidget.personTab.setEnabled(False)
                self.persControlNo.setChecked(True)

        if self.project.selVariableDicts.hhldMargsModify:
            self.tabWidget.housingTab.modifyMargsYes.setChecked(True)
            self.tabWidget.housingTab.hhldsizeVarNameComboBox.setEnabled(True)
            text = self.project.selVariableDicts.hhldSizeVarName
            index = self.tabWidget.housingTab.hhldsizeVarNameComboBox.findText(text)
            if index>0:
                self.tabWidget.housingTab.hhldsizeVarNameComboBox.setCurrentIndex(index)

            hhldSize = self.project.selVariableDicts.aveHhldSizeLastCat
            self.tabWidget.housingTab.hhldsizeAverageLineEdit.setEnabled(True)
            self.tabWidget.housingTab.hhldsizeAverageLineEdit.setText(hhldSize)

            self.tabWidget.housingTab.persRefVarNameComboBox.setEnabled(True)
            text = self.project.selVariableDicts.refPersName
            index = self.tabWidget.housingTab.persRefVarNameComboBox.findText(text)

            if index>0:
                self.tabWidget.housingTab.persRefVarNameComboBox.setCurrentIndex(index)
        else:
            self.tabWidget.housingTab.modifyMargsNo.setChecked(True)




    def acceptCheck(self):
        if self.tabWidget.housingTab.modifyMargsYes.isChecked():
            #print 'in correspondence hhlds are modified'
            self.project.selVariableDicts.hhldMargsModify = True
            self.project.selVariableDicts.hhldSizeVarName = self.tabWidget.housingTab.hhldsizeVarNameComboBox.currentText()
            self.project.selVariableDicts.aveHhldSizeLastCat = self.tabWidget.housingTab.hhldsizeAverageLineEdit.text()
            self.project.selVariableDicts.refPersName = self.tabWidget.housingTab.persRefVarNameComboBox.currentText()
            if self.checkIfRefPersCorrDefined():
                refPersCheck = True
            else:
                refPersCheck = False

        else:
            self.project.selVariableDicts.hhldMargsModify = False
            self.project.selVariableDicts.hhldSizeVarName = ""                    
            self.project.selVariableDicts.aveHhldSizeLastCat = ""
            self.project.selVariableDicts.refPersName = ""
            refPersCheck = True

        


        if self.tabWidget.housingTab.check():
            #print 'original', self.project.selVariableDicts.hhld
            #print 'modified', self.tabWidget.housingTab.selVariables
            if self.project.selVariableDicts.hhld <> self.tabWidget.housingTab.selVariables:
                self.project.selVariableDicts.hhld = self.tabWidget.housingTab.selVariables
                self.project.hhldVars, self.project.hhldDims =  self.checkIfRelationsDefined(self.project.selVariableDicts.hhld)
            hhldCheck = True
        else:
            hhldCheck = False            

                #self.clearTables('hhld')
        if self.tabWidget.personAnalyzed:
            if self.tabWidget.personTab.check():
                if self.project.selVariableDicts.person <> self.tabWidget.personTab.selVariables:
                    self.project.selVariableDicts.person = self.tabWidget.personTab.selVariables
                    self.project.personVars, self.project.personDims = self.checkIfRelationsDefined(self.project.selVariableDicts.person, True)
                persCheck = True
                        #self.clearTables('person')
            else:
                persCheck = False
        else:
            persCheck = True

        if self.tabWidget.gqAnalyzed:
            if self.tabWidget.gqTab.checkNumRelationsDefined():
                if self.project.selVariableDicts.gq <> self.tabWidget.gqTab.selVariables:
                    self.project.selVariableDicts.gq = self.tabWidget.gqTab.selVariables
                    self.project.gqVars, self.project.gqDims = self.checkIfRelationsDefined(self.project.selVariableDicts.gq, True)
                        #self.clearTables('gq')


        if refPersCheck and hhldCheck and persCheck:
            self.acceptAction()

    def checkIfRefPersCorrDefined(self):
        refPersName = self.tabWidget.housingTab.persRefVarNameComboBox.currentText()
        
        row = self.tabWidget.personTab.selSampleVarListWidget.rowOf(refPersName)
        
        if row < 0:
            QMessageBox.warning(self, "Corresponding Sample Categories with Marginal Variables", 
                                """Reference person variable selected but the correspondence between the selected variable's categories """
                                """and the columns in the marginals table not defined in the 'Person Variables' tab.""", QMessageBox.Ok)
            return False
        else:
            return True
                        

    def acceptAction(self):
        self.projectDBC.dbc.close()
        #QDialog.hide(self)
        QDialog.accept(self)
        

    def clearTables(self, tableNamePrefix):
        #print "variable relations modified - %s" %(tableNamePrefix)
        self.projectDBC.dbc.open()
        query = QSqlQuery(self.projectDBC.dbc)
        if not query.exec_("""show tables"""):
            raise FileError, query.lastError().text()

        query1 = QSqlQuery(self.projectDBC.dbc)

        while query.next():
            tableName = query.value(0).toString()
            if tableName.startsWith(tableNamePrefix) and (tableName.endsWith("_joint_dist") or tableName.endsWith("_ipf")):
                if not query1.exec_("""drop table %s""" %(tableName)):
                    raise FileError, query1.lastError().text()


    def checkIfRelationsDefined(self, vardict, override=False):
        if len (vardict.keys()) > 0 or override:
            controlVariables = ['%s' %i for i in vardict.keys()]
            controlVariables.sort()
            #controlDimensions = numpy.asarray([len(vardict[QString(i)].keys()) for i in controlVariables])
            controlDimensions = numpy.asarray([len(vardict[i].keys()) for i in controlVariables])

            #print controlVariables, controlDimensions

            return controlVariables, controlDimensions
        else:
            QMessageBox.warning(self, "Corresponding Sample Categories with Marginal Variables", """Control variables, and variable correspondence not defined appropriately. """
                                """Choose variables/ define relations and then run the synthesizer.""", QMessageBox.Ok)

    def reject(self):
        self.projectDBC.dbc.close()
        QDialog.reject(self)

class SetCorrTabWidget(QTabWidget):
    def __init__(self, project, parent=None):
        super(SetCorrTabWidget, self).__init__(parent)
        self.project = project

        layout = QVBoxLayout()


        tablesProject = self.tables()

        self.housingTab = TabWidgetItems(self.project, 'Household', 'hhld_marginals', 'hhld_sample')


        self.addTab(self.housingTab, 'Household Variables')

        self.personAnalyzed = self.isPersonAnalyzed()
        if self.personAnalyzed:
            self.personTab = TabWidgetItems(self.project, 'Person', 'person_marginals', 'person_sample')
            self.addTab(self.personTab, 'Person Variables')

        self.gqAnalyzed = self.isGqAnalyzed()
        if self.gqAnalyzed:
            self.gqTab = TabWidgetItems(self.project, 'Groupquarter', 'gq_marginals', 'gq_sample')
            self.addTab(self.gqTab, 'Groupquarters Variables')

        self.setLayout(layout)



    def isPersonAnalyzed(self):
        if self.project.controlUserProv.userProv == True and self.project.controlUserProv.personLocation == "":
            return False
        else:
            return True



    def isGqAnalyzed(self):
        if self.project.sampleUserProv.userProv == False and self.project.controlUserProv.userProv == False:
            return True

        if self.project.sampleUserProv.userProv == True and self.project.sampleUserProv.gqLocation <> "":
            return True

        if self.project.controlUserProv.userProv == True and self.project.controlUserProv.gqLocation <> "":
            return True

        return False



    def tables(self):
        projectDBC = createDBC(self.project.db, self.project.name)
        projectDBC.dbc.open()

        tables = []
        query = QSqlQuery(projectDBC.dbc)
        if not query.exec_("""show tables"""):
            raise FileError, query.lastError().text()

        while query.next():
            tables.append('%s' %query.value(0).toString())

        projectDBC.dbc.close()
        return tables


class TabWidgetItems(QWidget):
    def __init__(self, project, controlType, controlTable, sampleTable, parent=None):
        super(TabWidgetItems, self).__init__(parent)

        self.project = project

        self.selVariables = defaultdict(dict)

        self.controlType = controlType

        self.controlTable = controlTable
        self.sampleTable = sampleTable

        self.sampleVarsDict = {}

        self.selVarCatStrings = {}
        self.relationStrings = {}

        sampleTableLabel = QLabel("Sample Table")
        sampleVarLabel = QLabel("Sample Variable")
        selSampleVarLabel = QLabel("Selected Variable")
        selSampleVarCatLabel = QLabel("Selected Variable Categories")
        self.sampleTableComboBox = QComboBox()
        self.sampleTableComboBox.setEnabled(False)

        self.sampleVarListWidget = ListWidget()
        self.selSampleVarListWidget = ListWidget()
        self.selSampleVarCatListWidget = ListWidget()
        self.selSampleVar = QPushButton("Select>>")
        self.selSampleVar.setEnabled(False)
        self.deselSampleVar = QPushButton("<<Deselect")
        self.deselSampleVar.setEnabled(False)


        vLayout4 = QVBoxLayout()
        vLayout4.addItem(QSpacerItem(10,50))
        vLayout4.addWidget(self.selSampleVar)
        vLayout4.addWidget(self.deselSampleVar)
        vLayout4.addItem(QSpacerItem(10,50))



        vLayout5 = QVBoxLayout()
        vLayout5.addWidget(sampleVarLabel)
        vLayout5.addWidget(self.sampleVarListWidget)


        vLayout6 = QVBoxLayout()
        vLayout6.addWidget(selSampleVarLabel)
        vLayout6.addWidget(self.selSampleVarListWidget)

        vLayout7 = QVBoxLayout()
        vLayout7.addWidget(selSampleVarCatLabel)
        vLayout7.addWidget(self.selSampleVarCatListWidget)


        hLayout2 = QHBoxLayout()
        hLayout2.addLayout(vLayout5)
        hLayout2.addLayout(vLayout4)
        hLayout2.addLayout(vLayout6)
        hLayout2.addLayout(vLayout7)

        vLayout2 = QVBoxLayout()
        vLayout2.addWidget(sampleTableLabel)
        vLayout2.addWidget(self.sampleTableComboBox)
        #vLayout2.addWidget(sampleVarLabel)
        vLayout2.addLayout(hLayout2)

        controlTableLabel = QLabel("Marginal Table")
        controlVarLabel = QLabel("Marginal Variables")
        self.controlTableComboBox = QComboBox()
        self.controlTableComboBox.setEnabled(False)
        self.controlVarListWidget = ListWidget()

        vLayout3 = QVBoxLayout()
        vLayout3.addWidget(controlTableLabel)
        vLayout3.addWidget(self.controlTableComboBox)
        vLayout3.addWidget(controlVarLabel)
        vLayout3.addWidget(self.controlVarListWidget)


        hLayout1 = QHBoxLayout()
        hLayout1.addLayout(vLayout2)
        hLayout1.addLayout(vLayout3)

        relationLabel = QLabel("Correspondence between the Sample Variable Categories and the Marginal Variables")
        self.relationsListWidget = ListWidget()
        self.addRelation = QPushButton("Add Correspondence")
        self.deleteRelation = QPushButton("Delete Correspondence")
        self.deleteRelation.setEnabled(False)

        vLayout3 = QVBoxLayout()
        vLayout3.addWidget(self.addRelation)
        vLayout3.addWidget(self.deleteRelation)
        vLayout3.addItem(QSpacerItem(10,100))


        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(self.relationsListWidget)
        hLayout2.addLayout(vLayout3)


        layout = QVBoxLayout()


        if controlType == 'Household':
            modifyMargsGrpBox = QGroupBox("Do you wish to modify the household size marginal distribution?")
            self.modifyMargsYes = QRadioButton("Yes")
            self.modifyMargsNo = QRadioButton("No")
            self.modifyMargsNo.setChecked(True)
            
            self.hhldsizeVarNameLabel = QLabel("Select the household size variable name")
            self.hhldsizeVarNameComboBox = QComboBox()
            self.hhldsizeVarNameComboBox.setMaximumSize(250,20)
            self.hhldsizeVarNameComboBox.setEnabled(False)
            self.hhldsizeVarNameLabel.setEnabled(False)

            self.hhldsizeAverageLabel = QLabel("Enter the average value for the last household size category")
            self.hhldsizeAverageLineEdit = QLineEdit()
            self.hhldsizeAverageLineEdit.setMaximumSize(250, 20)
            self.hhldsizeAverageLabel.setEnabled(False)
            self.hhldsizeAverageLineEdit.setEnabled(False)

            self.persRefVarNameLabel = QLabel("Select the person variable to obtain the person total")
            self.persRefVarNameComboBox = QComboBox()
            self.persRefVarNameComboBox.setMaximumSize(250, 20)
            self.persRefVarNameComboBox.setEnabled(False)
            self.persRefVarNameLabel.setEnabled(False)

            hLayout11 = QHBoxLayout()
            hLayout11.addWidget(self.modifyMargsYes)
            hLayout11.addWidget(self.modifyMargsNo)

            vLayout13 = QVBoxLayout()
            vLayout13.addWidget(self.hhldsizeVarNameLabel)
            vLayout13.addWidget(self.hhldsizeVarNameComboBox)


            vLayout12 = QVBoxLayout()
            vLayout12.addWidget(self.hhldsizeAverageLabel)
            vLayout12.addWidget(self.hhldsizeAverageLineEdit)

            vLayout14 = QVBoxLayout()
            vLayout14.addWidget(self.persRefVarNameLabel)
            vLayout14.addWidget(self.persRefVarNameComboBox)


            hLayout12 = QHBoxLayout()
            hLayout12.addLayout(vLayout13)
            #hLayout12.addItem(QSpacerItem(150,10))
            hLayout12.addLayout(vLayout12)
            hLayout12.addLayout(vLayout14)

            vLayout11 = QVBoxLayout()
            vLayout11.addLayout(hLayout11)
            vLayout11.addLayout(hLayout12)


            
            modifyMargsGrpBox.setLayout(vLayout11)

            layout.addWidget(modifyMargsGrpBox)
            
            self.connect(self.modifyMargsYes, SIGNAL("clicked()"), self.modifyMargsYesAction)
            self.connect(self.modifyMargsNo, SIGNAL("clicked()"), self.modifyMargsNoAction)


        layout.addLayout(hLayout1)
        layout.addWidget(relationLabel)
        layout.addLayout(hLayout2)


        self.setLayout(layout)

        self.connect(self.addRelation, SIGNAL("clicked()"), self.addRelationAction)
        self.connect(self.relationsListWidget, SIGNAL("itemSelectionChanged()"), self.deleteRelationAction)
        self.connect(self.sampleVarListWidget, SIGNAL("itemSelectionChanged()"), self.enableSelButton)
        self.connect(self.selSampleVarListWidget, SIGNAL("itemSelectionChanged()"), self.enableDeselButton)
        self.connect(self, SIGNAL("addSampleVar(QListWidgetItem *)"), self.addSampleVarCats)
        self.connect(self, SIGNAL("removeSampleVar(QListWidgetItem *)"), self.removeSampleVarCats)
        self.connect(self.selSampleVar, SIGNAL("clicked()"), self.moveSelVars)
        self.connect(self.deselSampleVar, SIGNAL("clicked()"), self.moveDeselVars)
        self.connect(self.deleteRelation, SIGNAL("clicked()"), self.deleteRelationNow)
        self.connect(self.sampleTableComboBox, SIGNAL("highlighted(int)"), self.populateSampleVariables)
        self.connect(self.controlTableComboBox, SIGNAL("highlighted(int)"), self.populateControlVariables)

        self.populate()


    def modifyMargsYesAction(self):
        self.hhldsizeVarNameComboBox.setEnabled(True)
        self.persRefVarNameComboBox.setEnabled(True)        
        self.hhldsizeVarNameLabel.setEnabled(True)
        self.persRefVarNameLabel.setEnabled(True)
        self.hhldsizeAverageLabel.setEnabled(True)
        self.hhldsizeAverageLineEdit.setEnabled(True)

    def modifyMargsNoAction(self):
        self.hhldsizeVarNameComboBox.setEnabled(False)
        self.persRefVarNameComboBox.setEnabled(False)
        self.hhldsizeVarNameLabel.setEnabled(False)
        self.persRefVarNameLabel.setEnabled(False)
        self.hhldsizeAverageLabel.setEnabled(False)
        self.hhldsizeAverageLineEdit.setEnabled(False)


    def check(self):
        if self.controlType == 'Household':
            if self.modifyMargsYes.isChecked():
                if not self.checkHhldSizeSelected():
                    return False
                else:
                    pass
                    #print 'Household size selected and correspondences checked'

                
                    
            if self.modifyMargsYes.isChecked():
                if not self.checkHhldSize():
                    return False
                else:
                    pass
                    #print 'checking last household size category value'

                
                    
        

        check = self.checkSelectedVariables() and self.checkNumRelationsDefined()

        return check

    def checkHhldSize(self):
        value = self.hhldsizeAverageLineEdit.text()
        if len(value) > 0:
            for i in value:
                if not re.match("[0-9.]", i):
                    self.promptHhldSizeError()
                    return False
            return True
        else:
            self.promptHhldSizeError()
            return False
            
    def promptHhldSizeError(self):
        QMessageBox.warning(self, "Corresponding Sample Categories with Marginal Variables",
                            """Please enter a valid number for the last household size category.""",
                            QMessageBox.Ok)              
        self.hhldsizeAverageLineEdit.setFocus()
        self.hhldsizeAverageLineEdit.selectAll()

            
        

    def checkHhldSizeSelected(self):
        row = self.selSampleVarListWidget.rowOf(self.hhldsizeVarNameComboBox.currentText())

        if row < 0:
            QMessageBox.warning(self, "Corresponding Sample Categories with Marginal Variables",
                                """Household size variable selected but variable correspondences """
                                """are missing.""",
                                QMessageBox.Ok)              

            return False
        else:
            return True


    def checkSelectedVariables(self):
        if (not self.project.selVariableDicts.persControl) and self.controlType == 'Person':
            return True
        if not (self.selSampleVarListWidget.count() > 0):
            QMessageBox.warning(self, "Corresponding Sample Categories with Marginal Variables",
                                """No variable was selected for %s control."""
                                """ Select variables and define relations to continue.""" %self.controlType,
                                QMessageBox.Ok)
            return False
        else:
            return True


    def checkNumRelationsDefined(self):
        if self.relationsListWidget.count() <> self.selSampleVarCatListWidget.count():
            QMessageBox.warning(self, "Corresponding Sample Categories with Marginal Variables",
                                """Insufficient correspondence defined for the selected <b>%s</b> control variable(s).""" %self.controlType,
                                QMessageBox.Ok)
            return False
        else:
            return True


    def populateSampleVariables(self, index):
        self.sampleSelTable = self.sampleTableComboBox.itemText(index)
        self.sampleVars = self.variablesInTable(self.sampleSelTable)
        self.sampleVarListWidget.clear()
        self.selSampleVarListWidget.clear()
        self.selSampleVarCatListWidget.clear()

        self.sampleVars = self.removeVariables(self.sampleVars)

        if self.controlType == 'Household':
            self.hhldsizeVarNameComboBox.addItems(self.sampleVars)
            personSampleVars = self.variablesInTable('person_sample')
            personSampleVars = self.removeVariables(personSampleVars)
            self.persRefVarNameComboBox.addItems(personSampleVars)

        self.sampleVarListWidget.addItems(self.sampleVars)

    def removeVariables(self, variables):
        vars = ['state', 'pumano', 'hhid', 'serialno', 'pnum', 'hhlduniqueid', 'gquniqueid', 'personuniqueid']

        for i in vars:
            try:
                variables.remove(i)
            except:
                pass     
        return variables

    def populateControlVariables(self, index):
        self.controlSelTable = self.controlTableComboBox.itemText(index)
        self.controlVars = self.variablesInTable(self.controlSelTable)
        self.controlVarListWidget.clear()
        self.controlVarListWidget.addItems(self.controlVars)


    def variablesInTable(self, tablename):
        projectDBC = createDBC(self.project.db, self.project.name)
        projectDBC.dbc.open()

        variables = []
        query = QSqlQuery(projectDBC.dbc)
        if not query.exec_("""desc %s""" %tablename):
            raise FileError, query.lastError().text()

        FIELD = 0

        while query.next():
            field = query.value(FIELD).toString()
            variables.append('%s' %field)

        projectDBC.dbc.close()
        return variables

    def enableSelButton(self):
        if len(self.sampleVarListWidget.selectedItems())>0:
            self.selSampleVar.setEnabled(True)
        else:
            self.selSampleVar.setEnabled(False)

    def enableDeselButton(self):
        if len(self.selSampleVarListWidget.selectedItems())>0:
            self.deselSampleVar.setEnabled(True)
        else:
            self.deselSampleVar.setEnabled(False)


    def moveSelVars(self):
        item = self.sampleVarListWidget.currentItem()
        self.sampleVarListWidget.remove()
        self.selSampleVarListWidget.addItem(item)
        self.emit(SIGNAL("addSampleVar(QListWidgetItem *)"), item)

    def moveDeselVars(self):
        item = self.selSampleVarListWidget.currentItem()
        self.selSampleVarListWidget.remove()
        self.sampleVarListWidget.addItem(item)
        self.emit(SIGNAL("removeSampleVar(QListWidgetItem *)"), item)


    def addSampleVarCats(self, item):
        varName = item.text()

        self.categories(varName)
        varCats = self.sampleVarsDict['%s' %varName]

        string = self.varCatStrings(varName, varCats)

        for i in string:
            self.selVarCatStrings[i] = '%s' %varName

        self.selSampleVarCatListWidget.addItems(string)



    def categories(self, varname):
        projectDBC = createDBC(self.project.db, self.project.name)
        projectDBC.dbc.open()

        cats = []
        query = QSqlQuery(projectDBC.dbc)
        if not query.exec_("""select %s from %s group by %s""" %(varname, self.sampleSelTable, varname)):
            raise FileError, query.lastError().text()

        CATEGORY = 0

        while query.next():
            cat = unicode(query.value(CATEGORY).toString())

            cats.append(cat)
        self.sampleVarsDict['%s' %varname] = cats
        projectDBC.dbc.close()

    def varCatStrings(self, varName, varCats):
        string = []
        for i in varCats:
            string.append("%s, Category %s" %(varName, i))

        return string



    def removeSampleVarCats(self, item):
        varName = '%s' %item.text()

        for i in self.selVarCatStrings.keys():
            if self.selVarCatStrings[i] == varName:
                row = self.selSampleVarCatListWidget.rowOf(i)
                self.selSampleVarCatListWidget.takeItem(row)

        for i in self.relationStrings.keys():
            if self.relationStrings[i] == varName:
                row = self.relationsListWidget.rowOf(i)
                self.relationsListWidget.takeItem(row)
        try:
            self.selVariables.pop(varName)
        except Exception, e:
            #print e
            pass

    def addRelationAction(self):
        try:
            sampleVarCat = '%s' %self.selSampleVarCatListWidget.currentItem().text()
            controlVar = '%s' %self.controlVarListWidget.currentItem().text()
            varName = self.selVarCatStrings[sampleVarCat]

            try:
                controlVar = self.selVariables[varName][sampleVarCat]
                relation = '%s -  %s' %(sampleVarCat, controlVar)
                raise Exception, "The relation already exists"
            #print relation
            except Exception, e:
                #print '%s:%s' %(Exception, e)
                self.selVariables[varName][sampleVarCat] = controlVar
                relation = '%s -  %s' %(sampleVarCat, controlVar)
                self.relationStrings[relation] = varName

            row = self.relationsListWidget.rowOf(relation)
            itemAt = self.relationsListWidget.item(row)

            if row >= 0:
                QMessageBox.warning(self, "Corresponding Sample Categories with Marginal Variables", """If you wish to change the control variable """
                                    """corresponding to a category of the control variable, delete the existing correspondence """
                                    """and define again.""", QMessageBox.Ok)
                self.relationsListWidget.setCurrentItem(itemAt)
            else:
                self.relationsListWidget.addItem(relation)

        except Exception, e:
            QMessageBox.warning(self, "Corresponding Sample Categories with Marginal Variables", """Select a variable category """
                                """and a variable name to add a relation.""", QMessageBox.Ok)




    def deleteRelationAction(self):
        if len(self.relationsListWidget.selectedItems()) >0:
            self.deleteRelation.setEnabled(True)

    def deleteRelationNow(self):
        self.parseRelation(self.relationsListWidget.currentItem())
        self.relationsListWidget.remove()
        #print self.selVariables



    def parseRelation(self, item):
        relation = '%s' %item.text()
        for i in self.selVariables.keys():
            for j in self.selVariables[i].keys():
                matchRelation = '%s -  %s' %(j, self.selVariables[i][j])
                if matchRelation == relation:
                    self.selVariables[i].pop(j)

    def populate(self):
        self.sampleTableComboBox.addItem(self.sampleTable)
        self.controlTableComboBox.addItem(self.controlTable)
        self.sampleTableComboBox.emit(SIGNAL("highlighted(int)"), 0)
        self.controlTableComboBox.emit(SIGNAL("highlighted(int)"), 0)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = 1
    form = SetCorrDialog(a)
    #form = TabWidget(a)
    form.show()
    app.exec_()
