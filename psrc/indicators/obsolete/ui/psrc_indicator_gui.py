#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

# open a traits-based GUI for editing PSRC indicator requests


from urbansim.indicators.indicator_configuration import IndicatorConfiguration
from urbansim.indicators.ui.indicator_configuration_handler import IndicatorConfigurationHandler
from opus_core.configurations.dataset_description import DatasetDescription

all_datasets = [DatasetDescription(dataset_name='gridcell', package_name='urbansim', nchunks=2), 
                DatasetDescription(dataset_name='household', package_name='urbansim'), 
                DatasetDescription(dataset_name='job', package_name='urbansim'),
                DatasetDescription(dataset_name='zone', package_name='urbansim'),
                DatasetDescription(dataset_name='travel_data', package_name='urbansim')
                ]

all_years = range(2000,2031)

all_single_year_requests = [
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
                'attribute':{'indicator_name': 'psrc.large_area.de_population_%(year)s',
                             'scale':[1,750000]
                             }
                },  
               {'dataset':'large_area',
                'image_type':'map',
                'attribute':{'indicator_name': 'psrc.large_area.de_employment_%(year)s',
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
                'attribute':{'indicator_name': 'psrc.large_area.share_of_de_population_%(year)s',
                             'scale':[0, 0.2]
                             }
                }, 
               {'dataset':'large_area',
                'image_type':'map',
                'attribute':{'indicator_name': 'psrc.large_area.share_of_de_employment_%(year)s',
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
                             'arguments':['psrc.large_area.de_population_%(year)s', 
                                 'psrc.large_area.de_population_2000'],
                             'scale':[-5000, 250000]
                             }
                }, 
               {'dataset':'large_area',
                'image_type':'map',
                'attribute':{'indicator_name': 'de_employment_change',
                             'operation':'subtract',
                             'arguments':['psrc.large_area.de_employment_%(year)s', 
                                 'psrc.large_area.de_employment_2000'],
                             'scale':[1000, 200000]
                             }
                }, 
# these aren't working:
#               {'dataset':'large_area',
#                'image_type':'map',
#                'attribute':{"indicator_name":'share_of_de_population_change',
#                             "operation":'subtract',
#                             "arguments":['psrc.large_area.share_of_de_population_%(year)s',
#                                 'psrc.large_area.share_of_de_population_2000'],
#                             "scale":[-0.02, 0.02]
#                             }
#                }, 
#               {'dataset':'large_area',
#                'image_type':'map',
#                'attribute':{"indicator_name":'share_of_de_employment_change',
#                             "operation":'subtract',
#                             "arguments":['psrc.large_area.share_of_de_employment_%(year)s',
#                                 'psrc.large_area.share_of_de_employment_2000'],
#                             "scale":[-0.03, 0.03]
#                             }
#                }, 
#                
               # urbansim DE difference
               {'dataset':'large_area',
                'image_type':'map',
                'attribute':{'indicator_name': 'urbansim_de_population_difference',
                             'operation':'subtract',
                             'arguments':['psrc.large_area.population', 
                                 'psrc.large_area.de_population_%(year)s'],
                             'scale':[-75000, 100000]
                             }
                },
               {'dataset':'large_area',
                'image_type':'map',
                'attribute':{'indicator_name': 'urbansim_de_employment_difference',
                             'operation':'subtract',
                             'arguments':['psrc.large_area.number_of_jobs_without_resource_construction_sectors', 
                             'psrc.large_area.de_employment_%(year)s'],
                             'scale':[-50000, 25000]
                             }
                }, 
                
               {'dataset':'large_area',
                'image_type':'map',
                'attribute':{'indicator_name': 'urbansim_de_share_of_population_difference',
                             'operation':'subtract',
                             'arguments':['psrc.large_area.share_of_population', 
                                 'psrc.large_area.share_of_de_population_%(year)s'],
                             'scale':[-0.03, 0.03]
                             }
                }, 
               {'dataset':'large_area',
                'image_type':'map',
                'attribute':{'indicator_name': 'urbansim_de_share_of_employment_difference',
                             'operation':'subtract',
                             'arguments':['psrc.large_area.share_of_employment', 
                                  'psrc.large_area.share_of_de_employment_%(year)s'],
                             'scale':[-0.02, 0.02]
                             }
                }, 

                
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
                 'attribute':{'indicator_name': 'psrc.faz.share_of_de_population_%(year)s',
                              'scale':[0, 0.02]
                              }
                },
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':{'indicator_name': 'psrc.faz.share_of_de_employment_%(year)s',
                              'scale':[0, 0.1]
                              }
                },  
                
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':{'indicator_name': 'de_population_%(year)s',
                              'scale':[1, 60000]
                              }
                }, 
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':{'indicator_name': 'de_employment_%(year)s',
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
                              'arguments':['de_population_%(year)s', 'de_population_2000'],
                              'scale':[-8000, 40000]
                              }
                },
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':{'indicator_name': 'de_employment_change',
                              'operation':'subtract',
                              'arguments':['de_employment_%(year)s', 'de_employment_2000'],
                              'scale':[-2000, 40000]
                              }
                },    
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':{"indicator_name":'share_of_de_population_change',
                              "operation":'subtract',
                              "arguments":['psrc.faz.share_of_de_population_%(year)s',
                                  'psrc.faz.share_of_de_population_2000'],
                              "scale":[-0.001, 0.001]
                              }
                },
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':{"indicator_name":'share_of_de_employment_change',
                              "operation":'subtract',
                              "arguments":['psrc.faz.share_of_de_employment_%(year)s',
                                  'psrc.faz.share_of_de_employment_2000'],
                              "scale":[-0.03, 0.03]
                              }
                },
                
               # urbansim DE difference
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':{'indicator_name': 'urbansim_de_population_difference',
                              'operation':'subtract',
                              'arguments':['urbansim.faz.population', 'de_population_%(year)s'],
                              'scale':[-30000, 30000]
                              }
                }, 
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':{'indicator_name': 'urbansim_de_employment_difference',
                              'operation':'subtract',
                              'arguments':['psrc.faz.number_of_jobs_without_resource_construction_sectors', 
                                  'de_employment_%(year)s'],
                              'scale':[-25000, 10000]
                              }
                }, 
                
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':{'indicator_name': 'urbansim_de_share_of_population_difference',
                              'operation':'subtract',
                              'arguments':['psrc.faz.share_of_population', 
                                  'psrc.faz.share_of_de_population_%(year)s'],
                              'scale':[-0.01, 0.01]
                              }
                }, 
               {'dataset':'faz',
                 'image_type':'map',
                 'attribute':{'indicator_name': 'urbansim_de_share_of_employment_difference',
                              'operation':'subtract',
                              'arguments':['psrc.faz.share_of_employment', 
                                  'psrc.faz.share_of_de_employment_%(year)s'],
                              'scale':[-0.01, 0.01]
                              }
                },
                
                # absolute values
                {'dataset':'zone',
                 'image_type':'map',
                 'attribute':{'indicator_name':'psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone'
                              }
                 },
                {'dataset':'zone',
                 'image_type':'map',
                 'attribute':{'indicator_name':'psrc.zone.generalized_cost_hbw_am_drive_alone_to_129'
                              }
                 },
                 
