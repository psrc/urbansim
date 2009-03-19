# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 
    
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