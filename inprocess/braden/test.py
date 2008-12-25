import opus_core.tests.opus_unittest
import sys
try:
    import lxml.etree
except:
    pass

class TestXMLSchema(opus_core.tests.opus_unittest.OpusTestCase):

    def setUp(self):
        pass

    def test_test(self):
        xml_file = open("test.xml","r")
        xmlschema_file = open("opus_project.xsd","r")
        self.validate_xml(xml_file, xmlschema_file)

    def validate_xml(self, xml_file, xmlschema_file):
        if "lxml" in globals():
            xml_doc = lxml.etree.parse(xml_file)
            xmlschema_doc = lxml.etree.parse(xmlschema_file)
            xmlschema = lxml.etree.XMLSchema(xmlschema_doc)
            result = xmlschema.validate(xml_doc)
            if not result:
                error_log = xmlschema.error_log
                message = "XML validation error:\n"
                for error in error_log:
                    message += "  %s:%s:%s:\n" % (error.filename, str(error.line), str(error.column))
                    message += "    [%s] %s\n" % (error.level_name, error.message)
                raise Exception(message)
        else:
            sys.stderr.write("lxml not found; skipping xml schema validation test")
        
    def tearDown(self):
        pass


if __name__ == '__main__':
    opus_core.tests.opus_unittest.main()
