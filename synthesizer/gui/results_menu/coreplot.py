# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

"""
This demo demonstrates how to embed a matplotlib (mpl) plot
into a PyQt4 GUI application, including:

* Using the navigation toolbar
* Adding data to the plot
* Dynamically modifying the plot's properties
* Processing mpl events
* Saving the plot to a file from a menu

The main goal is to serve as a basis for developing rich PyQt GUI
applications featuring mpl plots (using the mpl OO API).

Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 19.01.2009
"""
import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from misc.errors import FileError
from database.createDBConnection import createDBC

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure


class Matplot(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setMinimumSize(QSize(800,500))
        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.project = None
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        # Since we have only one plot, we can use add_axes
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)

        self.vbox = QVBoxLayout()

        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok)

        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self, SLOT("accept()"))


    def isValid(self):
        pass

    def on_draw(self):
        pass

    def create_action(  self, text, slot=None, shortcut=None,
                        icon=None, tip=None, checkable=False,
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def executeSelectQuery(self, dbc, vars, tablename, filter="", group =""):
        if self.checkIfTableExists(tablename):
            query = QSqlQuery(dbc)
            if filter != "" and group != "":
                if not query.exec_("""SELECT %s FROM %s WHERE %s GROUP BY %s"""%(vars,tablename,filter,group)):
                    raise FileError, query.lastError().text()
            elif filter != "" and group == "":
                if not query.exec_("""SELECT %s FROM %s WHERE %s"""%(vars,tablename,filter)):
                    raise FileError, query.lastError().text()
            elif filter == "" and group != "":
                if not query.exec_("""SELECT %s FROM %s GROUP BY %s"""%(vars,tablename,group)):
                    raise FileError, query.lastError().text()
            else:
                if not query.exec_("""SELECT %s FROM %s"""%(vars,tablename)):
                    raise FileError, query.lastError().text()
            return query
        else:
            QMessageBox.warning(self, "Results", "A table with name - %s does not exist." %(tablename), QMessageBox.Ok)
            return False



    def checkIfTableExists(self, tablename):
        tables = self.tableList()

        try:
            tables.index(tablename)
        except:
            return False
        return True


    def tableList(self):
        scenarioDatabase = '%s%s%s' %(self.project.name, 'scenario', self.project.scenario)        
        self.projectDBC = createDBC(self.project.db, scenarioDatabase)
        self.projectDBC.dbc.open()
        self.query = QSqlQuery(self.projectDBC.dbc)

        tables = []

        if not self.query.exec_("""show tables"""):
            raise FileError, self.query.lastError.text()
        while self.query.next():
            tables.append('%s' %self.query.value(0).toString())
        return tables

    def getGeographies(self):
        self.geolist = []
        for geo in self.project.synGeoIds.keys():
            geostr = str(geo[0]) + "," + str(geo[1]) + "," + str(geo[3]) + "," + str(geo[4])
            self.geolist.append(geostr)

class LabComboBox(QWidget):
    def __init__(self, label, list, parent=None):
        QDialog.__init__(self, parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(label)
        self.combobox = QComboBox()
        self.list = list
        self.combobox.addItems(self.list)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combobox)
        self.connect(self.combobox, SIGNAL("currentIndexChanged(const QString&)"), self.emitSignal)
        self.label.setFixedWidth(70)
        self.setFixedWidth(300)

    def emitSignal(self):
        self.emit(SIGNAL("currSelChanged"))

    def getCurrentText(self):
        return self.combobox.currentText()

    def setCurrentText(self,txt):
        self.combobox.setCurrentIndex(self.list.index(txt))

def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
