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
from opus_core.tests import opus_unittest

from psrc.configs.baseline import Baseline
import pickle

class TestPickleConfiguration(opus_unittest.OpusIntegrationTestCase):

    def test_pickling_configuration_doesnt_fail(self):
        config = Baseline()
        pickled_config = None
        try:
            pickled_config = pickle.dumps(config)
        except: pass
        self.assertTrue(pickled_config is not None)
            

if __name__ == "__main__":
    opus_unittest.main()