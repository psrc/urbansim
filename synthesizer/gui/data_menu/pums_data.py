# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from __future__ import with_statement

import urllib
import os
import copy

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from database.createDBConnection import createDBC
from misc.errors import FileError
from misc.utils import UnzipFile
from misc.widgets import VariableSelectionDialog
from import_data import ImportUserProvData, FileProperties

from global_vars import *

class UserImportSampleData():
    def __init__(self, project):
        self.project = project
        self.projectDBC = createDBC(self.project.db, self.project.name)
        self.projectDBC.dbc.open()
        self.query = QSqlQuery(self.projectDBC.dbc)

    def createHhldTable(self):
        check = self.checkIfTableExists('hhld_sample')

        if check:
            hhldTableQuery = self.mysqlQueries('hhld_sample', self.project.sampleUserProv.hhLocation)

            if not self.query.exec_(hhldTableQuery.query1):
                raise FileError, self.query.lastError().text()

            if not self.query.exec_(hhldTableQuery.query2):
                raise FileError, self.query.lastError().text()

            #print 'hhld index'
            if not self.query.exec_("""alter table hhld_sample add index(serialno)"""):
                #raise FileError, self.query.lastError().text()
                print "Warning: %s" %self.query.lastError.text()




    def createGQTable(self):
        check = self.checkIfTableExists('gq_sample')

        if check:
            gqLocLen = len(self.project.sampleUserProv.gqLocation)

            if gqLocLen > 1:
                gqTableQuery = self.mysqlQueries('gq_sample', self.project.sampleUserProv.gqLocation)

                if not self.query.exec_(gqTableQuery.query1):
                    raise FileError, self.query.lastError().text()

                if not self.query.exec_(gqTableQuery.query2):
                    raise FileError, self.query.lastError().text()

                #print 'gq index'
                if not self.query.exec_("""alter table gq_sample add index(serialno)"""):
                    #raise FileError, self.query.lastError().text()
                    print "Warning: %s" %self.query.lastError.text()


    def createPersonTable(self):
        check = self.checkIfTableExists('person_sample')

        if check:
            personTableQuery = self.mysqlQueries('person_sample', self.project.sampleUserProv.personLocation)

            if not self.query.exec_(personTableQuery.query1):
                raise FileError, self.query.lastError().text()

            if not self.query.exec_(personTableQuery.query2):
                raise FileError, self.query.lastError().text()

            #print 'person index'
            if not self.query.exec_("""alter table person_sample add index(serialno, pnum)"""):
                #raise FileError, self.query.lastError().text()
                print "Warning: %s" %self.query.lastError.text()

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



