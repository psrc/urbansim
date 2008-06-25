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
from PyQt4.QtCore import QString, QObject, SIGNAL, QRegExp, QSize, Qt, QVariant
from PyQt4.QtGui import QDialog, QVBoxLayout, QFrame, QWidget, QHBoxLayout, QLabel, QPalette, QLineEdit


from opus_gui.results.forms.edit_indicator_ui import Ui_dlgEditIndicator
from opus_gui.results.xml_helper_methods import get_child_values, ResultsManagerXMLHelper

class EditIndicatorDialog(QDialog, Ui_dlgEditIndicator):
    def __init__(self, resultManagerBase, selected_index):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint

        QDialog.__init__(self, resultManagerBase.mainwindow, flags)
        self.setupUi(self)
        self.resultManagerBase = resultManagerBase
        self.model = resultManagerBase.toolboxStuff.resultsManagerTree.model
        self.selected_index = selected_index
        #fill in existing values...
        if self.selected_index is not None:
            base_node = self.selected_index.internalPointer().node()
            cur_vals = get_child_values(parent = base_node,
                                        child_names = ['package','expression'])
            self.txtIndicator_name.setText(base_node.nodeName())
            self.txtPackage_name.setText(cur_vals['package'])
            self.txtExpression.setText(cur_vals['expression'])
    
        
    def on_buttonBox_accepted(self):
        indicator_name = self.txtIndicator_name.text()
        package_name = self.txtPackage_name.text()
        expression = self.txtExpression.text()
        
        if self.selected_index is not None:
#            indicator_name = QVariant(indicator_name)
#            package_name = QVariant(package_name)
#            expression = QVariant(expression)
            
            # Keep track of any edits so we can mark the GUI as edited and force a save
            # as well as make the node editable if it is not already...
            dirty = False

            # Grab the base node... this is a QDomNode
            base_node = self.selected_index.internalPointer().node()
            if not base_node.isNull():
                # We only want to check out this node if it is of type "element"
                if base_node.isElement():
                    domElement = base_node.toElement()
                    if not domElement.isNull():
                        # Now we check to see if the tagname is the one we are looking for
                        name = str(domElement.tagName())
                        # and more importantly if it has changed... we only update on a changed value
                        if name != indicator_name:
                            # This path is to allow us to verify if the node being modified
                            # is inherited and needs to be added back in
                            domNodePath = self.model.domNodePath(base_node)
                            # Actually update the tagname
                            domElement.setTagName(QString(indicator_name))
                            # Now search and check if inherited and needs to be added back in to tree
                            self.model.checkIfInheritedAndAddBackToTree(domNodePath, self.selected_index.parent())
                            # We have made updates so we need to do the "dirty stuff" later
                            dirty = True

            # Lets avoid calling setData directly... Will create a new method that will do the above
            #self.model.setData(self.selected_index,QVariant(indicator_name),Qt.EditRole)
            
            vals = {
                    'package': package_name,
                    'expression': expression
            }

            # Get the first child node (also a QDomNode) for traversal
            node = base_node.firstChild()
            
            # Only march on if we have non-null nodes
            while not node.isNull():
                # We only want to check out this node if it is of type "element"
                if node.isElement():
                    domElement = node.toElement()
                    if not domElement.isNull():
                        # Now we check to see if the tagname is the one we are looking for
                        name = str(domElement.tagName())
                        if name in vals:
                            # We have a match se we need to grab the text node for the element
                            elementText = str(domElement.text())
                            # If the text node value has changed we need to update
                            if elementText != vals[name]:
                                # We need to grab the text node from the element
                                if domElement.hasChildNodes():
                                    children = domElement.childNodes()
                                    for x in xrange(0,children.count(),1):
                                        if children.item(x).isText():
                                            textNode = children.item(x).toText()
                                            # Finally set the text node value
                                            textNode.setData(vals[name])
                                            # We have made this element dirty so we need to mark it all dirty
                                            dirty = True
                # Continue to loop through children
                node = node.nextSibling()
                
            # TODO: Should gather all of this into a method in the model to allow for bulk update
            if dirty:    
                # If we have changed something we need to make sure the node we are editing is marked
                # as editable since there was no check that the node was editable before allowing
                # the right click edit option.
                self.model.makeEditable(base_node)
                # Flag the model as dirty to prompt for save
                self.model.markAsDirty()

        else:
            xml_helper = ResultsManagerXMLHelper(self.resultManagerBase.toolboxStuff)
            xml_helper.addNewIndicator(indicator_name = indicator_name, 
                                       package_name = package_name, 
                                       expression = expression)
            
        self.close()

    def on_buttonBox_rejected(self):
        self.close()