# **************** geotiff and openev maps not currently working: ******************
#
#                {'dataset':'gridcell',
#                 'image_type':'geotiff',
#                 'attribute':{'indicator_name':'urbansim.gridcell.population',
#                              'prototype_dataset':'W:/GIS_Data/PSRC/Raster/idgrid.tif',
#                             }
#                 },  
#                 
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'urbansim.gridcell.population',
#                     #'legend_file':'gridcell_population.leg'
#                     'legend_scheme':{'range':[0, 10, 50, 100], 
#                     'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },  
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'psrc.gridcell.number_of_nhb_jobs_without_resource_construction_sectors',
#                              #'legend_file':'gridcell_number_of_jobs.leg'
#                              'legend_scheme':{'range':[0, 5, 20, 100], 
#                              'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'urbansim.gridcell.residential_units',
#                              #'legend_file':'gridcell_number_of_jobs.leg'
#                              'legend_scheme':{'range':[0, 5, 25, 50], 
#                              'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'urbansim.gridcell.commercial_sqft',
#                              #'legend_file':'gridcell_number_of_jobs.leg'
#                              'legend_scheme':{'range':[0, 500, 5000, 25000], 
#                              'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'urbansim.gridcell.industrial_sqft',
#                              #'legend_file':'gridcell_number_of_jobs.leg'
#                              'legend_scheme':{'range':[0, 500, 5000, 25000], 
#                              'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'urbansim.gridcell.developable_maximum_residential_units',
#                              #'legend_file':'gridcell_residential_units_capacity.leg'
#                              'legend_scheme':{'range':[0, 6, 22, 67], 
#                              'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'urbansim.gridcell.developable_maximum_commercial_sqft',
#                              #'legend_file':'gridcell_commercial_sqft_capacity.leg'
#                              'legend_scheme':{'range':[0, 500, 5000, 25000], 
#                              'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'urbansim.gridcell.developable_maximum_industrial_sqft',
#                              #'legend_file':'gridcell_industrial_sqft_capacity.leg'
#                              'legend_scheme':{'range':[0, 500, 5000, 25000], 
#                              'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'urbansim.gridcell.total_land_value',
#                              'legend_scheme':{'range':[0, 50000, 250000, 1000000], 
#                              'color':['#b2b2aea3', '#ccff00ff','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },
#                 
#                 # change value
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'urbansim_population_change',
#                              'operation':'change',
#                              'arguments':['urbansim.gridcell.population'],
#                              'legend_scheme':{'range':[-1, 0, 20, 40], 
#                              'color':['#ccff00ff','#b2b2aea3','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },
#                {'dataset':'gridcell',
#                 'image_type':'openev_map',
#                 'attribute':{'indicator_name':'urbansim_employment_change',
#                              'operation':'change',
#                              'arguments':['psrc.gridcell.number_of_nhb_jobs_without_resource_construction_sectors'],
#                              'legend_scheme':{'range':[-1, 0, 5, 15], 
#                              'color':['#ccff00ff','#b2b2aea3','#ffcc00ff','#ff6500ff','#ff0000ff']}
#                              }
#                 },
         
         # ************* indicators typically produced for several years *****************
         # absolute values
         {'dataset':'zone',
          'image_type':'map',
          'attribute':{'indicator_name':'psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone',
          'scale':[0, 10000]}
         },
         {'dataset':'zone',
          'image_type':'map',
          'attribute':{'indicator_name':'psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd',
          'scale':[0, 150]}
         }
    ]

