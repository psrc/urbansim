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
    
class Command:
    def execute(self):
        """
        Execute this command.
        """
        raise NotImplementedError('Subclasses of Command must implement execute.')
    
    def is_valid(self):
        """
        Are the parameters for this command valid?
        """
        raise NotImplementedError('Subclasses of Command must implement is_valid.')
        
    def get_validation_information(self):
        """
        Returns a ValidationInformation object describing which parameters,
        if any, failed to validate, and why.
        """
        raise NotImplementedError('Subclasses of Command must implement get_validation_information.')
            

from opus_core.tests import opus_unittest 


class CommandTest(opus_unittest.TestCase):
    def setUp(self):
        self.command = Command()
        
    def tearDown(self):
        pass
        
    def test_raises_NotImplementedError_on_execute(self):
        self.assertRaises(NotImplementedError, self.command.execute)
        
    def test_raises_NotImplementedError_on_is_valid(self):
        self.assertRaises(NotImplementedError, self.command.is_valid)
        
    def test_raises_NotImplementedError_on_get_validation_information(self):
        self.assertRaises(NotImplementedError, self.command.get_validation_information)
        

if __name__ == '__main__':
    opus_unittest.main()