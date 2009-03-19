# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE
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