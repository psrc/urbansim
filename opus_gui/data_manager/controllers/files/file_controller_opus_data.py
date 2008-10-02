# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
from PyQt4.QtCore import QString, Qt, QRegExp, QObject, SIGNAL, QModelIndex
from PyQt4.QtGui import QTextBrowser, QGroupBox, QTableView, QWidget, QIcon, QAction, QVBoxLayout, QMenu, QCursor

#from opus_gui.data_manager.run_tool import *
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_gui.abstract_manager.models.table_model import TableModel
from opus_gui.data_manager.controllers.dialogs.executetool import ExecuteToolGui
from StringIO import StringIO

from opus_gui.abstract_manager.controllers.files.file_controller import FileController

class FileController_OpusData(FileController):
    def __init__(self, toolboxbase, controller_type,opusDataPath, parentWidget, listen_to_menu = True):

        FileController.__init__(self, toolboxbase = toolboxbase, controller_type = controller_type,
                                    opusDataPath = opusDataPath, parentWidget = parentWidget,
                                    listen_to_menu = listen_to_menu)

        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.refreshIcon = QIcon(":/Images/Images/arrow_refresh.png")
        self.tableGoIcon = QIcon(":/Images/Images/table_go.png")

        self.actRefresh = QAction(self.refreshIcon, "Refresh Tree",
                                  self.mainwindow)
        QObject.connect(self.actRefresh, SIGNAL("triggered()"),
                        self.refreshAction)

        self.actViewDataset = QAction(self.applicationIcon, "View Dataset",
                                      self.mainwindow)
        QObject.connect(self.actViewDataset, SIGNAL("triggered()"),
                        self.viewDatasetAction)
        
        self.actOpenTextFile = QAction(self.applicationIcon, "Open Text File",
                                       self.mainwindow)
        QObject.connect(self.actOpenTextFile, SIGNAL("triggered()"),
                        self.openTextFile)
        
        self.xml_model = toolboxbase.dataManagerTree.model

    def viewDatasetAction(self):
        #print "viewDatasetAction"
        model = self.model
        table_name = str(model.fileName(self.currentIndex))
        table_name_full = str(model.filePath(self.currentIndex))
        parentIndex = model.parent(self.currentIndex)
        parent_name = str(model.fileName(parentIndex))
        parent_name_full = str(model.filePath(parentIndex))
        storage = StorageFactory().get_storage('flt_storage', storage_location=parent_name_full)
        columns = storage.get_column_names(table_name)
        # temporarily use the table name for the dataset name
        # dataset_name = DatasetFactory().dataset_name_for_table(table_name)
        # Aaron - please check this way of getting the XMLConfiguration -- is this the best way?
        general = self.mainwindow.toolboxBase.opus_core_xml_configuration.get_section('general')
        # problem: this gets the package order for the current project, but the viewer shows all the data
        package_order = general['dataset_pool_configuration'].package_order
        # PREVIOUS HACK: 
        # package_order = ['seattle_parcel','urbansim_parcel', 'eugene', 'urbansim', 'opus_core']
        # temporary code: just use a generic dataset for now
        data = Dataset(in_storage=storage, dataset_name=table_name, in_table_name=table_name, id_name=[])
        # code to get a more specialized dataset if possible (doesn't work with table names not ending in 's'
        # unless they are in the exceptions list in DatasetFactory)
        # data = DatasetFactory().search_for_dataset_with_hidden_id(dataset_name, package_order, 
        #    arguments={'in_storage': storage, 'in_table_name': table_name})
        # Need to add a new tab to the main tabs for display of the data
        tabs = self.mainwindow.tabWidget
        container = QWidget()
        widgetLayout = QVBoxLayout(container)
        summaryGroupBox = QGroupBox(container)
        summaryGroupBox.setTitle(QString("Summary statistics for dataset %s"%table_name))
        summaryGroupBox.setFlat(True)
        summaryGroupBoxLayout = QVBoxLayout(summaryGroupBox)
        # Grab the summary data
        buffer = StringIO()
        data.summary(output=buffer)
        strng = buffer.getvalue()
        buffer.close()
        textBrowser = QTextBrowser()
