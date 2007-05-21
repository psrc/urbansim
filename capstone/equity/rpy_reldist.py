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
import os, re, sys, time, traceback
from copy import copy

from opus_core.indicator_framework.abstract_indicator import AbstractIndicator

from numpy import newaxis, array

try:
    from rpy import *
except:
    pass
else:
    
    class Reldist(AbstractIndicator):
    
        def __init__(self, source_data, dataset_name, 
                     attribute = None, 
                     years = None, expression = None, name = None):
            AbstractIndicator.__init__(self, source_data, dataset_name, attribute, years, expression, name)
    
        def is_single_year_indicator_image_type(self):
            return False
        
        def get_file_extension(self):
            return 'png'
        
        def get_shorthand(self):
            return 'reldist'
        
        def _create_indicator(self, years):
            """Create a chart for the given indicator, save it to the cache
            directory's 'indicators' sub-directory.
            """
                
            values, years = self._get_indicator_for_years(self.attribute, years)
            
            if len(years) != 2:
                raise Exception, 'This plot can only compare 2 years'
            
            file_path = self.get_file_path()    
            
            r.library('reldist')
            r.png(file_path)
            r.reldist(y=values[1],yo=values[0],
                      ci=False,smooth=0.4,
                      cdfplot=True, 
                      yolabs=array([-1.0, -0.5,  0.0,  0.5,  1.0,  1.5,  2.0,  2.5,  3.0]), 
                      ylabs=array([-1.0, -0.5,  0.0,  0.5,  1.0,  1.5,  2.0,  2.5,  3.0]), 
                      cex=0.8, 
                      ylab="proportion of the recent cohort, year: %d" % years[1], 
                      xlab="proportion of the original cohort, year: %d"  % years[0] ) 
            r.dev_off()
            
            return file_path

