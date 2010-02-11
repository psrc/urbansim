# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import shutil, urllib, os

from database.createDBConnection import createDBC
from summary_page import SummaryPage
from data_menu.data_process_status import DataDialog
from data_menu.display_data import DisplayTable
from data_menu.sf_data import AutoImportSF2000Data
from file_menu.open_project import SaveFile
from misc.widgets import RecodeDialog, VariableSelectionDialog, CreateVariable, NameDialog, DeleteRows

from misc.errors import *

from default_census_cat_transforms import *

class QTreeWidgetCMenu(QTreeWidget):
    def __init__(self, project=None, parent = None):
        super(QTreeWidgetCMenu, self).__init__(parent)
        self.setMinimumSize(350, 400)
        self.setColumnCount(2)
        self.setHeaderLabels(["Name", "Value"])
        self.setColumnWidth(0, 150)
        self.setItemsExpandable(True)
        self.setEnabled(False)
        self.project = project
        self.tables = []


    def contextMenuEvent(self, event):
        menu = QMenu()
        importDataAction = menu.addAction("&Import Data")
        editProjectAction = menu.addAction("&Edit Project")

        menuTableEdit = QMenu()
        displayTableAction = menuTableEdit.addAction("Display")
        menuTableEdit.addSeparator()
        createVarAction = menuTableEdit.addAction("Create New Variable")
        recodeCatsAction = menuTableEdit.addAction("Recode Categories")
        deleteColAction = menuTableEdit.addAction("Delete Column(s)")
        deleteRowsAction = menuTableEdit.addAction("Delete Record(s)")
        dropAction = menuTableEdit.addAction("Delete Table")
        copyAction = menuTableEdit.addAction("Copy Table")
        renameAction = menuTableEdit.addAction("Rename Table")
        menuTableEdit.addSeparator()
        exportActionCSV = menuTableEdit.addAction("Export Table (CSV format)")
        exportActionTab = menuTableEdit.addAction("Export Table (Tab-delimited format)")
        menuTableEdit.addSeparator()
        defaultTransforAction = menuTableEdit.addAction("Default Transformation")

        self.connect(importDataAction, SIGNAL("triggered()"), self.importData)
        self.connect(editProjectAction, SIGNAL("triggered()"), self.editProject)
        self.connect(displayTableAction, SIGNAL("triggered()"), self.displayTable)
        self.connect(recodeCatsAction, SIGNAL("triggered()"), self.modifyCategories)
        self.connect(createVarAction, SIGNAL("triggered()"), self.createVariable)
        self.connect(deleteColAction, SIGNAL("triggered()"), self.deleteColumns)
        self.connect(deleteRowsAction, SIGNAL("triggered()"), self.deleteRows)
        self.connect(copyAction, SIGNAL("triggered()"), self.copyTable)
        self.connect(renameAction, SIGNAL("triggered()"), self.renameTable)
        self.connect(dropAction, SIGNAL("triggered()"), self.dropTable)

        self.connect(exportActionCSV, SIGNAL("triggered()"), self.exportTableCSV)
        self.connect(exportActionTab, SIGNAL("triggered()"), self.exportTableTab)
        self.connect(defaultTransforAction, SIGNAL("triggered()"), self.defaultTransformations)


        if self.item.parent() is None:
            menu.exec_(event.globalPos())
        else:
            if self.item.parent().text(0) == 'Project Tables' or self.item.parent().text(0) == 'Scenario Tables':
                menuTableEdit.exec_(event.globalPos())


    def exportTableCSV(self):
        tablename = self.item.text(0)
        fileDlg = SaveFile(self.project, "csv", tablename, self.item.parent().text(0))

    def exportTableTab(self):
        tablename = self.item.text(0)
        fileDlg = SaveFile(self.project, "dat", tablename, self.item.parent().text(0))


    def deleteRows(self):
        tablename = self.item.text(0)

        parentText = self.item.parent().text(0)
        if parentText == 'Project Tables':
            database = self.project.name
        elif parentText == 'Scenario Tables':
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)            
            
        self.populateVariableDictionary(tablename)

        projectDBC = createDBC(self.project.db, database)
        projectDBC.dbc.open()

        deleteRows = DeleteRows(self.project, parentText, tablename, self.variableTypeDictionary, "Delete Records", "modifydata")
        if deleteRows.exec_():
            projectDBC.dbc.open()
            reply = QMessageBox.question(self, "Delete Records", "Would you like to continue?",
                                         QMessageBox.Yes| QMessageBox.Cancel)
            if reply == QMessageBox.Yes:

                query = QSqlQuery(projectDBC.dbc)
                whereExpression = deleteRows.whereEdit.toPlainText()
                #print whereExpression, 'is the text'
                if not whereExpression == "":

                    if not query.exec_("""delete from %s where %s""" %(tablename, whereExpression)):
                        raise FileError, query.lastError().text()
                else:
                    QMessageBox.warning(self, "Delete Records", """No filter expression selected, 0 records deleted.""",
                                        QMessageBox.Ok)

        projectDBC.dbc.close()


    def copyTable(self):
        tablename = self.item.text(0)

        parent = self.item.parent().text(0)
        if parent == 'Project Tables':
            database = self.project.name
        elif parent == 'Scenario Tables':
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)            

        copyNameDialog = NameDialog("Copy Table - %s" %tablename)
        if copyNameDialog.exec_():
            newTablename = copyNameDialog.nameLineEdit.text()
            projectDBC = createDBC(self.project.db, database)
            projectDBC.dbc.open()

            query = QSqlQuery(projectDBC.dbc)
            if not query.exec_("""create table %s select * from %s""" %(newTablename, tablename)):
                raise FileError, query.lastError().text()
            self.populate()
            projectDBC.dbc.close()

    def renameTable(self):
        tablename = self.item.text(0)
        parent = self.item.parent().text(0)
        if parent == 'Project Tables':
            database = self.project.name
        elif parent == 'Scenario Tables':
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)            

        renameNameDialog = NameDialog("Rename Table - %s" %tablename)
        if renameNameDialog.exec_():
            newTablename = renameNameDialog.nameLineEdit.text()

            projectDBC = createDBC(self.project.db, database)
            projectDBC.dbc.open()

            query = QSqlQuery(projectDBC.dbc)
            if not query.exec_("""alter table %s rename to %s""" %(tablename, newTablename)):
                raise FileError, query.lastError().text()
            self.populate()
            projectDBC.dbc.close()

    def dropTable(self):
        tablename = self.item.text(0)

        parent = self.item.parent().text(0)
        if parent == 'Project Tables':
            database = self.project.name
        elif parent == 'Scenario Tables':
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)            

        reply = QMessageBox.question(self, "Delete Table - %s" %tablename, "Do you wish to continue?",
                                     QMessageBox.Yes| QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            projectDBC = createDBC(self.project.db, database)

            projectDBC.dbc.open()

            query = QSqlQuery(projectDBC.dbc)
            if not query.exec_("""drop table %s""" %tablename):
                raise FileError, query.lastError().text()
            self.populate()
            projectDBC.dbc.close()


    def click(self, item, column):
        self.item = item

    def createVariable(self):
        parent = self.item.parent().text(0)
        if parent == 'Project Tables':
            database = self.project.name
        elif parent == 'Scenario Tables':
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)            

        projectDBC = createDBC(self.project.db, database)
        projectDBC.dbc.open()

        tablename = self.item.text(0)
        self.populateVariableDictionary(tablename)

        create = CreateVariable(self.project, database, tablename, self.variableTypeDictionary, "Create New Variable", "modifydata")
        if create.exec_():
            projectDBC.dbc.open()
            newVarName = create.newVarNameEdit.text()
            numericExpression = create.formulaEdit.toPlainText()
            whereExpression = create.whereEdit.toPlainText()
            if len(whereExpression)<1:
                whereExpression = '1'
            if len(numericExpression) <1:
                QMessageBox.warning(self, "Data", QString("""Invalid numeric expression, enter again"""))
            else:
                query = QSqlQuery(projectDBC.dbc)
                if not query.exec_("""alter table %s add column %s text""" %(tablename, newVarName)):
                    print ("""alter table %s add column %s text""" %(tablename, newVarName))
                    raise FileError, query.lastError().text()
                if not query.exec_("""update %s set %s = %s where %s""" %(tablename, newVarName,
                                                                          numericExpression, whereExpression)):
                    raise FileError, query.lastError().text()

        projectDBC.dbc.close()



    def displayTable(self):
        tablename = self.item.text(0)

        disp = DisplayTable(self.project, "%s" %tablename, self.item.parent().text(0))
        disp.exec_()

    def modifyCategories(self):
        parentText = self.item.parent().text(0)
        """
        if parentText == 'Project Tables':
            database = self.project.name
        elif parentText == 'Scenario Tables':
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)            
        projectDBC = createDBC(self.project.db, database)

        projectDBC.dbc.open()
        """
        tablename = self.item.text(0)
        modify = RecodeDialog(self.project, parentText, tablename, title = "Recode Categories - %s" %tablename, icon = "modifydata")
        modify.exec_()

        #projectDBC.dbc.close()


    def deleteColumns(self):
        parent = self.item.parent().text(0)

        if parent == 'Project Tables':
            database = self.project.name
        elif parent == 'Scenario Tables':
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)            

        projectDBC = createDBC(self.project.db, database)

        tablename = self.item.text(0)
        self.populateVariableDictionary(tablename)
        projectDBC.dbc.open()
        query = QSqlQuery(projectDBC.dbc)

        title = "Delete Dialog - %s" %tablename
        deleteVariablesdia = VariableSelectionDialog(self.variableTypeDictionary, title = title, icon = "modifydata",
                                                     warning = "Note: Select variables to delete.")

        if deleteVariablesdia.exec_():
            deleteVariablesSelected = deleteVariablesdia.selectedVariableListWidget.variables

            for i in deleteVariablesSelected:
                if not query.exec_("""alter table %s drop %s""" %(tablename, i)):
                    raise FileError, query.lastError().text()

        projectDBC.dbc.close()


    def defaultTransformations(self):
        projectDBC = createDBC(self.project.db, self.project.name)
        projectDBC.dbc.open()

        query = QSqlQuery(projectDBC.dbc)

        tablename = self.item.text(0)

        checkPUMSTableTransforms = False
        checkSFTableTransforms = False

        if not self.project.sampleUserProv.userProv:
            if tablename == 'housing_pums':
                if self.project.sampleUserProv.defSource == 'Census 2000':
                    queries = DEFAULT_HOUSING_PUMS2000_QUERIES
                    checkPUMSTableTransforms = True
                else:
                    queries = DEFAULT_HOUSING_PUMSACS_QUERIES
                    checkPUMSTableTransforms = True

            if tablename == 'person_pums':
                if self.project.sampleUserProv.defSource == 'Census 2000':
                    queries = DEFAULT_PERSON_PUMS2000_QUERIES
                    checkPUMSTableTransforms = True
                else:
                    queries = DEFAULT_PERSON_PUMSACS_QUERIES
                    checkPUMSTableTransforms = True

            if checkPUMSTableTransforms:
                for i in queries:
                    #print "Executing Query: %s" %i
                    if not query.exec_("""%s""" %i):
                        if not query.lastError().number() == 1051:
                            print "FileError: %s" %query.lastError().text()


        if not self.project.controlUserProv.userProv:
            if tablename[:13] == 'mastersftable':
                checkSFTableTransforms = True

            if checkSFTableTransforms:
                if self.project.controlUserProv.defSource == 'Census 2000':
                    queries = DEFAULT_SF2000_QUERIES
                else:
                    queries = DEFAULT_SFACS_QUERIES

                for i in queries:
                    #print "Executing Query: %s" %i
                    if not query.exec_(i %tablename):
                        print "FileError: %s" %query.lastError().text()

        if not (checkPUMSTableTransforms or checkSFTableTransforms):
            QMessageBox.warning(self, "Default Transformations", 
                                """No default transformations are defined for the table""",
                                QMessageBox.Ok)
            #print "FileError: The file does not have default transformations"

        projectDBC.dbc.close()
        self.populate()


    def populateVariableDictionary(self, tablename):
        parent = self.item.parent().text(0)

        if parent == 'Project Tables':
            database = self.project.name
        elif parent == 'Scenario Tables':
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)            


        projectDBC = createDBC(self.project.db, database)
        projectDBC.dbc.open()

        self.variableTypeDictionary = {}
        query = QSqlQuery(projectDBC.dbc)
        query.exec_("""desc %s""" %tablename)

        FIELD, TYPE, NULL, KEY, DEFAULT, EXTRA = range(6)

        while query.next():
            field = query.value(FIELD).toString()
            type = query.value(TYPE).toString()
            null = query.value(NULL).toString()
            key = query.value(KEY).toString()
            default = query.value(DEFAULT).toString()
            extra = query.value(EXTRA).toString()

            self.variableTypeDictionary['%s' %field] = type
        projectDBC.dbc.close()

    def editProject(self):

        editWidget = QWizard()
        editWidget.setWindowTitle("Edit Project")
        editWidget.setWindowIcon(QIcon("./images/editproject.png"))
        editWidget.setWizardStyle(QWizard.ClassicStyle)
        editWidget.setOption(QWizard.NoBackButtonOnStartPage)

        self.page = SummaryPage()
        self.page.setTitle("Summary")
        self.page.projectLocationDummy = True
        self.page.projectDatabaseDummy = True
        self.page.fillPage(self.project)
        self.page.enableEditableWidgets()
        editWidget.addPage(self.page)


        if editWidget.exec_():
            check1 = (self.page.projectDescLineEdit.text() == self.project.description)
            check2 = (self.page.projectResolutionComboBox.currentText() == self.project.resolution)

            #print check1, check2, 'checkkkkkkkkksssssssssssssssssss'

            if check1 and check2:
                pass
            else:
                #print 'Poject properties altered'
                self.page.updateProject()
                self.project = self.page.project
                self.project.save()
                self.populate()

            if not check2 and not self.project.controlUserProv.userProv:

                #print 'Project resolution changed'
                autoImportSFDataInstance = AutoImportSF2000Data(self.project)
                autoImportSFDataInstance.createMasterSubSFTable()
                autoImportSFDataInstance.projectDBC.dbc.close()
                tablename = 'mastersftable%s' %(self.page.projectResolutionComboBox.currentText())
                self.project.save()
                self.populate()




    def importData(self):
        #QMessageBox.information(None, "Check", "Import Data", QMessageBox.Ok)
        dataprocesscheck = DataDialog(self.project)
        dataprocesscheck.exec_()
        self.populate()


    def populate(self):
        self.setEnabled(True)
        self.clear()

        projectAncestor = QTreeWidgetItem(self, [QString("Project: " + self.project.name)])
        informationParent = QTreeWidgetItem(projectAncestor, [QString("Information")])

        dummy = ""
        if self.project.region is not None:
            for i in self.project.region.keys():
                dummy = dummy + i + ", "+ self.project.region[i]+ "; "


        resolutionText = self.project.resolution

        if resolutionText == "Tract":
            resolution = 'Census Tract'
        elif resolutionText == "Blockgroup":
            resolution = 'Census Blockgroup'
        elif resolutionText == 'TAZ':
            resolution = 'Traffic Analysis Zone (TAZ)'
        else:
            resolution = 'County'



        informationItems = {"Location":self.project.location,
                            "Description":self.project.description,
                            "Region":dummy,
                            "Resolution":resolution}
        for i,j in informationItems.items():
            child = QTreeWidgetItem(informationParent, [i, QString(j)])

        geocorrParent = QTreeWidgetItem(projectAncestor, [QString("Geographic Correspondence")])
        geocorrUserProvText = self.userProvText(self.project.geocorrUserProv.userProv)
        geocorrItems = {"User Provided":geocorrUserProvText,
                        "Location":self.project.geocorrUserProv.location}

        for i,j in geocorrItems.items():
            child = QTreeWidgetItem(geocorrParent, [i, QString("%s"%j)])

        sampleParent = QTreeWidgetItem(projectAncestor, [QString("Sample")])
        sampleUserProvText = self.userProvText(self.project.sampleUserProv.userProv, 
                                               self.project.sampleUserProv.defSource)
        sampleItems = {"User Provided":sampleUserProvText,
                       "Household Data Location": self.project.sampleUserProv.hhLocation,
                       "GQ Data Location": self.project.sampleUserProv.gqLocation,
                       "Person Data Location": self.project.sampleUserProv.personLocation}

        for i,j in sampleItems.items():
            child = QTreeWidgetItem(sampleParent, [i, QString("%s"%j)])

        controlParent = QTreeWidgetItem(projectAncestor, [QString("Control")])
        controlUserProvText = self.userProvText(self.project.controlUserProv.userProv,
                                                self.project.controlUserProv.defSource)
        controlItems = {"User Provided":controlUserProvText,
                       "Household Data Location": self.project.controlUserProv.hhLocation,
                       "GQ Data Location": self.project.controlUserProv.gqLocation,
                       "Person Data Location": self.project.controlUserProv.personLocation}

        for i,j in controlItems.items():
            child = QTreeWidgetItem(controlParent, [i, QString("%s"%j)])

        dbParent = QTreeWidgetItem(projectAncestor, [QString("Database")])
        dbItems = {"Hostname":self.project.db.hostname,
                   "Username":self.project.db.username}
        #"Password":self.project.db.password}

        for i,j in dbItems.items():
            child = QTreeWidgetItem(dbParent, [QString(i), QString(j)])


        projectTableParent = QTreeWidgetItem(projectAncestor, [QString("Project Tables")])
        scenarioTableParent = QTreeWidgetItem(projectAncestor, [QString("Scenario Tables")])

        self.tableChildren(projectTableParent, 0)
        self.tableChildren(scenarioTableParent, 1)

        self.expandItem(projectAncestor)
        self.expandSort(informationParent, 0)
        self.expandSort(geocorrParent, 0)
        self.expandSort(sampleParent, 0)
        self.expandSort(controlParent, 0)
        self.expandSort(dbParent, 0)
        self.expandSort(projectTableParent, 0)
        self.expandSort(scenarioTableParent, 0)


    def userProvText(self, text, source='default'):
        if text:
            return "Yes"
        else:
            return "No, %s data will be used" %source



    def tableChildren(self, parent, scenario=0):

        if scenario > 0:
            databaseName = self.project.name + 'scenario' + str(self.project.scenario)
        else:
            databaseName = self.project.name

        projectDBC = createDBC(self.project.db, databaseName)

        projectDBC.dbc.open()

        self.query = QSqlQuery(projectDBC.dbc)

        if not self.query.exec_("""show tables"""):
            raise FileError, self.query.lastError().text()

        tableItems = []

        while self.query.next():
            tableItems.append(self.query.value(0).toString())

        projectDBC.dbc.close()

        tableItems.sort()

        for i in tableItems:
            child = QTreeWidgetItem(parent, [QString(i)])

    def expandSort(self, item, index):
        self.expandItem(item)
        item.sortChildren(index, Qt.AscendingOrder)


