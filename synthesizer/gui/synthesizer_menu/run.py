# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

import datetime, time, numpy, re, sys
import copy
import MySQLdb
import pp
import cPickle as pickle

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSql import *

from database.createDBConnection import createDBC
from synthesizer_algorithm.prepare_data import prepare_data
from synthesizer_algorithm.prepare_data_noper import prepare_data_noper
from synthesizer_algorithm.prepare_data_nogqs import prepare_data_nogqs
from synthesizer_algorithm.prepare_data_nogqs_noper import prepare_data_nogqs_noper
from synthesizer_algorithm.drawing_households import person_index_matrix
import synthesizer_algorithm.demo as demo
import synthesizer_algorithm.demo_nogqs as demo_nogqs
import synthesizer_algorithm.demo_noper as demo_noper
import synthesizer_algorithm.demo_nogqs_noper as demo_nogqs_noper

import synthesizer_algorithm.demo_parallel as demo_parallel
import synthesizer_algorithm.demo_parallel_nogqs as demo_parallel_nogqs
import synthesizer_algorithm.demo_parallel_noper as demo_parallel_noper
import synthesizer_algorithm.demo_parallel_nogqs_noper as demo_parallel_nogqs_noper


import synthesizer_algorithm.demo_parallel as demo_parallel
import synthesizer_algorithm.demo_parallel_nogqs as demo_parallel_nogqs
from gui.file_menu.newproject import Geography
from gui.misc.widgets import VariableSelectionDialog, ListWidget
from gui.misc.errors  import *

