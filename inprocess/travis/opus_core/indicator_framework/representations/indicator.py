#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from opus_core.variables.variable_name import VariableName
import os

class Indicator:
    def __init__(self, dataset_name, attribute, name = None):

        self.dataset_name = dataset_name 
        self.attribute = attribute
        self.name = name
        self.name = self.get_indicator_name(year = None)
        self.date_computed = None
                    
        #TODO: write this method
        #self._check_integrity()
        
    def get_indicator_name(self, year = None):
        if self.name is None:
            name = self.get_attribute_alias(year)
        else:
            name = self.name
            
        return name
        
    def get_variable_name(self, year = None):
        attribute = self.attribute
        if year is not None:
            attribute = self.attribute.replace('DDDD',repr(year))
        return VariableName(attribute)

    def get_attribute_alias(self, year = None):
        varname = self.get_variable_name(year)
        #TODO: less hacky way to do this
        if self.attribute[:10] == 'autogenvar':
            return varname.get_squished_expression()
        else:
            return varname.get_alias()