all_multi_year_requests = [
        {'dataset':'county',
         'image_type':'chart',
         'attribute':'psrc.county.population'
        },
        {'dataset':'county',
         'image_type':'chart',
         'attribute':'psrc.county.number_of_jobs'
        }, 
        {'dataset':'county',
         'image_type':'table',
         'attribute':'psrc.county.population'
        },
        {'dataset':'county',
         'image_type':'table',
         'attribute':'psrc.county.number_of_jobs'
        }, 
        {'dataset':'large_area',
         'image_type':'table',
         'attribute':'psrc.large_area.population'
         },
        {'dataset':'large_area',
         'image_type':'table',
         'attribute':'psrc.large_area.number_of_jobs'
         },
        {'dataset':'large_area',
         'image_type':'table',
         'attribute':'psrc.large_area.number_of_jobs_without_resource_construction_sectors'
         },
# aggregate doesn't seem to be working
#        {'label': 'table of urbansim.gridcell.residential_units aggregated',
#         'dataset':'alldata',
#         'image_type':'table',
#         'attribute':'core.func.Residential_Units = alldata.aggregate_all(urbansim.gridcell.residential_units, function=sum)'
#          }, 
         {'dataset':'large_area',
          'image_type':'table',
          'attribute':'psrc.large_area.average_land_value_for_plan_type_group_residential'
         },
         {'dataset':'large_area',
          'image_type':'table',
          'attribute':'psrc.large_area.average_land_value_for_plan_type_group_non_residential'
         },  
         {'dataset':'faz',
          'image_type':'table',
          'attribute':'urbansim.faz.population'
         },   
         {'dataset':'faz',
          'image_type':'table',
          'attribute':'urbansim.faz.number_of_jobs'
         },
         {'dataset':'zone',
          'image_type':'table',
          'attribute':'urbansim.zone.number_of_jobs'
         }
    ]

config = IndicatorConfiguration()
#config.database_configuration.database_name = 'PSRC_2000_baseyear'
#config.cache_directory = r'\\viborg\d_urbansim_cache\run_695.2006_10_06_13_02'
#config.run_description = '(run 329 - baseline 5/2)'

#config.use_cache_directory_for_output = True

#config.datasets_to_preload = all_datasets

#handler = IndicatorConfigurationHandler(all_datasets=all_datasets, 
#                                        all_years=all_years, 
#                                        all_single_year_requests=all_single_year_requests, 
#                                        all_multi_year_requests=all_multi_year_requests)

handler = IndicatorConfigurationHandler()
handler.open_editor(config)