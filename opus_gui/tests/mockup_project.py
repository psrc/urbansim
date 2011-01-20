# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
#

from opus_gui.main.opus_project import OpusProject
from opus_core.configurations.xml_configuration import XMLConfiguration
from lxml.etree import tostring

class MockupOpusProject(OpusProject):

    '''
    Mockup class for creating a fake Opus project
    '''

    def __init__(self, xml = '<opus_project />'):
        OpusProject.__init__(self)
        xml_config = XMLConfiguration()
        xml_config.update(xml)
        self._read_xml_from_config(xml_config)

if __name__ == '__main__':
    instance = MockupOpusProject()
    print 'XML Data:'
    print tostring(instance._root_node)
