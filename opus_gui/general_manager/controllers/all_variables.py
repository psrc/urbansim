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

from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.general_manager.models.all_variables_table_model import AllVariablesTableModel
from opus_gui.general_manager.views.all_variables_table_view_delegate import AllVariablesTableViewDelegate
from opus_gui.general_manager.views.ui_all_variables_edit import Ui_AllVariablesEditGui
from opus_gui.general_manager.views.ui_all_variables_select import Ui_AllVariablesSelectGui
from opus_gui.general_manager.views.ui_all_variables_new import Ui_AllVariablesNewGui
from opus_gui.general_manager.run.variable_validator import VariableValidator
from opus_core.variables.variable_name import VariableName
from xml.etree.cElementTree import Element

import random,pprint,string

class AllVariablesNewGui(QDialog, Ui_AllVariablesNewGui):
    def __init__(self, opus_gui, fl, allVariablesGui, row = 0, initialParams = None, create_new_from_old = False):
        QDialog.__init__(self, opus_gui, fl)
        self.setupUi(self)
        self.allVariablesGui = allVariablesGui
        self.initialParams = initialParams
        self.row = row
        self.opus_gui = opus_gui
        self.parent = opus_gui

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
            #self._setup_co_dataset_name(value = self.initialParams[1])
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
        #else:
            #self._setup_co_dataset_name()

#    def _setup_co_dataset_name(self, value = None):
#        from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper
#        xml_helper = ResultsManagerXMLHelper(self.mainwindow.toolboxBase)
#
#        available_datasets = xml_helper.get_available_datasets()
#
#        for dataset in available_datasets:
#            self.cbo_dataset_name.addItem(QString(dataset))
#
#        if value is not None:
#            idx = self.cbo_dataset_name.findText(value)
#            if idx != -1:
#                self.dataset_name = value
#                self.cbo_dataset_name.setCurrentIndex(idx)

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
        project = self.opus_gui.project
        success, errors = VariableValidator(project).check_parse_errors(variables = [self._get_variable_definition()])

        if success:
            MessageBox.information(mainwindow = self,
                              text = 'Variable syntax check successful!',
                              detailed_text = '')
        else:
            errorString = "Parse errors: <br><br>  " + "<br><br>".join(errors)
            MessageBox.warning(mainwindow = self,
                              text = "There is a variable syntax error.",
                              detailed_text = errorString)

    def on_cboCheckData_released(self):
        success, errors = VariableValidator(toolboxBase=self.mainwindow.toolboxBase).check_data_errors(variables = [self._get_variable_definition()])
        if success:
            MessageBox.information(mainwindow = self,
                              text = 'Variable checked successfully against baseyear data!',
                              detailed_text = '')
        else:
            MessageBox.warning(mainwindow = self,
                              text = "There was an error executing the variable on the baseyear data.",
                              detailed_text = "<br><br>".join(errors))



    def _get_variable_definition(self):
        variable_name = str(self.lineEdit.text())

        if self.cbIndicatorUse.isChecked():
            if self.cbModelUse.isChecked():
                use = 'both'
            else:
                use = 'indicator'
        elif self.cbModelUse.isChecked():
            use = 'model variable'
        else:
            MessageBox.warning(mainwindow = self,
                              text = 'The variable must have a use (Indicator and/or Model variable) specified!',
                              detailed_text = '')
            
            return None
        source = str(self.comboBox_2.currentText())
        definition = str(self.textEdit.toPlainText())
        n = VariableName(expression = definition)
        dataset_name = n.get_dataset_name()
        if dataset_name is None:
            # TODO: FIX THIS -- LOOK UP THE TUPLE IN THE AVAILABLE DATASETS
            p = n.get_interaction_set_names()
            if len(p)==2:
                dataset_name = p[0] + '_x_' + p[1]
            else:
                raise ValueError, "couldn't determine interaction set name for %s" % definition
        return (variable_name, dataset_name, use, source, definition)


class AllVariablesGui(object):
    def __init__(self, opus_gui, editable):
        #if edit_select:
        #    print "Select GUI"
        #else:
        #    print "Edit GUI"
        self.opus_gui = opus_gui
        model = opus_gui.managers['general'].xml_controller.model
        index = None
        for i in range(0, model.rowCount(QModelIndex())):
            index = model.index(i, 0, QModelIndex())
            if index.internalPointer().node.tag == 'expression_library':
                break
        if index is None:
            print 'Could not find expression_library in general managers visible tree'
            return

        self.all_variables_index = index

        # Is the tableview dirty?
        self.dirty = False

        #Add a default table
        tv = QTableView()
        delegate = AllVariablesTableViewDelegate(tv)
        tv.setItemDelegate(delegate)
        tv.setSortingEnabled(True)
        tv.setColumnWidth(0, 25) # adjust size to fit check box
