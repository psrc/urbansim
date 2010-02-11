# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from database.createDBConnection import createDBC
from misc.errors import FileError
from import_data import ImportUserProvData, FileProperties

class UserImportGeocorrData():
    def __init__(self, project):
        self.project = project
        self.projectDBC = createDBC(self.project.db, self.project.name)
        self.projectDBC.dbc.open()
        self.query = QSqlQuery(self.projectDBC.dbc)

    def createGeocorrTable(self):
        check = self.checkIfTableExists('geocorr')

        if check:
            geocorrTableQuery = self.mysqlQueries('geocorr', self.project.geocorrUserProv.location)

            if not self.query.exec_(geocorrTableQuery.query1):
                raise FileError, self.query.lastError().text()

            if not self.query.exec_(geocorrTableQuery.query2):
                raise FileError, self.query.lastError().text()

    def mysqlQueries(self, name, filePath):
        fileProp = FileProperties(filePath)
        fileQuery = ImportUserProvData(name,
                                       filePath,
                                       fileProp.varNames,
                                       fileProp.varTypes,
                                       fileProp.varNamesDummy,
                                       fileProp.varTypesDummy)
        return fileQuery

    def checkIfTableExists(self, tablename):
        # 0 - some other error, 1 - overwrite error (table deleted)
        if not self.query.exec_("""create table %s (dummy text)""" %tablename):
            if self.query.lastError().number() == 1050:
                reply = QMessageBox.question(None, "Import",
                                             QString("""A table with name %s already exists. Would you like to overwrite?""" %tablename),
                                             QMessageBox.Yes| QMessageBox.No)
                if reply == QMessageBox.Yes:
                    if not self.query.exec_("""drop table %s""" %tablename):
                        raise FileError, self.query.lastError().text()
                    return 1
                else:
                    return 0
            else:
                raise FileError, self.query.lastError().text()
        else:
            if not self.query.exec_("""drop table %s""" %tablename):
                raise FileError, self.query.lastError().text()
            return 1

class AutoImportGeocorrData():
    def __init__(self, project):
        self.project = project
        self.projectDBC = createDBC(self.project.db, self.project.name)
        self.projectDBC.dbc.open()
        self.query = QSqlQuery(self.projectDBC.dbc)

    def createGeocorrTable(self):
        check = self.checkIfTableExists('geocorr')

        if check:
            if self.project.controlUserProv.defSource <> 'ACS 2005-2007':
                geocorrTableQuery = ImportUserProvData('geocorr',
                                                       "./data/us2000geocorr.csv",
                                                       [], [], True, True)
            else:
                geocorrTableQuery = ImportUserProvData('geocorr',
                                                       "./data/usacsgeocorr.csv",
                                                       [], [], True, True)                

            if not self.query.exec_(geocorrTableQuery.query1):
                raise FileError, self.query.lastError().text()

            if not self.query.exec_(geocorrTableQuery.query2):
                raise FileError, self.query.lastError().text()


    def checkIfTableExists(self, tablename):
        # 0 - some other error, 1 - overwrite error (table deleted)
        if not self.query.exec_("""create table %s (dummy text)""" %tablename):
            if self.query.lastError().number() == 1050:
                reply = QMessageBox.question(None, "Import",
                                             QString("""A table with name %s already exists. Would you like to overwrite?""" %tablename),
                                             QMessageBox.Yes| QMessageBox.No)
                if reply == QMessageBox.Yes:
                    if not self.query.exec_("""drop table %s""" %tablename):
                        raise FileError, self.query.lastError().text()
                    return 1
                else:
                    return 0
            else:
                raise FileError, self.query.lastError().text()
        else:
            if not self.query.exec_("""drop table %s""" %tablename):
                raise FileError, self.query.lastError().text()
            return 1
