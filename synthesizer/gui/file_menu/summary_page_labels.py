# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from database.createDBConnection import createDBC
from misc.widgets import *

import os, shutil


class SummaryPage(QWizardPage):
    def __init__(self, parent=None):
        super(SummaryPage, self).__init__(parent)

        self.projectLocationDummy = False
        self.projectDatabaseDummy = False

        self.setTitle("Step 6: Project Summary")
        vlayoutCol1 = QVBoxLayout()

        vlayoutCol1.addWidget(QLabel(self.leftPad("Project name")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Project location")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Project description")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Selected counties")))
        vlayoutCol1.addWidget(Separator())
        vlayoutCol1.addWidget(QLabel(self.leftPad("Geographic resolution of population synthesis")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Geographic correspondence data provided by the user")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Location of the geographic correspondence file")))
        vlayoutCol1.addWidget(Separator())
        vlayoutCol1.addWidget(QLabel(self.leftPad("Sample data provided by the user")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Location of the household sample file")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Location of the groupquarter sample file")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Location of the person sample file")))
        vlayoutCol1.addWidget(Separator())
        vlayoutCol1.addWidget(QLabel(self.leftPad("Marginals data provided by the user")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Location of the household marginals data file")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Location of the groupquarter marginals data file")))
        vlayoutCol1.addWidget(QLabel(self.leftPad("Location of the person marginals data file")))


        vlayoutCol2 = QVBoxLayout()

        self.projectName = QLabel()
        vlayoutCol2.addWidget(self.projectName)

        self.projectLocation = QLabel()
        vlayoutCol2.addWidget(self.projectLocation)

        self.projectDesc = QLabel()
        vlayoutCol2.addWidget(self.projectDesc)

        self.projectRegion = QLabel()
        vlayoutCol2.addWidget(self.projectRegion)

        vlayoutCol2.addWidget(Separator())

        self.projectResolution = QLabel()
        vlayoutCol2.addWidget(self.projectResolution)

        self.geocorrUserProv = QLabel()
        vlayoutCol2.addWidget(self.geocorrUserProv)

        self.geocorrUserProvLocation = QLabel()
        vlayoutCol2.addWidget(self.geocorrUserProvLocation)

        vlayoutCol2.addWidget(Separator())

        self.sampleUserProv = QLabel()
        vlayoutCol2.addWidget(self.sampleUserProv)

        self.sampleHHLocation = QLabel()
        vlayoutCol2.addWidget(self.sampleHHLocation)

        self.sampleGQLocation = QLabel()
        vlayoutCol2.addWidget(self.sampleGQLocation)

        self.samplePersonLocation = QLabel()
        vlayoutCol2.addWidget(self.samplePersonLocation)


        vlayoutCol2.addWidget(Separator())

        self.controlUserProv = QLabel()
        vlayoutCol2.addWidget(self.controlUserProv)

        self.controlHHLocation = QLabel()
        vlayoutCol2.addWidget(self.controlHHLocation)

        self.controlGQLocation = QLabel()
        vlayoutCol2.addWidget(self.controlGQLocation)

        self.controlPersonLocation = QLabel()
        vlayoutCol2.addWidget(self.controlPersonLocation)


        hlayout = QHBoxLayout()
        hlayout.addLayout(vlayoutCol1)
        hlayout.addLayout(vlayoutCol2)
        self.setLayout(hlayout)


    def leftPad(self, text):
        text = str(text)
        text = text.ljust(70, '.')
        return text



    def fillPage(self, project):
        self.project = project
        self.projectName.setText(self.formatText(self.project.name))
        self.projectLocation.setText(self.formatText(self.project.location))
        self.projectDesc.setText(self.formatText(self.project.description))
        dummy = ""
        if self.project.region is not None:
            for i in self.project.region.keys():
                dummy = dummy + i + ", "+ self.project.region[i]+ "; "
        self.projectRegion.setText(self.formatText("%s"%dummy[:-2]))

        resolutionText = self.project.resolution

        if resolutionText == "Tract":
            resolution = 'Census Tract'
        elif resolutionText == "Blockgroup":
            resolution = 'Census Blockgroup'
        elif resolutionText == 'TAZ':
            resolution = 'Traffic Analysis Zone (TAZ)'
        else:
            resolution = 'County'


        self.projectResolution.setText(self.formatText(resolution))
        #self.projectResolutionComboBox.findAndSet(self.project.resolution)

        text = self.convertBoolToString(self.project.geocorrUserProv.userProv)
        self.geocorrUserProv.setText(self.formatText(text))
        self.geocorrUserProvLocation.setText(self.formatText(self.project.geocorrUserProv.location))

        text = self.convertBoolToString(self.project.sampleUserProv.userProv, self.project.sampleUserProv.defSource)
        self.sampleUserProv.setText(self.formatText(text))
        self.sampleHHLocation.setText(self.formatText(self.project.sampleUserProv.hhLocation))
        self.sampleGQLocation.setText(self.formatText(self.project.sampleUserProv.gqLocation))
        self.samplePersonLocation.setText(self.formatText(self.project.sampleUserProv.personLocation))

        text = self.convertBoolToString(self.project.controlUserProv.userProv, self.project.controlUserProv.defSource)
        self.controlUserProv.setText(self.formatText(text))
        self.controlHHLocation.setText(self.formatText(self.project.controlUserProv.hhLocation))
        self.controlGQLocation.setText(self.formatText(self.project.controlUserProv.gqLocation))
        self.controlPersonLocation.setText(self.formatText(self.project.controlUserProv.personLocation))


    def convertBoolToString(self, value, source='default'):
        if value:
            text = 'Yes'
        else:
            text = 'No, %s data will be used' %source
        return text

    def formatText(self, text):
        if text == "":
            text = "-"

        return ("<font color = brown>" + '%s' %text + "</font>")



    def isComplete(self):
        if self.projectLocationDummy and self.projectDatabaseDummy:
            return True
        else:
            return False

    def checkFileLocation(self, filePath):
        try:
            open(filePath, 'r')
        except IOError, e:
            raise IOError, e

    def checkProjectLocation(self, projectLocation, projectName):
        try:
            os.makedirs("%s/%s/results" %(projectLocation, projectName))
            self.projectLocationDummy = True
        except WindowsError, e:
            print e
            reply = QMessageBox.question(self, "Project Setup Wizard",
                                         QString("""Cannot create a project folder when the folder already exists. \n\nDo you wish"""
                                                 """ to keep the previous data?"""
                                                 """\n    If Yes then re-specify the project location. """
                                                 """\n    If you wish to delete the previous data, select No."""),
                                         QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.No:
                confirm = QMessageBox.question(self, "Project Setup Wizard",
                                               QString("""Are you sure you want to continue?"""),
                                               QMessageBox.Yes|QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    shutil.rmtree("%s/%s" %(projectLocation, projectName))
                    os.makedirs("%s/%s/results" %(projectLocation, projectName))
                    self.projectLocationDummy = True
                else:
                    self.projectLocationDummy = False
            else:
                self.projectLocationDummy = False
        self.emit(SIGNAL("completeChanged()"))

    def checkProjectDatabase(self, db, projectName):
        projectDBC = createDBC(db)
        projectDBC.dbc.open()

        query = QSqlQuery(projectDBC.dbc)
        if not query.exec_("""Create Database %s""" %(projectName)):
            print query.lastError().text()
            reply = QMessageBox.question(self, "Project Setup Wizard",
                                         QString("""Cannot create a MySQL database when the database already exists. \n\n"""
                                                 """Do you wish to keep the old MySQL database?"""
                                                 """\n    If Yes then re-specify the project name."""
                                                 """\n    If you wish to delete the previous MySQL data, select No."""),
                                         QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.No:
                confirm = QMessageBox.question(self, "Project Setup Wizard",
                                               QString("""Are you sure you want to continue?"""),
                                               QMessageBox.Yes|QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    if not query.exec_("""Drop Database %s""" %(projectName)):
                        print "FileError: %s" %(query.lastError().text())
                        projectDBC.dbc.close()
                        self.projectDatabaseDummy = False
                    if not query.exec_("""Create Database %s""" %(projectName)):
                        print "FileError: %s" %(query.lastError().text())
                        projectDBC.dbc.close()
                        self.projectDatabaseDummy = False

                    for i in range(5):
                        if not query.exec_("""Drop Database %s%s%s""" %(projectName, 'scenario', str(i + 1))):
                            print "FileError: %s" %(query.lastError().text())
                            self.projectDatabaseDummy = False
                        if not query.exec_("""Create Database %s%s%s""" %(projectName, 'scenario', str(i + 1))):
                            print "FileError: %s" %(query.lastError().text())
                            self.projectDatabaseDummy = False
                    projectDBC.dbc.close()
                    self.projectDatabaseDummy = True
                else:
                    projectDBC.dbc.close()
                    self.projectDatabaseDummy = False
            else:
                projectDBC.dbc.close()
                self.projectDatabaseDummy =  False
        else:
            for i in range(5):
                if not query.exec_("""Create Database %s%s%s""" %(projectName, 'scenario', str(i + 1))):
                    print "FileError: %s" %(query.lastError().text())
                    self.projectDatabaseDummy = False
            projectDBC.dbc.close()
            self.projectDatabaseDummy = True


        self.emit(SIGNAL("completeChanged()"))

