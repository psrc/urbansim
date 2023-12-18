# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, sys

from opus_core.tests import opus_unittest
from opus_core.opus_package import OpusPackage


class TestTutorialCode(opus_unittest.OpusTestCase):
    """Fails if tutorial_code.py fails.
    """
    def test_tutorial_code(self):
        opus_docs_path = OpusPackage().get_path_for_package('opus_docs')
        error_code = os.system('%s "%s"'
            % (sys.executable, os.path.join(opus_docs_path, 'manual', 'part-command-line', 'tutorial_code.py')))
        
        self.assertTrue(not error_code)


if __name__=="__main__":
    opus_unittest.main()