class AutoImportPUMS2000Data():
    def __init__(self, project):
        self.project = project
        self.state = self.project.state
        self.stateAbb = self.project.stateAbb
        self.stateCode = self.project.stateCode


        self.loc = DATA_DOWNLOAD_LOCATION + os.path.sep + self.state + os.path.sep + 'PUMS2000'
        self.loc = os.path.realpath(self.loc)

        self.projectDBC = createDBC(self.project.db, self.project.name)
        self.projectDBC.dbc.open()

        self.query = QSqlQuery(self.projectDBC.dbc)

        self.housingVariablesSelected = []
        self.housingVariablesSelectedDummy = False
        self.personVariablesSelected = []
        self.personVariablesSelectedDummy = False

        self.pumsVariableTable()

        #self.checkHousingPUMSTable()
        #self.checkPersonPUMSTable()

    def checkHousingPUMSTable(self):
        if self.checkIfTableExists('housing_pums'):
            self.downloadPUMSData()
            self.housingVarDicts()
            self.housingDefVar()
            self.housingSelVars()
            self.createHousingPUMSTable()

    def checkPersonPUMSTable(self):
        if self.checkIfTableExists('person_pums'):
            self.downloadPUMSData()
            self.personVarDicts()
            self.personDefVar()
            self.personSelVars()
            self.createPersonPUMSTable()

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


    def downloadPUMSData(self):

        try:
            os.makedirs(self.loc)
            self.retrieveAndStorePUMS()
        except WindowsError, e:
            reply = QMessageBox.question(None, "Import",
                                         QString("""Cannot download data when the data already exists.\n\n"""
                                                 """Would you like to keep the existing files?"""
                                                 """\nSelect No if you would like to download the files again."""),
                                         QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.No:
                confirm = QMessageBox.question(None, "Import",
                                               QString("""Would you like to continue?"""),
                                               QMessageBox.Yes|QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    self.retrieveAndStorePUMS()

        self.extractPUMS()


    def retrieveAndStorePUMS(self):
        web_state = '%s' %self.state
        web_state = web_state.replace(' ', '_')
        download_location = self.loc + os.path.sep + 'all_%s.zip' %(web_state)
        urllib.urlretrieve("""http://ftp2.census.gov/census_2000/datasets/"""
                           """PUMS/FivePercent/%s/all_%s.zip""" %(web_state, web_state),
                           download_location)

    def extractPUMS(self):

        web_state = '%s' %self.state
        web_state = web_state.replace(' ', '_')
        file = UnzipFile(self.loc, "all_%s.zip" %(web_state))
        file.unzip()





    def pumsVariableTable(self):
        # Creats a table that contains the location of the different PUMS variables in the raw data files
        check = self.checkIfTableExists('PUMS2000VariableList')
        if check:
            PUMSVariableDefTable = ImportUserProvData("PUMS2000VariableList",
                                                      "./data/PUMS2000_Variables.csv",
                                                      [], [],True, True)
            if not self.query.exec_(PUMSVariableDefTable.query1):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_(PUMSVariableDefTable.query2):
                raise FileError, self.query.lastError().text()


    def housingVarDicts(self):
        # Reading the list of PUMS housing variable names
        if not self.query.exec_("""select variablename, description, beginning, length from pums2000variablelist where type = 'H'"""):
            raise FileError, self.query.lastError().text()
        else:
            self.housingVariableDict = {}
            self.housingVarBegDict = {}
            self.housingVarLenDict = {}
            while (self.query.next()):
                self.housingVariableDict['%s'%self.query.value(0).toString()] = '%s'%self.query.value(1).toString()
                self.housingVarBegDict['%s'%self.query.value(0).toString()] = '%s'%self.query.value(2).toString()
                self.housingVarLenDict['%s'%self.query.value(0).toString()] = '%s'%self.query.value(3).toString()

    def housingDefVar(self):
        # Reading the list of PUMS default housing variable names
        if not self.query.exec_("""select variablename from pums2000variablelist where type = 'H' and defaultvar = 1"""):
            raise FileError, self.query.lastError().text()
        else:
            self.housingDefaultVariables = []
            while (self.query.next()):
                self.housingDefaultVariables.append(self.query.value(0).toString())


    def personVarDicts(self):
        # Reading the list of PUMS person variable names
        if not self.query.exec_("""select variablename, description, beginning, length from pums2000variablelist where type = 'P'"""):
            raise FileError, self.query.lastError().text()
        else:
            self.personVariableDict = {}
            self.personVarBegDict = {}
            self.personVarLenDict = {}
            while (self.query.next()):
                self.personVariableDict['%s'%self.query.value(0).toString()] = '%s'%self.query.value(1).toString()
                self.personVarBegDict['%s'%self.query.value(0).toString()] = '%s'%self.query.value(2).toString()
                self.personVarLenDict['%s'%self.query.value(0).toString()] = '%s'%self.query.value(3).toString()


    def personDefVar(self):
        # Reading the list of PUMS default person variable names
        if not self.query.exec_("""select variablename from pums2000variablelist where type = 'P' and defaultvar = 1"""):
            raise FileError, self.query.lastError().text()
        else:
            self.personDefaultVariables = []
            while (self.query.next()):
                self.personDefaultVariables.append(self.query.value(0).toString())


    def housingSelVars(self):
        housingVariablesDialog = VariableSelectionDialog(self.housingVariableDict, self.housingDefaultVariables,
                                                         "PUMS Housing Variable(s) Selection",
                                                         "controlvariables", warning="Note: Select variables to import")

        # Launch a dialogbox to select the housing variables of interest
        if housingVariablesDialog.exec_():
            self.housingVariablesSelectedDummy = True
            self.housingVariablesSelected = housingVariablesDialog.selectedVariableListWidget.variables
        else:
            self.housingVariablesSelectedDummy = False



    def personSelVars(self):
        personVariablesDialog = VariableSelectionDialog(self.personVariableDict, self.personDefaultVariables,
                                                        "PUMS Person Variable(s) Selection",
                                                        "controlvariables", warning="Note: Select variables to import")

        # Launch a dialogbox to select the person variables of interest
        if personVariablesDialog.exec_():
            self.personVariablesSelectedDummy = True
            self.personVariablesSelected = personVariablesDialog.selectedVariableListWidget.variables

        else:
            self.personVariablesSelectedDummy = False


    def checkIfFileExists(self, file):
        try:
            fileInfo = os.stat(file)

            reply = QMessageBox.question(None, "Import",
                                         QString("""File %s exists. Would you like to overwrite?""" %(file)),
                                         QMessageBox.Yes| QMessageBox.No)

            if reply == QMessageBox.Yes:
                return 0
            else:
                return 1
        except WindowsError, e:
            print 'Warning: File - %s not present' %(file)
            return 0

    def createHousingPUMSTable(self):
        # Creating a Housing PUMS Table
        self.housingFileName = 'PUMS5_hou_%s.csv' %(self.stateCode[self.state])
        self.housingPUMSloc = os.path.join(self.loc, self.housingFileName)

        if not self.checkIfFileExists(self.housingPUMSloc):
            self.createHousingPUMSFile()

        housingVariablesSelected = copy.deepcopy(self.housingVariablesSelected)
        housingVariablesSelected.insert(0, 'hhid')

        housingVariablesSelectedType = ['bigint'] * len(housingVariablesSelected)

        try:
            housingPUMSTableQuery = ImportUserProvData("housing_pums", self.housingPUMSloc,
                                                       housingVariablesSelected, housingVariablesSelectedType, False, False)
        except Exception, e:
            raise FileError, e
        if not self.query.exec_(housingPUMSTableQuery.query1):
            raise FileError, self.query.lastError().text()

        if not self.query.exec_(housingPUMSTableQuery.query2):
            raise FileError, self.query.lastError().text()



    def createPersonPUMSTable(self):
        # Creating a Person PUMS Table
        self.personFileName = 'PUMS5_per_%s.csv' %(self.stateCode[self.state])
        self.personPUMSloc = os.path.join(self.loc, self.personFileName)

        if not self.checkIfFileExists(self.personPUMSloc):
            self.createPersonPUMSFile()


        personVariablesSelected = copy.deepcopy(self.personVariablesSelected)


        personVariablesSelected.insert(0, 'hhid')
        personVariablesSelected.insert(0, 'pumano')
        personVariablesSelected.insert(0, 'state')

        personVariablesSelectedType = ['bigint'] * len(personVariablesSelected)

        try:
            personPUMSTableQuery = ImportUserProvData("person_pums", self.personPUMSloc,
                                                      personVariablesSelected, personVariablesSelectedType, False, False)
        except Exception, e:
            raise FileError, e

        if not self.query.exec_(personPUMSTableQuery.query1):
            raise FileError, self.query.lastError().text()

        if not self.query.exec_(personPUMSTableQuery.query2):
            raise FileError, self.query.lastError().text()


#    def createPUMSFile(self):
#        pumsFilename = 'PUMS5_%s.TXT' %(self.stateCode[self.state])
#        pumspersonFilename = 'PUMS5_per_%s.TXT' %(self.stateCode[self.state])
#        pumshousingFilename = 'PUMS5_hou_%s.TXT' %(self.stateCode[self.state])

#        with open(os.path.join(self.loc, pumsFilename), 'r') as f:
#            with open(os.path.join(self.loc, pumspersonFilename), 'w') as fperson:
#                with open(os.path.join(self.loc, pumshousingFilename), 'w') as fhousing:
#                    nperson = 0
#                    nhousing = 0
#                    if self.personVariablesSelectedDummy:
#                        for i in f:
#                            rectype = i[0:1]
#                            if rectype == 'P':
#                                personRec = self.parsePerson(i)
#                                fperson.write(personRec)
#                                nperson = nperson + 1
#                    if self.housingVariablesSelectedDummy:
#                        for i in f:
#                            rectype = i[0:1]
#                            if rectype == 'P':
#                                housingRec = self.parseHousing(i)
#                                fhousing.write(housingRec)
#                                nhousing = nhousing + 1

 #       print 'Housing Records Parsed - %s' %nhousing
 #       print 'Person Records Parsed - %s' %nperson


    def createPersonPUMSFile(self):
        pumsFilename = 'PUMS5_%s.TXT' %(self.stateCode[self.state])
        pumspersonFilename = 'PUMS5_per_%s.csv' %(self.stateCode[self.state])

        with open(os.path.join(self.loc, pumsFilename), 'r') as f:
            with open(os.path.join(self.loc, pumspersonFilename), 'w') as fperson:
                nperson = 0
                nhousing = 0
                if self.personVariablesSelectedDummy:
                    for i in f:
                        rectype = i[0:1]
                        if rectype == 'P':
                            personRec = self.parsePerson(i, state, puma5, nhousing)
                            fperson.write(personRec)
                            nperson = nperson + 1
                        else:
                            puma5 = i[13:18]
                            state = i[9:11]
                            nhousing = nhousing + 1
                else:
                    QMessageBox.warning(None, "Import", QString("""Empty person PUMS File and empty person PUMS"""
                                                                """ table will be created since no"""
                                                                """ variables were selected for extraction."""),
                                        QMessageBox.Ok)
        #print 'Person Records Parsed - %s' %nperson


    def createHousingPUMSFile(self):
        pumsFilename = 'PUMS5_%s.TXT' %(self.stateCode[self.state])
        pumshousingFilename = 'PUMS5_hou_%s.csv' %(self.stateCode[self.state])

        with open(os.path.join(self.loc, pumsFilename), 'r') as f:
            with open(os.path.join(self.loc, pumshousingFilename), 'w') as fhousing:
                nhousing = 0
                if self.housingVariablesSelectedDummy:
                    for i in f:
                        rectype = i[0:1]
                        if rectype == 'H':
                            nhousing = nhousing + 1
                            housingRec = self.parseHousing(i, nhousing)
                            fhousing.write(housingRec)

                else:
                    QMessageBox.warning(None, "Import", QString("""Empty housing PUMS File and empty housing PUMS"""
                                                                """ table will be created since no"""
                                                                """ variables were selected for extraction."""),
                                        QMessageBox.Ok)
        #print 'Housing Records Parsed - %s' %nhousing


    def parseHousing(self, record, nhousing):
        string = "%s," %(nhousing)
        for i in self.housingVariablesSelected:
            start = int(self.housingVarBegDict['%s'%i])-1
            end = start + int(self.housingVarLenDict['%s'%i])
            value = record[start:end]
            string = string + value + ','

        string = string[:-1] + '\n'
        return string



    def parsePerson(self, record, state, puma5, nhousing):
        string = "%s,%s,%s," %(state, puma5, nhousing)
        for i in self.personVariablesSelected:
            start = int(self.personVarBegDict['%s'%i])-1
            end = start + int(self.personVarLenDict['%s'%i])
            value = record[start:end]
            string = string + value + ','

        string = string[:-1] + '\n'
        return string


class AutoImportPUMSACSData(AutoImportPUMS2000Data):
    def __init__(self, project):
        AutoImportPUMS2000Data.__init__(self, project)
        self.project = project

        self.loc = DATA_DOWNLOAD_LOCATION + os.path.sep + self.state + os.path.sep + 'PUMSACS'
        self.loc = os.path.realpath(self.loc)


    def pumsVariableTable(self):
        check = self.checkIfTableExists('PUMSACSVariableList')
        if check:
            PUMSVariableDefTable = ImportUserProvData("PUMSACSVariableList",
                                                      "./data/PUMSACS_Variables.csv",
                                                      [], [],True, True)
            if not self.query.exec_(PUMSVariableDefTable.query1):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_(PUMSVariableDefTable.query2):
                raise FileError, self.query.lastError().text()


    def checkHousingPUMSTable(self):
        if self.checkIfTableExists('housing_pums'):
            self.downloadPUMSData('H')
            self.housingVarDicts()
            self.housingDefVar()
            self.housingSelVars()
            self.createHousingPUMSTable()

    def checkPersonPUMSTable(self):
        if self.checkIfTableExists('person_pums'):
            self.downloadPUMSData('P')
            self.personVarDicts()
            self.personDefVar()
            self.personSelVars()
            self.createPersonPUMSTable()

    def createHousingPUMSTable(self):
        web_stabb = self.project.stateAbb[self.state]
        hMasterFile = self.loc + os.path.sep + 'ss07h%s.csv' %web_stabb

        hMasterVariablesTypes = ['bigint'] * HACS_VARCOUNT
        
        hMasterPUMSTableQuery = ImportUserProvData("housing_raw", hMasterFile, 
                                                   varTypes=hMasterVariablesTypes, 
                                                   varNamesFileDummy=True, 
                                                   varTypesFileDummy=False)

        if self.checkIfTableExists('housing_raw'):

            if not self.query.exec_(hMasterPUMSTableQuery.query1):
                raise FileError, self.query.lastError().text()

            if not self.query.exec_(hMasterPUMSTableQuery.query2):
                raise FileError, self.query.lastError().text()


        dummyString = ''
        for i in self.housingVariablesSelected:
            dummyString = dummyString + i + ','
            
        dummyString = dummyString[:-1]
        #print dummyString
        
        

        if not self.query.exec_("""create table housing_pums select %s from housing_raw"""
                                %(dummyString)):
            raise FileError, self.query.lastError().text()


    def createPersonPUMSTable(self):
        web_stabb = self.project.stateAbb[self.state]
        pMasterFile = self.loc + os.path.sep + 'ss07p%s.csv' %web_stabb

        pMasterVariablesTypes = ['bigint'] * PACS_VARCOUNT
        
        pMasterPUMSTableQuery = ImportUserProvData("person_raw", pMasterFile, 
                                                   varTypes=pMasterVariablesTypes, 
                                                   varNamesFileDummy=True, 
                                                   varTypesFileDummy=False)

        import time
        ti = time.time()
        if self.checkIfTableExists('person_raw'):

            if not self.query.exec_(pMasterPUMSTableQuery.query1):
                raise FileError, self.query.lastError().text()

            if not self.query.exec_(pMasterPUMSTableQuery.query2):
                raise FileError, self.query.lastError().text()


        dummyString = ''
        for i in self.personVariablesSelected:
            dummyString = dummyString + i + ','
            
        dummyString = dummyString[:-1]
        #print dummyString

        #print 'time for creating the raw person table - ', time.time()-ti

        ti = time.time()


        if not self.query.exec_("""create table person_pums select %s from person_raw"""
                                %(dummyString)):
            raise FileError, self.query.lastError().text()

        #print 'time for creating the small person table - ', time.time()-ti

        

    def downloadPUMSData(self, filetype):
        web_stabb = self.project.stateAbb[self.state]
        filename = self.loc + os.path.sep + 'csv_%s%s.zip' %(filetype, web_stabb)

        try:
            os.makedirs(self.loc)
        except WindowsError, e:
            print e


        try:
            
            open(filename)
            reply = QMessageBox.question(None, "Import",
                                         QString("""Cannot download data when the data already exists.\n\n"""
                                                 """Would you like to keep the existing files?"""
                                                 """\nSelect No if you would like to download the files again."""),
                                         QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.No:
                confirm = QMessageBox.question(None, "Import",
                                               QString("""Would you like to continue?"""),
                                               QMessageBox.Yes|QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    self.retrieveAndStorePUMS(filetype)
        except IOError, e:
            self.retrieveAndStorePUMS(filetype)

        self.extractPUMS(filetype)    



    def retrieveAndStorePUMS(self, filetype):
        web_stabb = self.project.stateAbb[self.state]
        
        if filetype == 'H':
            h_download_location = self.loc + os.path.sep + 'csv_h%s.zip' %(web_stabb)
            urllib.urlretrieve("""http://www2.census.gov/acs2007_3yr/pums/csv_h%s.zip""" %(web_stabb),
                               h_download_location)
        else:
            p_download_location = self.loc + os.path.sep + 'csv_p%s.zip' %(web_stabb)
            urllib.urlretrieve("""http://www2.census.gov/acs2007_3yr/pums/csv_p%s.zip""" %(web_stabb),
                               p_download_location)

    def extractPUMS(self, filetype):
        web_stabb = self.project.stateAbb[self.state]
        
        if filetype == 'H':
            hfile = UnzipFile(self.loc, "csv_h%s.zip" %(web_stabb))
            hfile.unzip()
        else:
            pfile = UnzipFile(self.loc, "csv_p%s.zip" %(web_stabb))
            pfile.unzip()        


    def housingVarDicts(self):
        # Reading the list of PUMS housing variable names
        if not self.query.exec_("""select variablename, description from """
                                """pumsACSvariablelist where type = 'H'"""):
            raise FileError, self.query.lastError().text()
        else:
            self.housingVariableDict = {}
            while (self.query.next()):
                self.housingVariableDict['%s'%self.query.value(0).toString()] = '%s'%self.query.value(1).toString()

    def housingDefVar(self):
        # Reading the list of PUMS default housing variable names
        if not self.query.exec_("""select variablename from pumsACSvariablelist where type = 'H' and defaultvar = 1"""):
            raise FileError, self.query.lastError().text()
        else:
            self.housingDefaultVariables = []
            while (self.query.next()):
                self.housingDefaultVariables.append(self.query.value(0).toString())

        


    def personVarDicts(self):
        # Reading the list of PUMS person variable names
        if not self.query.exec_("""select variablename, description from """
                                """pumsACSvariablelist where type = 'P'"""):
            raise FileError, self.query.lastError().text()
        else:
            self.personVariableDict = {}
            while (self.query.next()):
                self.personVariableDict['%s'%self.query.value(0).toString()] = '%s'%self.query.value(1).toString()



    def personDefVar(self):
        # Reading the list of PUMS default person variable names
        if not self.query.exec_("""select variablename from pumsACSvariablelist where type = 'P' and defaultvar = 1"""):
            raise FileError, self.query.lastError().text()
        else:
            self.personDefaultVariables = []
            while (self.query.next()):
                self.personDefaultVariables.append(self.query.value(0).toString())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    vars = {'a':'first', 'b':'second', 'c':'third', 'd':'fourth'}
    defvars = ['a','b']
    dlg = VariableSelectionDialog(vars, defvars)
    dlg.exec_()
