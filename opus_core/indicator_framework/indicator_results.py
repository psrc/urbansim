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
import os
from sets import Set

from time import strftime, localtime
from opus_core.logger import logger
import cPickle as pickle

from opus_core.indicator_framework import IndicatorMetaData
from opus_core.indicator_framework import SourceData
from opus_core.indicator_framework import AbstractIndicator

class IndicatorResults(object):
    """  Takes the descriptions and locations of precomputed indicators and generates an html file to browse them.
    
         The purpose of IndicatorResults is to take in a description of the indicators that were 
         requested through the GUI and output an html file that can be used to browse the indicator
         results. There is a single entry point and all the other functions are private.
    """ 
    
    def __init__(self, show_error_dialog = False):
        self.show_error_dialog = show_error_dialog
        
    def create_page(self, source_data, indicators, page_name = 'indicator_results.html'):
        """  Generates the html page based on information about precomputed indicators.
        
             The file path to the generated html page is returned.
             
             Parameters:
                 source_data -- informatiourl = self._get_documentation_url(attribute_alias)n about where the indicators were computed from
                 page_name -- the filename of the outputted html file
                 indicators -- a list of the generated indicators
        """
        
        #stores the html that is built up over the course of execution
        html = []
        
        indicator_directory = source_data.get_indicator_directory()
        self.indicator_documentation_mapping = {}
        
        html.append( self._output_header() )
        html.append( self._start_body() )

        #generate html for configuration info
        html.append( self._output_configuration_info(source_data) )
        html.append( self._start_table() )
        
        #load previously computed indicators
        try:
            indicators = self._reconstruct_from_metadata(indicator_directory)
        except: 
            indicators = []
        
        rows = []
        self._output_body(source_data, indicators, rows)
        
        unique_rows = dict([(' '.join(x), x) for x in rows])
        #rows_by_date_dict = dict([(x[4],x) for x in unique_rows.itervalues()])
        
        sorted_rows = unique_rows.items()
        sorted_rows.sort(reverse = True)
        
        sorted_rows = [row[1] for row in sorted_rows]

        for row in sorted_rows:
            html.append(self._output_row(row))
            
        html.append( self._end_table() )
        html.append( self._end_page() )

        file = open(os.path.join(
                         indicator_directory, 
                         page_name),
                         'w')   
        file.write(''.join(html))
        file.close()
        
        return file.name

    def _output_body(self, source_data, indicators, rows, test = False):
        """ Generates the html for the indicators. 
        
            Finds the indicator file for every year each of the indicators were run and formats this into a table.
            
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
               indicator.get_shorthand(), 
               image_paths
            ]
            rows.append(row)
    
    def _get_year_aggregation(self, years):
        """Given a sequence of years, outputs a string that represents the years with dashes
           between consecutive years (e.g. "1983,1985-1987,1999") 
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
    
    def _reconstruct_from_metadata(self, indicator_directory):
        '''scans the indicator directory for indicator meta files and 
           recreates the indicators'''
        indicators = []
        files = os.listdir(indicator_directory)
        for filename in files:
            if len(filename) >= 5 and filename[-5:] == '.meta':
                try:
                    meta_path = os.path.join(indicator_directory, filename)
                    indicator = AbstractIndicator.create_from_metadata(meta_path)
                    indicators.append(indicator)
                except: pass
        
        return indicators
    
    def _get_doc_link(self, indicator):
        try:
            attribute_alias = indicator.get_attribute_alias()
            url = self._get_documentation_url(attribute_alias)
        except: 
            url = None
            
        if url is None: 
            url = indicator.name
        else:
            url = self._get_link(url,indicator.name)
            
        return url
    
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

class IndicatorResultsTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.i_results = IndicatorResults()
        self.i_results.indicator_documentation_mapping = {}
        self.source_data = SourceData(
            cache_directory = '',
            run_description = '(xxx)',
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
                package_order_exceptions={},
            ))
        
    def tearDown(self):
        pass
            
    def test__year_aggregation(self):
        year_aggregation = self.i_results._get_year_aggregation([2001,2002,2004,2006,2007])
        self.assertEqual(year_aggregation, "2001-2002,2004,2006-2007")
        year_aggregation = self.i_results._get_year_aggregation([2001,2002,2004,2006])
        self.assertEqual(year_aggregation, "2001-2002,2004,2006")
        year_aggregation = self.i_results._get_year_aggregation([2000,2002])
        self.assertEqual(year_aggregation, "2000,2002")
    
    def test__output_configuration_info(self):                                              
        
        output = (
                  '<b>Cache directory: </b><br><br>\n'
                  )
        
        html = self.i_results._output_configuration_info(self.source_data)
        self.assertEqual(output, html)
        
    def test___get_documentation_url(self):
        output = 'http://www.urbansim.org/opus/opus_manual/docs/indicators/population.xml'
        result = self.i_results._get_documentation_url('population')
        self.assertEqual(result, output)
        
    def test__output_indicators(self):
        try:
            from opus_core.indicator_framework.image_types.matplotlib_map import Map
            from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
            from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
        except: pass
        else:
            self.source_data.years = [2000, 2002]
            
            requests = [
                Map(
                    source_data = self.source_data,
                    attribute = 'xxx.yyy.population',
                    scale = [1,75000],
                    dataset_name = 'yyy'
                ),
                Chart(
                    source_data = self.source_data,
                    attribute = 'xxx.yyy.population',
                    dataset_name = 'yyy',
                    name = 'my_name',    
                ),
                Chart(
                    source_data = self.source_data,
                    attribute = 'xxx.yyy.population',
                    dataset_name = 'yyy',
                    years = [2001]
                ),
                LorenzCurve(
                    source_data = self.source_data,
                    attribute = 'xxx.yyy.population',
                    dataset_name = 'yyy'
                ),
            ]
            attribute_name = 'population'
            
            image_type = requests[0].get_shorthand()
            (dataset,name) = (requests[0].dataset_name, 
                                   requests[0].name)
    
            image_type2 = requests[1].get_shorthand()
            (dataset2,name2) = (requests[1].dataset_name, 
                                 requests[1].name)
    
            image_type3 = requests[2].get_shorthand()
            (dataset3,name3) = (requests[2].dataset_name, 
                                     requests[2].name)
            
            image_type4 = requests[3].get_shorthand()
            (dataset4,name4) = (requests[3].dataset_name, 
                                     requests[3].name)
                                
            doc_link = '<A HREF="http://www.urbansim.org/opus/opus_manual/docs/indicators/population.xml">population</A>'
            doc_link2 = '<A HREF="http://www.urbansim.org/opus/opus_manual/docs/indicators/population.xml">my_name</A>'
            output = [
                [ doc_link,
                  dataset, 
                  image_type, 
                  ('<A HREF="%s__%s__%s__2000.png">2000</A>,'
                   '<A HREF="%s__%s__%s__2002.png">2002</A>')%
                     (dataset, image_type, name, dataset, image_type, name)
                ],
                [ doc_link2,
                  dataset2, 
                  image_type2, 
                  '<A HREF="%s__%s__%s.png">2000,2002</A>'%(dataset2,image_type2,name2)
                ],
                [ doc_link,
                  dataset3, 
                  image_type3, 
                  '<A HREF="%s__%s__%s.png">2001</A>'%(dataset3,image_type3,name3)
                ],
                [ doc_link,
                  dataset4, 
                  image_type4, 
                  ('<A HREF="%s__%s__%s__2000.png">2000</A>,'
                  '<A HREF="%s__%s__%s__2002.png">2002</A>')%
                  (dataset4,image_type4,name4,dataset4,image_type4,name4)
                ]
            ]
                      
            for rqst in requests:
                rqst.source_data = self.source_data
            rows = []
            self.i_results._output_body(self.source_data, requests, rows, test = True)
            #print ''
            #for l in output: print l
            #for l in rows: print l
            self.assertEqual(output, rows)
            
if __name__=='__main__':
    opus_unittest.main()
