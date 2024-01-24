# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from io import StringIO

from PyQt5.QtCore  import  Qt, QRegExp, QObject, pyqtSignal, QModelIndex
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QTextBrowser, QGroupBox, QTableView, QWidget, QAction, QVBoxLayout, QMenu

from opus_gui.util.icon_library import IconLibrary
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_gui.abstract_manager.models.table_model import TableModel
from opus_gui.data_manager.controllers.dialogs.executetool import ExecuteToolGui
from opus_gui.abstract_manager.controllers.files.file_controller import FileController
from opus_gui.data_manager.data_manager_functions import get_path_to_tool_modules


class FileController_OpusData(FileController):
    def __init__(self, manager, data_path, parent_widget, tools_model):

        FileController.__init__(self, manager, data_path, parent_widget)

        self.actRefresh = QAction(IconLibrary.icon('reload'), "Refresh Tree", self.treeview)
        self.actRefresh.triggered.connect(self.refreshAction)

        self.actViewDataset = QAction(IconLibrary.icon('inspect'), "View Dataset", self.treeview)
        self.actViewDataset.triggered.connect(self.viewDatasetAction)

        self.actOpenTextFile = QAction(IconLibrary.icon('text'), "Open Text File", self.treeview)
        self.actOpenTextFile.triggered.connect(self.openTextFile)

        self.tool_library_node = self.manager.project.find('data_manager/tool_library')
        
        self.tools_model = tools_model

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

#        general = self.mainwindow.toolboxBase.opus_core_xml_configuration.get_section('general')
#        # problem: this gets the package order for the current project, but the viewer shows all the data
#        package_order = general['dataset_pool_configuration'].package_order

        # PREVIOUS HACK:
        # package_order = ['seattle_parcel','urbansim_parcel', 'eugene', 'urbansim', 'opus_core']
        # temporary code: just use a generic dataset for now
        data = Dataset(in_storage=storage, dataset_name=table_name, in_table_name=table_name, id_name=[])
        # code to get a more specialized dataset if possible (doesn't work with table names not ending in 's'
        # unless they are in the exceptions list in DatasetFactory)
        # data = DatasetFactory().search_for_dataset_with_hidden_id(dataset_name, package_order,
        #    arguments={'in_storage': storage, 'in_table_name': table_name})
        # Need to add a new tab to the main tabs for display of the data
        container = QWidget()
        widgetLayout = QVBoxLayout(container)
        summaryGroupBox = QGroupBox(container)
        summaryGroupBox.setTitle(("Year: %s  Run name: %s" % (parent_name,table_name_full.split('/')[-3])))
        summaryGroupBox.setFlat(True)
        summaryGroupBoxLayout = QVBoxLayout(summaryGroupBox)
        # Grab the summary data
        buffer = StringIO()
        data.summary(output=buffer, unload_after_each_attribute=True)
        strng = buffer.getvalue()
        buffer.close()
        textBrowser = QTextBrowser()
#        textBrowser.insertPlainText(strng)
        textBrowser.insertHtml(self.parse_dataset_summary(strng))
        summaryGroupBoxLayout.addWidget(textBrowser)

        widgetLayout.addWidget(summaryGroupBox)

        tableGroupBox = QGroupBox(container)
        tableGroupBox.setTitle(("Table View"))
        tableGroupBox.setFlat(True)
        tableGroupBoxLayout = QVBoxLayout(tableGroupBox)
        tv = QTableView()
        header = columns
        tabledata_tmp = []
        for column in columns:
            tabledata_tmp.append(data.get_attribute(column))

        # Transpose the lists
        tabledata = list(*tabledata_tmp)

        # If the table data is not empty then we display it
        if tabledata:
            #tv.resizeColumnsToContents()
            tm = TableModel(tabledata, header, container)
            tv.setModel(tm)
            tv.setSortingEnabled(True)
            tableGroupBoxLayout.addWidget(tv)

        widgetLayout.addWidget(tableGroupBox)

        container.tabIcon = IconLibrary.icon('inspect')
        container.tabLabel = (table_name)
        self.manager._attach_tab(container)

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
        return ('\n'.join(html))


    def refreshAction(self):
        #print "refreshAction"
        self.model.refresh(self.treeview.rootIndex())

# Disabling editor support for now

    def openTextFile(self):
        print('openTextFile %s' % self.model.filePath(self.currentIndex))
        pass
