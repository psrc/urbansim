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
from PyQt4.QtCore import QString, Qt, QObject, SIGNAL, QModelIndex, QTimer
from PyQt4.QtGui import QIcon, QAction, QMenu, QCursor, QMessageBox, QTableView, QDialog
from PyQt4.QtXml import QDomNode

from opus_gui.general_manager.models.all_variables_table_model import AllVariablesTableModel
from opus_gui.general_manager.views.all_variables_table_view_delegate import AllVariablesTableViewDelegate
from opus_gui.general_manager.views.ui_all_variables_edit import Ui_AllVariablesEditGui
from opus_gui.general_manager.views.ui_all_variables_select import Ui_AllVariablesSelectGui
from opus_gui.general_manager.views.ui_all_variables_new import Ui_AllVariablesNewGui
from opus_gui.general_manager.run.variable_validator import VariableValidator

import random,pprint,string

class AllVariablesNewGui(QDialog, Ui_AllVariablesNewGui):
    def __init__(self, mainwindow, fl, allVariablesGui, row = 0, initialParams = None, create_new_from_old = False):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        self.allVariablesGui = allVariablesGui
        self.initialParams = initialParams
        self.row = row
        self.mainwindow = mainwindow.mainwindow
        self.parent = mainwindow
        
        if create_new_from_old:
            self.variableBox.setTitle(QString('Creating new variable (based on %s)'%initialParams[0]))
            self.mode = 2
        elif initialParams is not None:
            self.variableBox.setTitle(QString('Editing existing variable (%s)'%initialParams[0]))
            self.mode = 0
        else:
            self.mode = 1
            self.variableBox.setTitle(QString('Creating new variable'))

        if self.initialParams:
            self.lineEdit.setText(self.initialParams[0])
            self._setup_co_dataset_name(value = self.initialParams[1])
            if str(self.initialParams[2]) == "both":
                self.cbIndicatorUse.setChecked(True) 
                self.cbModelUse.setChecked(True)
            elif str(self.initialParams[2]) == 'indicator':
                self.cbIndicatorUse.setChecked(True)
                self.cbModelUse.setChecked(False)
            else:
                self.cbModelUse.setChecked(True)
                self.cbIndicatorUse.setChecked(False)
                
            self.comboBox_2.setCurrentIndex(self.comboBox_2.findText(self.initialParams[3]))
            self.textEdit.setPlainText(self.initialParams[4])
        else:
            self._setup_co_dataset_name()

    def _setup_co_dataset_name(self, value = None):
        from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper
        xml_helper = ResultsManagerXMLHelper(self.mainwindow.toolboxStuff)

        available_datasets = xml_helper.get_available_datasets()

        for dataset in available_datasets:
            self.cbo_dataset_name.addItem(QString(dataset))
        
        if value is not None:
            idx = self.cbo_dataset_name.findText(value)
            if idx != -1:
                self.dataset_name = value
                self.cbo_dataset_name.setCurrentIndex(idx)        
                            
    def editsMade(self):
        # If we dont have seed params, then this is a new variable
        if self.initialParams == None:
            return True
        # Else we are looking to see if any of the params have actually changed
        
        vals = [QString(v) for v in self._get_variable_definition()]
        return   (vals[0] != self.initialParams[0]) or \
                 (vals[1] != self.initialParams[1]) or \
                 (vals[2] != self.initialParams[2]) or \
                 (vals[3] != self.initialParams[3]) or \
                 (vals[4] != self.initialParams[4])
        
    def on_saveChanges_released(self):
        #print "save pressed"
        if self.editsMade():
            dirty = 0
            # If we have made edits then we check to see if this is a new
            # variable or editing an existing.  If editing an existing then
            # we remove the old row and mark the newly inserted row with dirty.
            if self.mode == 0:
                self.allVariablesGui.tm.removeRow(self.row)
                dirty = 1
                
            (variable_name, dataset_name, use, source, definition) = self._get_variable_definition()
            self.allVariablesGui.tm.insertRow(self.row,["",
                                                        QString(variable_name),
                                                        QString(dataset_name),
                                                        QString(use),
                                                        QString(source),
                                                        QString(definition),
                                                        0,0,dirty])
            self.allVariablesGui.tm.checkStateOfCheckBoxes(False)
            self.allVariablesGui.tm.emit(SIGNAL("layoutChanged()"))
        self.close()

    def on_cancelWindow_released(self):
        self.close()
                
    def on_cboCheckSyntax_released(self):
        success, errors = VariableValidator(toolboxStuff=self.mainwindow.toolboxStuff).check_parse_errors(variables = [self._get_variable_definition()])

        if success:
            QMessageBox.information(self, 'Variable check results', 'Variable syntax check successful!')
        else:
            errorString = "Parse errors: <br><br>  " + "<br><br>".join(errors)
            QMessageBox.warning(self, 'Variable check results', errorString)
            
    def on_cboCheckData_released(self):
        success, errors = VariableValidator(toolboxStuff=self.mainwindow.toolboxStuff).check_data_errors(variables = [self._get_variable_definition()])
        if success:
            QMessageBox.information(self, 'Variable data check results', 'Variable checked successfully against baseyear data!')
        else:
            errorString = "Errors executing expression on baseyear data: <br><br>  " + "<br><br>".join(errors)
            QMessageBox.warning(self, 'Variable check results', errorString)
                
        
    def _get_variable_definition(self):
        variable_name = str(self.lineEdit.text())
        dataset_name = str(self.cbo_dataset_name.currentText())
        if self.cbIndicatorUse.isChecked():
            if self.cbModelUse.isChecked():
                use = 'both'
            else:
                use = 'indicator'
        elif self.cbModelUse.isChecked():
            use = 'model variable'
        else:
            QMessageBox.warning(self, 'Variable specification', 'The variable must have a use (Indicator and/or Model variable) specified!')
            return None
        source = str(self.comboBox_2.currentText())
        definition = str(self.textEdit.toPlainText())
        return (variable_name, dataset_name, use, source, definition)

        
