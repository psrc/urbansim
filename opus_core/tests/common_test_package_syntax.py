# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.tests import opus_unittest

class TestPackageSyntax(opus_unittest.OpusTestCase):
    modul = None

    def __init__(self, method_name='test_no_opus_syntax_violations', 
                 package_name=None):
        opus_unittest.OpusTestCase.__init__(self, method_name)
        if package_name is not None:
            self.modul = package_name

    def test_no_opus_syntax_violations(self):
        if self.modul is not None:
            from opus_core.tests.find_opus_syntax_violations import OpusSyntaxChecker
            OpusSyntaxChecker().check_syntax_for_opus_package(
                self.modul, 
                file_names_that_do_not_need_gpl = 
                    ['wingdbstub\.py', 'ez_setup\.py', 'path\.py', 'opusmain_rc\.py', 'qrc_opusmain\.py', 'biogeme\.py', '.*_ui\.py$', '^ui_.*\.py$', "pydot\.py", "pyparsing\.py"])

if __name__ == "__main__":
    opus_unittest.main()
