# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from opus_core.indicator_framework.utilities.indicator_meta_data import IndicatorMetaData
from opus_core.indicator_framework.core.indicator_data_manager import IndicatorDataManager
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.logger import logger


class IndicatorResults(object):
    """  Takes the descriptions and locations of precomputed indicators 
         and generates an html file to browse them.
    
         The purpose of IndicatorResults is to take in a description 
         of the indicators that were requested through the GUI and output 
         an html file that can be used to browse the indicator results. 
         There is a single entry point and all the other functions are private.
    """ 
    
    def __init__(self, show_error_dialog = False):
        self.show_error_dialog = show_error_dialog
        self.data_manager = IndicatorDataManager()
        
    def create_page(self, 
                    source_data, 
                    indicators, 
                    output_directory = None,
                    page_name = 'indicator_results.html'):
        
        """  Generates the html page based on information about precomputed indicators.
        
             The file path to the generated html page is returned.
             
             Parameters:
                 source_data -- information about where the indicators were computed from
                 page_name -- the filename of the outputted html file
                 indicators -- a list of the generated indicators
        """
        
        #stores the html that is built up over the course of execution
        html = []
        
        self.indicator_documentation_mapping = {}
        
        html.append( self._output_header() )
        html.append( self._start_body() )

        #generate html for configuration info
        html.append( self._output_configuration_info(source_data) )
        html.append( self._start_table() )
        
        #load previously computed indicators
        indicator_dirs = []
        for i in indicators:
            if i.write_to_file:
                dir = i.get_storage_location()
                if not dir in indicator_dirs:
                    indicator_dirs.append(dir)
            
        indicators = []
        for dir in indicator_dirs: 
            try:
                indicators += self.data_manager.import_indicators(
                                 indicator_directory = dir)
            except: 
                logger.log_warning('Could not load indicators from directory %s'%dir)
        
        rows = []
        self._output_body(indicators, rows)
        
        unique_rows = dict([(' '.join(x), x) for x in rows])
        #rows_by_date_dict = dict([(x[4],x) for x in unique_rows.itervalues()])
        
        sorted_rows = unique_rows.items()
        sorted_rows.sort(reverse = True)
        
        sorted_rows = [row[1] for row in sorted_rows]

        for row in sorted_rows:
            html.append(self._output_row(row))
            
        html.append( self._end_table() )
        html.append( self._end_page() )

        if output_directory is None:
            output_directory = indicator_dirs[0]
            
        file = open(os.path.join(
                         output_directory, 
                         page_name),
                         'w')   
        file.write(''.join(html))
        file.close()
        
        return file.name

    def _output_body(self, indicators, rows, test = False):
        """ Generates the html for the indicators. 
        
            Finds the indicator file for every year each of the indicators 
            were run and formats this into a table.
            
            test is only used for unit testing
        """    
        for indicator in indicators:
            years = indicator.years
            
            if years == []: continue
            
            if indicator.is_single_year_indicator_image_type():
                links = []
                for year in years:
                    path = indicator.get_file_path(year)
                    if os.path.exists(path) or test:
                        link = self._get_link(indicator.get_file_name(year),str(year)) 
                        links.append(link)
                image_paths = ','.join(links)
            else:
                #aggregate multiyear run data so it is outputted nicely...
                path = indicator.get_file_path()
                if os.path.exists(path) or test:
                    year_aggregation = self._get_year_aggregation(years)
                    image_paths = self._get_link(indicator.get_file_name(),year_aggregation)
                
            doc_link = self._get_doc_link(indicator)
            
            row = [  
               doc_link,
               indicator.dataset_name,
               indicator.get_visualization_shorthand(), 
               image_paths
            ]
            rows.append(row)
    
    def _get_year_aggregation(self, years):
        """Given a sequence of years, outputs a string that represents 
           the years with dashes between consecutive years 
           (e.g. "1983,1985-1987,1999") 
        """
        years = list(years) #traits funniness
        years.sort()
        if years == []: return ''
        year_aggregation = []
        (first, last) = (years[0], years[0])
        for i in range(1,len(years)): 
            if years[i] == last + 1: last = years[i]
            else:
                if first == last: year_aggregation.append('%i' % first)
                else: year_aggregation.append('%i-%i' % (first, last))
                (first, last) = (years[i], years[i])
                
        if first == last: year_aggregation.append('%i' % first)
        else: year_aggregation.append('%i-%i' % (first, last))            
   
        return ','.join(year_aggregation)
        
    #private HTML output functions. None of the above functions directly outputs any HTML.
    def _output_configuration_info(self, source_data):
        html = []
        config_fields = { 
           'Cache directory: ' : source_data.cache_directory,
           }
        
        for title,value in config_fields.iteritems():
            html.append('<b>%s</b>%s<br><br>\n'%(title,value))
        
        return ''.join(html)
        
    def _get_doc_link(self, indicator):
        urls = []
        for attribute in indicator.attributes:
            try:
                attribute_alias = indicator.get_attribute_alias(attribute)
                url = self._get_documentation_url(attribute_alias)
            except: 
                url = None
                
            if url is None: 
                url = indicator.get_file_name(suppress_extension_addition=True)
            else:
                url = self._get_link(url,
                                     indicator.get_file_name(suppress_extension_addition=True))
            urls.append(url)
            
        return '<br>'.join(urls)
    
    def _get_link(self,url,name):
        url = url.replace('\\\\','/////').replace('\\','/')
        return '<A HREF="%s">%s</A>' % (url, name)
    
    def _get_documentation_url(self, attribute):
        """ A mapping between attribute name and documentation"""
        if self.indicator_documentation_mapping == {}:
            indicator_info = IndicatorMetaData.get_indicator_info()
            self.indicator_documentation_mapping = {}
            for (name, path, variable, documentation) in indicator_info:
                self.indicator_documentation_mapping[variable] = documentation
        
        try:
            doc_file = self.indicator_documentation_mapping[attribute] 
            prefix = IndicatorMetaData.get_indicator_documentation_URL() 
        except: return None
        return os.path.join(prefix,doc_file)
    
    #HTML outputting methods
    def _output_header(self):
        return '<head><title>Indicator Results</title></head>\n'
        
    def _output_section(self, title):
        return '<h2>%s</h2>\n' % title
        
    def _start_body(self):
        return '<body>\n' + '<h2>Indicator Results</h2>\n'
        
    def _start_table(self):
        return (
           '<table border=1 cellspacing="0" cellpadding="5" style="border-style: solid; border-color: black">\n'
           '\t<tr>\n'
           '\t\t<td><b>Indicator name</b></td>\n'
           '\t\t<td><b>Dataset</b></td>\n'
           '\t\t<td><b>Type</b></td>\n'
           '\t\t<td><b>Years</b></td>\n'
           '\t</tr>\n')
    
    def _end_table(self):
        return '</table>\n'
    
    def _output_row(self, row):
        html = ['\t<tr>\n']
        for col in row:
            html.append( '\t\t<td>%s</td>\n' % col )
        html.append( '\t</tr>\n' )
        return ''.join(html)
    
    def _end_page(self):
        return '</body>'
        
        
