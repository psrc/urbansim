#
# Opus software. Copyright (C) 1998-2007 University of Washington
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
        
