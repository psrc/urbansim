# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QString, Qt, QVariant
from PyQt4.QtGui import QFileDialog, QItemDelegate, QComboBox, QLineEdit

class XmlItemDelegate(QItemDelegate):
    '''
    Handles creation of editors depending on attributes for the node to edit
    '''

    def __init__(self, parent_view):
        '''
        @param parent_view (QAbstractItemView): parent view for this item editor
        '''
        QItemDelegate.__init__(self, parent_view)
        self.parent_view = parent_view

        # List of database connection names -- used for populating the editor
        # for a db_connection_hook
        self.known_db_connection_names = []

    def createEditor(self, parent_view, option, index):
        ''' PyQt API Method -- See the PyQt documentation for a description '''

        default_editor = QItemDelegate.createEditor(self, parent_view,
                                                    option, index)
        if not index.isValid():
            # Use default editor
            return default_editor

        item = index.internalPointer()
        node = item.node

        if index.column() == 0:
            # Use the default editor for tag name editing
            # Note: Editing the first column is currently disabled in XmlModel
            if type(default_editor) == QLineEdit:
                # Fill in the tag
                default_editor.setText(node.tag)
            return default_editor

        elif index.column() == 1:
            # Combobox for multiple choices
            editor = default_editor
            if node.get('choices') is not None:
                editor = QComboBox(parent_view)
                choices = [s.strip() for s in node.get('choices').split('|')]
                for item in choices:
                    editor.addItem(item)
                # Select the current choice
                choice = node.text.strip() if node.text else ''
                if choice in choices:
                    editor.setCurrentIndex(choices.index(choice))
            # Select database connection
            elif node.get('type') == 'db_connection_hook':
                editor = QComboBox(parent_view)
                # Get connection names from database_server_connections.xml
                choices = self.known_db_connection_names
                # Populate the editor with the choices
                for i in choices:
                    editor.addItem(i)
            # Select files and folders
            elif node.get('type') in ('file_path', 'dir_path'):
                editor_file = QFileDialog()
                filter_str = QString("*.*")
                editor_file.setFilter(filter_str)
                editor_file.setAcceptMode(QFileDialog.AcceptOpen)
                current_value = \
                    index.model().data(index, Qt.DisplayRole).toString()
                if node.get('type') == 'file_path':
                    method = editor_file.getOpenFileName
                    title = 'Please select a file...'
                else:
                    method = editor_file.getExistingDirectory
                    title = 'Please select a directory...'
                fd = method(self.parent_view, title, current_value)

                # Check for cancel
                if len(fd) == 0:
                    new_value = current_value
                else:
                    new_value = QString(fd)
                editor = QItemDelegate.createEditor(self, self.parent_view,
                                                    option, index)
                if type(editor) == QLineEdit:
                    editor.setText(new_value)
            # Edit passwords
            elif node.get('type') == 'password':
                editor.setText(str(node.text or ''))
                editor.setStyleSheet('QLineEdit { background-color: red }')
                # If we want to never show the characters, use
                # QLineEdit.Password
                editor.setEchoMode(QLineEdit.PasswordEchoOnEdit)
            # Use default editor
            else:
                if type(editor) == QLineEdit:
                    txt = index.model().data(index, Qt.DisplayRole).toString()
                    editor.setText(txt)

            return editor

    def setEditorData(self, editor, index):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        pass

    def setModelData(self,editor, model, index):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        if type(editor) == QComboBox:
            model.setData(index, QVariant(editor.currentText()), Qt.EditRole)
        else:
            QItemDelegate.setModelData(self, editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        if type(editor) == QComboBox:
            editor.setGeometry(option.rect)
        else:
            QItemDelegate.updateEditorGeometry(self, editor, option, index)
