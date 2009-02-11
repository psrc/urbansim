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

from PyQt4.QtCore import QString, SIGNAL, QSize, Qt
from PyQt4.QtGui import QHBoxLayout, QSizePolicy, QDialog
from PyQt4.QtXml import QDomElement

from opus_gui.models_manager.views.ui_model_from_template_dialog_base import Ui_ModelFromTemplateDialogBase

class ModelFromTemplateDialogBase(QDialog, Ui_ModelFromTemplateDialogBase):
    '''Base dialog class to allow for easy creation of more specific model
    template creation dialogs

    When the user clicks the OK button, this base calls the method
    setup_node() before inserting the cloned node into the model tree. Child
    dialogs should implement and handle their modification of the template
    node (self.model_template_node) in that method. They should not call
    _insert_model_and_create_estimation() or implement their own
    _on_accepted() or _on_rejected() methods.

    Models that do not have estimation components should set the instance
    variable create_estimation_component to False.
    '''
    def __init__(self, model_node, project = None, callback = None,
                 parent_widget = None):
        '''
        @param project (OpusProject): Currently loaded project
        @param model_node (Element): template node to base the new model on
        @param parent_widget (QObject): parent object
        @param callback (function(Element)): callback function for the
            modified node
        '''
        # parent window for the dialog box
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | \
                Qt.WindowMaximizeButtonHint | Qt.Sheet
        QDialog.__init__(self, parent_widget, flags)
        self.setupUi(self)

        self.model_node = model_node
        self.callback = callback
        self.project = project

        self.connect(self.buttonBox, SIGNAL("accepted()"), self._on_accepted)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self._on_rejected)

        self.setModal(True)

        # Base the default tag name on the tag for the template
        tag_name = model_node.tag.replace('_template', '')\
            .replace('_', ' ')
        self.leModelName.setText(tag_name)
        self.leModelName.selectAll()
        self.leModelName.focusWidget()

        title = str(self.windowTitle())
        newtitle = '%s %s'%(title, tag_name)
        self.setWindowTitle(QString(newtitle))

    def _add_widget_pair(self, left_widget, right_widget):
        '''Add a pair of widgets to the dialog.'''
        # make the leftmost widget (usually a label) constraint to a certain
        # size to maintain a nice grid
        left_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                              QSizePolicy.MinimumExpanding))
        right_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                               QSizePolicy.Maximum))

        left_widget.setMinimumSize(QSize(100, 0))
        left_widget.setMaximumSize(QSize(200, 16777215))

        layout = QHBoxLayout()
        layout.addWidget(left_widget)
        layout.addWidget(right_widget)
        self.groupBox.layout().addLayout(layout)

    def _get_xml_friendly_name(self):
        '''return a valid model name based on the string the user entered'''
        #TODO: make sure that the name is actually a valid XML tag
        return self.leModelName.text().replace(QString(' '), QString('_'))

    def _set_model_node_tag(self, value = None):
        '''set the name of the root node to a valid XML value.
        Default value is self.get_valid_model_name().'''
        xmlname = value if value is not None else self.get_valid_model_name()
        self.model_node.tag = xmlname

    def setup_node(self):
        ''' (Abstract) Setup the node based on values in the dialog. '''
        # code that sets the specific template variables goes here
        pass

    def _on_accepted(self):
        # Setup the model node before calling the callback
        self.setup_node()
        # Set correct type
        self.model_node.set('type', 'model')

        # Make sure we don't have any QStrings left in the node
        for node in self.model_node.getiterator():
            # Make sure all nodes tag, attribute values and texts are str()
            node.tag = str(node.tag)
            for key, value in node.attrib.items():
                node.attrib[key] = str(value)
            if node.text is not None:
                node.text = str(node.text)
        if self.callback:
            self.callback(self.model_node)
        self.close()

    def _on_rejected(self):
        self.close()
