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

import os, re, sys, time, traceback
from copy import copy
from opus_core.indicator_framework.abstract_indicator import AbstractIndicator

from opus_core.logger import logger
from numpy import array, arange
from numpy import ones, zeros, hstack, vstack
from numpy import trapz
from pylab import subplot, plot, show
from pylab import xlabel, ylabel, title, text
from pylab import MultipleLocator, FormatStrFormatter
from pylab import savefig

class LorenzCurve(AbstractIndicator):

    def __init__(self, source_data, dataset_name, 
                 attribute = None, 
                 years = None, expression = None, name = None,
                 scale = None):
        AbstractIndicator.__init__(self, source_data, dataset_name, attribute, years, expression, name)
        self.values = None
        self.ginicoeff = None

    def is_single_year_indicator_image_type(self):
        return True
    
    def get_file_extension(self):
        return 'png'
    
    def get_shorthand(self):
        return 'lorenz_curve'

    def _get_additional_metadata(self):
        return  []
    
    def _create_indicator(self, year):
        """Create a Lorenz Curve for the given indicator,
        save it to the cache directory's 'indicators' sub-directory.
        """
        
        attribute_short = self.get_attribute_alias(year)
        
        title = attribute_short + ' ' + str(year)
        if self.run_description is not None:
            title += '\n' + self.run_description

        # Do calculation
        self.values = array(self._get_indicator(self.attribute, year))
        num_values = self.values.size
        self.values.sort()
        F = arange(1, num_values + 1, 1, "float64")/num_values
        L = self.values.cumsum(dtype="float64")/sum(self.values)
        # Add (0, 0) as the first point for completeness (e.g. plotting)
        origin = array([[0], [0]])
        self.values = vstack((F, L)) 
        self.values = hstack((origin, self.values))
        # This is the simple form of (0.5 - integral) / 0.5
        self.ginicoeff = 1 - 2 * trapz(self.values[1], self.values[0])

        
        file_path = self.get_file_path(year = year)          
    
        self.plot(self.attribute, file_path, year);
        
        return file_path

    def plot(self, attribute, file_path, year):
        a = self.values[0] * 100 
        b = self.values[1] * 100 
        ax = subplot(111)
        plot(a, a, 'k--', a, b, 'r')
        ax.set_ylim([0,100])
        ax.grid(color='0.5', linestyle=':', linewidth=0.5)
        xlabel('population')
        ylabel(attribute)
        title('Lorenz curve')
        font = {'fontname'   : 'Courier',
          'color'      : 'r',
          'fontweight' : 'bold',
          'fontsize'   : 11
        }
        box = { 'pad' : 6,
          'facecolor' : 'w',
          'linewidth' : 1,
          'fill' : True
        }
        text(5, 90, 'Gini coefficient:  %(gini)f' % {'gini' : self.ginicoeff}, font, color='k', bbox=box )
        majorLocator = MultipleLocator(20)
        majorFormatter = FormatStrFormatter('%d %%')
        minorLocator = MultipleLocator(5)
        ax.xaxis.set_major_locator( majorLocator )
        ax.xaxis.set_major_formatter( majorFormatter)
        ax.xaxis.set_minor_locator( minorLocator )
        ax.yaxis.set_major_locator( majorLocator )
        ax.yaxis.set_major_formatter( majorFormatter)
        ax.yaxis.set_minor_locator( minorLocator )
        savefig(file_path)


import os
import tempfile
from opus_core.tests import opus_unittest

from shutil import copytree, rmtree

from opus_core.opus_package_info import package
from opus_core.configurations.dataset_description import DatasetDescription

from opus_core.indicator_framework.source_data import SourceData
from opus_core.indicator_framework.abstract_indicator import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
        
    def skip_test_create_indicator(self):
        ####NOTE: THIS TEST FAILS BECAUSE THE OPUS_CORE DATASET DOES NOT HAVE 2D ATTRIBUTES, X/Y AXES
        
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))
        
        map = Map(
                  source_data = self.source_data,
                  attribute = 'package.test.attribute',
                  dataset_name = 'test',
                  years = None, 
                  scale = [1,1000], 
                  name = 'my_name'
        )
                
        map.create(False)
        
        self.assert_(os.path.exists(indicator_path))
        self.assert_(os.path.exists(os.path.join(indicator_path, 'test__map__my_name__1980.png')))

if __name__ == '__main__':
    try: 
        import matplotlib
    except:
        print 'could not import matplotlib'
    else:
        opus_unittest.main()