class AllVariablesGui(object):
    def __init__(self, mainwindow, fl, editable):
        #if edit_select:
        #    print "Select GUI"
        #else:
        #    print "Edit GUI"
        self.mainwindow = mainwindow
        self.all_variables_index = None
        
        # Is the tableview dirty?
        self.dirty = False
        
        #Add a default table
        tv = QTableView()
        delegate = AllVariablesTableViewDelegate(tv)
        tv.setItemDelegate(delegate)
        tv.setSortingEnabled(True)
#        tv.setSelectionBehavior(QTableView.SelectRows)
        
        # So we have a data structure to define the headers for the table...
        # The first element is empty string because it is over the check box
        header = ["","Name","Dataset","Use","Source","Definition"]
        tabledata = []
        self.tabledata = tabledata
        # Grab the general section...
        tree = self.mainwindow.toolboxStuff.generalManagerTree
        self.tree = tree
        dbxml = tree.model.index(0,0,QModelIndex()).parent()
        all_variables_list = tree.model.findElementIndexByName("expression_library",dbxml,True)
        for all_variables in all_variables_list:
            # Should just be one all_variables section
            if all_variables.isValid():
                self.all_variables_index = all_variables
                # Now we have to loop through all the variables and create the data grid for the display
                tsindexlist = tree.model.findElementIndexByType("variable_definition",all_variables,True)
                self.tsindexlist = tsindexlist
                for tsindex in tsindexlist:
                    if tsindex.isValid():
                        # Now we have a valid variable, we fill in the set for display
                        tsitem = tsindex.internalPointer()
                        tsnode = tsitem.node()
                        if tsnode.isElement():
                            tselement = tsnode.toElement()
                            tselement_text = ""
                            if tselement.hasChildNodes():
                                classchildren = tselement.childNodes()
                                for x in xrange(0,classchildren.count(),1):
                                    if classchildren.item(x).isText():
                                        #print "Found some text in the classification element"
                                        tselement_text = classchildren.item(x).nodeValue()
                            tslist = ["",tselement.tagName(),
                                      tselement.attribute(QString("dataset")),
                                      tselement.attribute(QString("use")),
                                      tselement.attribute(QString("source")),
                                      tselement_text]
                            # Add on 3 slots for keeping track of:
                            # inherited,checked,dirty
                            if tselement.hasAttribute(QString("inherited")):
                                tslist.extend([1,0,0])
                            else:
                                tslist.extend([0,0,0])
                            tabledata.append(tslist)
        self.originalList = list(tabledata)
        for i,origListItem in enumerate(tabledata):
            self.originalList[i] = list(origListItem)
        tm = AllVariablesTableModel(tabledata, header, self, editable)
        tm.sort()
        self.tm = tm
        self.tv = tv
        tv.setModel(tm)
        tv.setColumnWidth(0,25)
        #tv.selectColumn(1)
        tv.setWordWrap(False)
        tv.setTextElideMode(Qt.ElideRight)
        QObject.connect(tm, SIGNAL("layoutChanged()"), self.updateVertLayout)
        #QObject.connect(tm, SIGNAL("layoutChanged()"), self.updateHorLayout)
        #QObject.connect(tm, SIGNAL("dataChanged(const QModelIndex &, const QModelIndex &)"), self.updateHorLayout)
        self.gridLayout.addWidget(tv)
        tv.horizontalHeader().setStretchLastSection(True)
        QTimer.singleShot(100, self.updateVertLayout)
        #QTimer.singleShot(200, self.updateHorLayout)

    def updateVertLayout(self):
        self.tv.resizeRowsToContents()

    def updateHorLayout(self):
        self.tv.resizeColumnsToContents()
        # HACK - Loop through and check if all columns widths add up to less than the container width,
        # and if so we expand the last column to span the space.  This is to make up for a issue
        # with the expression descriptions being one really long word and word wrap in the
        # text edit not wrapping correctly.
        realWidth = 0
        for x in xrange(0,6,1):
            realWidth = realWidth + self.tv.columnWidth(x)
            # print "%d %d" % (x, self.tv.columnWidth(x))
        if realWidth < self.variableBox.width():
            # print "We need to stretch last element %d %d" % (realWidth, self.variableBox.width())
            self.tv.setColumnWidth(5,(self.variableBox.width() - 30) - realWidth + self.tv.columnWidth(5))
        else:
            # print "We dont need to stretch last element"
            pass

