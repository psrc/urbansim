#
# Opus software. Copyright (C) 2005-2008 University of Washington
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

# unit test that requires that an X server be running to pass 
# (to make sure we can test the GUI under CruiseControl on the build machine)


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opus_core.tests import opus_unittest

class Tests(opus_unittest.OpusTestCase):

    def test_server(self):
        app = QApplication([''])
        label = QLabel("test")
        label.show()
        QTimer.singleShot(100, app.quit)
        app.exec_()
        print "exiting successfully from x server test"
        
         
if __name__=='__main__':
    opus_unittest.main()
