# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from __future__ import with_statement

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from database.createDBConnection import createDBC
from misc.errors import FileError
from misc.widgets import VariableSelectionDialog

import pickle, os


class OpenProject(QFileDialog):
    def __init__(self, parent=None):
        super(OpenProject, self).__init__(parent)
        self.file = self.getOpenFileName(parent, "Browse to select file", "/home",
                                         "PopGen File (*.pop)")



class SaveFile(QFileDialog):
    def __init__(self, project, fileType, tablename=None, treeParent=None, parent=None):
        super(SaveFile, self).__init__(parent)
        self.project = project
        self.fileType = fileType
        self.tablename = tablename
        self.treeParent = treeParent
        if self.fileType == 'csv':
            self.fileSep = ','
        elif self.fileType == 'dat':
            self.fileSep = '\t'
        self.folder = self.getExistingDirectory(self, QString("""Select a folder for storing the files. """
                                                              """Note that two files are exported for every data table: """
                                                              """a data file containing the data in the format chosen and a """
                                                              """metadata file which gives a list of the column names"""),
                                                "%s/%s" %(self.project.location, self.project.filename),
                                                QFileDialog.ShowDirsOnly)

        if not self.folder.isEmpty():
            if not self.tablename:
                self.save()
            else:
                self.saveSelectedTable()

    def saveSummaryStats(self):
        pass


    def save(self):
        scenarioDatabase = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)
        projectDBC = createDBC(self.project.db, scenarioDatabase)
        projectDBC.dbc.open()

        query = QSqlQuery(projectDBC.dbc)

        filename = '%s/housing_synthetic_data.%s' %(self.folder, self.fileType)
        check = self.checkIfFileExists(filename)
        if check == 0:
            os.remove(filename)
        if check < 2:
            hhldVariablesDict, hhldVariables = self.getVariables('hhld_sample', query)
            hhldVariablesDict = self.deleteDictEntries(hhldVariablesDict)
            hhldSelVariables = self.getSelectedVariables(hhldVariablesDict, self.project.hhldVars, 
                                                         "Select Household Variables to Add to Synthetic Data")
            hhldvarstr = ","
            if hhldSelVariables is not None:
                for  i in hhldSelVariables:
                    hhldvarstr = hhldvarstr + '%s,' %i
                hhldvarstr = hhldvarstr[:-1]
            else:
                hhldvarstr = ""
                QMessageBox.warning(self, "Export Synthetic Population Tables", 
                                    """No household variables selected for exporting""", QMessageBox.Ok)                
            
            if not query.exec_("""drop table temphou1"""):
                print "FileError:%s" %query.lastError().text()
            if not query.exec_("""create table temphou1 select housing_synthetic_data.* %s from housing_synthetic_data"""
                               """ left join hhld_sample using (serialno)""" %(hhldvarstr)):
                raise FileError, query.lastError().text()
            if not query.exec_("""alter table temphou1 drop column hhuniqueid"""):
                raise FileError, query.lastError().text()
            if not query.exec_("""alter table temphou1 add index(serialno)"""):
                raise FileError, query.lastError().text()


            if self.project.gqVars:
                gqVariablesDict, gqVariables = self.getVariables('gq_sample', query)
                gqVariablesDict = self.deleteDictEntries(gqVariablesDict)
                gqSelVariables = self.getSelectedVariables(gqVariablesDict, self.project.gqVars, 
                                                         "Select Groupquarter Variables to Add to Synthetic Data")
                gqvarstr = ","
                if gqSelVariables is not None:
                    for  i in gqSelVariables:
                        gqvarstr = gqvarstr + '%s,' %i
                    gqvarstr = gqvarstr[:-1]
                else:
                    gqvarstr = ""
                    QMessageBox.warning(self, "Export Synthetic Population Tables", 
                                        """No groupquarter variables selected for exporting""", QMessageBox.Ok)          
                  
                if not query.exec_("""drop table temphou2"""):
                    print "FileError:%s" %query.lastError().text()
                if not query.exec_("""create table temphou2 select temphou1.* %s from temphou1"""
                                   """ left join gq_sample using (serialno)""" %(gqvarstr)):
                    raise FileError, query.lastError().text()
            else:
                if not query.exec_("""alter table temphou1 rename to temphou2"""):
                    raise FileError, query.lastError().text()                

            if self.project.sampleUserProv.defSource == "ACS 2005-2007":
                #print 'ACS HOUSING DATA MODIFYING THE SERIALNOS'
                if not query.exec_("""drop table temphou3"""):
                    print "FileError:%s" %query.lastError().text()
                if not query.exec_("""alter table temphou2 drop column serialno"""):
                    raise FileError, query.lastError().text()
                if not query.exec_("""alter table temphou2 add index(hhid)"""):
                    raise FileError, query.lastError().text()
                if not query.exec_("""alter table serialcorr add index(hhid)"""):
                    raise FileError, query.lastError().text()
                if not query.exec_("""create table temphou3 select temphou2.*, serialno from temphou2"""
                                   """ left join serialcorr using (hhid)"""):
                    raise FileError, query.lastError().text()

                if not query.exec_("""select * from temphou3 into outfile """
                                   """'%s/housing_synthetic_data.%s' fields terminated by '%s'"""
                                   %(self.folder, self.fileType, self.fileSep)):
                    raise FileError, query.lastError().text()

                housingSynTableVarDict, housingSynTableVars = self.getVariables('temphou3', query)

                if not query.exec_("""drop table temphou3"""):
                    print "FileError:%s" %query.lastError().text()

            else:
                if not query.exec_("""select * from temphou2 into outfile """
                                   """'%s/housing_synthetic_data.%s' fields terminated by '%s'"""
                                   %(self.folder, self.fileType, self.fileSep)):
                    raise FileError, query.lastError().text()

                housingSynTableVarDict, housingSynTableVars = self.getVariables('temphou2', query)
            
            self.storeMetaData(housingSynTableVars, self.folder, 'housing_synthetic_data')
            
            if not query.exec_("""drop table temphou1"""):
                print "FileError:%s" %query.lastError().text()

            if not self.project.gqVars:
                if not query.exec_("""drop table temphou2"""):
                    print "FileError:%s" %query.lastError().text()


        filename = '%s/person_synthetic_data.%s' %(self.folder, self.fileType)
        check = self.checkIfFileExists(filename)
        if check == 0:
            os.remove(filename)
        if check  < 2:
            personVariablesDict, personVariables = self.getVariables('person_sample', query)
            personVariablesDict = self.deleteDictEntries(personVariablesDict)
            personSelVariables = self.getSelectedVariables(personVariablesDict, self.project.personVars, 
                                                           "Select Person Variables to Add to Synthetic Data")

            personvarstr = ","
            if personSelVariables is not None:
                for  i in personSelVariables:
                    personvarstr = personvarstr + '%s,' %i
                personvarstr = personvarstr[:-1]
            else:
                personvarstr = ""
                QMessageBox.warning(self, "Export Synthetic Population Tables", 
                                    """No person variables selected for exporting""", QMessageBox.Ok)                
            
            if not query.exec_("""drop table tempperson"""):
                print "FileError:%s" %query.lastError().text()
            if not query.exec_("""create table tempperson select person_synthetic_data.* %s from person_synthetic_data"""
                               """ left join person_sample using (serialno)""" %(personvarstr)):
                raise FileError, query.lastError().text()
            if not query.exec_("""alter table tempperson drop column personuniqueid"""):
                raise FileError, query.lastError().text()

            

            if self.project.sampleUserProv.defSource == "ACS 2005-2007":
                #print 'ACS PERSON DATA MODIFYING THE SERIALNOS'
                if not query.exec_("""drop table tempperson1"""):
                    print "FileError:%s" %query.lastError().text()
                if not query.exec_("""alter table tempperson drop column serialno"""):
                    raise FileError, query.lastError().text()
                if not query.exec_("""alter table tempperson add index(hhid)"""):
                    raise FileError, query.lastError().text()
                if not query.exec_("""create table tempperson1 select tempperson.*, serialno from tempperson"""
                                   """ left join serialcorr using (hhid)"""):
                    raise FileError, query.lastError().text()

                if not query.exec_("""select * from tempperson1 into outfile """
                                   """'%s/person_synthetic_data.%s' fields terminated by '%s'"""
                                   %(self.folder, self.fileType, self.fileSep)):
                    raise FileError, query.lastError().text()

                personSynTableVarDict, personSynTableVars = self.getVariables('tempperson1', query)


                #if not query.exec_("""drop table tempperson1"""):
                #    print "FileError:%s" %query.lastError().text()
            else:
                if not query.exec_("""select * from tempperson into outfile """
                                   """'%s/person_synthetic_data.%s' fields terminated by '%s'"""
                                   %(self.folder, self.fileType, self.fileSep)):
                    raise FileError, query.lastError().text()


                personSynTableVarDict, personSynTableVars = self.getVariables('tempperson', query)
            
            self.storeMetaData(personSynTableVars, self.folder, 'person_synthetic_data')

            #if not query.exec_("""drop table tempperson"""):
            #    print "FileError:%s" %query.lastError().text()


        projectDBC.dbc.close()

    def deleteDictEntries(self, dict):
        vars = ['state', 'pumano', 'hhid', 'serialno', 'pnum', 'hhlduniqueid', 'gquniqueid', 'personuniqueid']
        for i in vars:
            try:
                dict.pop(i)
            except:
                pass
        return dict


    def storeMetaData(self, varNames, location, tablename):
        f = open('%s/%s_meta.txt' %(location, tablename), 'w')
        col = 1
        for i in varNames:
            f.write('column %s -  %s\n' %(col, i))
            col = col + 1
        f.close()


    def getVariables(self, tablename, query):
        if not query.exec_("""desc %s""" %(tablename)):
            raise FileError, query.lastError().text()
        
        varDict = {}
        varNameList = []
        while query.next():
            varname = query.value(0).toString()
            varDict['%s' %varname] = ""
            varNameList.append(varname)
            
        return varDict, varNameList
        
    
    def getSelectedVariables(self, varDict, defaultVariables, title, icon=None, warning=None):
        selDia = VariableSelectionDialog(varDict, defaultVariables, title, icon, warning)

        selVariables = []
        if selDia.exec_():
            selVarCount = selDia.selectedVariableListWidget.count()
            if selVarCount > 0:
                for i in range(selVarCount):
                    selVariables.append(selDia.selectedVariableListWidget.item(i).text())
            return selVariables
            




    def saveSelectedTable(self):
        if self.treeParent == "Project Tables":
            database = self.project.name
        if self.treeParent == "Scenario Tables":
            database = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)

        projectDBC = createDBC(self.project.db, database)
        projectDBC.dbc.open()

        query = QSqlQuery(projectDBC.dbc)


        filename = '%s/%s.%s' %(self.folder, self.tablename, self.fileType)
        check = self.checkIfFileExists(filename)
        if check == 0:
            os.remove(filename)

        if check < 2:
            if not query.exec_("""select * from %s into outfile """
                               """'%s' fields terminated by '%s'"""
                               %(self.tablename, filename, self.fileSep)):
                raise FileError, query.lastError().text()

        tableVarDict, tableVars = self.getVariables(self.tablename, query)
        self.storeMetaData(tableVars, self.folder, self.tablename)

        projectDBC.dbc.close()


    def checkIfFileExists(self, file):
        try:
            fileInfo = os.stat(file)

            reply = QMessageBox.question(None, "Import",
                                         QString("""File %s exists. Would you like to overwrite?""" %(file)),
                                         QMessageBox.Yes| QMessageBox.No)

            if reply == QMessageBox.Yes:
                return 0
            else:
                return 2
        except WindowsError, e:
            #print 'Warning: File - %s not present' %(file)
            return 1