class RunDialog(QDialog):

    def __init__(self, project, jobserver, parent=None):

        self.job_server = jobserver
        super(RunDialog, self).__init__(parent)

        self.setWindowTitle("Run Synthesizer")
        self.setWindowIcon(QIcon("./images/run.png"))
        self.setMinimumSize(800,500)

        self.project = project

        scenarioDatabase = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)
        self.projectDBC = createDBC(self.project.db, self.project.name)
        self.projectDBC.dbc.open()

        self.gqAnalyzed = self.isGqAnalyzed()

        self.runGeoIds = []

        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)



        selGeographiesLabel = QLabel("Selected Geographies")
        self.selGeographiesList = ListWidget()
        outputLabel = QLabel("Output Window")
        self.outputWindow = QTextEdit()
        self.selGeographiesButton = QPushButton("Select Geographies")
        self.runSynthesizerButton = QPushButton("Run Synthesizer")
        self.runSynthesizerButton.setEnabled(False)

        runWarning = QLabel("""<font color = blue>Note: Select geographies by clicking on the <b>Select Geographies</b> button """
                            """and then click on <b>Run Synthesizer</b> to start synthesizing population.</font>""")
        runWarning.setWordWrap(True)

        vLayout1 = QVBoxLayout()
        vLayout1.addWidget(self.selGeographiesButton)
        vLayout1.addWidget(selGeographiesLabel)
        vLayout1.addWidget(self.selGeographiesList)

        vLayout2 = QVBoxLayout()
        vLayout2.addWidget(self.runSynthesizerButton)
        vLayout2.addWidget(outputLabel)
        vLayout2.addWidget(self.outputWindow)

        hLayout = QHBoxLayout()
        hLayout.addLayout(vLayout1)
        hLayout.addLayout(vLayout2)

        vLayout3 = QVBoxLayout()
        vLayout3.addLayout(hLayout)
        vLayout3.addWidget(runWarning)
        vLayout3.addWidget(self.dialogButtonBox)


        self.setLayout(vLayout3)

        self.connect(self.selGeographiesButton, SIGNAL("clicked()"), self.selGeographies)
        self.connect(self.runSynthesizerButton, SIGNAL("clicked()"), self.runSynthesizer)
        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), self, SLOT("reject()"))


    def accept(self):
        self.projectDBC.dbc.close()

        QDialog.accept(self)

    def reject(self):
        self.projectDBC.dbc.close()
        QDialog.accept(self)


    def variableControlCorrDict(self, vardict):
        varCorrDict = {}
        vars = vardict.keys()
        for i in vars:
            for j in vardict[i].keys():
                cat = (('%s' %j).split())[-1]
                varCorrDict['%s%s' %(i, cat)] = '%s' %vardict[i][j]
        return varCorrDict

    def runSynthesizer(self):

        date = datetime.date.today()
        ti = time.localtime()

        self.outputWindow.append("Project Name - %s" %(self.project.name))
        self.outputWindow.append("Population Synthesized at %s:%s:%s on %s" %(ti[3], ti[4], ti[5], date))

        if self.gqAnalyzed and self.project.selVariableDicts.persControl:
            preprocessDataTables = ['sparse_matrix_99999', 'index_matrix_99999', 'housing_synthetic_data', 'person_synthetic_data',
                                    'performance_statistics', 'hhld_0_joint_dist', 'gq_0_joint_dist', 'person_0_joint_dist']
        if self.gqAnalyzed and not self.project.selVariableDicts.persControl:
            preprocessDataTables = ['sparse_matrix_99999', 'index_matrix_99999', 'housing_synthetic_data', 'person_synthetic_data',
                                    'performance_statistics', 'hhld_0_joint_dist', 'gq_0_joint_dist']
        if not self.gqAnalyzed and self.project.selVariableDicts.persControl:
            preprocessDataTables = ['sparse_matrix_99999', 'index_matrix_99999', 'housing_synthetic_data', 'person_synthetic_data',
                                    'performance_statistics', 'hhld_0_joint_dist', 'person_0_joint_dist']            
        if not self.gqAnalyzed and not self.project.selVariableDicts.persControl:
            preprocessDataTables = ['sparse_matrix_99999', 'index_matrix_99999', 'housing_synthetic_data', 'person_synthetic_data',
                                    'performance_statistics', 'hhld_0_joint_dist']            

        databaseName = self.project.name + 'scenario' + str(self.project.scenario)
        self.projectDBC.dbc.setDatabaseName(databaseName)
        self.projectDBC.dbc.open()
        
        query = QSqlQuery(self.projectDBC.dbc)
        if not query.exec_("""show tables"""):
            raise FileError, self.query.lastError().text()

        
        varCorrDict = {}

        hhldDict = copy.deepcopy(self.project.selVariableDicts.hhld)

        if self.project.selVariableDicts.hhldMargsModify:
            for i in hhldDict.keys():
                for j in hhldDict[i].keys():
                    hhldDict[i][j] = 'mod' + hhldDict[i][j]

                                
        varCorrDict.update(self.variableControlCorrDict(hhldDict))
        if self.gqAnalyzed:
            varCorrDict.update(self.variableControlCorrDict(self.project.selVariableDicts.gq))
        varCorrDict.update(self.variableControlCorrDict(self.project.selVariableDicts.person))


        projectTables = []
        missingTables = []
        missingTablesString = ""
        while query.next():
            projectTables.append('%s' %(query.value(0).toString()))

        for i in preprocessDataTables:
            try:
                projectTables.index(i)
            except:
                missingTablesString = missingTablesString + ', ' + i
                missingTables.append(i)

        self.projectDBC.dbc.setDatabaseName(self.project.name)
        self.projectDBC.dbc.open()

        if len(missingTables) > 0:
            QMessageBox.warning(self, "Prepare Data", "The program will now prepare the data for population synthesis." )
            self.prepareData()
        # For now implement it without checking for each individual table that is created in this step
        # in a later implementation check for each table before you proceed with the creation of that particular table
        else:
            reply = QMessageBox.warning(self, "Prepare Data", """Would you like to prepare the data? """
                                        """Run this step if the control variables or their categories have changed.""",
                                        QMessageBox.Yes| QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.prepareData()
        

#    def randomText(self):
        self.readData()

        if len(self.runGeoIds) > 0:
            
            if self.job_server.get_ncpus() > 1:
                reply = QMessageBox.question(self, "Run Synthesizer", """Would you like to run the synthesizer in parallel """
                                             """to take advantage of multiple cores on your processor?""", QMessageBox.Yes| QMessageBox.No| QMessageBox.Cancel)

            else:
                reply = QMessageBox.No

            if reply <> QMessageBox.Cancel:
                
                scenarioDatabase = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)
                for i in self.runGeoIds:
                    ti = time.time()
                    if not query.exec_("""delete from %s.housing_synthetic_data where state = %s and county = %s """
                                       """ and tract = %s and bg = %s  """ 
                                       %(scenarioDatabase, i[0], i[1], i[3], i[4])):
                        raise FileError, query.lastError().text()
                    
                    if not query.exec_("""delete from %s.person_synthetic_data where state = %s and county = %s """
                                       """ and tract = %s and bg = %s  """ 
                                       %(scenarioDatabase, i[0], i[1], i[3], i[4])):
                        raise FileError, query.lastError().text()
                    a = self.project.synGeoIds.pop(i, -99)


            if reply == QMessageBox.Yes:
                print '------------------------------------------------------------------'
                print 'Generating synthetic population in Parallel...'


                dbList = ['%s' %self.project.db.hostname, '%s' %self.project.db.username, '%s' %self.project.db.password, '%s' %self.project.name]
                # breaking down the whole list into lists of 100 geographies each

                from math import floor

                geoCount = len(self.runGeoIds)
                binsize = 50

                bins = int(floor(geoCount/binsize))



            
                index = [((i+1)*binsize, (i+1)*binsize+binsize) for i in range(bins-1)]
                
                if bins > 0:
                    index.append((1, binsize))
                    index.append((bins*binsize, geoCount))

                else:
                    if geoCount > 1:
                        index.append((1, geoCount))

                geo = self.runGeoIds[0]

                geo = Geography(geo[0], geo[1], geo[3], geo[4], geo[2])
            
                #print 'unsorted', index

                index.sort()

                #print 'sorted', index

                # Synthesizing the first geography in serial to create the necessary tables
                
                try:
                    self.outputWindow.append("Running Syntheiss for geography State - %s, County - %s, Tract - %s, BG - %s"
                                             %(geo.state, geo.county, geo.tract, geo.bg))
                    if self.gqAnalyzed and self.project.selVariableDicts.persControl:
                        print 'GQ ANALYZED WITH PERSON ATTRIBUTES CONTROLLED'
                        demo.configure_and_run(self.project, geo, varCorrDict)
                    if self.gqAnalyzed and not self.project.selVariableDicts.persControl:
                        print 'GQ ANALYZED WITH NO PERSON ATTRIBUTES CONTROLLED'
                        demo_noper.configure_and_run(self.project, geo, varCorrDict)
                    if not self.gqAnalyzed and self.project.selVariableDicts.persControl:
                        print 'NO GQ ANALYZED WITH PERSON ATTRIBUTES CONTROLLED'
                        demo_nogqs.configure_and_run(self.project, geo, varCorrDict)
                    if not self.gqAnalyzed and not self.project.selVariableDicts.persControl:
                        print 'NO GQ ANALYZED WITH NO PERSON ATTRIBUTES CONTROLLED'
                        demo_nogqs_noper.configure_and_run(self.project, geo, varCorrDict)
                    self.project.synGeoIds[(geo.state, geo.county, geo.puma5, geo.tract, geo.bg)] = True                        
                except Exception, e:
                    self.outputWindow.append("\t- Error in the Synthesis for geography")
                    print ('Exception: %s' %e)

                # Synthesizing the population for all geographies in parallel after the first one is done in serial

                for i in index:
                    
                    if self.gqAnalyzed and self.project.selVariableDicts.persControl:
                        #print 'GQ ANALYZED WITH PERSON ATTRIBUTES CONTROLLED'
                        demo_parallel.run_parallel(self.job_server, self.project, self.runGeoIds[i[0]:i[1]], varCorrDict)
                    if self.gqAnalyzed and not self.project.selVariableDicts.persControl:
                        #print 'GQ ANALYZED WITH NO PERSON ATTRIBUTES CONTROLLED'
                        demo_parallel_noper.run_parallel(self.job_server, self.project, self.runGeoIds[i[0]:i[1]], varCorrDict)
                    if not self.gqAnalyzed and self.project.selVariableDicts.persControl:
                        #print 'NO GQ ANALYZED WITH PERSON ATTRIBUTES CONTROLLED'
                        demo_parallel_nogqs.run_parallel(self.job_server, self.project, self.runGeoIds[i[0]:i[1]], varCorrDict)
                    if not self.gqAnalyzed and not self.project.selVariableDicts.persControl:
                        #print 'NO GQ ANALYZED WITH NO PERSON ATTRIBUTES CONTROLLED'
                        demo_parallel_nogqs_noper.run_parallel(self.job_server, self.project, self.runGeoIds[i[0]:i[1]], varCorrDict)

                self.selGeographiesButton.setEnabled(False)
                for geo in self.runGeoIds[1:]:
                    self.project.synGeoIds[(geo[0], geo[1], geo[2], geo[3], geo[4])] = True

                    self.outputWindow.append("Running Syntheiss for geography State - %s, County - %s, Tract - %s, BG - %s"
                                             %(geo[0], geo[1], geo[3], geo[4]))

                print 'Completed generating synthetic population'
                print '------------------------------------------------------------------'

            elif reply == QMessageBox.No:
                print '------------------------------------------------------------------'
                print 'Generating synthetic population in Series...'

                for geo in self.runGeoIds:
                    self.project.synGeoIds[(geo[0], geo[1], geo[2], geo[3], geo[4])] = True

                    geo = Geography(geo[0], geo[1], geo[3], geo[4], geo[2])

                    self.outputWindow.append("Running Syntheiss for geography State - %s, County - %s, Tract - %s, BG - %s"
                                             %(geo.state, geo.county, geo.tract, geo.bg))

                    try:
                        if self.gqAnalyzed and self.project.selVariableDicts.persControl:
                            print 'GQ ANALYZED WITH PERSON ATTRIBUTES CONTROLLED'
                            demo.configure_and_run(self.project, geo, varCorrDict)
                        if self.gqAnalyzed and not self.project.selVariableDicts.persControl:
                            print 'GQ ANALYZED WITH NO PERSON ATTRIBUTES CONTROLLED'
                            demo_noper.configure_and_run(self.project, geo, varCorrDict)
                        if not self.gqAnalyzed and self.project.selVariableDicts.persControl:
                            print 'NO GQ ANALYZED WITH PERSON ATTRIBUTES CONTROLLED'
                            demo_nogqs.configure_and_run(self.project, geo, varCorrDict)
                        if not self.gqAnalyzed and not self.project.selVariableDicts.persControl:
                            print 'NO GQ ANALYZED WITH NO PERSON ATTRIBUTES CONTROLLED'
                            demo_nogqs_noper.configure_and_run(self.project, geo, varCorrDict)
                    except Exception, e:
                        self.outputWindow.append("\t- Error in the Synthesis for geography")
                        print ('Exception: %s' %e)

                self.selGeographiesButton.setEnabled(False)
            else:
                self.runGeoIds = []
                self.selGeographiesList.clear()

                print 'Completed generating synthetic population'
                print '------------------------------------------------------------------'

    def getPUMA5(self, geo):
        query = QSqlQuery(self.projectDBC.dbc)

        if not geo.puma5:
            if self.project.resolution == 'County':
                geo.puma5 = int('99999' + str(geo.county).rjust(3, '0'))

            elif self.project.resolution == 'Tract':
                if not query.exec_("""select pumano from geocorr where state = %s and county = %s and tract = %s and bg = 1"""
                                   %(geo.state, geo.county, geo.tract)):
                    raise FileError, query.lastError().text()
                while query.next():
                    geo.puma5 = query.value(0).toInt()[0]
            else:
                if not query.exec_("""select pumano from geocorr where state = %s and county = %s and tract = %s and bg = %s"""
                                   %(geo.state, geo.county, geo.tract, geo.bg)):
                    raise FileError, query.lastError().text()
                while query.next():
                    geo.puma5 = query.value(0).toInt()[0]

        return geo

    def selGeographies(self):
        self.runGeoIds=[]
        geoids = self.allGeographyids()
        dia = VariableSelectionDialog(geoids, title = "Select Geographies", icon = "run", warning = "Note: Select geographies to synthesize")
        if dia.exec_():
            exists = True
            notoall = False

            if dia.selectedVariableListWidget.count() > 0:
                self.selGeographiesList.clear()
                for i in range(dia.selectedVariableListWidget.count()):
                    itemText = dia.selectedVariableListWidget.item(i).text()

                    item = re.split("[,]", itemText)
                    state, county, tract, bg = item
                    geo = Geography(int(state), int(county), int(tract), int(bg))
                    geo = self.getPUMA5(geo)

                    try:

                        if not exists:
                            raise DummyError, 'skip messagebox'

                        self.project.synGeoIds[(geo.state, geo.county, geo.puma5, geo.tract, geo.bg)]

                        if not notoall:
                            reply = QMessageBox.warning(self, "Run Synthesizer", """Synthetic population for """
                                                        """<b>State - %s, County - %s, PUMA5 - %s, Tract - %s, BG - %s</b> exists. """
                                                        """Would you like to re-run the synthesizer for the geography(s)?"""
                                                        %(geo.state, geo.county, geo.puma5, geo.tract, geo.bg),
                                                        QMessageBox.Yes| QMessageBox.No| QMessageBox.YesToAll| QMessageBox.NoToAll)
                            if reply == QMessageBox.Yes:
                                self.runGeoIds.append((geo.state, geo.county, geo.puma5, geo.tract, geo.bg))
                                self.selGeographiesList.addItem(itemText)
                                exists = True
                            elif reply == QMessageBox.No:
                                exists = True
                            elif reply == QMessageBox.YesToAll:
                                self.runGeoIds.append((geo.state, geo.county, geo.puma5, geo.tract, geo.bg))
                                self.selGeographiesList.addItem(itemText)
                                exists = False
                            elif reply == QMessageBox.NoToAll:
                                notoall = True

                    except Exception, e:
                        #print e
                        self.runGeoIds.append((geo.state, geo.county, geo.puma5, geo.tract, geo.bg))
                        self.selGeographiesList.addItem(itemText)
                if self.selGeographiesList.count()>0:
                    self.runSynthesizerButton.setEnabled(True)
                else:
                    self.runSynthesizerButton.setEnabled(False)
            else:
                self.selGeographiesList.clear()
                self.runSynthesizerButton.setEnabled(False)


    def allGeographyids(self):
        query = QSqlQuery(self.projectDBC.dbc)
        allGeoids = {}
        for i in self.project.region.keys():
            countyName = i
            stateName = self.project.region[i]
            countyText = '%s,%s' %(countyName, stateName)
            countyCode = self.project.countyCode[countyText]
            stateCode = self.project.stateCode[stateName]

            

            if self.project.resolution == 'County':
                if not query.exec_("""select state, county from geocorr where state = %s and county = %s"""
                                   """ group by state, county"""
                                   %(stateCode, countyCode)):
                    raise FileError, query.lastError().text()
            elif self.project.resolution == 'Tract':
                if not query.exec_("""select state, county, tract from geocorr where state = %s and county = %s"""
                                   """ group by state, county, tract"""
                                   %(stateCode, countyCode)):
                    raise FileError, query.lastError().text()
            else:
                if not query.exec_("""select state, county, tract, bg from geocorr where state = %s and county = %s"""
                                   """ group by state, county, tract, bg"""
                                   %(stateCode, countyCode)):
                    raise FileError, query.lastError().text()
        #return a dictionary of all VALID geographies

            STATE, COUNTY, TRACT, BG = range(4)


            tract = 0
            bg = 0

            while query.next():
                state = query.value(STATE).toInt()[0]
                county = query.value(COUNTY).toInt()[0]

                if self.project.resolution == 'Tract' or self.project.resolution == 'Blockgroup' or self.project.resolution == 'TAZ':
                    tract = query.value(TRACT).toInt()[0]
                if self.project.resolution == 'Blockgroup' or self.project.resolution == 'TAZ':
                    bg = query.value(BG).toInt()[0]

                id = '%s,%s,%s,%s' %(state, county, tract, bg)
                idText = 'State - %s, County - %s, Tract - %s, Block Group - %s' %(state, county, tract, bg)

                allGeoids[id] = idText

        return allGeoids




    def prepareData(self):
        if self.project.selVariableDicts.hhldMargsModify:
            self.modifyMarginals()
        
        self.removeTables()
        self.project.synGeoIds = {}
        
        db = MySQLdb.connect(user = '%s' %self.project.db.username,
                             passwd = '%s' %self.project.db.password,
                             db = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario))

        try:
            if self.gqAnalyzed and self.project.selVariableDicts.persControl:
                prepare_data(db, self.project)
            if self.gqAnalyzed and not self.project.selVariableDicts.persControl:
                prepare_data_noper(db, self.project)
            if not self.gqAnalyzed and self.project.selVariableDicts.persControl:
                prepare_data_nogqs(db, self.project)
            if not self.gqAnalyzed and not self.project.selVariableDicts.persControl:
                prepare_data_nogqs_noper(db, self.project)
                pass
        except KeyError, e:
        
            QMessageBox.warning(self, "Run Synthesizer", QString("""Check the <b>hhid, serialno</b> columns in the """
                                                                 """data. If you wish not to synthesize groupquarters, make"""
                                                                 """ sure that you delete all person records corresponding """
                                                                 """to groupquarters. In PopGen, when Census data is used, """
                                                                 """by default groupquarters need"""
                                                                 """ to be synthesized because person marginals include """
                                                                 """individuals living in households and groupquarters. Fix the data"""
                                                                 """ and run synthesizer again."""), 
                                QMessageBox.Ok)
            
            self.dialogButtonBox.emit(SIGNAL("accepted()"))
        db.commit()
        db.close()
                                                         


    def addTotalColumn(self, vars, tablename, varname):
        #refPersName = self.project.selVariableDicts.refPersName
        #vars = self.project.sleVariableDicts.person['%s' %refPersName].values()

        varString = ''
        for i in vars:
            varString = varString + i + '+'
        varString = varString[:-1]

        databaseName = self.project.name
        self.projectDBC.dbc.setDatabaseName(databaseName)
        self.projectDBC.dbc.open()        
            
        query = QSqlQuery(self.projectDBC.dbc)

        if not query.exec_("alter table %s add index(state, county, tract, bg)" %tablename):
            raise FileError, query.lastError().text()

        if not query.exec_("alter table %s add column %s bigint" %(tablename, varname)):
            print "FileError: %s" %query.lastError().text()
            
        if not query.exec_("update %s set %s = %s" %(tablename, varname, varString)):
            raise FileError, query.lastError().text()        

    def createModHhldTable(self):
        databaseName = self.project.name
        self.projectDBC.dbc.setDatabaseName(databaseName)
        self.projectDBC.dbc.open()        
            
        query = QSqlQuery(self.projectDBC.dbc)        

        if not query.exec_("drop table hhld_marginals_modp"):
            print "FileError: %s" %query.lastError().text()

        if not query.exec_("drop table hhld_marginals_modpgq"):
            print "FileError: %s" %query.lastError().text()

        if not query.exec_("""create table hhld_marginals_modp select hhld_marginals.*, persontotal from hhld_marginals"""
                           """ left join person_marginals using(state, county, tract, bg)"""):
            raise FileError, query.lastError().text()
        
        if self.gqAnalyzed:
            if not query.exec_("""create table hhld_marginals_modpgq select hhld_marginals_modp.*, gqtotal from hhld_marginals_modp"""
                               """ left join gq_marginals using(state, county, tract, bg)"""):
                raise FileError, query.lastError().text()
        else:
            if not query.exec_("""create table hhld_marginals_modpgq select * from hhld_marginals_modp"""):
                raise FileError, query.lastError().text()
            
            if not query.exec_("""alter table hhld_marginals_modpgq add column gqtotal bigint default 0"""):
                raise FileError, query.lastError().text()


    def createHhldVarProportions(self):
        databaseName = self.project.name
        self.projectDBC.dbc.setDatabaseName(databaseName)
        self.projectDBC.dbc.open()        
            
        query = QSqlQuery(self.projectDBC.dbc)

        #calculating the proportions

        for i in self.project.selVariableDicts.hhld.keys():
            sumString = ''
            for j in self.project.selVariableDicts.hhld[i].values():
                sumString = sumString + j + '+'
            sumString = sumString[:-1]

            for j in self.project.selVariableDicts.hhld[i].values():
                if not query.exec_("""alter table hhld_marginals_modpgq add column p%s float(27)""" %j):
                    print "FileError: %s" %query.lastError().text()

                if not query.exec_("""update hhld_marginals_modpgq set p%s = %s/(%s)""" %(j, j, sumString)):
                    raise FileError, query.lastError().text()

    def calcExtraHhldsToSyn(self):
        databaseName = self.project.name
        self.projectDBC.dbc.setDatabaseName(databaseName)
        self.projectDBC.dbc.open()        
            
        query = QSqlQuery(self.projectDBC.dbc)

        # Calculating the number of extra households to be synthesizsed
        # PEQP = Person Equivalent Proportions
        # PEQ = Person Equivalents
        # PSUM = Proportions Sum
        hhldsizeVarName = self.project.selVariableDicts.hhldSizeVarName
        vars = self.project.selVariableDicts.hhld['%s' %hhldsizeVarName].values()
        vars.sort()

        hhldsizePEQPString = ''
        hhldsizePEQString = ''
        hhldsizePSumString = ''
        size = 1
        for i in vars[:-1]:
            hhldsizePEQPString = hhldsizePEQPString + 'p' + i + '*%s+' %size
            hhldsizePEQString = hhldsizePEQString + i + '*%s+' %size
            hhldsizePSumString = hhldsizePSumString + 'p' + i + '+'
            size = size + 1
        hhldsizePEQPString = hhldsizePEQPString[:-1]
        hhldSize = self.project.selVariableDicts.aveHhldSizeLastCat
        hhldsizePEQString = hhldsizePEQString + vars[-1]+'*%s' %hhldSize
        #print 'hhldsizemod string after - ', hhldsizePEQString + vars[-1]+'*%s' %hhldSize

        # this is a makeshift change to modify the marginals distributions
        print hhldsizePEQPString
        hhldsizePEQPString = hhldsizePEQPString + '+ p' + vars[-1] +'*%s' %hhldSize
        print hhldsizePEQPString


        hhldsizePSumString = hhldsizePSumString[:-1]

        # Creating person equivalents column
        if not query.exec_("""alter table hhld_marginals_modpgq add column perseq bigint"""):
            print "FileError: %s" %query.lastError().text()

        if not query.exec_("""update hhld_marginals_modpgq set perseq = %s + gqtotal""" %(hhldsizePEQString)):
            raise FileError, query.lastError().text()

        # Creating person total deficiency
        if not query.exec_("""alter table hhld_marginals_modpgq add column perstotdef bigint"""):
            print "FileError: %s" %query.lastError().text()

        if not query.exec_("""update hhld_marginals_modpgq set perstotdef = persontotal - perseq"""):
            raise FileError, query.lastError().text()
        
        # Creating the number of deficient household equivalents
        if not query.exec_("""alter table hhld_marginals_modpgq add column hhldeqdef float(27)"""):
            print "FileError: %s" %query.lastError().text()

        if not query.exec_("""update hhld_marginals_modpgq set hhldeqdef = perstotdef/(%s)""" %hhldsizePEQPString):
            raise FileError, query.lastError().text()

        #print 'PEQ string', hhldsizePEQString            
        #print 'PEQP String', hhldsizePEQPString
        #print 'PSUM String', hhldsizePSumString


    def calcModifiedMarginals(self):
        databaseName = self.project.name
        self.projectDBC.dbc.setDatabaseName(databaseName)
        self.projectDBC.dbc.open()        
            
        query = QSqlQuery(self.projectDBC.dbc)

        #calculating the proportions

        #print self.project.selVariableDicts.hhld.keys()

        hhldsizeVar = self.project.selVariableDicts.hhldSizeVarName
        hhldSizeCats = self.project.selVariableDicts.hhld['%s'%hhldsizeVar].keys()

        numCats = len(hhldSizeCats)

        #print self.project.selVariableDicts.hhld


        lastCatKey = hhldsizeVar + ', Category %s'%numCats
        
        lastCatMarg = self.project.selVariableDicts.hhld['%s'%hhldsizeVar]['%s'%lastCatKey]

        for i in self.project.selVariableDicts.hhld.keys():
            sumString = ''
            for j in self.project.selVariableDicts.hhld[i].values():
                sumString = sumString + j + '+'
            sumString = sumString[:-1]

            for j in self.project.selVariableDicts.hhld[i].values():
                #print ("""alter table hhld_marginals_modpgq add column mod%s float(27)""" %j)
                if not query.exec_("""alter table hhld_marginals_modpgq add column mod%s float(27)""" %j):
                    print "FileError: %s" %query.lastError().text()

                # this is a makeshift change to modify the marginals distributions                   
                #if j == lastCatMarg and i == hhldsizeVar:
                #    #print 'last category marginal found'
                #    print ("""update hhld_marginals_modpgq set mod%s = %s """ %(j, j))
                #    if not query.exec_("""update hhld_marginals_modpgq set mod%s = %s """ %(j, j)):
                #        raise FileError, query.lastError().text()        
                #else:
                #    print ("""update hhld_marginals_modpgq set mod%s = %s + p%s * hhldeqdef""" %(j, j, j))
                #    if not query.exec_("""update hhld_marginals_modpgq set mod%s = %s + p%s * hhldeqdef""" %(j, j, j)):
                #        raise FileError, query.lastError().text()        

                #print ("""update hhld_marginals_modpgq set mod%s = %s + p%s * hhldeqdef""" %(j, j, j))
                if not query.exec_("""update hhld_marginals_modpgq set mod%s = %s + p%s * hhldeqdef""" %(j, j, j)):
                    raise FileError, query.lastError().text()        

    def modifyMarginals(self):
        databaseName = self.project.name
        self.projectDBC.dbc.setDatabaseName(databaseName)
        self.projectDBC.dbc.open()        
            
        query = QSqlQuery(self.projectDBC.dbc)


        # Calculating the Person Total
        refPersName = self.project.selVariableDicts.refPersName
        vars = self.project.selVariableDicts.person['%s' %refPersName].values()

        self.addTotalColumn(vars, 'person_marginals', 'persontotal')

        # Calculating the groupquarter Total
        if self.gqAnalyzed:
            refGQName = self.project.selVariableDicts.gq.keys()[0]
            vars = self.project.selVariableDicts.gq['%s' %refGQName].values()
            self.addTotalColumn(vars, 'gq_marginals', 'gqtotal')
        
        # Calculating the household total
        refHhldName = self.project.selVariableDicts.hhldSizeVarName
        vars = self.project.selVariableDicts.hhld['%s' %refHhldName].values()

        self.addTotalColumn(vars, 'hhld_marginals', 'hhldtotal')

        
        # Create the new modified hhld marginals table
        self.createModHhldTable()
        
        # Create hhld variable proportions
        self.createHhldVarProportions()
        
        # Create the number of deficient households
        self.calcExtraHhldsToSyn()

        self.calcModifiedMarginals()

    def removeTables(self):
        databaseName = self.project.name + 'scenario' + str(self.project.scenario)
        self.projectDBC.dbc.setDatabaseName(databaseName)
        self.projectDBC.dbc.open()

        tables = self.tableList()
        query = QSqlQuery(self.projectDBC.dbc)
        for i in tables:
            if not query.exec_("""drop table %s""" %i):
                print "Warning: %s" %query.lastError().text()


        self.projectDBC.dbc.setDatabaseName(self.project.name)
        self.projectDBC.dbc.open()

    def tableList(self):
        tables = []

        query = QSqlQuery(self.projectDBC.dbc)
        if not query.exec_("""show tables"""):
            raise FileError, query.lastError.text()
        while query.next():
            tables.append('%s' %query.value(0).toString())
            
        return tables


    def isGqAnalyzed(self):
        if not self.project.gqVars:
            return False

        if self.project.sampleUserProv.userProv == False and self.project.controlUserProv.userProv == False:
            return True

        if self.project.sampleUserProv.userProv == True and self.project.sampleUserProv.gqLocation <> "":
            return True

        if self.project.controlUserProv.userProv == True and self.project.controlUserProv.gqLocation <> "":
            return True


        return False



    def readData(self):
        db = MySQLdb.connect(user = '%s' %self.project.db.username,
                             passwd = '%s' %self.project.db.password,
                             db = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario))
        dbc = db.cursor()

        #dbc.execute("""select * from index_matrix_%s""" %(0))
        #indexMatrix = numpy.asarray(dbc.fetchall())

        #f = open('indexMatrix_0.pkl', 'wb')
        #pickle.dump(indexMatrix, f)
        #f.close()


        dbc.execute("""select * from index_matrix_%s""" %(99999))
        indexMatrix = numpy.asarray(dbc.fetchall())

        f = open('indexMatrix_99999.pkl', 'wb')
        pickle.dump(indexMatrix, f)
        f.close()

        pIndexMatrix = person_index_matrix(db)
        f = open('pIndexMatrix.pkl', 'wb')
        pickle.dump(pIndexMatrix, f)
        f.close()






        dbc.close()
        db.close()



    def checkIfTableExists(self, tablename):
        # 0 - some other error, 1 - overwrite error (table deleted)
        if not self.query.exec_("""create table %s (dummy text)""" %tablename):
            if self.query.lastError().number() == 1050:
                reply = QMessageBox.question(None, "Processing Data",
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




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    a = '10'
    dia = RunDialog(a)
    dia.show()

    app.exec_()
