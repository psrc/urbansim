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
    from enthought.traits.api import Instance, Bool, DictStrAny, Directory, File, Int, List, ListStr, ListInt, Str
except:
    logger.log_warning('Could not load traits.ui. Skipping %s!' % __file__)
else:

    import os, sys
    from opus_core.configurations.abstract_configuration import AbstractConfiguration
    from opus_core.indicator_framework.source_data import SourceData
    from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
    
    class TraitsSourceData(AbstractConfiguration):
        """Configuration information for computing a set of indicators.  This uses the
        enthought traits package.  Public traits are as follows:
            cache_directory: A directory containing data from the simulation run 
            comparison_cache_directory: A second cache directory which any indicators using this source data object
                                will be compared against. This enables cross-scenario comparisons.
            run_description: A descriptive string
            file_name_for_indicator_results: The name of the outputed html file for viewing indicator results
        """
        
        # public traits
        cache_directory = Directory('')
        comparison_cache_directory = Directory('')
        run_description = Str('')
        package_order = ListStr([])
        
        def __init__(self, package_order):
            self.package_order = package_order 
            
        def detraitify(self):
            '''Returns a version of itself without traits. The other version
               may have more/different methods than the traits object'''
               
            new_source = SourceData(
                cache_directory = str(self.cache_directory),
                comparison_cache_directory = str(self.comparison_cache_directory),
                run_description = str(self.run_description),
                dataset_pool_configuration = DatasetPoolConfiguration(
                    package_order = [str(s) for s in self.package_order],
                    package_order_exceptions = {},        
                 ))
            return new_source
  
    from opus_core.tests import opus_unittest
    
    class TestTraitsSourceData(opus_unittest.OpusTestCase):
        
        def test__detraitify(self):
            source_data = TraitsSourceData(['opus_core'])
            source_data.cache_directory = 'cache'
            source_data.comparison_cache_directory = 'cache2'
            source_data.run_description = 'test'
            
            from opus_core.indicator_framework.source_data import SourceData
            correct = SourceData(cache_directory = 'cache',
                                 comparison_cache_directory = 'cache2',
                                 run_description = 'test',
                                 dataset_pool_configuration = DatasetPoolConfiguration(
                                    package_order=['opus_core'],
                                    package_order_exceptions={},
                                 ))
            
            returned = source_data.detraitify()
            self.assertEqual(correct.cache_directory,returned.cache_directory)
            self.assertEqual(correct.comparison_cache_directory,returned.comparison_cache_directory)            
            self.assertEqual(correct.run_description,returned.run_description)
            
            
    if __name__ == '__main__':
        opus_unittest.main()