# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from qgis.gui import *
import sys, os, re, shutil
import countydata, newproject
from database.createDBConnection import createDBC


class QWizardValidatePage(QWizardPage):
    def __init__(self, projectLocationDummy=False, projectDatabaseDummy=False, parent=None):
        super(QWizardValidatePage, self).__init__(parent)
        self.projectLocationDummy = projectLocationDummy
        self.projectDatabaseDummy = projectDatabaseDummy

    def isComplete(self):
        if self.isFinalPage():
            if self.projectLocationDummy and self.projectDatabaseDummy:
                return True
            else:
                return False
        else:
            return True

class ComboBoxFolder(QComboBox):
    def __init__(self, parent=None):
        super(ComboBoxFolder, self).__init__(parent)

    def browseFolder(self, index):
        if index  == self.count()-1:
            location = QFileDialog.getExistingDirectory(self, QString("Project Location"), "/home", QFileDialog.ShowDirsOnly)
            if not location.isEmpty():
                self.insertItem(0, QString(location))
                self.setCurrentIndex(0)
            else:
                self.setCurrentIndex(0)

class ComboBoxFile(QComboBox):
    def __init__(self, parent=None):
        super(ComboBoxFile, self).__init__(parent)

    def browseFile(self, index):
        if index == self.count()-1:
            file = QFileDialog.getOpenFileName(self, QString("Browse to select file"), "/home", "Data Files (*.dat *.txt)")
            if not file.isEmpty():
                self.insertItem(1, QString(file))
                self.setCurrentIndex(1)
            else:
                self.setCurrentIndex(0)


class DisplayLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(DisplayLineEdit, self).__init__(parent)
        #self.setReadOnly(True)
        self.setEnabled(False)


class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)


    def check(self):
        string = self.text()
        #print string
        if len(string)<>0:
            for i in string:
                if not re.match("[A-Za-z_]", i):
                    check_dummy = False
                    break
                else:
                    check_dummy = True

        else:
            check_dummy = False

        if not check_dummy:
            QMessageBox.information(self, "Warning", "Enter a valid entry.", QMessageBox.Ok)
            self.selectAll()
            self.setFocus()

