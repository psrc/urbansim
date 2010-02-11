# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

import urllib
import os
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from database.createDBConnection import createDBC
from misc.errors import FileError
from misc.utils import UnzipFile
from import_data import ImportUserProvData, FileProperties

from global_vars import *


class UserImportControlData():
    def __init__(self, project):
        self.project = project
        self.projectDBC = createDBC(self.project.db, self.project.name)
        self.projectDBC.dbc.open()
        self.query = QSqlQuery(self.projectDBC.dbc)


    def createHhldTable(self):
        check = self.checkIfTableExists('hhld_marginals')

        if check:
            hhldTableQuery = self.mysqlQueries('hhld_marginals', self.project.controlUserProv.hhLocation)

            if not self.query.exec_(hhldTableQuery.query1):
                raise FileError, self.query.lastError().text()

            if not self.query.exec_(hhldTableQuery.query2):
                raise FileError, self.query.lastError().text()

    def createGQTable(self):
        check = self.checkIfTableExists('gq_marginals')

        if check:
            gqLocLen = len(self.project.controlUserProv.gqLocation)

            if gqLocLen > 1:
                gqTableQuery = self.mysqlQueries('gq_marginals', self.project.controlUserProv.gqLocation)

                if not self.query.exec_(gqTableQuery.query1):
                    raise FileError, self.query.lastError().text()

                if not self.query.exec_(gqTableQuery.query2):
                    raise FileError, self.query.lastError().text()

    def createPersonTable(self):
        check = self.checkIfTableExists('person_marginals')

        if check:
            personTableQuery = self.mysqlQueries('person_marginals', self.project.controlUserProv.personLocation)

            if not self.query.exec_(personTableQuery.query1):
                raise FileError, self.query.lastError().text()

            if not self.query.exec_(personTableQuery.query2):
                raise FileError, self.query.lastError().text()


    def mysqlQueries(self, name, filePath):
        # Generate the mysql queries to import the tables
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

