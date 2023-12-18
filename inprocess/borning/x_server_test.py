# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

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
        print("exiting successfully from x server test")
        
         
if __name__=='__main__':
    opus_unittest.main()
