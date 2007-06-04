#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
from general_info import general_info
from urbansim.indicators.indicator_factory import IndicatorFactory

# The indicators to chart or map
general_info['year'] = 2030

indicators = [
        # absolute value      
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name':'psrc.large_area.population', 
                      'scale':[1,750000]
                      }
         },
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name':'psrc.large_area.number_of_jobs_without_resource_construction_sectors',
                      'scale':[1,700000]
                      }
         },
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'psrc.large_area.de_population_%s' % general_info['year'],
                      'scale':[1,750000]
                      }
         },
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'psrc.large_area.de_employment_%s' % general_info['year'],
                      'scale':[1,700000]
                      }
         },
         
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name':'psrc.large_area.share_of_population',
                      'scale':[0.0, 0.2]
                      }
         },
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name':'psrc.large_area.share_of_employment',
                      'scale':[0, 0.2]
                      }
         },
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'psrc.large_area.share_of_de_population_%s' % general_info['year'],
                      'scale':[0, 0.2]
                      }
         },
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'psrc.large_area.share_of_de_employment_%s' % general_info['year'],
                      'scale':[0, 0.2]
                      }
         },
         
        # change value    
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_population_change',
                      'operation':'change',
                      'arguments':['psrc.large_area.population'],
                      'scale':[-5000, 250000]
                      }
         },    
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_employment_change',
                      'operation':'change',
                      'arguments':['psrc.large_area.number_of_jobs_without_resource_construction_sectors'],
                      'scale':[1000, 200000]
                      }
         }, 
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'de_population_change',
                      'operation':'subtract',
                      'arguments':['psrc.large_area.de_population_%s' % general_info['year'], 
                                   'psrc.large_area.de_population_2000'],
                      'scale':[-5000, 250000]
                      }
         }, 
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'de_employment_change',
                      'operation':'subtract',
                      'arguments':['psrc.large_area.de_employment_%s' % general_info['year'], 
                                   'psrc.large_area.de_employment_2000'],
                      'scale':[1000, 200000]
                      }
         }, 
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{"indicator_name":'share_of_de_population_change',
                      "operation":'subtract',
                      "arguments":['psrc.large_area.share_of_de_population_%s' % general_info['year'],
                                   'psrc.large_area.share_of_de_population_2000'],
                      "scale":[-0.02, 0.02]
                      }
         }, 
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{"indicator_name":'share_of_de_employment_change',
                      "operation":'subtract',
                      "arguments":['psrc.large_area.share_of_de_employment_%s' % general_info['year'],
                                   'psrc.large_area.share_of_de_employment_2000'],
                      "scale":[-0.03, 0.03],
                      }
         }, 
         
        # urbansim DE difference 
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_de_population_difference',
                      'operation':'subtract',
                      'arguments':['psrc.large_area.population', 
                                   'psrc.large_area.de_population_%s' % general_info['year']],
                                   'scale':[-75000, 100000]
             }
         }, 
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_de_employment_difference',
                      'operation':'subtract',
                      'arguments':['psrc.large_area.number_of_jobs_without_resource_construction_sectors', 
                                   'psrc.large_area.de_employment_%s' % general_info['year']],
                      'scale':[-50000, 25000]
                      }
         },
         
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_de_share_of_population_difference',
                      'operation':'subtract',
                      'arguments':['psrc.large_area.share_of_population', 
                                   'psrc.large_area.share_of_de_population_%s' % general_info['year']],
                      'scale':[-0.03, 0.03]
                      }
         },
        {'dataset':'large_area',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_de_share_of_employment_difference',
                      'operation':'subtract',
                      'arguments':['psrc.large_area.share_of_employment', 
                                   'psrc.large_area.share_of_de_employment_%s' % general_info['year']],
                      'scale':[-0.02, 0.02]
                      }
         },
         
        # absolute values 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name':'urbansim.faz.population',
                      'scale':[1, 60000]
                      }
         },  
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name':'psrc.faz.number_of_jobs_without_resource_construction_sectors',
                      'scale':[1, 150000]
                      }
         }, 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name':'psrc.faz.share_of_population',
                      'scale':[0.0, 0.02]
                      }
         }, 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name':'psrc.faz.share_of_employment',
                      'scale':[0, 0.1]
                      }
         }, 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'psrc.faz.share_of_de_population_%s' % general_info['year'],
                      'scale':[0, 0.02]
                      }
         }, 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'psrc.faz.share_of_de_employment_%s' % general_info['year'],
                      'scale':[0, 0.1]
                      }
         }, 
        
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'de_population_%s' % general_info['year'],
                      'scale':[1, 60000]
                      }
         }, 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'de_employment_%s' % general_info['year'],
                      'scale':[1, 150000]
                      }
         },  
         
        # change value 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_population_change',
                      'operation':'change',
                      'arguments':['urbansim.faz.population'],
                      'scale':[-8000, 40000]
                      }
         },  
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_employment_change',
                      'operation':'change',
                      'arguments':['psrc.faz.number_of_jobs_without_resource_construction_sectors'],
                      'scale':[-2000, 40000]
                      }
         }, 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{"indicator_name":'urbansim_share_of_population_change',
                      "operation":'change',
                      "arguments":['psrc.faz.share_of_population'],
                      "scale":[-0.001, 0.001]
                      }
         }, 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{"indicator_name":'urbansim_share_of_employment_change',
                      "operation":'change',
                      "arguments":['psrc.faz.share_of_employment'],
                      "scale":[-0.03, 0.03]
                      }
         }, 
         
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'de_population_change',
                      'operation':'subtract',
                      'arguments':['de_population_%s' % general_info['year'], 'de_population_2000'],
                      'scale':[-8000, 40000]
                      }
         }, 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'de_employment_change',
                      'operation':'subtract',
                      'arguments':['de_employment_%s' % general_info['year'], 'de_employment_2000'],
                      'scale':[-2000, 40000]
                      }
         }, 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{"indicator_name":'share_of_de_population_change',
                      "operation":'subtract',
                      "arguments":['psrc.faz.share_of_de_population_%s' % general_info['year'],
                                   'psrc.faz.share_of_de_population_2000'],
                      "scale":[-0.001, 0.001]
                      }
         }, 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{"indicator_name":'share_of_de_employment_change',
                      "operation":'subtract',
                      "arguments":['psrc.faz.share_of_de_employment_%s' % general_info['year'],
                                   'psrc.faz.share_of_de_employment_2000'],
                      "scale":[-0.03, 0.03]
                      }
         }, 
         
        # urbansim DE difference 
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_de_population_difference',
                      'operation':'subtract',
                      'arguments':['urbansim.faz.population', 'de_population_%s' % general_info['year']],
                      'scale':[-30000, 30000]
                      }
         },
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_de_employment_difference',
                      'operation':'subtract',
                      'arguments':['psrc.faz.number_of_jobs_without_resource_construction_sectors', 
                                   'de_employment_%s' % general_info['year']],
                      'scale':[-25000, 10000]
                      }
         },     
         
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_de_share_of_population_difference',
                      'operation':'subtract',
                      'arguments':['psrc.faz.share_of_population', 
                                   'psrc.faz.share_of_de_population_%s' % general_info['year']],
                      'scale':[-0.01, 0.01]
                      }
         },
        {'dataset':'faz',
         'image_type':'map',
         
         'attribute':{'indicator_name': 'urbansim_de_share_of_employment_difference',
                      'operation':'subtract',
                      'arguments':['psrc.faz.share_of_employment', 
                                   'psrc.faz.share_of_de_employment_%s' % general_info['year']],
                      'scale':[-0.01, 0.01]
                      }
         },
         
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'urbansim.gridcell.population',
                      #'legend_file':'gridcell_population.leg'
                      'legend_scheme':{'range':[0, 10, 50, 100], 'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         }, 
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'psrc.gridcell.number_of_nhb_jobs_without_resource_construction_sectors',
                      #'legend_file':'gridcell_number_of_jobs.leg'
                      'legend_scheme':{'range':[0, 5, 20, 100], 'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         }, 
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'urbansim.gridcell.residential_units',
                      #'legend_file':'gridcell_number_of_jobs.leg'
                      'legend_scheme':{'range':[0, 5, 25, 50], 'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         }, 
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'urbansim.gridcell.commercial_sqft',
                      #'legend_file':'gridcell_number_of_jobs.leg'
                      'legend_scheme':{'range':[0, 500, 5000, 25000], 'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         }, 
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'urbansim.gridcell.industrial_sqft',
                      #'legend_file':'gridcell_number_of_jobs.leg'
                      'legend_scheme':{'range':[0, 500, 5000, 25000], 'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         }, 
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'urbansim.gridcell.developable_maximum_residential_units',
                      #'legend_file':'gridcell_residential_units_capacity.leg'
                      'legend_scheme':{'range':[0, 6, 22, 67], 'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         }, 
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'urbansim.gridcell.developable_maximum_commercial_sqft',
                      #'legend_file':'gridcell_commercial_sqft_capacity.leg'
                      'legend_scheme':{'range':[0, 500, 5000, 25000], 'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         }, 
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'urbansim.gridcell.developable_maximum_industrial_sqft',
                      #'legend_file':'gridcell_industrial_sqft_capacity.leg'
                      'legend_scheme':{'range':[0, 500, 5000, 25000], 'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         }, 
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'urbansim.gridcell.total_land_value',
                      'legend_scheme':{'range':[0, 50000, 250000, 1000000], 'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         }, 
        
        # change value  
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'urbansim_population_change',
                      'operation':'change',
                      'arguments':['urbansim.gridcell.population'],
                      'legend_scheme':{'range':[-1, 0, 20, 40], 'color':['#ccff00ff','#b2b2aea3','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         },
        {'dataset':'gridcell',
         'image_type':'openev_map',
         
         'attribute':{'indicator_name':'urbansim_employment_change',
                      'operation':'change',
                      'arguments':['psrc.gridcell.number_of_nhb_jobs_without_resource_construction_sectors'],
                      'legend_scheme':{'range':[-1, 0, 5, 15], 'color':['#ccff00ff','#b2b2aea3','#ffcc00ff','#ff6500ff','#ff0000ff']}
                      }
         }                       
    ]

IndicatorFactory().create_indicators(general_info, indicators)