class AllVariablesEditGui(QDialog, Ui_AllVariablesEditGui, AllVariablesGui):
    def __init__(self, mainwindow, fl):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        # Init the super class and let it know that we are an edit GUI
        # last param - 0=edit mode 1=select mode
        AllVariablesGui.__init__(self, mainwindow, fl, True)
        
        self.mainwindow = mainwindow

        # For now, disable the save button until we implement the write in the model...
#        self.saveChanges.setEnabled(False)

        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.editIcon = QIcon(":/Images/Images/application_edit.png")

        self.actRemoveRow = QAction(self.removeIcon,
                                    "Remove Variable",
                                    mainwindow)
        QObject.connect(self.actRemoveRow,
                        SIGNAL("triggered()"),
                        self.removeRow)

        self.actEditRow = QAction(self.editIcon,
                                  "Edit Variable",
                                  mainwindow)
        QObject.connect(self.actEditRow,
                        SIGNAL("triggered()"),
                        self.editRow)

        self.actCreateNewFromOld = QAction(self.editIcon,
                                  "Create new variable based on this variable",
                                  mainwindow)
        QObject.connect(self.actCreateNewFromOld,
                        SIGNAL("triggered()"),
                        self.createVariableLike)


        self.actCheckSyntax = QAction(self.editIcon,
                                  "Check Syntax",
                                  mainwindow)
        QObject.connect(self.actCheckSyntax,
                        SIGNAL("triggered()"),
                        self.checkSyntax)

        self.actCheckAgainstData = QAction(self.editIcon,
                                  "Check Against Data",
                                  mainwindow)
        QObject.connect(self.actCheckAgainstData,
                        SIGNAL("triggered()"),
                        self.checkAgainstData)
        
        
        self.tv.setContextMenuPolicy(Qt.CustomContextMenu)
        QObject.connect(self.tv,SIGNAL("customContextMenuRequested(const QPoint &)"),
                        self.processCustomMenu)

    def removeRow(self):
        #print "Remove Row Pressed"
        self.currentIndex.model().removeRow(self.currentIndex.row())
        self.currentIndex.model().checkStateOfCheckBoxes(False)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def editRow(self):
        #print "Remove Row Pressed"
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        row = self.currentIndex.row()
        initialParams = self.currentIndex.model().getRowDataList(self.currentIndex)
        window = AllVariablesNewGui(self,flags,self,row,initialParams)
        window.setModal(True)
        window.show()

    def createVariableLike(self):
        #print "Remove Row Pressed"
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        row = self.currentIndex.row()
        initialParams = self.currentIndex.model().getRowDataList(self.currentIndex)
        window = AllVariablesNewGui(self,flags,self, initialParams = initialParams, create_new_from_old = True)
        window.setModal(True)
        window.show()


    def processCustomMenu(self, position):
        #print "Custom Menu"
        if self.tv.indexAt(position).isValid():
            self.currentColumn = self.tv.indexAt(position).column()
            self.currentIndex = self.tv.indexAt(position)
            self.menu = QMenu(self.mainwindow)
            if self.menu:
                # Tack on a remove row item
                self.menu.addAction(self.actEditRow)
                self.menu.addAction(self.actCreateNewFromOld)
                self.menu.addSeparator()
                self.menu.addAction(self.actCheckSyntax)
                self.menu.addAction(self.actCheckAgainstData)
                if not self.tm.isInherited(self.currentIndex):
                    self.menu.addSeparator()
                    self.menu.addAction(self.actRemoveRow)
                if not self.menu.isEmpty():
                    self.menu.exec_(QCursor.pos())

    def findOriginalNode(self,list):
        for tsindex in self.tsindexlist:
            if tsindex.isValid():
                # Now we have a valid variable, we check if it is the one we want
                tsitem = tsindex.internalPointer()
                tsnode = tsitem.node()
                if tsnode.isElement():
                    tselement = tsnode.toElement()
                    if tselement.tagName() == list[1]:
                        return tsnode
        return None
        

    def updateNodeFromList(self,node,list):
        if not node.isNull():
            # We only want to check out this node if it is of type "element"
            if node.isElement():
                domElement = node.toElement()
                if not domElement.isNull():
                    # First set the tagName
                    domElement.setTagName(QString(list[1]))
                    # Now the attributes
                    domElement.setAttribute(QString("dataset"),QString(list[2]))
                    domElement.setAttribute(QString("use"),QString(list[3]))
                    domElement.setAttribute(QString("source"),QString(list[4]))
                    # Finally the description text
                    # We need to grab the text node from the element
                    if domElement.hasChildNodes():
                        children = domElement.childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                textNode = children.item(x).toText()
                                # Finally set the text node value
                                textNode.setData(list[5])
                    # Here we have to manually mark the model as dirty since
                    # we are changing out the XML DOM under the models nose
                    self.tree.model.markAsDirty()
                    self.tree.model.emit(SIGNAL("layoutChanged()"))

    def on_saveChanges_released(self):
        #print "save pressed"
        if self.dirty:
            # print "Need to save and patch the original XML"
            #### General scheme ####
            ## Loop through the new list and see:
            ## 1) are there any nodes that where in the original and have modified
            ##    attributes... update the attributes
            ## 2) are there any nodes that where not in the original... if so these
            ##    must be new nodes and need to be added
            ##
            ## Now we loop through the original list
            ## 1) see if there are any nodes that are now missing in the
            ##    new list... these have either had their tagname modified or
            ##    are removed.  In either case, remove the old node
            ##    and check if an inherited parent needs to be placed back in.
            
            # Loop through the list of lists and find the node in the XML and update it
            for i,testCase in enumerate(self.tm.arraydata):
                # Find the XML node that has the tag name in column 1
                nameToSearchFor = testCase[1]
                foundInOriginal = False
                for tsindex in self.tsindexlist:
                    if tsindex.isValid():
                        # Now we have a valid variable, we fill in the set for display
                        tsitem = tsindex.internalPointer()
                        tsnode = tsitem.node()
                        if tsnode.isElement():
                            tselement = tsnode.toElement()
                            if tselement.tagName() == nameToSearchFor:
                                # We have a match...
                                foundInOriginal = True
                if foundInOriginal:
                    # print "We have a match %s" % (nameToSearchFor)
                    # If the data is dirty we need to update the node
                    if testCase[-1]:
                        nodeToUpdate = self.findOriginalNode(testCase)
                        self.updateNodeFromList(nodeToUpdate,testCase)
                        self.tree.model.makeEditable(nodeToUpdate)
                else:
                    # print "We dont have a match %s" % (nameToSearchFor)
                    # Here we must have a new node (or renamed node) so
                    # we go ahead and add a new node to the XML
                    newElement = self.tree.model.domDocument.createElement(QString(testCase[1]))
                    newElement.setAttribute(QString("type"),QString("variable_definition"))                    
                    newElementText = self.tree.model.domDocument.createTextNode(QString(""))
                    newElement.appendChild(newElementText)
                    self.updateNodeFromList(newElement,testCase)
                    self.tree.model.insertRow(self.tree.model.rowCount(self.all_variables_index),
                                              self.all_variables_index,
                                              newElement)
                    self.tree.model.emit(SIGNAL("layoutChanged()"))
            # Now we look for any original nodes that are not in the new list...
            # These have either been renamed or deleted, so we have to look to see if
            # the original was inherited and add the inherited back in if needed
            for i,origTestCase in enumerate(self.originalList):
                # print "Testing if original is in the new list..."
                # Test to see if anything in the original is not in the new list
                weFoundIt = False
                for ii,newTestCase in enumerate(self.tm.arraydata):
                    if origTestCase[1] == newTestCase[1]:
                        weFoundIt = True
                        break
                if not weFoundIt:
                    # print "We have a missing node...%s" % (origTestCase[1])
                    testCaseIndex = self.tree.model.findElementIndexByName(origTestCase[1],self.all_variables_index,False)
                    self.tree.model.removeRow(testCaseIndex[0].internalPointer().row(),
                                              self.tree.model.parent(testCaseIndex[0]))
                    self.tree.model.emit(SIGNAL("layoutChanged()"))
        else:
            #print "Dont need to save"
            pass
        # Now disable the accept changes button
    #    self.saveChanges.setEnabled(False)
        self.dirty = False
        #self.close()

    def on_cancelWindow_released(self):
        #print "cancel pressed"
        saveBeforeClose = QMessageBox.Save
        if self.dirty:
            saveBeforeClose = QMessageBox.question(self,"Warning",
                                                   "Current expressions contain changes... \nShould we accept or discard these changes?",
                                                   QMessageBox.Discard,QMessageBox.Save)
        if saveBeforeClose == QMessageBox.Save:
            self.on_saveChanges_released()
        self.close()

    def on_deleteSelectedVariables_released(self):
        #print "delete pressed"
        self.tm.deleteAllChecked()

    def on_addNewVariable_released(self):
        #print "new pressed"
        #self.tm.insertRow(0,["",
        #                     "New_Node","Dataset","model variable","primary attribute","Description",
        #                     0,0,0])
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = AllVariablesNewGui(self,flags,self)
        window.setModal(True)
        window.show()

    def checkSyntax(self):
        row = self.currentIndex.row()
        success, errors = self.tm.checkSyntax(row = row)
        if success:
            QMessageBox.information(self, 'Variable check results', 'Variable syntax check successful!')
        else:
            errorString = "Parse errors: <br><br>  " + "<br><br>".join(errors)
            QMessageBox.warning(self, 'Variable check results', errorString)
                
    def checkAgainstData(self):
        row = self.currentIndex.row()
        success, errors = self.tm.checkAgainstData(row = row)
        if success:
            QMessageBox.information(self, 'Variable data check results', 'Variable checked successfully against baseyear data!')
        else:
            errorString = "Errors executing expression on baseyear data: <br><br>  " + "<br><br>".join(errors)
            QMessageBox.warning(self, 'Variable check results', errorString)
            
    
    def on_checkSelectedVariables_released(self):