#        textBrowser.insertPlainText(strng)
        textBrowser.insertHtml(self.parse_dataset_summary(strng))
        summaryGroupBoxLayout.addWidget(textBrowser)
        
        widgetLayout.addWidget(summaryGroupBox)
        
        tableGroupBox = QGroupBox(container)
        tableGroupBox.setTitle(QString("Table View"))
        tableGroupBox.setFlat(True)
        tableGroupBoxLayout = QVBoxLayout(tableGroupBox)
        tv = QTableView()
        header = columns
        tabledata_tmp = []
        for column in columns:
            tabledata_tmp.append(data.get_attribute(column))

        # Transpose the lists
        tabledata = map(None,*tabledata_tmp)

        # If the table data is not empty then we display it
        if tabledata:            
            #tv.resizeColumnsToContents()
            tm = TableModel(tabledata, header, container) 
            tv.setModel(tm)
            tv.setSortingEnabled(True)
            tableGroupBoxLayout.addWidget(tv)
            
        widgetLayout.addWidget(tableGroupBox)

        tabIcon = QIcon(":/Images/Images/cog.png")
        tabLabel = QString(table_name)
        tabs.insertTab(0,container,tabIcon,tabLabel)
        tabs.setCurrentIndex(0)

    def parse_dataset_summary(self, summary):
        html = ['''<style type="text/css">

            table.prettytable {
              background: white;
            }
            table.prettytable th {
              border: 1px black solid;
              padding: 0.2em;
              background: gainsboro;
              text-align: left;
                border-width: thin thin thin thin;
                padding: 2px 2px 2px 2px;
                border-style: inset inset inset inset;
                border-color: gray gray gray gray;
            }
            table.prettytable td {
              border: 1px black solid;
              padding: 0.2em;
            }
    
            table.prettytable caption {
              margin-left: inherit;
              margin-right: inherit;
            }
            #text a {
                color: #000000;
                position: relative;
                text-decoration: underline;
            }
            </style>''',
            '<body>',
            '<div id="text">',
            '<table class="prettytable">'
            ]
            
        summary_lines = summary.split('\n')
        for i, line in enumerate(summary_lines):
            if i == 1: continue
            html.append('<tr>')
            if i == 0:                                
                header = line.split()[1:]
                html.append(''.join(['<th>%s</th>'%col for col in header]))
            else:
                
                row = line.split()
                if len(row) == 0: continue
                if row[0] == 'Size:': 
                    start_end = i
                    break
                html.append(''.join(['<td>%s</td>'%col for col in row]))                
        
            html.append('</tr>')
        html.append('</table>')
        try:
            html.append('<br><br>' + '<br>'.join(summary_lines[start_end:]))
        except:
            pass
        html.append('</div></body>')
        return QString('\n'.join(html))
        
        
    def refreshAction(self):
        #print "refreshAction"
        self.model.refresh(self.treeview.rootIndex())

    def openTextFile(self):
        print "openTextFile pressed with column = %s and item = %s" % \
              (self.currentColumn, self.model.filePath(self.currentIndex))
        if self.mainwindow.editorStuff:
            print "Loading into qscintilla..."
            filename = self.model.filePath(self.currentIndex)
            self.mainwindow.editorStuff.clear()
            try:
                f = open(filename,'r')
            except:
                return
            for l in f.readlines():
                self.mainwindow.editorStuff.append(l)
            f.close()
            self.mainwindow.editorStatusLabel.setText(QString(filename))
            self.mainwindow.openEditorTab()

    def fillInAvailableTools(self):
        #print "Checking for tools"
        choices = {}
        classification = ""
        if self.model.isDir(self.currentIndex):
            regex = QRegExp("\\d{4}")
            name = self.model.fileName(self.currentIndex)
            parentname = self.model.fileName(self.model.parent(self.currentIndex))
            isdir = self.model.isDir(self.currentIndex)
            parentisdir = self.model.isDir(self.model.parent(self.currentIndex))
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
            model = self.model
            parentIndex = model.parent(self.currentIndex)
            parentparentIndex = model.parent(parentIndex)
            parentparentname = model.fileName(parentparentIndex)
            parentparentisdir = model.isDir(parentparentIndex)
            if parentparentisdir and regex.exactMatch(parentparentname):
                # We have a file with a parentparent which is a database classification
                classification = "array"
        # print "Classification = " + classification
        dbxml = self.xml_model.index(0,0,QModelIndex()).parent()
        # First loop through all tool_sets
        setsindexlist = self.xml_model.findElementIndexByType("tool_library",dbxml,True)
        for setsindex in setsindexlist:
            if setsindex.isValid():
                #print "Found valid tool_sets"
                # Now loop through all tool_set and find the ones with a matching classification
                tsindexlist = self.xml_model.findElementIndexByType("tool_file",setsindex,True)
                for tsindex in tsindexlist:
                    if tsindex.isValid():
                        #print "Found valid tool_set"
                        classificationtext = ""
                        tsitem = tsindex.internalPointer()
                        # We use the dom tree to find the classification because it is a hidden node
                        # in the XML tree and will not show up via a search on the model indexes (i.e. it
                        # is not actually in the model/view since it is hidden.
                        if tsitem.node().hasChildNodes():
                            tschildren = tsitem.node().childNodes()
                            for x in xrange(0,tschildren.count(),1):
                                if tschildren.item(x).isElement():
                                    tselement = tschildren.item(x).toElement()
                                    if tselement.hasAttribute(QString("type")) and \
                                           (tselement.attribute(QString("type")) == QString("acts_on")):
                                        if tselement.hasChildNodes():
                                            classchildren = tselement.childNodes()
                                            for x in xrange(0,classchildren.count(),1):
                                                if classchildren.item(x).isText():
                                                    #print "Found some text in the classification element"
                                                    classificationtext = classchildren.item(x).nodeValue()
                                    if tselement.hasAttribute(QString("type")) and \
                                           (tselement.attribute(QString("type")) == QString("exports_to")):
                                        #print tselement.text()
                                        export_to_text = tselement.text()
                        tagName = tsitem.domNode.toElement().tagName()
                        if classificationtext != "" and classificationtext == classification:
                            choices[tagName] = export_to_text
        self.classification = classification
        return choices

    def dataActionMenuFunction(self,action):
        QObject.disconnect(self.menu, SIGNAL("triggered(QAction*)"),self.dataActionMenuFunction)

        if action != self.actRefresh:
            #actiontext = action.text()
            actiontext = self.dynactions[action.text()]
            filename = self.model.fileName(self.currentIndex)
            filepath = self.model.filePath(self.currentIndex)
            parentfilepath = self.model.filePath(self.currentIndex.parent())
            # Add in the code to take action... like run a tool...
            # First find the batch to loop over the configs to execute
            toolxml = self.xml_model.index(0,0,QModelIndex()).parent()
            toolindexlist = self.xml_model.findElementIndexByName(actiontext,toolxml,False)
            toolindex = toolindexlist[0]
            if toolindex.isValid():
                #print toolindex.internalPointer().node().toElement().tagName()
                flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
                window = ExecuteToolGui(self.mainwindow,self.xml_model,
                                        toolindex.internalPointer().node().toElement(),
                                        None,flags,optional_params = None)
                tool_title = window.tool_title.replace('_', ' ')
                tool_title2 = str(tool_title).title()
                window.setWindowTitle(tool_title2)
                window.show()
                # We have the tool_set... time to loop over the children and get the configs
