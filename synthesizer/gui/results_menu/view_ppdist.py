# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from gui.misc.errors import *
import numpy as np

from coreplot import *

class Ppdist(Matplot):
    def __init__(self, project, parent=None):
        Matplot.__init__(self)
        self.setFixedSize(800,600)
        self.project = project
        self.valid = False
        self.variables = self.project.selVariableDicts.person.keys()

        if self.isValid():
            self.valid = True
            scenarioDatabase = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)            
            self.projectDBC = createDBC(self.project.db, scenarioDatabase)
            self.projectDBC.dbc.open()
            self.variables.sort()
            #self.dimensions = [len(project.selVariableDicts.person[i].keys()) for i in self.variables]

            self.setWindowTitle("Distribution of Person Variables")
            self.setWindowIcon(QIcon("./images/region.png"))
            ppdistWarning = QLabel("""<font color = blue>Note: The above chart compares the actual marginal distributions with """
                                   """ marginal distributions from the synthetic population for the person"""
                                   """ variables of interest. </font>""")
            ppdistWarning.setWordWrap(True)
            self.enableindgeo = True
            self.makeComboBox()
            self.vbox.addWidget(self.comboboxholder)
            self.vbox.addWidget(self.canvas)
            self.vbox.addWidget(ppdistWarning)
            self.vbox.addWidget(self.dialogButtonBox)
            self.setLayout(self.vbox)

            self.makeTempTables()
            self.on_draw()
            self.connect(self.attrbox, SIGNAL("currSelChanged"), self.on_draw)
            self.connect(self.geobox, SIGNAL("currSelChanged"), self.on_draw)
        else:
            QMessageBox.warning(self, "Results", """If you have supplied a person marginals table, """
                                """and wish to compare person distributions irrespective of whether """
                                """you controlled for person variables or not, """
                                """make sure that the correspondence between person variable """
                                """categories and the columns in the person marginals table are defined. """
                                """If you have not supplied or if the person marginals table is missing """
                                """then this option cannot be used.""", QMessageBox.Ok)
            self.projectDBC.dbc.close()

    def isValid(self):
        return (self.checkIfTableExists("person_synthetic_data") and 
                self.checkIfTableExists("person_marginals") and 
                len(self.variables) > 0)

    def accept(self):
        query = QSqlQuery(self.projectDBC.dbc)
        if not query.exec_("""drop table temp"""):
            raise FileError, query.lastError().text()

        self.projectDBC.dbc.close()
        QDialog.reject(self)

    def reject(self):
        self.accept()

    def makeTempTables(self):
        varstr = ""
        for i in self.variables:
            varstr = varstr + i + ','
        varstr = varstr[:-1]

        query = QSqlQuery(self.projectDBC.dbc)
        query.exec_(""" DROP TABLE IF EXISTS temp""")
        if not query.exec_("""CREATE TABLE temp SELECT person_synthetic_data.*,%s FROM person_synthetic_data"""
            """ LEFT JOIN person_sample using (serialno,pnum)""" %(varstr)):
            raise FileError, query.lastError().text()

    def on_draw(self):
        """ Redraws the figure
        """
        self.current = '%s' %self.attrbox.getCurrentText()
        selgeog = '%s' %self.geobox.getCurrentText()
        self.categories = self.project.selVariableDicts.person[self.current].keys()
        seladjdict = self.project.adjControlsDicts.person
        
        selsorteddict = {}
        for i in self.categories:
            catsplit = i.split()
            newkey = int(catsplit[len(catsplit)-1])
            selsorteddict[newkey] = self.project.selVariableDicts.person[self.current][i]
        self.categories = selsorteddict.keys()        
        self.categories.sort()
        #self.corrControlVariables =  self.project.selVariableDicts.person[self.current].values()

        filterAct = ""
        #self.countyCodes = []
        #for i in self.project.region.keys():
            #code = self.project.countyCode['%s,%s' % (i, self.project.state)]
            #self.countyCodes.append(code)
            #filterAct = filterAct + "county = %s or " %code
        #filterAct = filterAct[:-3]
        if selgeog == 'All':
            table = "person_synthetic_data"
            variable = "county,tract,bg"
            queryAct = self.executeSelectQuery(self.projectDBC.dbc,variable, table, "",variable)
            i=0
            while queryAct.next():
                filstr = self.getGeogFilStr(queryAct.value(0).toInt()[0],queryAct.value(1).toInt()[0],queryAct.value(2).toInt()[0])
                if i == 0:
                    filterAct = "(" + filterAct + filstr + ")"
                    i = 1
                else:
                    filterAct = filterAct + " or " + "(" + filstr + ")"
        else:
            geosplit = selgeog.split(',')
            filterAct = "county=%s and tract=%s and bg=%s" %(geosplit[1],geosplit[2],geosplit[3])

        actTotal = []
        estTotal = []
        self.catlabels = []
        tableAct = "person_marginals"
        for i in self.categories:
            variable = selsorteddict[i]
            self.catlabels.append(variable)
            variableAct = "sum(%s)" %variable
            try:
                sumdiff = 0
                if selgeog != 'All':
                    adjlist = seladjdict[selgeog][self.current][1]
                    actTotal.append(adjlist[i-1])
                else:
                    for j in seladjdict.keys():
                        try:
                            actlist = seladjdict[j][self.current][0]
                            adjlist = seladjdict[j][self.current][1]
                            sumdiff = sumdiff + adjlist[i-1] - actlist[i-1]
                        except:
                            pass
                    raise FileError, "Overrides"
            except:
                queryAct = self.executeSelectQuery(self.projectDBC.dbc,variableAct, tableAct, filterAct)
                while queryAct.next():
                    value = queryAct.value(0).toInt()[0]
                    value = value + sumdiff
                    actTotal.append(value)

            tableEst = "temp"
            filterEst = self.current + " = %s" % i
            if selgeog != 'All':
                filterEst = filterEst + ' and ' + filterAct
            variableEst = "sum(frequency)"
            queryEst = self.executeSelectQuery(self.projectDBC.dbc,variableEst, tableEst, filterEst)

            iteration = 0
            while queryEst.next():
                value = queryEst.value(0).toInt()[0]
                estTotal.append(value)
                iteration = 1
            if iteration == 0:
                estTotal.append(0)

        # clear the axes and redraw the plot anew
        self.axes.clear()
        self.axes.grid(True)

        N=len(actTotal)
        ind = np.arange(N)
        width = 0.35

        rects1 = self.axes.bar(ind, actTotal, width, color='r')
        rects2 = self.axes.bar(ind+width, estTotal, width, color='y')
        self.axes.set_xlabel("Person Variables")
        self.axes.set_ylabel("Frequency")
        self.axes.set_xticks(ind+width)
        # generic labels should be created
        if len(self.catlabels) >=10:
            self.axes.set_xticklabels(self.catlabels, size='xx-small')
        elif (len(self.catlabels[0]) >= 8 and len(self.catlabels) >=5):
            self.axes.set_xticklabels(self.catlabels, size='x-small')
        else:
            self.axes.set_xticklabels(self.catlabels)
        self.axes.legend((rects1[0], rects2[0]), ('Actual', 'Synthetic'))
        self.canvas.draw()

    def makeComboBox(self):
        self.comboboxholder = QWidget()
        self.hbox = QHBoxLayout()
        self.comboboxholder.setLayout(self.hbox)
        self.attrbox = LabComboBox("Variable:",self.variables)
        self.getGeographies()
        self.geolist.sort()
        self.geobox = LabComboBox("Geography:",["All"] + self.geolist)
        self.hbox.addWidget(self.attrbox)
        if self.enableindgeo:
            self.hbox.addWidget(self.geobox)
        self.hbox.addWidget(QWidget())
        self.hbox.addWidget(QWidget())

    def getGeogFilStr(self,county,tract,bg):
        if self.project.resolution == "County":
            str = "county=%s" %(county)
        if self.project.resolution == "Tract":
            str = "county=%s and tract=%s" %(county,tract)
        if self.project.resolution == "Blockgroup" or self.project.resolution == "TAZ" :
            str = "county=%s and tract=%s and bg=%s" %(county,tract,bg)
        return str

def main():
    app = QApplication(sys.argv)
    QgsApplication.setPrefixPath(qgis_prefix, True)
    QgsApplication.initQgis()
#    res.show()
#    app.exec_()
    QgsApplication.exitQgis()

if __name__ == "__main__":
    main()

