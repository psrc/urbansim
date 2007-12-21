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
    def __init__(self, dataset_name, attribute, 
                 operation = None, name = None):

        self.dataset_name = dataset_name 
        self.attribute = attribute
        self.operation = operation                        
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
            
        if self.operation is not None and name.find(self.operation) == -1:
            name = '%s_%s'%(self.operation, name)
            
        return name
        
    def get_attribute_alias(self, year = None):
        attribute = self.attribute
        if year is not None:
            attribute = self.attribute.replace('DDDD',repr(year))
            
        #TODO: less hacky way to do this
        if attribute[:10] == 'autogenvar':
            alias = VariableName(attribute).get_squished_expression()
        else:
            alias = VariableName(attribute).get_alias()
    
        return alias
    