#                configindexlist = self.xml_model.findElementIndexByType("tool_file",toolindex,True)
#                #print len(configindexlist)
#                for configindex in configindexlist:
#                    if configindex.isValid():
#                        params = {}
#                        thisElement = QString("opus_data_directory")
#                        if self.classification == "database":
#                            thisElementText = self.model.filePath(self.currentIndex.parent())
#                        elif self.classification == "dataset":
#                            thisElementText = self.model.filePath(self.currentIndex.parent().parent())
#                        elif self.classification == "array":
#                            thisElementText = self.model.filePath(self.currentIndex.parent().parent().parent())
#                        params[thisElement] = thisElementText
#                        thisElement2 = QString("opus_data_year")
#                        if self.classification == "database":
#                            thisElementText2 = self.model.fileName(self.currentIndex)
#                        elif self.classification == "dataset":
#                            thisElementText2 = self.model.fileName(self.currentIndex.parent())
#                        elif self.classification == "array":
#                            thisElementText2 = self.model.fileName(self.currentIndex.parent().parent())
#                        params[thisElement2] = thisElementText2
#                        thisElement3 = QString("opus_table_name")
#                        if self.classification == "database":
#                            thisElementText3 = "ALL"
#                        elif self.classification == "dataset":
#                            thisElementText3 = self.model.fileName(self.currentIndex)
#                        elif self.classification == "array":
#                            thisElementText3 = self.model.fileName(self.currentIndex.parent())
#                        params[thisElement3] = thisElementText3
#
#                        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
#                        window = ExecuteToolGui(self.mainwindow,self.xml_model,
#                                                configindex.internalPointer().node().toElement(),
#                                                None,flags,optional_params = params)
#                        tool_title = window.tool_title.replace('_', ' ')
#                        tool_title2 = str(tool_title).title()
#                        window.setWindowTitle(tool_title2)
#                        window.show()
        return


    def processCustomMenu(self, position):
        self.currentColumn = self.treeview.indexAt(position).column()
        self.currentIndex = self.treeview.indexAt(position)

        self.menu = QMenu(self.mainwindow)
        if self.currentIndex.isValid():
            if self.model.fileInfo(self.currentIndex).suffix() == "txt":
                self.menu.addAction(self.actOpenTextFile)
            else:
                # Do stuff for directories
                choices = self.fillInAvailableTools()
                if self.classification == "dataset":
                    self.export_menu = QMenu(QString('Export Opus dataset to'), self.mainwindow)
                    self.export_menu.setIcon(self.tableGoIcon)
                    if len(choices) > 0:
                        self.dynactions = {}
                        for i,j in choices.iteritems():
                            dynaction = QAction(self.applicationIcon, j, self.mainwindow)
                            self.export_menu.addAction(dynaction)
                            self.dynactions[j] = i
                        QObject.connect(self.export_menu, SIGNAL("triggered(QAction*)"),
                                        self.dataActionMenuFunction)                            
                    self.menu.addMenu(self.export_menu)
                    self.menu.addSeparator()
                    # We need to provide the option to open the dataset
                    self.menu.addAction(self.actViewDataset)
                if self.classification == "database":
                    self.export_menu = QMenu(QString('Export Opus database to'), self.mainwindow)
                    self.export_menu.setIcon(self.tableGoIcon)
                    if len(choices) > 0:
                        self.dynactions = {}
                        for i,j in choices.iteritems():
                            dynaction = QAction(self.applicationIcon, j, self.mainwindow)
                            self.export_menu.addAction(dynaction)
                            self.dynactions[j] = i
                        QObject.connect(self.export_menu, SIGNAL("triggered(QAction*)"),
                                        self.dataActionMenuFunction) 
                    self.menu.addMenu(self.export_menu)
                    self.menu.addSeparator()                  
        # Now tack on a refresh for all right clicks
        #print "Setting model refresh"
        self.menu.addAction(self.actRefresh)
        self.menu.exec_(QCursor.pos())