#        print "openTextFile pressed with column = %s and item = %s" % \
#              (self.currentColumn, self.model.filePath(self.currentIndex))
#        if self.mainwindow.editorStuff:
#            print "Loading into qscintilla..."
#            filename = self.model.filePath(self.currentIndex)
#            self.mainwindow.editorStuff.clear()
#            try:
#                f = open(filename,'r')
#            except:
#                return
#            for l in f.readlines():
#                self.mainwindow.editorStuff.append(l)
#            f.close()
#            self.mainwindow.editorStatusLabel.setText((filename))
#            self.mainwindow.openEditorTab()

    def fillInAvailableTools(self):

        # Operations on the selected item
        export_choices = {}
        import_choices = {}

        # Classification for the selected item
        classification = ""
        
        regex = QRegExp("\\d{4}")# match directory names with four digits
        def isYear(filename):
            return regex.exactMatch(filename)

        if self.model.isDir(self.currentIndex):

            def hasYearChild(index):
                return any([isYear(self.model.fileName(index.child(i,0))) 
                            for i in range(self.model.rowCount(index))])
            
            name = self.model.fileName(self.currentIndex)
            parentname = self.model.fileName(self.model.parent(self.currentIndex))
            isdir = self.model.isDir(self.currentIndex)
            if self.model.parent(self.currentIndex).isValid():
                parentisdir = self.model.isDir(self.model.parent(self.currentIndex))
            else:
                parentisdir = False
            # print "%s %s %s %s" % (name, parentname,isdir,parentisdir)
            if isdir and isYear(name):
                # We have a database dir
                # print "Database Dir"
                classification = "database"
            elif parentisdir and isYear(parentname):
                # We have a dataset
                # print "Dataset Dir"
                classification = "dataset"
            elif isdir and hasYearChild(self.currentIndex):
                classification = "database_collection"
                
        else:
            model = self.model
            parentIndex = model.parent(self.currentIndex)
            parentparentIndex = model.parent(parentIndex)
            parentparentname = model.fileName(parentparentIndex)
            parentparentisdir = model.isDir(parentparentIndex)
            if parentparentisdir and isYear(parentparentname):
                # We have a file with a parentparent which is a database classification
                classification = "array"

        # Build up a list of available operations based on the classification

        tool_set_nodes = [tool_set_node for tool_set_node in self.tool_library_node
                          if tool_set_node.tag == 'tool_group']
        tool_file_nodes = []
        for tool_set_node in tool_set_nodes:
            tool_file_nodes.extend([node for node in tool_set_node
                           if node.tag == 'tool'])

        # Find all tool_nodes that acts on the resolved classification
        # (by looking at the XML node 'acts_on')
        for tool_node in tool_file_nodes:
            acts_on_node = tool_node.find('acts_on')
            exports_to_node = tool_node.find('exports_to')
            imports_from_node = tool_node.find('imports_from')

            if acts_on_node is None:
                # This tool doesn't export or import anything
                continue

            tool_classifications = acts_on_node.text.split(',')
            
            if not imports_from_node is None:
                imports_from_value = imports_from_node.text
                if classification in tool_classifications:
                    import_choices[imports_from_value] = tool_node

            if not exports_to_node is None:
                exports_to_value = exports_to_node.text
                if classification in tool_classifications:
                    export_choices[exports_to_value] = tool_node
                
        self.classification = classification
        return (export_choices, import_choices)

