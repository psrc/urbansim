# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.abstract_manager.controllers.xml_configuration.renamedialog import * #@UnusedWildImport
from opus_core.tests.opus_gui_unittest import OpusGUITestCase

class RenameTest(OpusGUITestCase):

    def setUp(self):
        pass

    def test_rename(self):
        name = 'new name'
        d = RenameDialog(name, [], None)
        self.assertEqual(d.leName.text(), name)
        d.on_buttonBox_accepted()
        self.assertEqual(d.accepted_name, name)

        name = 'changed name'
        d.leName.setText(name)
        d.on_buttonBox_accepted()
        self.assertEqual(d.accepted_name, name)

        name = 'will never leave the dialog'
        d = RenameDialog(name, [], None)
        d.on_buttonBox_rejected()
        self.assertNotEqual(d.accepted_name, name)

    def test_not_unique_name(self):
        taken_names = ['guppy', 'squid', 'unicorn']
        not_unique = taken_names[0]
        d = RenameDialog(not_unique, taken_names, None)
        d.on_buttonBox_accepted()
        self.assert_(d.lbl_name_warning.isVisible())
        unique = 'french fries'
        d.leName.setText(unique)
        d.on_buttonBox_accepted()
        self.assert_(d.accepted_name == unique)
