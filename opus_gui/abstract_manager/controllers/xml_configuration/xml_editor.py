from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from opus_gui.abstract_manager.views.ui_xml_editor import Ui_XML_Editor
from lxml.etree import tostring, fromstring
from opus_gui.main.controllers.dialogs.message_box import MessageBox
from PyQt5 import QtCore

class XML_Editor_Gui(QDialog, Ui_XML_Editor):
    ATTENTION = '''Attention: This function didn't check whether the syntax makes sense to OPUS.  It just checks for a valid XML structure.'''
    
    def __init__(self, opus_gui_window, xml_controller, base_node):
        '''
        Dialog box for editing XML Data.
        @param opus_gui_window (OpusGui): Parent Opus Main Window
        @param xml_controller (XmlController): Parent XML controller
        @param base_node (Element): Base XML node to edit
        '''
        QDialog.__init__(self, opus_gui_window, QtCore.Qt.Window)
        self.setupUi(self)
        self.xml_controller = xml_controller
        self._base_node = base_node
        self._initTextBox()
        self.edited_node = None

    def _initTextBox(self):
        self.textEdit.setText(tostring(self._base_node))
        
    def _getXMLAsNode(self):
        return fromstring(str(self.textEdit.toPlainText()))
        
    def _checkImportNode(self):
        node = self._getXMLAsNode()
        self.xml_controller.check_import_node(self._base_node, node)
        return node
    
    def _checkImportNodeMsg(self):
        try:
            return self._checkImportNode()
        except Exception as e:
            MessageBox.error(self, 'This is not a valid XML structure.', \
                             '''%s.\n\n%s''' % (e, self.ATTENTION))
            return None

    @pyqtSlot()
    def on_okButton_clicked(self):
        node = self._checkImportNodeMsg()
        if node is None:
            return

        self.edited_node = node
        self.accept()

    @pyqtSlot()
    def on_cancelButton_clicked(self):
        self.edited_node = None
        self.reject()
        
    @pyqtSlot()
    def on_revertButton_clicked(self):
        self._initTextBox()
    
    @pyqtSlot()
    def on_syntaxButton_clicked(self):
        node = self._checkImportNodeMsg()
        if node is None:
            return
        
        MessageBox.information(self, 'Check passed!',
                               self.ATTENTION)