#        tv.setSelectionBehavior(QTableView.SelectRows)

        # So we have a data structure to define the headers for the table...
        # The first element is empty string because it is over the check box
        header = ["","Name","Dataset","Use","Source","Definition"]
        tabledata = []
        self.tabledata = tabledata
        # Grab the general section...
        tree = self.opus_gui.managers['general'].xml_controller
        self.tree = tree
        dbxml = tree.model.index(0,0,QModelIndex()).parent()
        expression_lib_node = self.opus_gui.project.find('./general/expression_library')
        if not expression_lib_node:
            print 'No expression library in project'
            return
        all_variables = []
        self.variable_nodes = expression_lib_node[:]
        for var in expression_lib_node:
            tslist = ['', var.tag, var.get('dataset'), var.get('use'),
                      var.get('source'), var.text ]
            if var.get('inherited'):
                tslist.extend([1, 0, 0])
            else:
                tslist.extend([0, 0, 0])
            all_variables.append(tslist)
        self.originalList = list(all_variables)

        for i,origListItem in enumerate(all_variables):
            self.originalList[i] = list(origListItem)

        tm = AllVariablesTableModel(all_variables, header, self, editable, self.opus_gui)
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
    def __init__(self, opus_gui, flags):
        '''
        @param opus_gui (OpusGui): application main window
        '''
        QDialog.__init__(self, opus_gui, flags)
        self.setupUi(self)
        # Init the super class and let it know that we are an edit GUI
        # last param - 0=edit mode 1=select mode
        AllVariablesGui.__init__(self, opus_gui, True)

        self.opus_gui = opus_gui

        # For now, disable the save button until we implement the write in the model...
