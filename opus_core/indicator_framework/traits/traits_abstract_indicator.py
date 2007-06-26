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

from opus_core.logger import logger
try:
    import enthought.traits.ui
    from enthought.traits.api import HasTraits, Str
    from enthought.traits.api import Item, View
    # later update the ui import to:   from enthought.traits.ui.api import Item, View
except:
    logger.log_warning('Could not load traits.ui. Skipping %s!' % __file__)
else:
    from opus_core.indicator_framework.utilities import display_message_dialog
    from opus_core.indicator_framework.core import AbstractIndicator
    from opus_core.variables.variable_name import VariableName
    
    class TraitsAbstractIndicator(HasTraits):
        '''The traits version of an abstract_indicator'''
        
        name = Str('')
        attribute = Str('')
        dataset_name = Str('')
        years = Str('(e.g. 2000,2004-2005)')
        
        #to do: support expressions in GUI
    
        def fill_indicator_with_basic_values(self, indicator):
            try:
                if self.name == '':
                    name = VariableName(self.attribute).get_alias()
                else:
                    name = self.name
            except:
                name = ''
                
            indicator.name = name
            indicator.dataset_name = self.dataset_name
            indicator.attribute = self.attribute
            indicator.years = self.years
            
        def _detraitify(self, detraits_dict, source_data):
            '''Detraitifies traits in abstract class and adds them to a dicationary.
            
               Should be called from all detraitify methods.
               
               detraits_dict -- a dictionary of all name/value pairs
               source_data -- the SourceData object which the detrait-ed object requires
            '''
            if self.name == '':
                name = VariableName(self.attribute).get_alias()
            else:
                name = self.name
            detraits_dict['name'] = str(name)
            detraits_dict['attribute'] = str(self.attribute)
            detraits_dict['dataset_name'] = str(self.dataset_name)
            detraits_dict['source_data'] = source_data
            detraits_dict['years'] = self._get_indicator_years(self.years)
            
        def detraitify(self, source_data):
            '''Detraitify output-type-specific traits.
            
               Method should be overridden by child classes.
               
               source_data -- the SourceData object which the detrait-ed object requires
            '''
            logger.log_warning('_detraitify should be overridden by child indicator')
            detraits_dict = {}
            self._detraitify(detraits_dict, source_data)
            new_indicator = AbstractIndicator(**detraits_dict)
            return new_indicator

        def _get_indicator_years(self, year_string):
            '''processes a year string into a list of years.
            
               A year string of the form '2001, 2003-2005, 2008' would result
               in the list [2001,2003,2004,2005,2008] '''
            years = []
            year_tokens = year_string.split(',')
            for year_token in year_tokens:
                try:
                    if year_token.find('-') == -1:
                        years.append(int(year_token))
                    else:
                        #tokens of the form '2000-2003'
                        (start,end) = year_token.split('-')
                        (start,end) = (int(start),int(end))
                        if end < start: 
                            temp = end
                            end = start
                            start = temp
                        years += range(start, end + 1)
                except:
                    display_message_dialog('The year(s) field is malformatted. Please specify years ' 
                                'in the proper format (e.g. "2002,2005-2009")')
            years.sort()
            return years
                    
    from opus_core.tests import opus_unittest
    from opus_core.indicator_framework.core import SourceData
    from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
    from opus_core.indicator_framework.core import AbstractIndicator    
    from opus_core.indicator_framework.test_classes import TestWithAttributeData
    
    class TraitsAbstractIndicatorTest(TestWithAttributeData):
        def test_detraitify(self):
            indicator = TraitsAbstractIndicator()
            indicator.name = 'my_name'
            indicator.attribute = 'my_attribute'
            indicator.dataset_name = 'test'
            indicator.years = '1980-1982'
 
            source_data = SourceData(
                             cache_directory = self.temp_cache_path, 
                             years = [],
                             dataset_pool_configuration = DatasetPoolConfiguration(
                                 package_order=['opus_core'],
                                 package_order_exceptions={},
                             ))
            returned = indicator.detraitify(source_data = source_data)

            correct = AbstractIndicator(dataset_name = 'test',
                                        attribute = 'my_attribute',
                                        name = 'my_name',
                                        source_data = source_data,
                                        years = [1980, 1981, 1982])
            self.assertEqual(correct.dataset_name, returned.dataset_name)
            self.assertEqual(correct.attribute, returned.attribute)
            self.assertEqual(correct.name, returned.name)
            
        def test_detraitify2(self):
            indicator = TraitsAbstractIndicator()
            indicator.attribute = 'my_attribute'
            indicator.dataset_name = 'test'
            indicator.years = '1980,1982'

            source_data = SourceData(
                             cache_directory = self.temp_cache_path, 
                             years = [],
                             dataset_pool_configuration = DatasetPoolConfiguration(
                                 package_order=['opus_core'],
                                 package_order_exceptions={},
                             ))
            returned = indicator.detraitify(source_data = source_data)
            correct = AbstractIndicator(dataset_name = 'test',
                                        attribute = 'my_attribute',
                                        source_data = source_data,
                                        years = [1980,1982]
                                        )
            self.assertEqual(correct.dataset_name, returned.dataset_name)
            self.assertEqual(correct.attribute, returned.attribute)
            self.assertEqual(correct.name, returned.name)

        def test__get_indicator_years(self):
            indicator = TraitsAbstractIndicator()
            year_string = '2000'
            years = indicator._get_indicator_years(year_string)
            self.assertEqual(years, [2000,])
            year_string = '2000, 2001,2002'
            years = indicator._get_indicator_years(year_string)
            self.assertEqual(years, [2000,2001,2002])
            year_string = '2000-2002'
            years = indicator._get_indicator_years(year_string)
            self.assertEqual(years, [2000,2001,2002])
            year_string = '1995, 2000-2002, 2007'
            years = indicator._get_indicator_years(year_string)
            self.assertEqual(years, [1995,2000,2001,2002,2007])
            year_string = '2007, 2002-2000, 1995'
            years = indicator._get_indicator_years(year_string)
            self.assertEqual(years, [1995,2000,2001,2002,2007])
                        
    if __name__ == '__main__':
        opus_unittest.main()
