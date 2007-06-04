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

import os

from opus_core.tests import opus_unittest
from opus_core.opus_package import OpusPackage


class TestTutorialCode(opus_unittest.OpusTestCase):
    """Fails if tutorial_code.py fails.
    """
    def test_tutorial_code(self):
        opus_manual_path = OpusPackage().get_path_for_package('opus_docs')
        error_code = os.system('python "%s"'
            % os.path.join(opus_manual_path, 'docs', 'latex', 'tutorial_code.py'))
        
        self.assert_(not error_code)


if __name__=="__main__":
    opus_unittest.main()
