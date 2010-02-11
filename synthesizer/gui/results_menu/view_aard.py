# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from coreplot import *

class Absreldiff(Matplot):
    def __init__(self, project, parent=None):
        Matplot.__init__(self)
        self.project = project
        self.valid = False
        if self.isValid():
            self.valid = True
            self.setWindowTitle("Average Absolute Relative Difference Distribution")
            self.setWindowIcon(QIcon("./images/region.png"))
            aardWarning = QLabel("""<font color = blue>Note: The above chart shows the distribution of the """
                                 """Average Absolute Relative Difference (AARD)"""
                                 """ across all geographies for which a synthetic population was generated. """
                                 """ The AARD measure gives the average deviation of the person weighted sums """
                                 """with respect to composite person type constraints. """
                                 """The measure is used to monitor convergence in the Iterative Proportional Updating (IPU)"""
                                 """ algorithm of PopGen. </font>""")

            aardWarning.setWordWrap(True)
            self.vbox.addWidget(self.canvas)
            self.vbox.addWidget(aardWarning)
            self.vbox.addWidget(self.dialogButtonBox)
            self.setLayout(self.vbox)
            self.on_draw()
        else:
            QMessageBox.warning(self, "Results", "A table with name - performance_statistics does not exist.", QMessageBox.Ok)

    def isValid(self):
        return self.checkIfTableExists("performance_statistics")

    def on_draw(self):
        """ Redraws the figure
        """
        self.err = []
        if self.retrieveResults():

            # clear the axes and redraw the plot anew
            self.axes.clear()
            self.axes.grid(True)

            #self.axes.hist(err, range=(1,10), normed=True, cumulative=False, histtype='bar', align='mid', orientation='vertical', log=False)
            self.axes.hist(self.err , normed=False, align='left', bins=10)
            self.axes.set_xlabel("Average Absolute Relative Differences")
            self.axes.set_ylabel("Frequency")
            self.axes.set_xlim(xmin=0)
            self.canvas.draw()

    def retrieveResults(self):
        scenarioDatabase = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)
        projectDBC = createDBC(self.project.db, scenarioDatabase)
        projectDBC.dbc.open()

        # Get aard-values from performance statistics
        performancetable = "performance_statistics"
        aardvalvar = "aardvalue"
        filter = ""
        group = ""
        query = self.executeSelectQuery(projectDBC.dbc,aardvalvar, performancetable, filter, group)

        if query:
            while query.next():
                aardval = query.value(0).toDouble()[0]
                self.err.append(aardval)
            projectDBC.dbc.close()
            return True
        else:
            projectDBC.dbc.close()
            return False


def main():
    app = QApplication(sys.argv)
    QgsApplication.setPrefixPath(qgis_prefix, True)
    QgsApplication.initQgis()
#    res.show()
#    app.exec_()
    QgsApplication.exitQgis()

if __name__ == "__main__":
    main()

