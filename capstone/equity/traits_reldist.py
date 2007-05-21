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
    from enthought.traits import HasTraits, Str, ListInt
    from enthought.traits.ui import Item, View
except:
    logger.log_warning('Could not load traits.ui. Skipping %s!' % __file__)
else:
    from opus_core.indicator_framework.image_types.rpy_reldist import Reldist
    from opus_core.indicator_framework.traits.traits_abstract_indicator import TraitsAbstractIndicator
    
    class TraitsReldist(TraitsAbstractIndicator):
        '''The traits version of a reldist'''
        
        traits_view = View(
            Item('attribute', label = 'Attribute', width = 300),
            Item('name', label = 'Name (optional)', width = 300),
            Item('dataset_name', label = 'Dataset', width = 300),     
            Item('years', label = 'Year(s)', width = 300),
        )
        
        def detraitify(self, source_data):
            '''Detraitify output-type-specific traits.
            
               source_data -- the SourceData object which the detrait-ed object requires
            '''
            detraits_dict = {}
            TraitsAbstractIndicator._detraitify(self, detraits_dict, source_data)
            reldist = Reldist(**detraits_dict)
            return reldist
            
    from opus_core.tests import opus_unittest
    from opus_core.indicator_framework.source_data import SourceData
    from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
        
    class TraitsReldistTest(opus_unittest.OpusTestCase):
        def test_detraitify(self):
            indicator = TraitsChart()
            indicator.name = 'my_name'
            indicator.attribute = 'my_attribute'
            indicator.dataset_name = 'my_dataset'
            indicator.years = '2005'
            
            source_data = SourceData(
                             cache_directory = '', 
                             years = [],
                             dataset_pool_configuration = DatasetPoolConfiguration(
                                 package_order=['opus_core'],
                                 package_order_exceptions={},
                             ))
            returned = indicator.detraitify(source_data = source_data)
            correct = Chart(source_data = source_data,
                          dataset_name = 'my_dataset',
                          attribute = 'my_attribute',
                          name = 'my_name',
                          years = [2005])
            
            self.assertEqual(correct.dataset_name, returned.dataset_name)
            self.assertEqual(correct.attribute, returned.attribute)
            self.assertEqual(correct.name, returned.name)
            
    if __name__ == '__main__':
        opus_unittest.main()