from opus_core.tests import opus_unittest
import tempfile
import shutil
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.test_classes.test_with_attribute_data import TestWithAttributeData

class IndicatorResultsTests(TestWithAttributeData):
    def setUp(self):
        TestWithAttributeData.setUp(self)
        self.i_results = IndicatorResults()
        self.i_results.indicator_documentation_mapping = {}
        self.source_data = SourceData(
            cache_directory = self.temp_cache_path,
            run_description = '(opus_core)',
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
            ))
            
    def test__year_aggregation(self):
        year_aggregation = self.i_results._get_year_aggregation([2001,2002,2004,2006,2007])
        self.assertEqual(year_aggregation, "2001-2002,2004,2006-2007")
        year_aggregation = self.i_results._get_year_aggregation([2001,2002,2004,2006])
        self.assertEqual(year_aggregation, "2001-2002,2004,2006")
        year_aggregation = self.i_results._get_year_aggregation([2000,2002])
        self.assertEqual(year_aggregation, "2000,2002")
    
    def test__output_configuration_info(self):                                              
        
        output = (
                  '<b>Cache directory: </b>%s<br><br>\n'%self.temp_cache_path
                  )
        
        html = self.i_results._output_configuration_info(self.source_data)
        self.assertEqual(output, html)
        
    def test___get_documentation_url(self):
        output = 'http://www.urbansim.org/docs/indicators/population.xml'
        result = self.i_results._get_documentation_url('population')
        self.assertEqual(result, output)
        
    def test__output_indicators(self):
        try:
            from opus_core.indicator_framework.image_types.matplotlib_map import Map
            from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
            from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
        except: pass
        else:
            self.source_data.years = [1980, 1982]
            
            requests = [
                Map(
                    source_data = self.source_data,
                    attribute = 'opus_core.test.population',
                    scale = [1,75000],
                    dataset_name = 'test'
                ),
                Chart(
                    source_data = self.source_data,
                    attribute = 'opus_core.test.population',
                    dataset_name = 'test',
                    name = 'my_name',    
                ),
                Chart(
                    source_data = self.source_data,
                    attribute = 'opus_core.test.population',
                    dataset_name = 'test',
                    years = [1981]
                ),
                LorenzCurve(
                    source_data = self.source_data,
                    attribute = 'opus_core.test.population',
                    dataset_name = 'test'
                ),
            ]
            
            image_type = requests[0].get_visualization_shorthand()
            (dataset,name) = (requests[0].dataset_name, 
                                   requests[0].name)
    
            image_type2 = requests[1].get_visualization_shorthand()
            (dataset2,name2) = (requests[1].dataset_name, 
                                 requests[1].name)
    
            image_type3 = requests[2].get_visualization_shorthand()
            (dataset3,name3) = (requests[2].dataset_name, 
                                     requests[2].name)
            
            image_type4 = requests[3].get_visualization_shorthand()
            (dataset4,name4) = (requests[3].dataset_name, 
                                     requests[3].name)
                                            
            doc_link = '<A HREF="http://www.urbansim.org/docs/indicators/population.xml">%s__%s__population</A>'
            doc_link2 = '<A HREF="http://www.urbansim.org/docs/indicators/population.xml">%s__%s__my_name</A>'
            output = [
                [ doc_link%('test',image_type),
                  dataset, 
                  image_type, 
                  ('<A HREF="%s__%s__%s__1980.png">1980</A>,'
                   '<A HREF="%s__%s__%s__1982.png">1982</A>')%
                     (dataset, image_type, name, dataset, image_type, name)
                ],
                [ doc_link2%('test',image_type2),
                  dataset2, 
                  image_type2, 
                  '<A HREF="%s__%s__%s.png">1980,1982</A>'%(dataset2,image_type2,name2)
                ],
                [ doc_link%('test',image_type3),
                  dataset3, 
                  image_type3, 
                  '<A HREF="%s__%s__%s.png">1981</A>'%(dataset3,image_type3,name3)
                ],
                [ doc_link%('test',image_type4),
                  dataset4, 
                  image_type4, 
                  ('<A HREF="%s__%s__%s__1980.png">1980</A>,'
                  '<A HREF="%s__%s__%s__1982.png">1982</A>')%
                  (dataset4,image_type4,name4,dataset4,image_type4,name4)
                ]
            ]
                      
            for rqst in requests:
                rqst.source_data = self.source_data
            rows = []
            self.i_results._output_body(#self.source_data, 
                                        requests, rows, test = True)
            
            for i in range(len(output)):
                if output[i] != rows[i]:
                    print output[i]
                    print rows[i]
            #print ''
            #for l in output: print l
            #for l in rows: print l
            self.assertEqual(output, rows)
            
if __name__=='__main__':
    opus_unittest.main()
