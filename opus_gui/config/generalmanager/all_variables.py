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

from opus_gui.config.xmlmodelview.opusallvariablestablemodel import OpusAllVariablesTableModel
from opus_gui.config.xmlmodelview.opusallvariablesdelegate import OpusAllVariablesDelegate
from opus_gui.config.generalmanager.all_variables_edit_ui import Ui_AllVariablesEditGui
from opus_gui.config.generalmanager.all_variables_select_ui import Ui_AllVariablesSelectGui

import random,pprint,string

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
        delegate = OpusAllVariablesDelegate(tv)
        tv.setItemDelegate(delegate)
        tv.setSortingEnabled(True)
        
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
        tm = OpusAllVariablesTableModel(tabledata, header, self, editable)
        self.tm = tm
        self.tv = tv
        tv.setModel(tm)
        tv.setColumnWidth(0,25)
        #tv.selectColumn(1)
        tv.horizontalHeader().setStretchLastSection(True)
        tv.setTextElideMode(Qt.ElideNone)
        self.gridlayout.addWidget(tv)


class AllVariablesEditGui(QDialog, Ui_AllVariablesEditGui, AllVariablesGui):
    def __init__(self, mainwindow, fl):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        # Init the super class and let it know that we are an edit GUI
        # last param - 0=edit mode 1=select mode
        AllVariablesGui.__init__(self, mainwindow, fl, True)

        # For now, disable the save button until we implement the write in the model...
        self.saveChanges.setEnabled(False)

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
            for i,testCase in enumerate(self.tabledata):
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
                for ii,newTestCase in enumerate(self.tabledata):
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
            print "Dont need to save"
        self.close()

    def on_cancelWindow_released(self):
        #print "cancel pressed"
        self.close()

    def on_deleteVariables_released(self):
        #print "delete pressed"
        self.tm.deleteAllChecked()

    def on_addNewVariable_released(self):
        #print "new pressed"
        self.tm.insertRow(0,["",
                             "New_Node","Dataset","Use","Source","Description",
                             0,0,0])


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

