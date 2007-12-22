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

import os
from inprocess.travis.opus_core.indicator_framework.representations.visualization import Visualization as VisualizationRepresentation

class Visualization(object):

    def get_name(self,
                 dataset_name,
                 years,
                 attribute_names = None):
        years = self._get_year_string(years = years)
        
        components = [dataset_name,
                      self.get_visualization_type(),
                      years]
        if attribute_names is not None:
            names = '-'.join(sorted(attribute_names))
            components.append(names)
        name = '|'.join(components)
                    
        return name
    
    def _get_visualization_metadata(self, computed_indicators,
                           indicators_to_visualize,
                           table_name,
                           years):
        return VisualizationRepresentation(
                 indicators = [computed_indicators[ind] 
                               for ind in indicators_to_visualize],
                 visualization_type = self.get_visualization_type(),
                 name = self.name,
                 years = years,
                 table_name = table_name,
                 storage_location = self.storage_location,
                 file_extension = self.get_file_extension()
                )
        
    def _get_year_string(self, years):
        year_agg = []
        years_string = []
        for year in sorted(years):
            if len(year_agg) > 0 and year == year_agg[-1] + 1:
                year_agg.append(year)
            else:
                if len(year_agg) == 1:
                    years_string.append(repr(year_agg[0]))
                elif len(year_agg) > 0:
                    years_string.append('%i-%i'%(year_agg[0],year_agg[-1]))
                year_agg = [year]

        if len(year_agg) == 1:
            years_string.append(repr(year_agg[0]))                    
        elif len(year_agg) > 0:
            years_string.append('%i-%i'%(year_agg[0],year_agg[-1]))
    
        return '_'.join(years_string)


    def visualize(self):
        '''Visualizes the given indicators and returns a dictionary
           with the visualized indicators. 
        '''
        message = ('visualization.visualize needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)

    def get_file_extension(self):
        '''Returns the file extension of the outputted indicator 
        
           Abstract method that needs to be overridden in child classes.
        '''
        message = ('visualization.get_file_extension needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)

    def get_visualization_shorthand(self):
        '''Returns the shorthand for this output type
        
           Abstract method that needs to be overridden in child classes.
        '''
        message = ('visualization.get_visualization_shorthand needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)
            
    def get_additional_metadata(self):
        '''returns additional attributes
        
           Child method should override this method if there are any 
           additional attributes that it has. Return a list of
           (attr_name,value) tuples.
        '''
        return []