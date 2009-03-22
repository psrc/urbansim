# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
import os, re, sys, time, traceback
from copy import copy
from opus_gui.results_manager.run.indicator_framework.visualizer.visualizers.abstract_visualization import Visualization
    
from numpy import newaxis
try:
    from matplotlib.pylab import clf, gca, plot, setp, title, legend, grid, figlegend
    from matplotlib.pylab import subplot, savefig, xlabel, ylabel, axis
    from matplotlib.ticker import FormatStrFormatter
    from matplotlib.ticker import FixedLocator, ScalarFormatter
except:
    pass
else:
    
    class MatplotlibChart(Visualization):
    
        def __init__(self, 
                     indicator_directory,
                     name = None,
                     scale = None,
                     storage_location = None):
            
            self.name = name
            if storage_location is None:
                storage_location = indicator_directory
            self.storage_location = storage_location
            self.indicator_directory = indicator_directory

        def get_file_extension(self):
            return 'png'
        
        def get_visualization_type(self):
            return 'chart'

        __year_pattern = re.compile('.*([0-9][0-9][0-9][0-9]).*')        
        def plot_chart(self, data, primary_keys, years, chart_title, file_path):
            """Create a chart for the given indicator, save it to the cache
            directory's 'indicators' sub-directory.
            """
            
            line_styles = [
                '-',    # solid line
                '--',    # dashed line
                '-.',    # dash-dot line
                ':',     # dotted line
                '.',     # points
                '+',     # plus symbols
                'x'     # cross symbols 
                ',',     # pixels
                'o',     # circle symbols
                '^',     # triangle up symbols
                'v',     # triangle down symbols
                '<',     # triangle left symbols
                '>',     # triangle right symbols
                's',     # square symbols
            ]
            
            
            if len(primary_keys) > 1:
                keys = [data[key] for key in primary_keys]
                keys = zip(*keys)
            else:
                keys = data[primary_keys[0]]
            
            plot_str = []
            legend_str = []
            
            clf()
            grid(True)
            title(chart_title)  

            row = 0
            row_y_vals = {}
            cols = sorted([col for col in data.keys() if col not in primary_keys])
            years = [int(self.__year_pattern.match(col).group(1)) for col in cols]

            for key in keys:
                row_y_vals[row] = [data[col][row] for col in cols]
                plot_str.append("years, row_y_vals[%i], '%s'" % (row, line_styles[row%len(line_styles)]))
                legend_str.append(str(key))
                row += 1
            
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
                
            args = [
                    'linewidth = 1'
            ]
            lines = eval('plot(' + ','.join(plot_str+args) + ')' )
            setp(lines, marker='o')
    #        interval = years.append(9999) - [0].append(years)
            majorLocator = FixedLocator(years)
            majorFormatter = FormatStrFormatter ('%d')
            ax = subplot(111)
            ax.xaxis.set_major_locator(majorLocator)
            ax.xaxis.set_major_formatter(majorFormatter)
            #ax.xaxis.set_major_formatter(ScalarFormatter())
    #        setp(gca(), 'xticklabels', [str(year) for year in years])
            legend(legend_str,shadow = True, numpoints=2)
            xlabel('years')
            ylabel('value')
            (xmin,xmax,ymin,ymax) = axis()
            xmin = years[0] - 1
            xmax = years[-1] + 1
            axis((xmin,xmax,ymin,ymax))
                
            savefig(file_path)
            
            return file_path

        def visualize(self, 
                      indicators_to_visualize,
                      computed_indicators):
            """Create a map for the given indicator, save it to the cache
            directory's 'indicators' sub-directory."""
            
            #TODO: eliminate this example indicator stuff
            example_indicator = computed_indicators[indicators_to_visualize[0]]
            source_data = example_indicator.source_data        
    
            years = source_data.years
            self._create_input_stores(years = years)
    
            dataset_to_attribute_map = {}
            for name, computed_indicator in computed_indicators.items():
                if name not in indicators_to_visualize: continue
                
                if computed_indicator.source_data != source_data:
                    raise Exception('result templates in indicator batch must all be the same.')
                dataset_name = computed_indicator.indicator.dataset_name
                if dataset_name not in dataset_to_attribute_map:
                    dataset_to_attribute_map[dataset_name] = []
                dataset_to_attribute_map[dataset_name].append(name)
    
            viz_metadata = []
            for dataset_name, indicator_names in dataset_to_attribute_map.items():  
                attributes = [(name,computed_indicators[name].get_computed_dataset_column_name())
                              for name in indicator_names]    
                example_indicator = computed_indicators[indicator_names[0]]
                primary_keys = example_indicator.primary_keys
                
                data = self._get_PER_ATTRIBUTE_form(
                     dataset_name = dataset_name,
                     attributes = attributes,
                     primary_keys = primary_keys,
                     years = source_data.years
                )
                for name, data_subset in data.items():
                    
                    table_name = self.get_name(
                        dataset_name = dataset_name,
                        years = years,
                        attribute_names = [name])
    
                    file_path = os.path.join(self.storage_location,
                                         table_name+ '.' + self.get_file_extension())
    
                    self.plot_chart(
                        data = data_subset, 
                        primary_keys = primary_keys, 
                        years = years, 
                        chart_title = table_name, 
                        file_path = file_path                          
                    )
                    metadata = ([name], table_name, years)
                    viz_metadata.append(metadata)
                    
            visualization_representations = []
            for indicator_names, table_name, years in viz_metadata:
                visualization_representations.append(
                    self._get_visualization_metadata(
                        computed_indicators = computed_indicators,
                        indicators_to_visualize = indicator_names,
                        table_name = table_name,
                        years = years
                ))                  
            
            return visualization_representations
            
        

    from opus_core.tests import opus_unittest    
    from opus_gui.results_manager.run.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest
    from opus_gui.results_manager.run.indicator_framework.maker.maker import Maker
    from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator
    
    class Tests(AbstractIndicatorTest):
        def skip_test_create_indicator(self):
            
            indicator_path = os.path.join(self.temp_cache_path, 'indicators')
            self.assert_(not os.path.exists(indicator_path))
            
            chart = MatplotlibChart(
                      source_data = self.source_data,
                      attribute = 'opus_core.test.attribute',
                      dataset_name = 'test',
                      years = None
            )
            
            chart.create(False)
            
            self.assert_(os.path.exists(indicator_path))
            self.assert_(os.path.exists(os.path.join(indicator_path, 'test__chart__attribute.png')))

        def skip_test_create_indicator2(self):
            
            # if the environment variable DISPLAY isn't defined, exit this test
            if 'DISPLAY' not in os.environ:
                return
                
            indicator_path = self.source_data.get_indicator_directory()
            self.assert_(not os.path.exists(indicator_path))
    
            self.source_data.years = range(1980,1984)
            indicator = Indicator(
                      dataset_name = 'test', 
                      attribute = 'opus_core.test.attribute'
            )        
    
            indicator2 = Indicator(
                      dataset_name = 'test', 
                      attribute = 'opus_core.test.attribute2'
            )
                    
            maker = Maker(project_name = 'test', test = True)
            computed_indicators = maker.create_batch(
                indicators = {'attr1':indicator, 
                              'attr2':indicator2}, 
                source_data = self.source_data)
            
            chart = MatplotlibChart(
                        name = 'test_chart',
                        indicator_directory = self.source_data.get_indicator_directory())
            chart._create_input_stores(range(1980,1984))
            
            viz_results = chart.visualize(
                            indicators_to_visualize = ['attr1',
                                                       'attr2'], 
                            computed_indicators = computed_indicators)
            
            
            for viz_result in viz_results:
                if viz_result.indicators[0].indicator.name == 'attribute':
                    name = 'attr1'
                else:
                    name = 'attr2'
                file_name = 'test_chart_1980-1983_%s.png'%name
                    
                self.assertEqual(
                     os.path.join(viz_result.storage_location,
                                  viz_result.table_name + '.' + viz_result.file_extension), 
                     os.path.join(indicator_path, file_name))     

                        
    if __name__ == '__main__':
        opus_unittest.main()
    
