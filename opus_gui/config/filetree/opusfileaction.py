# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 



# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opus_gui.run.script.opusrunscript import *
from opus_core.storage_factory import StorageFactory

#Jesse changes:
#from opus_core.datasets.dataset import Dataset
from opus_core.datasets.gui_dataset import GuiDataset

import sys
import operator

class CatchOutput(QTextBrowser):
    class Output:
        def __init__( self, writefunc ):
            self.writefunc = writefunc
        def write( self, line ):
            if line != "\n":
                map( self.writefunc, line.split("\n") )
        def flush( self ):
            pass
                
    def __init__( self,parent ):
        QTextBrowser.__init__( self, parent )
        self.output = CatchOutput.Output(self.writeResult)
        self.stdout = sys.stdout
        self.stderr = sys.stderr
    def writeResult( self, result ):
        if result == "":
            return
        self.append( result )
    def start(self):
        #print "Getting Start"
        #sys.stdout, sys.stderr = self.output, self.output
        sys.stdout = self.output
    def stop(self):
        #print "Getting Stop"
        #sys.stdout, sys.stderr = self.stdout, self.stderr
        sys.stdout = self.stdout

class OpusTableModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parent=None, *args): 
        QAbstractTableModel.__init__(self, parent, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
 
    def rowCount(self, parent): 
        return len(self.arraydata) 
        #return len(self.arraydata[0]) 
 
    def columnCount(self, parent): 
        return len(self.arraydata[0]) 
        #return len(self.arraydata) 
 
    def data(self, index, role): 
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        return QVariant(self.arraydata[index.row()][index.column()])
        #return QVariant(self.arraydata[index.column()][index.row()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        #self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))        
        orderList = range(len(self.headerdata))
        orderList.remove(Ncol)
        orderList.insert(0,Ncol)
        #print orderList
        self.arraydata.sort(key=operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))
        
