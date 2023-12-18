# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, re, sys, time, traceback
from copy import copy
from opus_core.indicator_framework.core.abstract_indicator import AbstractIndicator

from opus_core.logger import logger
from numpy import array, arange
from numpy import ones, zeros, hstack, vstack
from numpy import trapz, trim_zeros
from pylab import subplot, plot, show
from pylab import xlabel, ylabel, title, text
from pylab import MultipleLocator, FormatStrFormatter
from pylab import savefig, clf, close

class LorenzCurve(AbstractIndicator):

    def __init__(self, source_data, dataset_name, 
                 attribute = None, 
                 years = None, operation = None, name = None, scale = None,
                 storage_location = None):
        AbstractIndicator.__init__(self, source_data, dataset_name, [attribute], 
                                   years, operation, name,
                                   storage_location)
        self._values = None
        self._ginicoeff = None

    def is_single_year_indicator_image_type(self):
        return True
    
    def get_file_extension(self):
        return 'png'
    
    def get_visualization_shorthand(self):
        return 'lorenzcurve'

    def get_additional_metadata(self):
        return  []
    
    def _create_indicator(self, year):
        """Create a Lorenz Curve for the given indicator,
        save it to the cache directory's 'indicators' sub-directory.
        """
        
        attribute_short = self.get_attribute_alias(attribute = self.attributes[0],
                                                   year = year)
        
        title = attribute_short + ' ' + str(year)
        if self.run_description is not None:
            title += '\n' + self.run_description

        # Do calculation
        # Make fresh copy with dtype float64 to avoid overflows
        self._values = array(self._get_indicator(year, wrap = False).astype('float64'))
        self._compute_lorenz()
        
        file_path = self.get_file_path(year = year)
        self._plot(attribute_short, file_path );
        
        return file_path
    
    def _compute_lorenz(self ):
        ''' Do the lorenz curve computation and save the result in the corresponding
        class variables
        '''
        self._values.sort()
        
        #remove 0 values from array
        self._values = trim_zeros(self._values,'f')
        
        num_values = self._values.size
        F = arange(1, num_values + 1, 1, "float64")/num_values
        L = self._values.cumsum(dtype="float64")/sum(self._values)
        # Add (0, 0) as the first point for completeness (e.g. plotting)
        origin = array([[0], [0]])
        self._values = vstack((F, L)) 
        self._values = hstack((origin, self._values))
        # This is the simple form of (0.5 - integral) / 0.5
        self._ginicoeff = 1 - 2 * trapz(self._values[1], self._values[0])

    def _plot(self, attribute_name, file_path=None ):
        clf() # Clear existing plot
        a = self._values[0] * 100 
        b = self._values[1] * 100 
        ax = subplot(111)
        plot(a, a, 'k--', a, b, 'r')
        ax.set_ylim([0,100])
        ax.grid(color='0.5', linestyle=':', linewidth=0.5)
        xlabel('population')
        ylabel(attribute_name)
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
        text(5, 90, 'Gini coefficient:  %(gini)f' % {'gini' : self._ginicoeff}, font, color='k', bbox=box )
        majorLocator = MultipleLocator(20)
        majorFormatter = FormatStrFormatter('%d %%')
        minorLocator = MultipleLocator(5)
        ax.xaxis.set_major_locator( majorLocator )
        ax.xaxis.set_major_formatter( majorFormatter)
        ax.xaxis.set_minor_locator( minorLocator )
        ax.yaxis.set_major_locator( majorLocator )
        ax.yaxis.set_major_formatter( majorFormatter)
        ax.yaxis.set_minor_locator( minorLocator )
        
        if file_path:
            savefig(file_path)
            close()
        else:
            show()

