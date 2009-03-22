# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

#IGNORE_THIS_FILE
# the tests work, but the test server doesn't have a X-server so it can't 
# start the application process
from opus_core.tests import opus_unittest

from PyQt4.QtGui import QApplication

from PyQt4.QtXml import QDomDocument, QDomElement

from opus_gui.main.controllers.mainwindow import OpusGui
from opus_gui.tests import test_model_dialogs_sample_xml as sample_xml

from opus_gui.models_manager.controllers.dialogs.model_from_template_dialog_base import ModelFromTemplateDialogBase

from opus_gui.models_manager.controllers.dialogs.regression_model_from_template import RegressionModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.simple_model_from_template import SimpleModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.allocation_from_template import AllocationModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.choice_from_template import ChoiceModelFromTemplateDialog
from opus_gui.models_manager.controllers.dialogs.agent_location_choice_from_model import AgentLocationChoiceModelFromTemplateDialog

class TestModelManagerDialogs(opus_unittest.OpusTestCase):
    
    modul = "opus_gui"
    
    def _helper_find_text_value(self, rootnode, textvalue):
        '''traverse the entire sub tree from the rootnode down and look for (text) value. return True if found, False otherwise.'''
        children = rootnode.childNodes()
        
        for subnode_i in xrange(0, children.length()):
            subnode = children.item(subnode_i)
#            if subnode.isElement():
#                print subnode.toElement().tagName()
#                if subnode.firstChild().isText():
#                    print 'txt: %s' %subnode.firstChild().nodeValue()
            if subnode.firstChild().isText() and \
               subnode.firstChild().nodeValue() == textvalue:
                return True
            elif not subnode.firstChild().isNull():
                if self._helper_find_text_value(subnode, textvalue):
                    return True
        return False
    
    def setUp(self):
        '''Provide a framework for testing the gui by setting up a working app instance etc'''
        self.app = QApplication([])
        self.mainwindow = OpusGui()
        
        self.doc = QDomDocument()
        self.doc.setContent(sample_xml.model_templates_xml)
        self.root = self.doc.documentElement()
        
    def test_setup_ok(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.mainwindow is not None)
        self.assertFalse(self.doc.toString() == u'') # assure some data was actually set 
        self.assertTrue(self.doc is not None)
        self.assertFalse(self.root.isNull())
        
    def test_model_dialog_base(self):
        # test_model_element = self.doc.firstChildElement('simple_model_template')
        
        dummy_e = self.root.firstChildElement('dummy_model')
        dialog = ModelFromTemplateDialogBase(self.mainwindow,
                                             dummy_e, None)

        self.assertTrue(dummy_e is not None)
        self.assertTrue(isinstance(dummy_e, QDomElement) and 
                        (not dummy_e.isNull()))
        
        self.assertTrue(dialog is not None, 'Did not create dialog')
        
        # make sure that the name is transformed back and forth from the dialog
        # as it should
        name_after_init = dialog.leModelName.text()
        name_from_get_name = dialog.get_model_xml_name()
        
        self.assertTrue(name_after_init == 'dummy model')
        self.assertTrue(name_from_get_name == 'dummy_model')
        
        pre_name = dialog.model_template_node.toElement().tagName()
        dialog.set_model_name()
        self.assertTrue(dialog.model_template_node.toElement().tagName() == \
                        dialog.get_model_xml_name())
        dialog.set_model_name('gunk')
        self.assertTrue(dialog.model_template_node.toElement().tagName() == \
                        'gunk')
        
        dummy_child = dummy_e.firstChildElement('structure'). \
                    firstChildElement('dummy_child')
        cur_text = dummy_child.firstChild().nodeValue()
        new_text = 'splendid'
        dialog.set_structure_element_to_value('dummy_child', new_text)
        # make sure the structure element was set correctly
        self.assertEquals(dummy_child.firstChild().nodeValue(), new_text)
        # trying to set nonexisting paths should raise value error
        self.assertRaises(ValueError,
                          dialog.set_structure_element_to_value, 
                          'some/nonexisting/path/', 
                          new_text)
        
        
    def test_simple_model_dialog(self):
        template_node = self.root.firstChildElement('simple_model_template').cloneNode().toElement()
        
        dialog = SimpleModelFromTemplateDialog(self.mainwindow, template_node, None)
        
        self.assertTrue(dialog is not None)
        self.assertTrue(template_node is not None)
        
        # make sure that all fields with text value 'fill in' are indeed filled in by setup
        dialog.setup_node()
        self.assertFalse(self._helper_find_text_value(template_node, 'fill in'))

    def test_agent_location_model_dialog(self):
        template_node = self.root.firstChildElement('agent_location_choice_model_template').cloneNode().toElement()
        dialog = AgentLocationChoiceModelFromTemplateDialog(self.mainwindow, template_node, None)

        self.assertTrue(dialog is not None)
        self.assertTrue(template_node is not None)
        
        # make sure that all fields with text value 'fill in' are indeed filled in by setup
        dialog.setup_node()
        self.assertFalse(self._helper_find_text_value(template_node, 'fill in'))
        
    def test_allocation_model_dialog(self):
        template_node = self.root.firstChildElement('allocation_model_template').cloneNode().toElement()
        dialog = AllocationModelFromTemplateDialog(self.mainwindow, template_node, None)

        self.assertTrue(dialog is not None)
        self.assertTrue(template_node is not None)

        # make sure that all fields with text value 'fill in' are indeed filled in by setup
        dialog.setup_node()
        self.assertFalse(self._helper_find_text_value(template_node, 'fill in'))

    def test_choice_model_dialog(self):
        template_node = self.root.firstChildElement('choice_model_template').cloneNode().toElement()
        dialog = ChoiceModelFromTemplateDialog(self.mainwindow, template_node, None)

        self.assertTrue(dialog is not None)
        self.assertTrue(template_node is not None)
        
        # make sure that all fields with text value 'fill in' are indeed filled in by setup
        dialog.setup_node()
        self.assertFalse(self._helper_find_text_value(template_node, 'fill in'))

    def test_regression_model_dialog(self):
        template_node = self.root.firstChildElement('regression_model_template').cloneNode().toElement()
        dialog = RegressionModelFromTemplateDialog(self.mainwindow, template_node, None)

        self.assertTrue(dialog is not None)
        self.assertTrue(template_node is not None)

        # make sure that all fields with text value 'fill in' are indeed filled in by setup
        dialog.setup_node()
        self.assertFalse(self._helper_find_text_value(template_node, 'fill in'))

    def tearDown(self):
        pass
    
if __name__ == '__main__':
    opus_unittest.main()