# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
import os, re, sys, time, traceback
from copy import copy

from opus_core.indicator_framework.core.abstract_indicator import AbstractIndicator

from numpy import newaxis
try:
    from matplotlib.pylab import clf, gca, plot, setp, title, legend
    from matplotlib.pylab import subplot, savefig, xlabel, ylabel, axis
    from matplotlib.ticker import FormatStrFormatter
    from matplotlib.ticker import FixedLocator, ScalarFormatter
except:
    pass
else:
    
    class Chart(AbstractIndicator):
    
        def __init__(self, source_data, dataset_name, 
                     attribute = None, 
                     years = None, operation = None, name = None,
                     storage_location = None):
            
            AbstractIndicator.__init__(self, source_data, dataset_name, 
                                       [attribute], years, operation, name,
                                       storage_location)
    
        def is_single_year_indicator_image_type(self):
            return False
        
        def get_file_extension(self):
            return 'png'
        
        def get_visualization_shorthand(self):
            return 'chart'
        
        def _create_indicator(self, years):
            """Create a chart for the given indicator, save it to the cache
            directory's 'indicators' sub-directory.
            """
                
            values, years = self._get_indicator_for_years(years,
                                                          wrap = False)
            
            dataset = self._get_dataset(years[-1])
    
            ids = dataset.get_id_attribute()
            #each row corresponds to year's result, each col corresponds to an record in dataset
            rows = ids.size
            if rows == 1:
                values = values[:, newaxis]
    
            clf()
            chart_title = self.get_attribute_alias(self.attributes[0])
            if self.run_description is not None:
                chart_title += '\n' + self.run_description
            title(chart_title)        
    
            plot_str = []
            legend_str = []
            for row in range(rows):
                plot_str.append('years, values[:, %s]' % row)
                legend_str.append(str(ids[row]))
            
            row_limit = 20
            if len(plot_str) > row_limit:
                plot_str = plot_str[0:row_limit-1]
                legend_str = legend_str[0:row_limit-1]
                logger.log_warning('The chart has too many rows. '
                                        'This chart will be truncated. ' 
                                        'For better results, try a dataset '
                                        'that is more coarse-grained (e.g. if the indicator '
                                        'is at the gridcell level, try the county level.) '
                                        'or an image type like a table')
                
            lines = eval('plot(' + ','.join(plot_str) + ')' )
            setp(lines, marker='o')
    #        interval = years.append(9999) - [0].append(years)
            majorLocator = FixedLocator(years)
            majorFormatter = FormatStrFormatter ('%d')
            ax = subplot(111)
            ax.xaxis.set_major_locator(majorLocator)
            ax.xaxis.set_major_formatter(majorFormatter)
            #ax.xaxis.set_major_formatter(ScalarFormatter())
    #        setp(gca(), 'xticklabels', [str(year) for year in years])
            legend(legend_str,numpoints=1)
            xlabel('years')
            ylabel('value')
            (xmin,xmax,ymin,ymax) = axis()
            xmin = years[0] - 1
            xmax = years[-1] + 1
            axis((xmin,xmax,ymin,ymax))
                
            file_path = self.get_file_path()           
            savefig(file_path)
            
            return file_path
            
        

    from opus_core.tests import opus_unittest    
    from opus_core.indicator_framework.core.source_data import SourceData
    from opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest
    
    class Tests(AbstractIndicatorTest):
        def test_create_indicator(self):
            
            # if the environment variable DISPLAY isn't defined, exit this test
            if 'DISPLAY' not in os.environ:
                return
            
            indicator_path = os.path.join(self.temp_cache_path, 'indicators')
            self.assertTrue(not os.path.exists(indicator_path))
            
            chart = Chart(
                      source_data = self.source_data,
                      attribute = 'opus_core.test.attribute',
                      dataset_name = 'test',
                      years = None
            )
            
            chart.create(False)
            
            self.assertTrue(os.path.exists(indicator_path))
            self.assertTrue(os.path.exists(os.path.join(indicator_path, 'test__chart__attribute.png')))
                        
    if __name__ == '__main__':
        opus_unittest.main()
    