import os
from opus_core.tests import opus_unittest
from numpy import allclose
from opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
            
    def test_create_indicator(self):
            
        # if the environment variable DISPLAY isn't defined, exit this test
        if 'DISPLAY' not in os.environ:
            return
        
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assertTrue(not os.path.exists(indicator_path))
        
        lorenzcurve = LorenzCurve(
                  source_data = self.source_data,
                  attribute = 'opus_core.test.attribute',
                  dataset_name = 'test',
                  years = None
        )
        
        lorenzcurve.create(False)
        
        self.assertTrue(os.path.exists(indicator_path))
        self.assertTrue(os.path.exists(os.path.join(indicator_path, 'test__lorenzcurve__attribute__1980.png')))

    def test_perfect_equality(self):
        """Perfect equality is when everybody has the same amount of something"""
        # if the environment variable DISPLAY isn't defined, exit this test
        if 'DISPLAY' not in os.environ:
            return
        lorenzcurve = LorenzCurve(
                  source_data = self.source_data,
                  attribute = 'opus_core.test.attribute',
                  dataset_name = 'test',
                  years = None
        )
        incomes = ones(100)
        lorenzcurve._values = incomes
        lorenzcurve._compute_lorenz()
        wanted_result = vstack((arange(0, 101) / 100., arange(0, 101) / 100.))
        self.assertTrue(allclose(lorenzcurve._values, wanted_result))

    def test_perfect_inequality(self):
        """Perfect inequality is when one person has all of something"""
        # if the environment variable DISPLAY isn't defined, exit this test
        if 'DISPLAY' not in os.environ:
            return
        lorenzcurve = LorenzCurve(
                  source_data = self.source_data,
                  attribute = 'opus_core.test.attribute',
                  dataset_name = 'test',
                  years = None
        )
        incomes = zeros(100)
        incomes[0] = 42
        lorenzcurve._values = incomes
        lorenzcurve._compute_lorenz()
        #We strip all the zero values, so the result consists of only two values
        wanted_result = [[0.,1.],[0.,1.]]
        self.assertTrue(allclose(lorenzcurve._values, wanted_result))
        
    def test_small_lorenz(self):
        """Test case for less than 100 people"""
        # if the environment variable DISPLAY isn't defined, exit this test
        if 'DISPLAY' not in os.environ:
            return
        lorenzcurve = LorenzCurve(
                  source_data = self.source_data,
                  attribute = 'opus_core.test.attribute',
                  dataset_name = 'test',
                  years = None
        )
        incomes = array([1, 1, 2, 3, 4, 5])
        lorenzcurve._values = incomes
        lorenzcurve._compute_lorenz()
        wanted_result = array(
            [[ 0, 1/6.,  2/6.,  3/6.,  4/6.,  5/6.,   6/6. ],
             [ 0, 1/16., 2/16., 4/16., 7/16., 11/16., 16/16. ]])
        self.assertTrue(allclose(lorenzcurve._values, wanted_result))
        
    def test_small_gini(self):
        """Test case for gini coefficient for the small case"""
        # if the environment variable DISPLAY isn't defined, exit this test
        if 'DISPLAY' not in os.environ:
            return
        lorenzcurve = LorenzCurve(
                  source_data = self.source_data,
                  attribute = 'opus_core.test.attribute',
                  dataset_name = 'test',
                  years = None
        )
        incomes = array([1, 1, 2, 3, 4, 5])
        
        lorenzcurve._values = incomes
        lorenzcurve._compute_lorenz()

        self.assertAlmostEqual(lorenzcurve._ginicoeff, 0.3125)
        

    def test_large_lorenz(self):
        """Test case for more than 100 people"""
        # if the environment variable DISPLAY isn't defined, exit this test
        if 'DISPLAY' not in os.environ:
            return
        lorenzcurve = LorenzCurve(
                  source_data = self.source_data,
                  attribute = 'opus_core.test.attribute',
                  dataset_name = 'test',
                  years = None
        )
        incomes = array([731, 700, 619, 450, 419, 512, 232, 266, 131, 188,
                         498, 293, 935, 177, 160, 380, 538, 783, 256, 280,
                         731, 362, 870, 970, 674, 211, 524, 207, 513, 461,
                         280, 275, 410, 282, 144, 682, 573, 252, 382, 909,
                         719, 666, 236, 636, 628, 542, 630, 484, 629, 974,
                         747, 509, 281, 725, 377, 565, 495, 840, 391, 191,
                         929, 679, 217, 179, 336, 562, 293, 881, 271, 172,
                         426, 697, 293, 576, 203, 390, 522, 948, 312, 491,
                         531, 959, 646, 495, 306, 631, 722, 322, 876, 586,
                         316, 124, 796, 250, 456, 112, 661, 294, 749, 619,
                         134, 582, 996, 413, 421, 219, 796, 923, 832, 557])
        lorenzcurve._values = incomes
        lorenzcurve._compute_lorenz()

        wanted_result_F = arange(0, 111) / 110.
        wanted_result_L = array([ 0, 0.00202803,  0.00427335,  0.00664542,  0.00907181,  0.01167928,
        0.01457647,  0.01769094,  0.02089595,  0.02413718,  0.02754138,
        0.03099989,  0.0346757 ,  0.03842393,  0.04224459,  0.0461739 ,
        0.05013943,  0.05434035,  0.0586137 ,  0.06314055,  0.06770362,
        0.07233912,  0.07715569,  0.0820628 ,  0.08704234,  0.09211241,
        0.09718249,  0.10227067,  0.10737696,  0.11268243,  0.1179879 ,
        0.12329338,  0.12861696,  0.13415782,  0.13980734,  0.14552928,
        0.15135987,  0.15744396,  0.16399884,  0.17082534,  0.17770615,
        0.18462318,  0.19168508,  0.19876507,  0.20618911,  0.21366748,
        0.22125448,  0.2288777 ,  0.23659146,  0.2447398 ,  0.25299678,
        0.26134429,  0.27010828,  0.27899902,  0.28796219,  0.29692536,
        0.30594285,  0.31515953,  0.32443052,  0.33371962,  0.34317169,
        0.35265998,  0.36227502,  0.3720168 ,  0.38183102,  0.39191685,
        0.40209322,  0.41232391,  0.42269945,  0.43312932,  0.44366784,
        0.45427878,  0.46548727,  0.47669576,  0.48806721,  0.49945678,
        0.51086445,  0.52229023,  0.53380654,  0.54550393,  0.55747293,
        0.56953247,  0.58173686,  0.5940318 ,  0.60638105,  0.61900192,
        0.63167711,  0.64469634,  0.65776989,  0.67089777,  0.68413428,
        0.6973708 ,  0.71089704,  0.72445949,  0.7386376 ,  0.7530511 ,
        0.7674646 ,  0.78252997,  0.79774019,  0.81349364,  0.82935574,
        0.84530837,  0.86176801,  0.87848115,  0.89530294,  0.91223337,
        0.9293992 ,  0.94676421,  0.9643284 ,  0.98196502,  1.        ])

        self.assertTrue(allclose(lorenzcurve._values, vstack((wanted_result_F, wanted_result_L))))
    
if __name__ == '__main__':
    try: 
        import matplotlib
    except:
        print('could not import matplotlib')
    else:
        opus_unittest.main()
