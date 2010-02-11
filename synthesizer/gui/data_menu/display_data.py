# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from misc.widgets import RecodeDialog
from file_menu.newproject import DBInfo
from database.createDBConnection import createDBC
from misc.widgets import *
from misc.errors import *

class DisplayTable(QDialog):
    def __init__(self, project, tablename, treeParent, parent=None):
        super(DisplayTable, self).__init__(parent)

        self.project = project

        if treeParent == 'Project Tables':
            databaseName = self.project.name
        else:
            databaseName = self.project.name + 'scenario' + str(self.project.scenario)

        self.projectDBC = createDBC(self.project.db, databaseName)
        self.projectDBC.dbc.open()

        self.tablename = tablename

        self.setWindowTitle("Data Table - %s" %self.tablename)
        self.setWindowIcon(QIcon("./images/modifydata.png"))


        self.variableTypeDictionary = {}

        self.populateVariableDictionary()

        self.model = QSqlTableModel(parent, self.projectDBC.dbc)
        self.model.setTable(self.tablename)
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setMinimumSize(QSize(800, 500))

        outputLabel = QLabel("Output")

        self.output = QTextEdit()
        self.output.setMinimumSize(QSize(800, 100))

        layoutView = QVBoxLayout()
        layoutView.addWidget(self.view)
        layoutView.addWidget(outputLabel)
        layoutView.addWidget(self.output)

        descButton = QPushButton("Descriptives")
        freqButton = QPushButton("Frequencies")

        layoutButton = QVBoxLayout()
        layoutButton.addWidget(descButton)
        layoutButton.addWidget(freqButton)
        layoutButton.addItem(QSpacerItem(10, 550))

        hLayout = QHBoxLayout()
        hLayout.addLayout(layoutView)
        hLayout.addLayout(layoutButton)



        buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)

        vLayout = QVBoxLayout()
        vLayout.addLayout(hLayout)
        vLayout.addWidget(buttonBox)

        self.setLayout(vLayout)

        self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(buttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))

        self.connect(descButton, SIGNAL("clicked()"), self.descriptives)
        self.connect(freqButton, SIGNAL("clicked()"), self.frequencies)


    def descriptives(self):
        descriptivesVarDialog = VariableSelectionDialog(self.variableTypeDictionary,
                                                        title = "Descriptives", icon = "modifydata")
        if descriptivesVarDialog.exec_():
            self.descriptivesVariablesSelected = descriptivesVarDialog.selectedVariableListWidget.variables


            COUNT, AVERAGE, MINIMUM, MAXIMUM, SUM = range(5)

            query = QSqlQuery(self.projectDBC.dbc)

            self.output.append("DESCRIPTIVES:")
            self.output.append("%s, %s, %s, %s, %s, %s" %('FIELD', 'COUNT', 'AVERAGE', 'MINIMUM', 'MAXIMUM', 'SUM'))

            for i in self.descriptivesVariablesSelected:

                if not query.exec_("""select count(%s), avg(%s), min(%s), max(%s), sum(%s) from %s"""
                               %(i, i, i, i, i, self.tablename)):
                    raise FileError, query.lastError().text()
                while query.next():
                    count = query.value(COUNT).toInt()[0]
                    average = query.value(AVERAGE).toDouble()[0]
                    minimum = query.value(MINIMUM).toDouble()[0]
                    maximum = query.value(MAXIMUM).toDouble()[0]
                    sum = query.value(SUM).toDouble()[0]
                self.output.append("%s, %d, %.4f, %.4f, %.4f, %.4f" %(i, count, average, minimum, maximum, sum))
            self.output.append("")


    def frequencies(self):
        frequenciesVarDialog = VariableSelectionDialog(self.variableTypeDictionary,
                                                        title = "Frequencies", icon = "modifydata")
        if frequenciesVarDialog.exec_():
            self.frequenciesVariablesSelected = frequenciesVarDialog.selectedVariableListWidget.variables

            CATEGORY, FREQUENCY = range(2)

            query = QSqlQuery(self.projectDBC.dbc)

            self.output.append("FREQUENCIES:")

            for i in self.frequenciesVariablesSelected:
                self.output.append("Variable Name - %s" %i)
                self.output.append("%s, %s" %('CATEGORY', 'FREQUENCY'))

                if not query.exec_("""select %s, count(*) from %s group by %s"""
                               %(i, self.tablename, i)):
                    raise FileError, query.lastError().text()
                while query.next():
                    category = query.value(CATEGORY).toString()
                    frequency = query.value(FREQUENCY).toInt()[0]
                    self.output.append("%s, %s" %(category, frequency))
                self.output.append("The %s variable has a total of %s categories" %(i, query.size()))
                self.output.append("")


    def populateVariableDictionary(self):
        query = QSqlQuery(self.projectDBC.dbc)
        query.exec_("""desc %s""" %self.tablename)

        FIELD, TYPE, NULL, KEY, DEFAULT, EXTRA = range(6)

        while query.next():
            field = query.value(FIELD).toString()
            type = query.value(TYPE).toString()
            null = query.value(NULL).toString()
            key = query.value(KEY).toString()
            default = query.value(DEFAULT).toString()
            extra = query.value(EXTRA).toString()

            self.variableTypeDictionary['%s' %field] = type


    def accept(self):
        self.projectDBC.dbc.close()
        QDialog.accept(self)

    def reject(self):
        self.projectDBC.dbc.close()
        QDialog.reject(self)


class DisplayTableStructure(QDialog):
    def __init__(self, tabledata, headers, title, text, parent=None):
        super(DisplayTableStructure, self).__init__(parent)

        self.setWindowTitle("%s" %title)
        self.setWindowIcon(QIcon("./images/structure.png"))

        # create table
        self.tabledata = tabledata
        self.headers = headers


        table = self.createTable()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(table)
        label = QLabel("<font color = blue>%s </font>" %text)
        label.setWordWrap(True)
        layout.addWidget(label)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))


    def accept(self):
        QDialog.accept(self)


    def createTable(self):
        # create the view
        tableview = QTableView()

        # set the table model
        tablemodel = MyTableModel(self.tabledata, self.headers, self)
        tableview.setModel(tablemodel)

        # set the minimum size
        tableview.setMinimumSize(800, 300)

        # hide vertical header
        vertheader = tableview.verticalHeader()
        vertheader.setVisible(False)

        # set column width to fit contents
        tableview.resizeColumnsToContents()

        # set row height
        nrows = len(self.tabledata)
        for row in xrange(nrows):
            tableview.setRowHeight(row, 18)

        return tableview

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