#        self.saveChanges.setEnabled(False)

        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.editIcon = QIcon(":/Images/Images/application_edit.png")

        self.actRemoveRow = QAction(self.removeIcon,
                                    "Remove Variable",
                                    self)
        QObject.connect(self.actRemoveRow,
                        SIGNAL("triggered()"),
                        self.removeRow)

        self.actEditRow = QAction(self.editIcon,
                                  "Edit Variable",
                                  self)
        QObject.connect(self.actEditRow,
                        SIGNAL("triggered()"),
                        self.editRow)

        self.actCreateNewFromOld = QAction(self.editIcon,
                                  "Create new variable based on this variable",
                                  self)
        QObject.connect(self.actCreateNewFromOld,
                        SIGNAL("triggered()"),
                        self.createVariableLike)


        self.actCheckSyntax = QAction(self.editIcon,
                                  "Check Syntax",
                                  self)
        QObject.connect(self.actCheckSyntax,
                        SIGNAL("triggered()"),
                        self.checkSyntax)

        self.actCheckAgainstData = QAction(self.editIcon,
                                  "Check Against Data",
                                  self)
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
        window = AllVariablesNewGui(self.opus_gui, flags,self,row,initialParams)
        window.setModal(True)
        window.show()

    def createVariableLike(self):
        #print "Remove Row Pressed"
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        row = self.currentIndex.row()
        initialParams = self.currentIndex.model().getRowDataList(self.currentIndex)
        window = AllVariablesNewGui(self.opus_gui, flags,self, initialParams = initialParams, create_new_from_old = True)
        window.setModal(True)
        window.show()

    def processCustomMenu(self, position):
        #print "Custom Menu"
        if self.tv.indexAt(position).isValid():
            self.currentColumn = self.tv.indexAt(position).column()
            self.currentIndex = self.tv.indexAt(position)
            self.menu = QMenu(self.tv)
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

    def findOriginalNode(self, list):
        for node in self.variable_nodes:
            if node.tag == list[1]:
                return node
        return None

    def updateNodeFromList(self,node,list):
        if node is None: return
        node.tag = str(list[1])
        node.set('dataset', str(list[2]))
        node.set('use', str(list[3]))
        node.set('source', str(list[4]))
        node.text = str(list[5])
        self.opus_gui.project.dirty = True
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
            for i, testCase in enumerate(self.tm.arraydata):
                # Find the XML node that has the tag name in column 1
                nameToSearchFor = testCase[1]
                foundInOriginal = False
                for node in self.variable_nodes:
                    # Now we have a valid variable, we fill in the set for display
                    if node.tag == nameToSearchFor:
                        foundInOriginal = True

                if foundInOriginal:
                    # print "We have a match %s" % (nameToSearchFor)
                    # If the data is dirty we need to update the node
                    if testCase[-1]:
                        nodeToUpdate = self.findOriginalNode(testCase)
                        self.updateNodeFromList(nodeToUpdate,testCase)
                        # Temporary hack until we have a new variable library editor
                        # we normally make items editable but here we only have
                        # the node as a reference. So first we resolve the node path
                        # and then we select the item in that path
                        def node_item_in_subtree(node, this_item):
                            if this_item.node == node:
                                return this_item
                            else:
                                # check if any of the children contains the node
                                for child_item in this_item.child_items:
                                    found_item = node_item_in_subtree(node, child_item)
                                    if found_item is not None:
                                        return found_item
                            return None
                        item = node_item_in_subtree(nodeToUpdate,
                                                    self.tree.model.root_item())
                        if item is not None:
                            self.tree.model.makeItemEditable(item)
                else:
                    # print "We don't have a match %s" % (nameToSearchFor)
                    # Here we must have a new node (or renamed node) so
                    # we go ahead and add a new node to the XML
                    node = Element('', {'type':'variable_definition'})
                    self.updateNodeFromList(node,testCase)
                    self.tree.model.insertRow(self.tree.model.rowCount(self.all_variables_index),
                                              self.all_variables_index,
                                              node)
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
                    start_index = self.tree.model.index(0, 0, self.all_variables_index)
                    row_count = self.tree.model.rowCount(self.all_variables_index)
                    index = None
                    for i in range(0, row_count):
                        index = self.tree.model.index(i, 0, self.all_variables_index)
                        if index.internalPointer().node.tag == origTestCase[1]:
                            break
                    self.tree.model.removeRow(index.row(), self.all_variables_index)
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
        window = AllVariablesNewGui(self.opus_gui, flags,self)
        window.setModal(True)
        window.show()

    def checkSyntax(self):
        row = self.currentIndex.row()
        success, errors = self.tm.checkSyntax(row = row)
        
        if success:
            MessageBox.information(mainwindow = self,
                              text = 'Variable syntax check successful!',
                              detailed_text = '')
        else:
            errorString = "Parse errors: <br><br>  " + "<br><br>".join(errors)
            MessageBox.warning(mainwindow = self,
                              text = "There is a variable syntax error.",
                              detailed_text = errorString)

    def checkAgainstData(self):
        row = self.currentIndex.row()
        success, errors = self.tm.checkAgainstData(row = row)
        if success:
            MessageBox.information(mainwindow = self,
                              text = 'Variable checked successfully against baseyear data!',
                              detailed_text = '')
        else:
            MessageBox.warning(mainwindow = self,
                              text = "There was an error executing the variable on the baseyear data.",
                              detailed_text = "<br><br>".join(errors))

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
    def __init__(self, opus_gui, nodeToUpdate=None, callback=None):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | \
            Qt.WindowMaximizeButtonHint
        QDialog.__init__(self,opus_gui, flags)
        self.setupUi(self)

        self.setModal(True)

        # Init the super class and let it know that we are an edit GUI
        # last param - 0=edit mode 1=select mode
        AllVariablesGui.__init__(self, opus_gui, False)
        self.pp = pprint.PrettyPrinter(indent=4)
        self.nodeToUpdate = nodeToUpdate
        self.callback = callback
        self.tm.initCheckBoxes(self.getCurrentList(self.nodeToUpdate))

    def getCurrentList(self, node):
        node_text = node.text
        if node is None:
            return []
        node_text = node_text.strip()
        return [var_name for var_name in node_text.split(',')]

    def updateNodeFromListString(self,node,listString):
        node.text = listString
        self.opus_gui.project.dirty = True
        self.tree.model.emit(SIGNAL("layoutChanged()"))

    def on_saveSelections_released(self):
        # print "save pressed"
        returnList = []
        # Loop through the list of lists and test the check box... if checked then add to the
        # Python list that is returned with selected items
        for i, testCase in enumerate(self.tabledata):
            if testCase[-2]:
                # We have one that is checked... push it into the return list
                returnList.append(str(testCase[1]))

        # The variable selector has no way of differenting variables with same
        # name but different definitions appart. This results in two variables
        # (or more), with the same name but different dataset, being selected
        # in the selector. If the user clicks accept selection, all of these
        # names will end up in returnList which is not what we want.
        # For now we 'solve' this by just filter out duplicates.
        returnList = list({}.fromkeys(returnList))

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