class OpusFileAction(object):
    def __init__(self, parent):
        self.parent = parent
        self.xmlFileObject = parent

        self.currentColumn = None
        self.currentIndex = None
        self.classification = ""

        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.refreshIcon = QIcon(":/Images/Images/arrow_refresh.png")

        self.actRefresh = QAction(self.refreshIcon, "Refresh Tree",
                                  self.xmlFileObject.mainwindow)
        QObject.connect(self.actRefresh, SIGNAL("triggered()"),
                        self.refreshAction)

        self.actViewDataset = QAction(self.applicationIcon, "View Dataset",
                                      self.xmlFileObject.mainwindow)
        QObject.connect(self.actViewDataset, SIGNAL("triggered()"),
                        self.viewDatasetAction)
        
        self.actOpenTextFile = QAction(self.applicationIcon, "Open Text File",
                                       self.xmlFileObject.mainwindow)
        QObject.connect(self.actOpenTextFile, SIGNAL("triggered()"),
                        self.openTextFile)

        QObject.connect(self.xmlFileObject.treeview,
                        SIGNAL("customContextMenuRequested(const QPoint &)"),
                        self.processCustomMenu)

    def viewDatasetAction(self):
        print "viewDatasetAction"
        model = self.xmlFileObject.model
        dataset_name = str(model.fileName(self.currentIndex))
        dataset_name_full = str(model.filePath(self.currentIndex))
        parentIndex = model.parent(self.currentIndex)
        parent_name = str(model.fileName(parentIndex))
        parent_name_full = str(model.filePath(parentIndex))
        storage = StorageFactory().get_storage('flt_storage',
                                               storage_location=parent_name_full)
        columns = storage.get_column_names(dataset_name)
        
        #Jesse changes
        #data = Dataset(in_storage=storage,
        #               in_table_name=dataset_name,id_name=columns[0])
        data = GuiDataset(in_storage=storage,
                       in_table_name=dataset_name,id_name=columns[0])
        
        # Need to add a new tab to the main tabs for display of the data
        tabs = self.xmlFileObject.mainwindow.tabWidget
        container = QWidget()
        widgetLayout = QVBoxLayout(container)
        summaryGroupBox = QGroupBox(container)
        summaryGroupBox.setTitle(QString("Summary"))
        summaryGroupBoxLayout = QVBoxLayout(summaryGroupBox)
        # Add in the summary here
        
        #Jesse changes
        #textBrowser = CatchOutput(container)
        #textBrowser.start()
        #data.summary()
        #textBrowser.stop()
        #summaryGroupBoxLayout.addWidget(textBrowser)
        data_summary = data.summary()
        strng = QString(data_summary.getvalue())
        textBrowser = QTextBrowser()
        textBrowser.insertPlainText(strng)
        summaryGroupBoxLayout.addWidget(textBrowser)
        
        
        widgetLayout.addWidget(summaryGroupBox)

        tableGroupBox = QGroupBox(container)
        tableGroupBox.setTitle(QString("Table View"))
        tableGroupBoxLayout = QVBoxLayout(tableGroupBox)
        tv = QTableView()
        #header = ['date', 'time']
        header = columns
        tabledata_tmp = []
        for column in columns:
            tabledata_tmp.append(data.get_attribute(column))
        tabledata = []
        #print len(tabledata_tmp[0])
        #print len(tabledata_tmp)
        for ii in range(len(tabledata_tmp[0])):
            tabledata.append([])
            for i in range(len(tabledata_tmp)):
                #print "ii = %d, i = %d" % (ii,i)
                tabledata[ii].append(tabledata_tmp[i][ii])
            
        #print tabledata
        #tabledata = [[1,2],
        #             [3,4]]
        tm = OpusTableModel(tabledata, header, container) 
        tv.setModel(tm)
        tv.setSortingEnabled(True)
        tableGroupBoxLayout.addWidget(tv)

        #tableWidget = QTableWidget(container)
        #tableWidget.setObjectName("tableWidget")
        #tableGroupBoxLayout.addWidget(tableWidget)

        widgetLayout.addWidget(tableGroupBox)

        tabIcon = QIcon(":/Images/Images/cog.png")
        tabLabel = QString(dataset_name)
        tabs.insertTab(0,container,tabIcon,tabLabel)
        tabs.setCurrentIndex(0)


    def refreshAction(self):
        #print "refreshAction"
        self.xmlFileObject.model.refresh(self.xmlFileObject.treeview.rootIndex())

    def openTextFile(self):
        print "openTextFile pressed with column = %s and item = %s" % \
              (self.currentColumn, self.xmlFileObject.model.filePath(self.currentIndex))
        if self.xmlFileObject.mainwindow.editorStuff:
            print "Loading into qscintilla..."
            filename = self.xmlFileObject.model.filePath(self.currentIndex)
            self.xmlFileObject.mainwindow.editorStuff.clear()
            try:
                f = open(filename,'r')
            except:
                return
            for l in f.readlines():
                self.xmlFileObject.mainwindow.editorStuff.append(l)
            f.close()
            self.xmlFileObject.mainwindow.editorStatusLabel.setText(QString(filename))
            self.xmlFileObject.mainwindow.openEditorTab()

    def fillInAvailableScripts(self):
        #print "Checking for scripts"
        choices = []
        classification = ""
        if self.xmlFileObject.model.isDir(self.currentIndex):
            regex = QRegExp("\\d{4}")
            name = self.xmlFileObject.model.fileName(self.currentIndex)
            parentname = self.xmlFileObject.model.fileName(self.xmlFileObject.model.parent(self.currentIndex))
            isdir = self.xmlFileObject.model.isDir(self.currentIndex)
            parentisdir = self.xmlFileObject.model.isDir(self.xmlFileObject.model.parent(self.currentIndex))
            # print "%s %s %s %s" % (name, parentname,isdir,parentisdir)
            if isdir and regex.exactMatch(name):
                # We have a database dir
                # print "Database Dir"
                classification = "database"
            elif parentisdir and regex.exactMatch(parentname):
                # We have a dataset
                # print "Dataset Dir"
                classification = "dataset"
        else:
            regex = QRegExp("\\d{4}")
            model = self.xmlFileObject.model
            parentIndex = model.parent(self.currentIndex)
            parentparentIndex = model.parent(parentIndex)
            parentparentname = model.fileName(parentparentIndex)
            parentparentisdir = model.isDir(parentparentIndex)
            if parentparentisdir and regex.exactMatch(parentparentname):
                # We have a file with a parentparent which is a database classification
                classification = "array"
        tree = self.xmlFileObject.mainwindow.toolboxStuff.dataManagerTree
        dbxml = tree.model.index(0,0,QModelIndex()).parent()
        dbindexlist = tree.model.findElementIndexByType("script_batch",dbxml,True)
        for dbindex in dbindexlist:
            if dbindex.isValid():
                classificationindex = tree.model.findElementIndexByType("classification",dbindex)
                classificationindexElement = None
                classificationtext = ""
                if classificationindex[0].isValid():
                    classificationindexElement = classificationindex[0].internalPointer()
                    if classificationindexElement.node().hasChildNodes():
                        children = classificationindexElement.node().childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                classificationtext = children.item(x).nodeValue()
                dbindexElement = dbindex.internalPointer()
                tagName = dbindexElement.domNode.toElement().tagName()
                if classificationtext != "" and classificationtext == classification:
                    choices.append(tagName)
        self.classification = classification
        return choices

    def dataActionMenuFunction(self,action):
        # print "%s - %s" % (filename,actiontext)
        QObject.disconnect(self.menu, SIGNAL("triggered(QAction*)"),self.dataActionMenuFunction)

        if action != self.actRefresh:
            actiontext = action.text()
            filename = self.xmlFileObject.model.fileName(self.currentIndex)
            filepath = self.xmlFileObject.model.filePath(self.currentIndex)
            parentfilepath = self.xmlFileObject.model.filePath(self.currentIndex.parent())
            # Add in the code to take action... like run a script...
            # First find the batch to loop over the configs to execute
            tree = self.xmlFileObject.mainwindow.toolboxStuff.dataManagerTree
            scriptxml = tree.model.index(0,0,QModelIndex()).parent()
            scriptindexlist = tree.model.findElementIndexByName(actiontext,scriptxml,False)
            scriptindex = scriptindexlist[0]
            if scriptindex.isValid():
                # print scriptindex.internalPointer().node().toElement().tagName()
                # We have the script_batch... time to loop over the children and get the configs
                configindexlist = tree.model.findElementIndexByType("script_config",scriptindex,True)
                # print len(configindexlist)
                for configindex in configindexlist:
                    if configindex.isValid():
                        # Now for each config index we need to run the scripts
                        # Now find the script that this config refers to...
                        configNode = configindex.internalPointer().node().toElement()
                        script_hook = configNode.elementsByTagName(QString("script_hook")).item(0)
                        script_name = QString("")
                        if script_hook.hasChildNodes():
                            children = script_hook.childNodes()
                            for x in xrange(0,children.count(),1):
                                if children.item(x).isText():
                                    script_name = children.item(x).nodeValue()
                        # This will be in the script_library
                        library = configindex.model().xmlRoot.toElement().elementsByTagName(QString("script_library")).item(0)
                        script_path = library.toElement().elementsByTagName("script_path").item(0)
                        script = library.toElement().elementsByTagName(script_name).item(0)

                        # First find the script path text...
                        if script_path.hasChildNodes():
                            children = script_path.childNodes()
                            for x in xrange(0,children.count(),1):
                                if children.item(x).isText():
                                    scriptPath = children.item(x).nodeValue()
                        if script.hasChildNodes():
                            children = script.childNodes()
                            for x in xrange(0,children.count(),1):
                                if children.item(x).isText():
                                    filePath = children.item(x).nodeValue()
                        importPath = QString(scriptPath).append(QString(".")).append(QString(filePath))
                        # print "New import ", importPath

                        # Now loop and build up the parameters...
                        params = {}
                        childNodes = configNode.childNodes()
                        for x in xrange(0,childNodes.count(),1):
                            thisElement = childNodes.item(x)
                            thisElementText = QString("")
                            if thisElement.hasChildNodes():
                                children = thisElement.childNodes()
                                for x in xrange(0,children.count(),1):
                                    if children.item(x).isText():
                                        thisElementText = children.item(x).nodeValue()
                            if thisElement.toElement().tagName() == QString("opus_data_directory"):
                                if self.classification == "database":
                                    thisElementText = self.xmlFileObject.model.filePath(self.currentIndex.parent())
                                elif self.classification == "dataset":
                                    thisElementText = self.xmlFileObject.model.filePath(self.currentIndex.parent().parent())
                                elif self.classification == "array":
                                    thisElementText = self.xmlFileObject.model.filePath(self.currentIndex.parent().parent().parent())
                            if thisElement.toElement().tagName() == QString("opus_data_year"):
                                if self.classification == "database":
                                    thisElementText = self.xmlFileObject.model.fileName(self.currentIndex)
                                elif self.classification == "dataset":
                                    thisElementText = self.xmlFileObject.model.fileName(self.currentIndex.parent())
                                elif self.classification == "array":
                                    thisElementText = self.xmlFileObject.model.fileName(self.currentIndex.parent().parent())
                            if thisElement.toElement().tagName() == QString("opus_table_name"):
                                if self.classification == "database":
                                    thisElementText = "ALL"
                                elif self.classification == "dataset":
                                    thisElementText = self.xmlFileObject.model.fileName(self.currentIndex)
                                elif self.classification == "array":
                                    thisElementText = self.xmlFileObject.model.fileName(self.currentIndex.parent())
                            if thisElement.toElement().tagName() != QString("script_hook"):
                                params[thisElement.toElement().tagName()] = thisElementText
                        x = OpusScript(self.xmlFileObject.mainwindow,importPath,params)
                        y = RunScriptThread(self.xmlFileObject.mainwindow,x)
                        y.run()
        return


    def processCustomMenu(self, position):
        self.currentColumn = self.xmlFileObject.treeview.indexAt(position).column()
        self.currentIndex = self.xmlFileObject.treeview.indexAt(position)

        self.menu = QMenu(self.xmlFileObject.mainwindow)
        if self.currentIndex.isValid():
            if self.xmlFileObject.model.fileInfo(self.currentIndex).suffix() == "txt":
                self.menu.addAction(self.actOpenTextFile)
            else:
                # Do stuff for directories
                choices = self.fillInAvailableScripts()
                if self.classification == "dataset":
                    # We need to provide the option to open the dataset
                    self.menu.addAction(self.actViewDataset)
                if len(choices) > 0:
                    self.dynactions = []
                    for i,choice in enumerate(choices):
                        # Add choices with custom text...
                        dynaction = QAction(self.applicationIcon, choice, self.xmlFileObject.mainwindow)
                        self.dynactions.append(dynaction)
                        self.menu.addAction(dynaction)
                    QObject.connect(self.menu, SIGNAL("triggered(QAction*)"),
                                    self.dataActionMenuFunction)
        # Now tack on a refresh for all right clicks
        #print "Setting model refresh"
        self.menu.addAction(self.actRefresh)
        self.menu.exec_(QCursor.pos())
