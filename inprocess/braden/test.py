# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import opus_core.tests.opus_unittest
import sys
try:
    import lxml.etree
except:
    pass

class TestXMLSchema(opus_core.tests.opus_unittest.OpusTestCase):

    def setUp(self):
        pass

    def test_configs(self):
        xmlschema_file = open("inprocess/braden/opus_project.xsd","r")
        xml_files = []
        xml_files.append(open("urbansim/configs/urbansim.xml","r"))
        xml_files.append(open("urbansim_parcel/configs/urbansim_parcel.xml","r"))
        xml_files.append(open("seattle_parcel/configs/seattle_parcel.xml","r"))
        self.validate_xml(xml_files, xmlschema_file)

    def validate_xml(self, xml_files, xmlschema_file):
        if "lxml" in globals():
            xmlschema_doc = lxml.etree.parse(xmlschema_file)
            xmlschema = lxml.etree.XMLSchema(xmlschema_doc)
            error = False
            message = "XML validation error:\n"
            for xml_file in xml_files:
                xml_doc = lxml.etree.parse(xml_file)
                result = xmlschema.validate(xml_doc)
                if not result:
                    error = True
                    error_log = xmlschema.error_log
                    for error in error_log:
                        message += "  %s, line %s, col %s:\n" % (error.filename, str(error.line), str(error.column))
                        message += "    [%s] %s\n" % (error.level_name, error.message)
            if error:
                raise Exception(message)
        else:
            sys.stderr.write("lxml not found; skipping xml schema validation test")
        
    def tearDown(self):
        pass


if __name__ == '__main__':
    opus_core.tests.opus_unittest.main()
