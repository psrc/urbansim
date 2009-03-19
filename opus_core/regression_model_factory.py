# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE
 
from opus_core.class_factory import ClassFactory
from opus_core.model_component_creator import ModelComponentCreator

class RegressionModelFactory(ModelComponentCreator):
    """ Creates a regression model.
    """ 
    def get_model(self, name="opus_core.linear_regression", 
                  resources=None, debuglevel=0):
        """name is of the form 'package_name.class_name'.
        """
        return ClassFactory().get_class(name, debug=debuglevel)
        
