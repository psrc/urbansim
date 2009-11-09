# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import * #@UnusedWildImport

from lxml.etree import Element, fromstring

from opus_gui.tests.mockup_manager import MockupManager

from opus_core.tests.opus_gui_unittest import OpusGUITestCase

class TestXmlController(OpusGUITestCase):

    def _make_ctrl(self, xml):
        mgr = MockupManager(xml, 'parent')
        return XmlController(mgr)

    def test_get_unique_name_like_node(self):
        xml = \
        '''
        <opus_project>
         <parent>
          <child name="unique" />
          <child name="not unique" />
          <child name="Copy of not unique" />
          <child name="abundant" />
          <child name="Copy of abundant" />
          <child name="Copy 1 of abundant" />
          <child name="Copy 2 of abundant" />
          <child name="Copy 3 of abundant" />
         </parent>
        </opus_project>
        '''
        xctrl = self._make_ctrl(xml)
        project = xctrl.project
        unique_node = project.find('parent/child', name = 'unique')
        not_unique_node = project.find('parent/child', name = 'not unique')
        abundant_node = project.find('parent/child', name = 'abundant')
        # there's no node named 'brand new' so it should be a unique name
        brand_new_node = Element('child', {'name': 'brand new'})
        self.assertEqual(xctrl._get_unique_name_like_node(brand_new_node), 'brand new')
        # there's already a node named unique, so the unique name would be Copy of...
        self.assertEqual(xctrl._get_unique_name_like_node(unique_node), 'Copy of unique')
        # already a copy of Copy of... start counting
        self.assertEqual(xctrl._get_unique_name_like_node(not_unique_node), 'Copy 1 of not unique')
        # and continue counting...
        self.assertEqual(xctrl._get_unique_name_like_node(abundant_node), 'Copy 4 of abundant')