class Separator(QFrame):
    def __init__(self, parent=None):
        super(Separator, self).__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class Wizard(QWizard):
    def __init__(self, parent=None):
        super(Wizard, self).__init__(parent)
        self.setFixedSize(QSize(800,500))
        self.setWizardStyle(QWizard.ClassicStyle)
        self.counties = countydata.CountyContainer(QString("./data/counties.csv"))
        self.selectedCounties = None
        self.addPage(self.createIntroPage())
        self.addPage(self.createResolutionPage())
        self.addPage(self.createSampleDataPage())
        self.addPage(self.createControlDataPage())
        self.addPage(self.createDBConnectionPage())
        self.addPage(self.createSummaryPage())
        self.setWindowTitle("New Project Wizard")

        self.connect(self.locationComboBox, SIGNAL("activated(int)"), self.locationComboBox.browseFolder)
        self.connect(self.geocorrLocationComboBox, SIGNAL("activated(int)"), self.geocorrLocationComboBox.browseFile)
        self.connect(self.sampleHHLocationComboBox, SIGNAL("activated(int)"), self.sampleHHLocationComboBox.browseFile)
        self.connect(self.sampleGQLocationComboBox, SIGNAL("activated(int)"), self.sampleGQLocationComboBox.browseFile)
        self.connect(self.samplePersonLocationComboBox, SIGNAL("activated(int)"), self.samplePersonLocationComboBox.browseFile)
        self.connect(self.controlHHLocationComboBox, SIGNAL("activated(int)"), self.controlHHLocationComboBox.browseFile)
        self.connect(self.controlGQLocationComboBox, SIGNAL("activated(int)"), self.controlGQLocationComboBox.browseFile)
        self.connect(self.controlPersonLocationComboBox, SIGNAL("activated(int)"), self.controlPersonLocationComboBox.browseFile)

        #self.connect(self.nameLineEdit, SIGNAL("editingFinished()"), self.nameLineEdit.check)
        #self.connect(self.hostnameLineEdit, SIGNAL("editingFinished()"), self.hostnameLineEdit.check)
        #self.connect(self.usernameLineEdit, SIGNAL("editingFinished()"), self.usernameLineEdit.check)

        self.connect(self.geocorrAutoRadio, SIGNAL("clicked()"), self.geocorrAutoAction)
        self.connect(self.geocorrUserProvRadio, SIGNAL("clicked()"), self.geocorrUserProvAction)
        self.connect(self.sampleAutoRadio, SIGNAL("clicked()"), self.sampleAutoAction)
        self.connect(self.sampleUserProvRadio, SIGNAL("clicked()"), self.sampleUserProvAction)
        self.connect(self.controlAutoRadio, SIGNAL("clicked()"), self.controlAutoAction)
        self.connect(self.controlUserProvRadio, SIGNAL("clicked()"), self.controlUserProvAction)

        self.connect(self.countySelectTree, SIGNAL("itemSelectionChanged()"), self.showCountySelection)

        self.connect(self, SIGNAL("currentIdChanged(int)"), self.updateSummary)

        self.connect(self.button(QWizard.CancelButton), SIGNAL("pressed()"), self.reject)

        sampleGQLocationComboBox = QLabel("Select the groupquarter sample file")
        samplePersonLocationComboBox = QLabel("Select the population sample file")

    def reject(self):
        reply = QMessageBox.question(None, "PopGen: New Project Wizard",
                                     QString("Do you wish to continue?"),
                                     QMessageBox.Yes| QMessageBox.No)
        if reply == QMessageBox.Yes:
            QDialog.reject(self)


    def showCountySelection(self):
        if self.countySelectTree.selectedItems() is not None:
            for selection in self.countySelectTree.selectedItems():
                if selection.parent() is None:
                    selection.setSelected(False)

            self.selectedCounties = self.countySelectTree.selectedItems()

    def geocorrAutoAction(self):
        self.geocorrUserProvGroupBox.setEnabled(False)
        self.geocorrLocationComboBox.setCurrentIndex(0)

    def geocorrUserProvAction(self):
        self.geocorrUserProvGroupBox.setEnabled(True)

    def sampleAutoAction(self):
        self.sampleUserProvGroupBox.setEnabled(False)
        self.sampleHHLocationComboBox.setCurrentIndex(0)
        self.sampleGQLocationComboBox.setCurrentIndex(0)
        self.samplePersonLocationComboBox.setCurrentIndex(0)


    def sampleUserProvAction(self):
        self.sampleUserProvGroupBox.setEnabled(True)

    def controlAutoAction(self):
        self.controlUserProvGroupBox.setEnabled(False)
        self.controlHHLocationComboBox.setCurrentIndex(0)
        self.controlGQLocationComboBox.setCurrentIndex(0)
        self.controlPersonLocationComboBox.setCurrentIndex(0)

    def controlUserProvAction(self):
        self.controlUserProvGroupBox.setEnabled(True)

    def createIntroPage(self):
        page = QWizardValidatePage()
        page.setTitle("Step 1: Region")

        # Project Description
        nameLabel = QLabel("Project Name")
        self.nameLineEdit = LineEdit()
        self.nameLineEdit.setText("Enter a name for the project")
        self.nameLineEdit.selectAll()
        nameLabel.setBuddy(self.nameLineEdit)
        locationLabel = QLabel("Project Location")
        self.locationComboBox = ComboBoxFolder()
        #self.locationComboBox.addItems([QString("C:/"), QString("Browse to select folder...")])
        self.locationComboBox.addItems([QString("C:/SynTest"), QString("Browse to select folder...")])
        locationLabel.setBuddy(self.locationComboBox)
        descLabel = QLabel("Project Description")
        self.descTextEdit = QTextEdit()
        descLabel.setBuddy(self.descTextEdit)
        # Project Description Layout
        projectVLayout = QVBoxLayout()
        projectVLayout.addWidget(nameLabel)
        projectVLayout.addWidget(self.nameLineEdit)
        projectVLayout.addWidget(locationLabel)
        projectVLayout.addWidget(self.locationComboBox)
        projectVLayout.addWidget(descLabel)
        projectVLayout.addWidget(self.descTextEdit)
        # Selecting Counties using the tree widget
        self.countySelectTree = QTreeWidget()
        self.countySelectTree.setColumnCount(1)
        self.countySelectTree.setHeaderLabels(["State/County"])
        self.countySelectTree.setItemsExpandable(True)
        state = QTreeWidgetItem(self.countySelectTree, [QString("State")])
        county = QTreeWidgetItem(state, [QString("County")])
        state = QTreeWidgetItem(self.countySelectTree, [QString("State1")])
        county = QTreeWidgetItem(state, [QString("County1")])
        # Displaying counties and selecting counties using the map
        canvas = QgsMapCanvas()
        canvas.setCanvasColor(QColor(0,0,0))
        canvas.enableAntiAliasing(True)
        canvas.useQImageToRender(False)
        #layerPath = "./data/NC_Selected_Counties.shp"
        layerPath = "./data/county.shp"
        layerName = "NCSelectedCounties"
        layerProvider = "ogr"
        layer = QgsVectorLayer(layerPath, layerName, layerProvider)
        if not layer.isValid():
            return

        QgsMapLayerRegistry.instance().addMapLayer(layer)
        canvas.setExtent(layer.extent())
        cl = QgsMapCanvasLayer(layer)
        layers = [cl]
        canvas.setLayerSet(layers)
        # Vertical layout of all elements
        vLayout = QVBoxLayout()
        vLayout.addLayout(projectVLayout)
        vLayout.addWidget(self.countySelectTree)
        # Horizontal layout of all elements
        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout)
        hLayout.addWidget(canvas)
        page.setLayout(hLayout)


        self.populateCountySelectTree()

        return page

    def populateCountySelectTree(self):

        self.initialLoad()
        self.countySelectTree.clear()
        self.countySelectTree.setColumnCount(1)
        self.countySelectTree.setHeaderLabels(["State/County"])
        self.countySelectTree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        #self.countySelectTree.setItemExpandable(True)

        parentFromState = {}
        parentFromStateCounty = {}
        for county in self.counties:
            ancestor = parentFromState.get(county.stateName)
            if ancestor is None:
                ancestor = QTreeWidgetItem(self.countySelectTree, [QString(county.stateName)])
                parentFromState[county.stateName]=ancestor

            stateCounty = "%s%s%s" %(county.stateName, "/", county.countyName)
            parent = parentFromStateCounty.get(stateCounty)
            if parent is None:
                parent = QTreeWidgetItem(ancestor, [QString(county.countyName)])
                parentFromStateCounty[stateCounty] = parent


        self.countySelectTree.sortItems(0, Qt.AscendingOrder)


    def initialLoad(self):
        try:
            self.counties.load()
        except IOError, e:
            QMessageBox.warning(self, "Counties - Error", "Failed to load: %s" %e)

    def createResolutionPage(self):
        page = QWizardValidatePage()
        page.setTitle("Step 2: Resolution of the Population Synthesis")

        resolutionLabel = QLabel("At what resolution do you want to synthesize the population (County/Tract/Blockgroup level)?")
        self.resolutionComboBox = QComboBox()
        self.resolutionComboBox.addItems([QString("County"), QString("Tract"), QString("Blockgroup")])
        self.resolutionComboBox.setFixedSize(QSize(250,20))
        self.geocorrGroupBox = QGroupBox("Will you provide Geographic Correspondence between the Geography and PUMA?")
        self.geocorrUserProvRadio = QRadioButton("Yes")
        self.geocorrAutoRadio = QRadioButton("No")
        self.geocorrUserProvRadio.setChecked(True)
        geocorrHLayout = QHBoxLayout()
        geocorrHLayout.addWidget(self.geocorrUserProvRadio)
        geocorrHLayout.addWidget(self.geocorrAutoRadio)
        self.geocorrGroupBox.setLayout(geocorrHLayout)

        geocorrLocationLabel = QLabel("Select the geographic correspondence file")
        self.geocorrLocationComboBox = ComboBoxFile()
        self.geocorrLocationComboBox.addItems([QString(""), QString("Browse to select file...")])
        geocorrLocationLabel.setBuddy(self.geocorrLocationComboBox)
        self.geocorrUserProvGroupBox = QGroupBox("User provided:")
        geocorrVLayout = QVBoxLayout()
        geocorrVLayout.addWidget(geocorrLocationLabel)
        geocorrVLayout.addWidget(self.geocorrLocationComboBox)
        self.geocorrUserProvGroupBox.setLayout(geocorrVLayout)

        vLayout = QVBoxLayout()
        vLayout.addWidget(resolutionLabel)
        vLayout.addWidget(self.resolutionComboBox)
        vLayout.addWidget(self.geocorrGroupBox)
        vLayout.addWidget(self.geocorrUserProvGroupBox)
        page.setLayout(vLayout)

        return page

    def createSampleDataPage(self):
        page = QWizardValidatePage()
        page.setTitle("Step 3: Population Sample")

        self.sampleGroupBox = QGroupBox("""Do you wish to provide sample data or the program will"""
                                         """use PUMS for population synthesis?""")
        self.sampleUserProvRadio = QRadioButton("Yes")
        self.sampleAutoRadio = QRadioButton("No")
        self.sampleUserProvRadio.setChecked(True)
        sampleHLayout = QHBoxLayout()
        sampleHLayout.addWidget(self.sampleUserProvRadio)
        sampleHLayout.addWidget(self.sampleAutoRadio)
        self.sampleGroupBox.setLayout(sampleHLayout)

        sampleHHLocationLabel = QLabel("Select the household sample file")
        sampleGQLocationLabel = QLabel("Select the groupquarter sample file")
        samplePersonLocationLabel = QLabel("Select the population sample file")

        self.sampleHHLocationComboBox = ComboBoxFile()
        self.sampleHHLocationComboBox.addItems([QString(""), QString("Browse to select file...")])
        sampleHHLocationLabel.setBuddy(self.sampleHHLocationComboBox)

        self.sampleGQLocationComboBox = ComboBoxFile()
        self.sampleGQLocationComboBox.addItems([QString(""), QString("Browse to select file...")])
        sampleGQLocationLabel.setBuddy(self.sampleGQLocationComboBox)

        self.samplePersonLocationComboBox = ComboBoxFile()
        self.samplePersonLocationComboBox.addItems([QString(""), QString("Browse to select file...")])
        samplePersonLocationLabel.setBuddy(self.samplePersonLocationComboBox)

        self.sampleUserProvGroupBox = QGroupBox("User provided:")
        sampleVLayout = QVBoxLayout()
        sampleVLayout.addWidget(sampleHHLocationLabel)
        sampleVLayout.addWidget(self.sampleHHLocationComboBox)
        sampleVLayout.addWidget(sampleGQLocationLabel)
        sampleVLayout.addWidget(self.sampleGQLocationComboBox)
        sampleVLayout.addWidget(samplePersonLocationLabel)
        sampleVLayout.addWidget(self.samplePersonLocationComboBox)
        self.sampleUserProvGroupBox.setLayout(sampleVLayout)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.sampleGroupBox)
        vLayout.addWidget(self.sampleUserProvGroupBox)
        page.setLayout(vLayout)

        return page

    def createControlDataPage(self):
        page = QWizardValidatePage()
        page.setTitle("Step 4: Control Totals")

        self.controlGroupBox = QGroupBox("""Do you wish to provide the marginal totals for"""
                                         """population characteristics of interest?""")
        self.controlUserProvRadio = QRadioButton("Yes")
        self.controlAutoRadio = QRadioButton("No")
        self.controlUserProvRadio.setChecked(True)
        controlHLayout = QHBoxLayout()
        controlHLayout.addWidget(self.controlUserProvRadio)
        controlHLayout.addWidget(self.controlAutoRadio)
        self.controlGroupBox.setLayout(controlHLayout)

        controlHHLocationLabel = QLabel("Select the household control file")
        controlGQLocationLabel = QLabel("Select the groupquarter control file")
        controlPersonLocationLabel = QLabel("Select the population control file")

        self.controlHHLocationComboBox = ComboBoxFile()
        self.controlHHLocationComboBox.addItems([QString(""), QString("Browse to select file...")])
        controlHHLocationLabel.setBuddy(self.controlHHLocationComboBox)

        self.controlGQLocationComboBox = ComboBoxFile()
        self.controlGQLocationComboBox.addItems([QString(""), QString("Browse to select file...")])
        controlGQLocationLabel.setBuddy(self.controlGQLocationComboBox)

        self.controlPersonLocationComboBox = ComboBoxFile()
        self.controlPersonLocationComboBox.addItems([QString(""), QString("Browse to select file...")])
        controlPersonLocationLabel.setBuddy(self.controlPersonLocationComboBox)

        self.controlUserProvGroupBox = QGroupBox("User provided:")
        controlVLayout = QVBoxLayout()
        controlVLayout.addWidget(controlHHLocationLabel)
        controlVLayout.addWidget(self.controlHHLocationComboBox)
        controlVLayout.addWidget(controlGQLocationLabel)
        controlVLayout.addWidget(self.controlGQLocationComboBox)
        controlVLayout.addWidget(controlPersonLocationLabel)
        controlVLayout.addWidget(self.controlPersonLocationComboBox)
        self.controlUserProvGroupBox.setLayout(controlVLayout)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.controlGroupBox)
        vLayout.addWidget(self.controlUserProvGroupBox)
        page.setLayout(vLayout)

        return page

    def createDBConnectionPage(self):
        page = QWizardValidatePage()
        page.setTitle("Step 5: MySQL Connection Settings")

        hostnameLabel = QLabel("Hostname")
        self.hostnameLineEdit = LineEdit()
        #self.hostnameLineEdit.setText("Enter a MYSQL hostname to connect to")
        self.hostnameLineEdit.setText("localhost")
        self.hostnameLineEdit.selectAll()
        hostnameLabel.setBuddy(self.hostnameLineEdit)
        hostnameHLayout = QHBoxLayout()
        hostnameHLayout.addWidget(hostnameLabel)
        hostnameHLayout.addWidget(self.hostnameLineEdit)

        usernameLabel = QLabel("Username")
        self.usernameLineEdit = LineEdit()
        #self.usernameLineEdit.setText("Enter username for the MYSQL account")
        self.usernameLineEdit.setText("root")
        usernameLabel.setBuddy(self.usernameLineEdit)
        usernameHLayout = QHBoxLayout()
        usernameHLayout.addWidget(usernameLabel)
        usernameHLayout.addWidget(self.usernameLineEdit)

        passwordLabel = QLabel("Password")
        self.passwordLineEdit = LineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        #self.passwordLineEdit.setText("Password")
        self.passwordLineEdit.setText("1234")
        passwordLabel.setBuddy(self.passwordLineEdit)
        passwordHLayout = QHBoxLayout()
        passwordHLayout.addWidget(passwordLabel)
        passwordHLayout.addWidget(self.passwordLineEdit)

        vLayout = QVBoxLayout()
        vLayout.addLayout(hostnameHLayout)
        vLayout.addLayout(usernameHLayout)
        vLayout.addLayout(passwordHLayout)
        page.setLayout(vLayout)

        return page


    def createSummaryPage(self):
        page = QWizardValidatePage()
        page.setTitle("Step 6: Summary")
        vlayoutCol1 = QVBoxLayout()
        vlayoutCol1.addWidget(QLabel("Project Name:"))
        vlayoutCol1.addWidget(QLabel("Project Location:"))
        vlayoutCol1.addWidget(QLabel("Project Description"))
        vlayoutCol1.addWidget(QLabel("Selected Counties:"))
        vlayoutCol1.addWidget(Separator())
        vlayoutCol1.addWidget(QLabel("Resolution of population Synthesis:"))
        vlayoutCol1.addWidget(QLabel("Geographic correspondence data provided by the user:"))
        vlayoutCol1.addWidget(QLabel("Location of the geographic correspondence file:"))
        vlayoutCol1.addWidget(Separator())
        vlayoutCol1.addWidget(QLabel(" data provided by the user:"))
        vlayoutCol1.addWidget(QLabel("Location of the household sample file:"))
        vlayoutCol1.addWidget(QLabel("Location of the group quarter sample file:"))
        vlayoutCol1.addWidget(QLabel("Location of the person sample file:"))
        vlayoutCol1.addWidget(Separator())
        vlayoutCol1.addWidget(QLabel("Control data provided by the user:"))
        vlayoutCol1.addWidget(QLabel("Location of the household control data file:"))
        vlayoutCol1.addWidget(QLabel("Location of the group quarter control data file:"))
        vlayoutCol1.addWidget(QLabel("Location of the person control data file:"))


        vlayoutCol2 = QVBoxLayout()

        self.projectNameLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.projectNameLineEdit)

        self.projectLocationLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.projectLocationLineEdit)

        self.projectDescLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.projectDescLineEdit)

        self.projectRegionLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.projectRegionLineEdit)

        vlayoutCol2.addWidget(Separator())

        self.projectResolutionLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.projectResolutionLineEdit)

        self.geocorrUserProvLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.geocorrUserProvLineEdit)

        self.geocorrUserProvLocationLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.geocorrUserProvLocationLineEdit)

        vlayoutCol2.addWidget(Separator())

        self.sampleUserProvLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.sampleUserProvLineEdit)

        self.sampleHHLocationLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.sampleHHLocationLineEdit)

        self.sampleGQLocationLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.sampleGQLocationLineEdit)

        self.samplePersonLocationLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.samplePersonLocationLineEdit)


        vlayoutCol2.addWidget(Separator())

        self.controlUserProvLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.controlUserProvLineEdit)

        self.controlHHLocationLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.controlHHLocationLineEdit)

        self.controlGQLocationLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.controlGQLocationLineEdit)

        self.controlPersonLocationLineEdit = DisplayLineEdit()
        vlayoutCol2.addWidget(self.controlPersonLocationLineEdit)


        hlayout = QHBoxLayout()
        hlayout.addLayout(vlayoutCol1)
        hlayout.addLayout(vlayoutCol2)
        page.setLayout(hlayout)

        return page

    def updateSummary(self, id):

        if id == 5:
            #self.currentPage().isFinalPage():

            geocorrLocation = self.geocorrLocationComboBox.currentText()
            geocorrUserProv = newproject.Geocorr(self.geocorrUserProvRadio.isChecked(),
                                                 geocorrLocation)

            sampleHHLocation = self.sampleHHLocationComboBox.currentText()
            sampleGQLocation = self.sampleGQLocationComboBox.currentText()
            samplePersonLocation = self.samplePersonLocationComboBox.currentText()
            sampleUserProv = newproject.Sample(self.sampleUserProvRadio.isChecked(),
                                               sampleHHLocation,
                                               sampleGQLocation,
                                               samplePersonLocation)

            controlHHLocation = self.controlHHLocationComboBox.currentText()
            controlGQLocation = self.controlGQLocationComboBox.currentText()
            controlPersonLocation = self.controlPersonLocationComboBox.currentText()
            controlUserProv = newproject.Control(self.controlUserProvRadio.isChecked(),
                                                 controlHHLocation,
                                                 controlGQLocation,
                                                 controlPersonLocation)

            db = newproject.DBInfo(self.hostnameLineEdit.text(),
                                   self.usernameLineEdit.text(),
                                   self.passwordLineEdit.text(),
                                   "QMYSQL")


            self.project = newproject.NewProject(self.nameLineEdit.text(),
                                                 self.locationComboBox.currentText(),
                                                 self.descTextEdit.toPlainText(),
                                                 self.selectedCounties,
                                                 self.resolutionComboBox.currentText(),
                                                 geocorrUserProv,
                                                 sampleUserProv,
                                                 controlUserProv,
                                                 db)


            self.projectNameLineEdit.setText(self.project.name)
            self.projectLocationLineEdit.setText(self.project.location)
            self.projectDescLineEdit.setText(self.project.description)

            dummy = ""
            if self.project.region is not None:
                for i in self.project.region:
                    dummy = dummy + i.text(0) + ", "+ i.parent().text(0)+ "; "

            self.projectRegionLineEdit.setText("%s"%dummy[:-2])
            self.projectResolutionLineEdit.setText(self.project.resolution)
            self.geocorrUserProvLineEdit.setText("%s" %self.project.geocorrUserProv.userProv)
            self.geocorrUserProvLocationLineEdit.setText(self.project.geocorrUserProv.location)
            self.sampleUserProvLineEdit.setText("%s" %self.project.sampleUserProv.userProv)
            self.sampleHHLocationLineEdit.setText(self.project.sampleUserProv.hhLocation)
            self.sampleGQLocationLineEdit.setText(self.project.sampleUserProv.gqLocation)
            self.samplePersonLocationLineEdit.setText(self.project.sampleUserProv.personLocation)
            self.controlUserProvLineEdit.setText("%s" %self.project.controlUserProv.userProv)
            self.controlHHLocationLineEdit.setText(self.project.controlUserProv.hhLocation)
            self.controlGQLocationLineEdit.setText(self.project.controlUserProv.gqLocation)
            self.controlPersonLocationLineEdit.setText(self.project.controlUserProv.personLocation)

            if not self.currentPage().projectLocationDummy:
                self.checkProjectLocation()
            if not self.currentPage().projectDatabaseDummy:
                self.checkProjectDatabase()






    def checkFileLocation(self, filePath):
        try:
            open(filePath, 'r')
        except IOError, e:
            raise IOError, e


    def checkSampleFiles(self):
        pass

    def checkControlFiles(self):
        pass


    def checkProjectLocation(self):
        try:
            os.makedirs("%s/%s/data" %(self.project.location, self.project.name))
            projectLocationDummy = True
        except WindowsError, e:
            reply = QMessageBox.question(None, "PopGen: Processing Data",
                                         QString("""Database Error: %s. \n\nDo you wish"""
                                                 """ to keep the previous data?"""
                                                 """\n    If Yes then rescpecify project location. """
                                                 """\n    If you wish to delete the previous data press No."""%e),
                                         QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.No:
                confirm = QMessageBox.question(None, "PopGen: Processing Data",
                                               QString("""Are you sure you want to continue?"""),
                                               QMessageBox.Yes|QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    shutil.rmtree("%s/%s" %(self.project.location, self.project.name))
                    os.makedirs("%s/%s/data" %(self.project.location, self.project.name))
                    projectLocationDummy = True
                else:
                    projectLocationDummy = False
            else:
                projectLocationDummy = False
        self.currentPage().projectLocationDummy = projectLocationDummy
        self.currentPage().emit(SIGNAL("completeChanged()"))

    def checkProjectDatabase(self):
        projectDBC = createDBC(self.project.db, self.project.name)

        if not projectDBC.dbc.open():
            QMessageBox.warning(None, "PopGen: Processing Data",
                                QString("DatabaseError: %s" %projectDBC.dbc.lastError().text()))
            projectDatabaseDummy = False
        else:
            query = QSqlQuery(projectDBC.dbc)
            if not query.exec_("""Create Database %s""" %(self.project.name)):
                reply = QMessageBox.question(None, "PopGen: Processing Data",
                                             QString("""QueryError: %s. \n\n"""
                                                     """Do you wish to keep the old MySQL database?"""
                                                     """\n    If Yes then respecify the project name."""
                                                     """\n    If you wish to delete press No."""%query.lastError().text()),
                                             QMessageBox.Yes|QMessageBox.No)
                if reply == QMessageBox.No:
                    confirm = QMessageBox.question(None, "PopGen: Processing Data",
                                                   QString("""Are you sure you want to continue?"""),
                                                   QMessageBox.Yes|QMessageBox.No)
                    if confirm == QMessageBox.Yes:
                        d1 = query.exec_("""Drop Database %s""" %(self.project.name))
                        d2 = query.exec_("""Create Database %s""" %(self.project.name))
                        projectDatabaseDummy = d1 and d2
                    else:
                        projectDatabaseDummy = False
                else:
                    projectDatabaseDummy = False
            else:
                projectDatabaseDummy = True


        self.currentPage().projectDatabaseDummy = projectDatabaseDummy
        self.currentPage().emit(SIGNAL("completeChanged()"))
        projectDBC.dbc.close()

def main():
    app = QApplication(sys.argv)
    QgsApplication.setPrefixPath(qgis_prefix, True)
    QgsApplication.initQgis()
    wiz = Wizard()
    wiz.show()
    app.exec_()
    QgsApplication.exitQgis()


if __name__ == "__main__":
    main()

