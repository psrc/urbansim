#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.variables.variable import Variable
from opus_core.logger import logger

class a_test_variable_with_two_dependencies(Variable):
    """A fake variable used for testing.
    Used by tests in test_dataset.py.
    Has to be in a separate file, since Opus looks for a file with the same name as the variable."""
    
    _return_type = 'int8'
    def dependencies(self):
        return ["opus_core.tests.a_dependent_variable2", "opus_core.tests.a_test_variable"]

    def compute(self, dataset_pool):
        logger.log_status(self._return_type)
        return self.get_dataset().get_attribute("a_dependent_variable2") + \
                self.get_dataset().get_attribute("a_test_variable")


from opus_core.tests import opus_unittest
class Tests(opus_unittest.OpusTestCase):
    def test_name(self):
        variable = a_test_variable_with_two_dependencies()
        self.assertEqual(variable.name(), self.__module__)


if __name__ == '__main__':
    opus_unittest.main()