class AutoImportSF2000Data():
    def __init__(self, project):
        self.project = project
        self.state = self.project.state
        self.stateAbb = self.project.stateAbb
        self.stateCode = self.project.stateCode

        self.loc = DATA_DOWNLOAD_LOCATION + os.path.sep + self.state + os.path.sep + 'SF2000'
        self.loc = os.path.realpath(self.loc)

        self.countiesSelected = self.project.region.keys()

        self.projectDBC = createDBC(self.project.db, self.project.name)
        self.projectDBC.dbc.open()

        self.query = QSqlQuery(self.projectDBC.dbc)

        self.rawSF = RAW_SUMMARY2000_FILES

        self.rawSFNamesNoExt = RAW_SUMMARY2000_FILES_NOEXT

        #self.downloadSFData()
        #self.createRawSFTable()
        #self.createMasterSFTable()
        #self.createMasterSubSFTable()

    def downloadSFData(self):
        try:
            os.makedirs(self.loc)
            self.retrieveAndStoreSF(self.state)
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
                    self.retrieveAndStoreSF(self.state)
        self.extractSF(self.state)


    def retrieveAndStoreSF(self, state):
        web_state = '%s' %state
        web_state = web_state.replace(' ', '_')
        for i in self.rawSF:
            sf_loc = self.loc + os.path.sep + '%s%s' %(self.stateAbb[state], i)
            urllib.urlretrieve("""http://www2.census.gov/census_2000/"""
                               """datasets/Summary_File_3/%s/%s%s""" %(web_state, self.stateAbb[state], i),
                               sf_loc)

    def extractSF(self, state):
        for i in self.rawSF:
            file = UnzipFile(self.loc, "%s%s" %(self.stateAbb[state],i))
            file.unzip()

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


    def createRawSFTable(self):
        # Create raw SF tables which can then be used to create the required summary file tables for use
        # population synthesis

        # First create the state geo table


        if self.checkIfTableExists('sf3filestablescorr'):
            sf3FilesTablesCorrTable = ImportUserProvData("sf3filestablescorr",
                                                         "./data/sf3filestablescorr.csv",
                                                         [], [], True, True)
            if not self.query.exec_(sf3FilesTablesCorrTable.query1):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_(sf3FilesTablesCorrTable.query2):
                raise FileError, self.query.lastError().text()

        tablename = '%sgeo' %(self.stateAbb[self.state])

        if self.checkIfTableExists(tablename):

            if not self.query.exec_("""create table %s (raw text, sumlev float, geocomp float, sfgeoid float, """
                                    """state float, county float, tract  float, bg float, logrecno float)"""
                                    %tablename):
                raise FileError, self.query.lastError().text()

            geo_loc = os.path.join(self.loc, '%s.uf3'%tablename)
            geo_loc = geo_loc.replace("\\", "/")


            if not self.query.exec_("""load data local infile '%s'"""
                                    """ into table %sgeo (raw)""" %(geo_loc, self.stateAbb[self.state])):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set sumlev = mid(raw, 9, 3)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set geocomp = mid(raw, 12, 2)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set sfgeoid = mid(raw, 19, 7)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set state = mid(raw, 30, 2)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set county = mid(raw, 32, 3)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set tract = mid(raw, 56, 6)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set bg = mid(raw, 62, 1)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set logrecno = mid(raw, 19, 7)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""alter table %sgeo modify logrecno int""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""alter table %sgeo add primary key (logrecno)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()

        # Load the other necessary tables

        for j in self.rawSFNamesNoExt[1:]:
            variables, variabletypes = self.variableNames(j)
            filename = "%s%s" %(self.stateAbb[self.state], j)
            sf_loc = os.path.join(self.loc, '%s.uf3' %(filename))
            sffile = ImportUserProvData(filename,
                                        sf_loc,
                                        variables, variabletypes, False, False)
            if self.checkIfTableExists(filename):

                if not self.query.exec_(sffile.query1):
                    raise FileError, self.query.lastError().text()
                if not self.query.exec_(sffile.query2):
                    raise FileError, self.query.lastError().text()
                if not self.query.exec_("alter table %s add primary key (logrecno)" %filename):
                    raise FileError, self.query.lastError().text()



    def variableNames(self, filenumber=None, tablenumber=None):
        import copy
        variables = copy.deepcopy(RAW_SUMMARY2000_FILES_COMMON_VARS)
        variabletypes = copy.deepcopy(RAW_SUMMARY2000_FILES_COMMON_VARS_TYPE)

        filenumber = str(filenumber).rjust(5, '0')

        if tablenumber is None and filenumber is not None:
            if not self.query.exec_("""select tabletype, tablenumber, numcat from sf3filestablescorr"""
                                    """ where filenumber = %s order by tablenumber""" %filenumber):
                raise FileError, self.query.lastError().text()
        if tablenumber is not None:
            if not self.query.exec_("""select tabletype, tablenumber, numcat from sf3filestablescorr"""
                                    """ where filenumber = %s and includeflag = 1""" %filenumber):
                raise FileError, self.query.lastError().text()
        if filenumber is None and tablenumber is None:
            raise FileError, "Insufficient parameters supplied"


        while self.query.next():
            tabletype = self.query.value(0).toString()
            tablenumber = str(self.query.value(1).toInt()[0]).rjust(3, '0')
            numcat = self.query.value(2).toInt()[0]
 
            #print 'tables', tablenumber, numcat
            
            for i in range(numcat):
                colname = '%s'%tabletype + tablenumber + str(i+1).rjust(3, '0')
                variables.append(colname)
                variabletypes.append('bigint')
                #print colname

        #print len(variables), len(variabletypes)

        return variables, variabletypes


    def createMasterSFTable(self):
        import copy
        var1 = copy.deepcopy(MASTER_SUMMARY_FILE_VARS)
        if self.project.controlUserProv.defSource <> 'Census 2000':
            var1.remove('geocomp')
        var1string = self.createVariableString(var1)

        var1.remove('logrecno')
        var1.append('temp1.logrecno')

        if self.checkIfTableExists('mastersftable'):
            self.checkIfTableExists('temp1')
            self.checkIfTableExists('temp2')
            if not self.query.exec_("""create table temp1 select %s from %sgeo"""
                                    %(var1string, self.stateAbb[self.state])):
                raise FileError, self.query.lastError().text()

            for j in self.rawSFNamesNoExt[1:]:
                var2, var2types = self.variableNames('%s' %j, 1)
                var1 = var1 + var2[6:]
                
                var1string = self.createVariableString(var1)

                tablename = '%s%s' %(self.stateAbb[self.state], j)


                if not self.query.exec_("""create table temp2 select %s from temp1, %s"""
                                        """ where temp1.logrecno = %s.logrecno""" %(var1string, tablename, tablename)):
                    raise FileError, self.query.lastError().text()
                if not self.query.exec_("""drop table temp1"""):
                    raise FileError, self.query.lastError().text()
                if not self.query.exec_("""alter table temp2 rename to temp1"""):
                    raise FileError, self.query.lastError().text()

            if not self.query.exec_("""alter table temp1 rename to mastersftable"""):
                raise FileError, self.query.lastError().text()


    def createMasterSubSFTable(self):
        #Based on the resolution import a summary file table for only that resolution

        if self.checkIfTableExists('mastersftable%s' %self.project.resolution):
            #print self.project.resolution
            if self.project.resolution == 'Blockgroup':
                sumlev = 150
            if self.project.resolution == 'Tract':
                sumlev = 140
            if self.project.resolution == 'County':
                sumlev = 50
            if not self.query.exec_("""create table mastersftable%s """
                                    """select * from mastersftable where sumlev = %s and geocomp = 00"""
                                    %(self.project.resolution, sumlev)):
                raise FileError, self.query.lastError().text()




    def createVariableString(self, variableList):
        variableString = ""
        for i in variableList:
            variableString = variableString + i + ", "
        return variableString[:-2]


