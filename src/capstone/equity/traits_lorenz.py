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
    from enthought.traits import HasTraits, Str, Int
    from enthought.traits.ui import Item, View, Group
except:
    logger.log_warning('Could not load traits.ui. Skipping %s!' % __file__)
else:
    from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
    from opus_core.indicator_framework.traits.traits_abstract_indicator import TraitsAbstractIndicator
    
    class TraitsLorenz(TraitsAbstractIndicator):
        '''The traits version of a Lorenz curve'''
        
        #todo: make this a reg expression
        min = Int
        max = Int

        traits_view = View(
            Item('attribute', label = 'Attribute', width = 300),
            Item('name', label = 'Name (optional)', width = 300),
            Item('dataset_name', label = 'Dataset', width = 300),     
            Item('years', label = 'Year(s)', width = 300)
        )
                    
        def detraitify(self, source_data):
            '''Detraitify output-type-specific traits.
               source_data -- the SourceData object which the detrait-ed object requires
            '''
            detraits_dict = {}
            TraitsAbstractIndicator._detraitify(self, detraits_dict, source_data)
            if self.max != self.min:
                detraits_dict['scale'] = [int(self.min), int(self.max)]
            else:
                detraits_dict['scale'] = None
            lorenz = LorenzCurve(**detraits_dict)
            return lorenz
            