#        saveBeforeCheck = QMessageBox.Yes
#        if self.dirty:
#            saveBeforeCheck = QMessageBox.question(self,"Warning",
#                                                   "Current expressions contain changes... \nShould we accept these changes before checking variables?",
#                                                   QMessageBox.No,QMessageBox.Yes)
#        if saveBeforeCheck == QMessageBox.Yes:
#            self.on_saveChanges_released()
        self.tm.checkSelectedVariables()

    def on_checkAllVariables_released(self):
#        saveBeforeCheck = QMessageBox.Yes
#        if self.dirty:
#            saveBeforeCheck = QMessageBox.question(self,"Warning",
#                                                   "Current expressions contain changes... \nShould we accept these changes before checking variables?",
#                                                   QMessageBox.No,QMessageBox.Yes)
#        if saveBeforeCheck == QMessageBox.Yes:
#            self.on_saveChanges_released()
        self.tm.checkAllVariables()
        

class AllVariablesSelectGui(QDialog, Ui_AllVariablesSelectGui, AllVariablesGui):
    def __init__(self, mainwindow, fl, nodeToUpdate=None, callback=None):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        # Init the super class and let it know that we are an edit GUI
        # last param - 0=edit mode 1=select mode
        AllVariablesGui.__init__(self, mainwindow, fl, False)
        self.pp = pprint.PrettyPrinter(indent=4)
        if nodeToUpdate:
            self.nodeToUpdate = nodeToUpdate
        else:
            self.nodeToUpdate = QDomNode()
        self.callback = callback
        self.tm.initCheckBoxes(self.getCurrentList(self.nodeToUpdate))
        
    def getCurrentList(self,node):
        if not node.isNull():
            # We only want to check out this node if it is of type "element"
            if node.isElement():
                domElement = node.toElement()
                if not domElement.isNull():
                    # Only set the text field to be the string representation of the
                    # python list of selections.
                    # We need to grab the text node from the element
                    if domElement.hasChildNodes():
                        children = domElement.childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                textNode = children.item(x).toText()
                                # Finally set the text node value
                                return map(lambda s: s.strip(), str(textNode.data()).split(','))
        return []
                                
    def updateNodeFromListString(self,node,listString):
        if not node.isNull():
            # We only want to check out this node if it is of type "element"
            if node.isElement():
                domElement = node.toElement()
                if not domElement.isNull():
                    # Only set the text field to be the string representation of the
                    # python list of selections.
                    # We need to grab the text node from the element
                    if domElement.hasChildNodes():
                        children = domElement.childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                textNode = children.item(x).toText()
                                # Finally set the text node value
                                textNode.setData(listString)
                                # Here we have to manually mark the model as dirty since
                                # we are changing out the XML DOM under the models nose
                                self.tree.model.markAsDirty()
                                self.tree.model.emit(SIGNAL("layoutChanged()"))

    def on_saveSelections_released(self):
        #print "save pressed"
        returnList = []
        # Loop through the list of lists and test the check box... if checked then add to the
        # Python list that is returned with selected items
        for i,testCase in enumerate(self.tabledata):
            if testCase[-2]:
                # We have one that is checked... push it into the return list
                returnList.append(str(testCase[1]))
        #self.pp.pprint(returnList)
        returnString = string.join(returnList,', ')
        #print returnString
        if self.nodeToUpdate:
            # We need to fill in the XML node for the client
            self.updateNodeFromListString(self.nodeToUpdate,returnString)
        if self.callback:
            # The client wants to be nodified... send back the list and string
            self.callback(returnList, returnString)
        self.close()

    def on_cancelWindow_released(self):
        #print "cancel pressed"
        self.close()