class ExportSummaryFile(SaveFile):
    def __init__(self, project, fileType, tablename=None, treeParent=None, parent=None):
        SaveFile.__init__(self, project, fileType, tablename=None, treeParent=None, parent=None)
        


    def save(self):
        scenarioDatabase = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)
        projectDBC = createDBC(self.project.db, scenarioDatabase)
        projectDBC.dbc.open()

        query = QSqlQuery(projectDBC.dbc)

        filename = '%s/summary.%s' %(self.folder, self.fileType)
        check = self.checkIfFileExists(filename)
        if check == 0:
            os.remove(filename)
        if check < 2:
            self.createSummaryTables(query, 'housing')
            self.createSummaryTables(query, 'person')

            """
            print self.project.selVariableDicts

            varCorrDict = {}
            varCorrDict.update(self.variableControlCorrDict(self.project.selVariableDicts.hhld))
            varCorrDict.update(self.variableControlCorrDict(self.project.selVariableDicts.gq))

            self.createControlVarTotals()


            varCorrDict.update(self.variableControlCorrDict(self.project.selVariableDicts.person))
            
            print varCorrDict
                
            """

            varCorrDict = {}
            varCorrDict.update(self.variableControlCorrDict(self.project.selVariableDicts.hhld))
            varCorrDict.update(self.variableControlCorrDict(self.project.selVariableDicts.gq))

            self.createHousingMarginalsTable(query, varCorrDict.values())

            varCorrDict = self.variableControlCorrDict(self.project.selVariableDicts.person)

            self.createMarginalsTable(query, varCorrDict.values())

            self.createGivenControlTotalColumns(query, self.project.selVariableDicts.hhld)
            self.createGivenControlTotalColumns(query, self.project.selVariableDicts.gq)
            self.createGivenControlTotalColumns(query, self.project.selVariableDicts.person)

            self.createMarginalsSummaryTable(query)
        
            if not query.exec_("""select * from comparison into outfile """
                               """'%s' fields terminated by '%s'""" %(filename, self.fileSep)):
                raise FileError, query.lastError().text()

            summaryTableVarDict, summaryTableVars = self.getVariables('comparison', query)
            self.storeMetaData(summaryTableVars, self.folder, 'summary')



    def createSummaryTables(self, query, synthesisType):
        
        if not query.exec_("""drop table %s_summary """%(synthesisType)):
            print "FileError:%s" %query.lastError().text()            

        if not query.exec_("""create table %s_summary """
                           """select state, county, tract, bg, sum(frequency) as %s_syn_sum from %s_synthetic_data """
                           """group by state, county, tract, bg""" %(synthesisType, synthesisType, synthesisType)):
            raise FileError, query.lastError().text()


    def createHousingMarginalsTable(self, query, housingVars):
        dummy = ''
        for i in housingVars:
            dummy = dummy + i + ','
        dummy = dummy[:-1]

        if not query.exec_("""drop table housing_marginals"""):
            print "FileError: %s" %query.lastError().text()            


        if not query.exec_("""alter table hhld_marginals add index(state, county, tract, bg)"""):
            raise FileError, query.lastError().text()

        if not query.exec_("""alter table gq_marginals add index(state, county, tract, bg)"""):
            raise FileError, query.lastError().text()


        if not query.exec_("""create table housing_marginals select state, county, tract, bg, %s """
                           """ from hhld_marginals left join gq_marginals using(state, county, tract, bg)"""
                           %dummy):
            raise FileError, query.lastError().text()


    def createMarginalsTable(self, query, persVars):
        dummy = ''
        for i in persVars:
            dummy = dummy + i + ','
        dummy = dummy[:-1]

        if not query.exec_("""drop table marginals"""):
            print "FileError: %s" %query.lastError().text()

        if not query.exec_("""alter table housing_marginals add index(state, county, tract, bg)"""):
            raise FileError, query.lastError().text()

        if not query.exec_("""alter table person_marginals add index(state, county, tract, bg)"""):
            raise FileError, query.lastError().text()


        if not query.exec_("""create table marginals select housing_marginals.*, %s """
                           """ from housing_marginals left join person_marginals using(state, county, tract, bg)"""
                           %dummy):
            raise FileError, query.lastError().text()

    def createMarginalsSummaryTable(self, query):
        if not query.exec_("""alter table marginals add index(state, county, tract, bg)"""):
            raise FileError, query.lastError().text()

        if not query.exec_("""alter table housing_summary add index(state, county, tract, bg)"""):
            raise FileError, query.lastError().text()

        if not query.exec_("""alter table person_summary add index(state, county, tract, bg)"""):
            raise FileError, query.lastError().text()

        if not query.exec_("""drop table summary"""):
            print "FileError: %s" %query.lastError().text()

        if not query.exec_("""drop table comparison"""):
            print "FileError: %s" %query.lastError().text()

        if not query.exec_("""create table summary select housing_summary.*, person_syn_sum """
                           """ from housing_summary left join person_summary using(state, county,tract, bg)"""):
            raise FileError, query.lastError().text()        

        if not query.exec_("""create table comparison select marginals.*, housing_syn_sum, person_syn_sum """
                           """ from marginals left join summary using(state, county,tract, bg)"""):
            raise FileError, query.lastError().text()


        
    def variableControlCorrDict(self, vardict):
        varCorrDict = {}
        vars = vardict.keys()
        for i in vars:
            for j in vardict[i].keys():
                cat = (('%s' %j).split())[-1]
                varCorrDict['%s%s' %(i, cat)] = '%s' %vardict[i][j]
        return varCorrDict

    def createGivenControlTotalColumns(self, query, varDict):
        for i in varDict.keys():
            if not query.exec_("""alter table marginals add column %s_act_sum bigint"""
                               %(i)):
                print "FileError: %s" %query.lastError().text()

            updateString = ''
            for j in varDict[i].keys():
                updateString = updateString + varDict[i][j] + "+"
            updateString = updateString[:-1]
                
            if not query.exec_("""update marginals set %s_act_sum = %s"""
                               %(i, updateString)):
                raise FileError, query.lastError().text()


            for j in varDict[i].keys():
                if not query.exec_("""alter table marginals drop %s"""
                                   %(varDict[i][j])):
                    raise FileError, query.lastError().text()
                


