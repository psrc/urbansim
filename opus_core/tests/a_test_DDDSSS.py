#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

class a_test_DDDSSS(Variable):
    """A fake variable used for testing.
    Used by tests in variable_family_name_translator.py.
    Has to be in a separate file, since Opus looks for a file with the same name as the variable."""
    
    _return_type = 'int8'
    
    def __init__(self,arg1,arg2):
        # just discard the additional arguments for DDD and SSS
        Variable.__init__(self)

    def dependencies(self):
        return ["tests.a_dependent_variable"]

    def compute(self, dataset_pool):
        logger.log_status(self._return_type)
        return self.get_dataset().get_attribute("a_dependent_variable") * 10