class AutoImportSFACSData(AutoImportSF2000Data):
    def __init__(self, project):
        AutoImportSF2000Data.__init__(self, project)
        self.project = project

        self.loc = DATA_DOWNLOAD_LOCATION + os.path.sep + self.state + os.path.sep + 'SFACS'
        self.loc = os.path.realpath(self.loc)
        
        self.rawSF = RAW_SUMMARYACS_FILES

        self.rawSFNamesNoExt = RAW_SUMMARYACS_FILES_NOEXT

    def retrieveAndStoreSF(self, state):
        web_state = '%s' %state
        web_state = web_state.replace(' ','')
        
        for i in self.rawSF:
            j = i %(self.stateAbb[self.state])
            sf_loc = self.loc + os.path.sep + j
            urllib.urlretrieve("""ftp://ftp2.census.gov/acs2005_2007_3yr/summaryfile/%s/%s"""
                               %(web_state, j), sf_loc)

    def extractSF(self, state):
        for i in self.rawSF[1:]:
            j = i %(self.stateAbb[self.state])
            file = UnzipFile(self.loc, j)
            file.unzip()

    def createRawSFTable(self):
        # Create raw SF tables which can then be used to create the required summary file tables for use
        # population synthesis

        # First create the state geo table


        if self.checkIfTableExists('sfacsfilestablescorr'):
            sfacsFilesTablesCorrTable = ImportUserProvData("sfacsfilestablescorr",
                                                         "./data/sfacsfilestablescorr.csv",
                                                         [], [], True, True)
            if not self.query.exec_(sfacsFilesTablesCorrTable.query1):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_(sfacsFilesTablesCorrTable.query2):
                raise FileError, self.query.lastError().text()

        tablename = '%sgeo' %(self.stateAbb[self.state])

        if self.checkIfTableExists(tablename):
            if not self.query.exec_("""create table %s (raw text, sumlev float, sfgeoid float, """
                                    """state float, county float, tract  float, bg float, logrecno float)"""
                                    %tablename):
                raise FileError, self.query.lastError().text()

            geo_loc = self.loc + os.path.sep + self.rawSF[0] %(self.stateAbb[self.state])
            geo_loc = geo_loc.replace("\\", "/")


            if not self.query.exec_("""load data local infile '%s'"""
                                    """ into table %sgeo (raw)""" %(geo_loc, self.stateAbb[self.state])):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set sumlev = mid(raw, 9, 3)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set sfgeoid = mid(raw, 12, 2)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set state = mid(raw, 26, 2)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set county = mid(raw, 28, 3)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set tract = mid(raw, 41, 6)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set bg = mid(raw, 47, 1)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""update %sgeo set logrecno = mid(raw, 14, 7)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""alter table %sgeo modify logrecno int""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()
            if not self.query.exec_("""alter table %sgeo add primary key (logrecno)""" %self.stateAbb[self.state]):
                raise FileError, self.query.lastError().text()

        # Load the other necessary tables

        for j in range(len(self.rawSFNamesNoExt[1:])):
            
            filenumber = self.rawSFNamesNoExt[j + 1]
            variables, variabletypes = self.variableNames(filenumber)
            tablename = "%s%s" %(self.stateAbb[self.state], filenumber)
            filename = ('e' + (self.rawSF[j+1]) %(self.stateAbb[self.state])).replace('zip', 'txt')
            
            sf_loc = (self.loc 
                      + os.path.sep + 'tab4' 
                      + os.path.sep + 'sumfile'
                      + os.path.sep + 'prod'
                      + os.path.sep + '2005thru2007'
                      + os.path.sep + 'data'
                      + os.path.sep + filename)

            sffile = ImportUserProvData(tablename,
                                        sf_loc,
                                        variables, variabletypes, False, False)


            if self.checkIfTableExists(tablename):
                if not self.query.exec_(sffile.query1):
                    raise FileError, self.query.lastError().text()
                if not self.query.exec_(sffile.query2):
                    raise FileError, self.query.lastError().text()
                if not self.query.exec_("alter table %s add primary key (logrecno)" %tablename):
                    raise FileError, self.query.lastError().text()
        
        
    def variableNames(self, filenumber=None, tablenumber=None):
        import copy
        variables = copy.deepcopy(RAW_SUMMARYACS_FILES_COMMON_VARS)
        variabletypes = copy.deepcopy(RAW_SUMMARYACS_FILES_COMMON_VARS_TYPE)

        if tablenumber is None and filenumber is not None:
            if not self.query.exec_("""select tablenumber, numcat from sfacsfilestablescorr"""
                                    """ where filenumber = %s order by tablenumber""" %filenumber):
                raise FileError, self.query.lastError().text()
        if tablenumber is not None:
            if not self.query.exec_("""select tablenumber, numcat from sfacsfilestablescorr"""
                                    """ where filenumber = %s and includeflag = 1""" %filenumber):
                raise FileError, self.query.lastError().text()
        if filenumber is None and tablenumber is None:
            raise FileError, "Insufficient parameters supplied"


        while self.query.next():
            tablenumber = str(self.query.value(0).toString()).ljust(9, '0')
            numcat = self.query.value(1).toInt()[0]

            for i in range(numcat):
                colname = tablenumber + str(i+1).rjust(3, '0')
                variables.append(colname)
                variabletypes.append('bigint')
                #print colname

        return variables, variabletypes


    def createMasterSubSFTable(self):
        #Based on the resolution import a summary file table for only that resolution

        if self.checkIfTableExists('mastersftable%s' %self.project.resolution):

            if self.project.resolution == 'County':
                sumlev = 50
                #print  'resolution is county and summayr level is --' ,  sumlev
                                
            if not self.query.exec_("""create table mastersftable%s """
                                    """select * from mastersftable where sumlev = %s """
                                    %(self.project.resolution, sumlev)):
                raise FileError, self.query.lastError().text()