#         print "Classification = " + classification
#        dbxml = self.treeview.model().index(0,0,QModelIndex()).parent()
#         First loop through all tool_sets
#        setsindexlist = self.treeview.findElementIndexByType("tool_library",dbxml,True)
#        for setsindex in setsindexlist:
#            if setsindex.isValid():
#                print "Found valid tool_sets"
#                 Now loop through all tool_set and find the ones with a matching classification
#                tsindexlist = self.xml_model.findElementIndexByType("tool_file",setsindex,True)
#                for tsindex in tsindexlist:
#                    if tsindex.isValid():
#                        print "Found valid tool_set"
#                        classificationtext = ""
#                        tsitem = tsindex.internalPointer()
#                         We use the dom tree to find the classification because it is a hidden node
#                         in the XML tree and will not show up via a search on the model indexes (i.e. it
#                         is not actually in the model/view since it is hidden.
#                        if tsitem.node().hasChildNodes():
#                            tschildren = tsitem.node().childNodes()
#                            for x in xrange(0,tschildren.count(),1):
#                                if tschildren.item(x).isElement():
#                                    tselement = tschildren.item(x).toElement()
#                                    if tselement.hasAttribute(("type")) and \
#                                           (tselement.attribute(("type")) == ("acts_on")):
#                                        if tselement.hasChildNodes():
#                                            classchildren = tselement.childNodes()
#                                            for x in xrange(0,classchildren.count(),1):
#                                                if classchildren.item(x).isText():
#                                                    print "Found some text in the classification element"
#                                                    classificationtext = classchildren.item(x).nodeValue()
#                                                    classificationtext = str(classchildren.item(x).nodeValue()).split(',')
#                                    if tselement.hasAttribute(("type")) and \
#                                           (tselement.attribute(("type")) == ("exports_to")):
#                                        print tselement.text()
#                                        export_to_text = tselement.text()
#                        tagName = tsitem.domNode.toElement().tagName()
#                        for i in classificationtext:
#                            if i != "" and i == classification:
#                                choices[tagName] = export_to_text
#        self.classification = classification
#        return choices

    def dataActionMenuFunctionImport(self, action):
        return self.dataActionMenuFunction(self.import_dynactions, action)
    
    def dataActionMenuFunctionExport(self, action):
        return self.dataActionMenuFunction(self.export_dynactions, action)

    def dataActionMenuFunction(self, dynactions, action):
        self.menu.triggered.disconnect(self.dataActionMenuFunction)
        if action != self.actRefresh:
            actiontext = str(action.text())
            tool_node = dynactions[actiontext]
            filename = self.model.fileName(self.currentIndex)
            filepath = self.model.filePath(self.currentIndex)
            parentfilepath = self.model.filePath(self.currentIndex.parent())

            params = self.getOptionalParams(actiontext)
            window = ExecuteToolGui(parent_widget = self.treeview,
                                    tool_node = tool_node,
                                    tool_config = None,
                                    tool_library_node = self.tool_library_node, 
                                    params = params,
                                    model = self.tools_model)
            window.show()
        return

    def getOptionalParams(self, actiontext):
        params = {'tool_path': get_path_to_tool_modules(self.manager.project)}
        if self.classification == 'database':
            params['opus_data_directory'] = str(self.model.filePath(self.currentIndex.parent()))
            params['opus_data_year'] = str(self.model.fileName(self.currentIndex))
            params['opus_table_name'] = 'ALL'
            if actiontext == 'CSV':
                params['csv_table_name'] = 'ALL'
        elif self.classification == 'dataset':
            params['opus_data_directory'] = str(self.model.filePath(self.currentIndex.parent().parent()))
            params['opus_data_year'] = str(self.model.fileName(self.currentIndex.parent()))
            params['opus_table_name'] = str(self.model.fileName(self.currentIndex))
            if actiontext == 'CSV':
                params['csv_table_name'] = str(self.model.fileName(self.currentIndex))
        elif self.classification == 'database_collection':
            params['opus_data_directory'] = str(self.model.filePath(self.currentIndex))
            params['opus_data_year'] = 'ALL'
            params['opus_table_name'] = 'ALL'
            if actiontext == 'CSV':
                params['csv_table_name'] = str(self.model.fileName(self.currentIndex))
        return params


    def process_custom_menu(self, position):
        self.currentColumn = self.treeview.indexAt(position).column()
        self.currentIndex=self.treeview.indexAt(position)

        self.menu = QMenu(self.treeview)

        if self.currentIndex.isValid():
            if self.model.fileInfo(self.currentIndex).suffix() == "txt":
                self.menu.addAction(self.actOpenTextFile)
            else:
                # Do stuff for directories
                export_choices, import_choices = self.fillInAvailableTools()
                
                if self.classification == "dataset" or self.classification == "database" or self.classification == "database_collection":
                    self.export_menu = QMenu(('Export Opus %s to' % self.classification), self.treeview)
                    self.export_menu.setIcon(IconLibrary.icon('export'))
                    self.import_menu = QMenu(('Import Opus %s from' % self.classification), self.treeview)
                    self.import_menu.setIcon(IconLibrary.icon('import'))
                    
                    if len(export_choices) > 0:
                        self.export_dynactions = {}
                        for export_type,tool_node in export_choices.items():
                            dynaction = QAction(IconLibrary.icon('spreadsheet'), export_type, self.treeview)
                            self.export_menu.addAction(dynaction)
                            self.export_dynactions[export_type] = tool_node
                        self.export_menu.triggered.connect(self.dataActionMenuFunctionExport)
                        self.menu.addMenu(self.export_menu)
                        
                    if len(import_choices) > 0:
                        self.import_dynactions = {}
                        for import_type,tool_node in import_choices.items():
                            dynaction = QAction(IconLibrary.icon('spreadsheet'), import_type, self.treeview)
                            self.import_menu.addAction(dynaction)
                            self.import_dynactions[import_type] = tool_node
                        self.import_menu.triggered.connect(self.dataActionMenuFunctionImport)
                        self.menu.addMenu(self.import_menu)
                        
                    self.menu.addSeparator()
                    
                    # We need to provide the option to open the dataset
                    self.menu.addAction(self.actViewDataset)

        # Now tack on a refresh for all right clicks
        #print "Setting model refresh"
        self.menu.addAction(self.actRefresh)
        self.menu.exec_(QCursor.pos())
