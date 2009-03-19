# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE
        
class IndicatorMetaData(object):
    ''' This is a collection of methods that return data about available indicators. 
    
        In the future, this information should be accessed in some other way.
    '''
        
    def get_indicator_documentation_URL(cls):
        return r'http://www.urbansim.org/docs/indicators/'
    
    def get_indicators_in_categories(cls):
        '''returns a breakdown of indicators into multiple categories'''
        
        return {
                'Transportation' : [
                                'Vehicle miles traveled',
                                'Vehicle miles traveled per capita',
                                'Gasoline consumed per capita',
                                'Percentage of trips taken by bike',
                                'Percentage of trips walked',
                                'Percentage of trips taken in a single occupancy vehicle',
                                'Percentage of trips taken via carpool',
                                'Percentage of trips taken on mass transit',
                                'Percentage of trips taken as park and ride',
                                'Percentage of trips taken by bike or walked',
                                'Percentage of automobile trips which are carpools',
                                
                                ],
                                
        
               'Environmental Impacts': [
                                 'Greenhouse gas emissions from vehicle use',
                                ],
                                         
               'Land Use and Real Estate Development':  [
                                'Residential units',
                                'Residential units added',
                                'Residential units added per starting development type',
                                'Residential units added per ending development type',
                                'Residential density',
                                'Occupied residential units',
                                'Vacant residential units',
                                'Residential vacancy rate',
                                'Residential vacancy rate per development type',
                                'Residential unit value',
                                'Nonresidential square feet',
                                'Nonresidential square feet added',
                                'Nonresidential square feet added per starting development type',
                                'Occupied nonresidential square feet',
                                'Vacant nonresidential square feet',
                                'Nonresidential square feet vacancy rate',
                                'Nonresidential square feet vacancy rate per development type',
                                'Nonresidential square foot value',
                                'Acres of vacant developable land',
                                'Acres of land converted from type vacant developable per development type',
                                'Development events',
                                'Development events per starting development type',
                                'Grid cells per development type',
                                ],
        
                'Employment ' : [
                                'Employment',
                                'Employment change',
                                'Employment density',
                                'Jobs housing balance',
                                'Jobs moving',
                                'Jobs per capita',
                                'Job spaces',
                                'Unplaced jobs',
                                ],
                'Households and Population': [
                                'Households',
                                'Households added or deleted',
                                'Household car ownership',
                                'Household density',
                                'Households moving',
                                'Mean household income',
                                'Unplaced households',
                                'Population',
                                'Population change',
                                'Population density',
                                'Fraction of population living in compact neighborhoods',
                                ],
                }
    
    def get_indicator_info(cls):
        '''returns a list of tuples, each of which represent an indicator.
        The tuple is of the format (name, path, variable, documentation)'''
        
        return [
                ('Greenhouse gas emissions from vehicle use',
                 'greenhouse_gas_emissions_from_vehicle_travel = alldata.aggregate_all(psrc.zone.greenhouse_gas_emissions_from_vehicle_travel, function=sum)',
                 'greenhouse_gas_emissions_from_vehicle_travel',
                 'greenhouse_gas_emissions_from_vehicle_travel.xml'),
                ('Vehicle miles traveled',
                 'vehicle_miles_traveled = alldata.aggregate_all(psrc.zone.vehicle_miles_traveled, function=sum)',
                 'vehicle_miles_traveled',
                 'vehicle_miles_traveled.xml'),
                ('Vehicle miles traveled per capita',
                 'vehicle_miles_traveled_per_capita = alldata.aggregate_all(psrc.zone.vehicle_miles_traveled_per_capita, function=mean)',
                 'vehicle_miles_traveled_per_capita',
                 'vehicle_miles_traveled.xml'),
                ('Gasoline consumed per capita',
                 'gasoline_consumed_per_capita = alldata.aggregate_all(psrc.zone.gasoline_consumed_per_capita, function=mean)',
                 'gasoline_consumed_per_capita',
                 'gasoline_consumed_per_capita.xml'),
                ('Percentage of trips taken by bike','',
                 '',
                 ''),
                ('Percentage of trips walked','',
                 '',
                 ''),
                ('Percentage of trips taken in a single occupancy vehicle','',
                 '',
                 ''),
                ('Percentage of trips taken via carpool','',
                 '',
                 ''),
                ('Percentage of trips taken on mass transit','',
                 '',
                 ''),
                ('Percentage of trips taken as park and ride','',
                 '',
                 ''),
                ('Percentage of trips taken by bike or walked','',
                 '',
                 ''),
                ('Percentage of automobile trips which are carpools','',
                 '',
                 ''),
                ('Residential units','',
                 '',
                 ''),
                ('Residential units added','',
                 '',
                 ''),
                ('Residential units added per starting development type','',
                 '',
                 ''),
                ('Residential units added per ending development type','',
                 '',
                 ''),
                ('Residential density','',
                 '',
                 ''),
                ('Occupied residential units','',
                 '',
                 ''),
                ('Vacant residential units','urbansim.gridcell.vacant_residential_units',
                 'vacant_residential_units',
                 'vac_res_units.xml'),
                ('Residential vacancy rate','',
                 '',
                 ''),
                ('Residential vacancy rate per development type','',
                 '',
                 ''),
                ('Residential unit value','',
                 '',
                 ''),
                ('Nonresidential square feet','',
                 '',
                 ''),
                ('Nonresidential square feet added','',
                 '',
                 ''),
                ('Nonresidential square feet added per starting development type','',
                 '',
                 ''),
                ('Occupied nonresidential square feet','',
                 '',
                 ''),
                ('Vacant nonresidential square feet','',
                 '',
                 ''),
                ('Nonresidential square feet vacancy rate','',
                 '',
                 ''),
                ('Nonresidential square feet vacancy rate per development type','',
                 '',
                 ''),
                ('Nonresidential square foot value','',
                 '',
                 ''),
                ('Acres of vacant developable land','',
                 '',
                 ''),
                ('Acres of land converted from type vacant developable per development type','',
                 '',
                 ''),
                ('Development events','',
                 '',
                 ''),
                ('Development events per starting development type','',
                 '',
                 ''),
                ('Grid cells per development type','',
                 '',
                 ''),
                ('Employment',
                 'urbansim.gridcell.number_of_jobs',
                 'number_of_jobs',
                 'employment.xml'),
                ('Employment change','',
                 '',
                 ''),
                ('Employment density','',
                 '',
                 ''),
                ('Jobs housing balance','',
                 '',
                 ''),
                ('Jobs moving','',
                 '',
                 ''),
                ('Jobs per capita','',
                 '',
                 ''),
                ('Job spaces','',
                 '',
                 ''),
                ('Unplaced jobs','',
                 '',
                 ''),
                ('Households','',
                 '',
                 ''),
                ('Households added or deleted','',
                 '',
                 ''),
                ('Household car ownership','',
                 '',
                 ''),
                ('Household density','',
                 '',
                 ''),
                ('Households moving','',
                 '',
                 ''),
                ('Mean household income',
                 'urbansim.gridcell.average_income',
                 'average_income',
                 'mean_household_income.xml'),
                ('Unplaced households','',
                 '',
                 ''),
                ('Population',
                 'urbansim.gridcell.population',
                 'population',
                 'population.xml'),
                ('Population change','',
                 '',
                 ''),
                ('Population density','',
                 '',
                 ''),
                ('Fraction of population living in compact neighborhoods', '',
                 '',
                 ''),
            ]    
        
    get_indicator_info = classmethod(get_indicator_info)
    get_indicator_documentation_URL = classmethod(get_indicator_documentation_URL)
    get_indicators_in_categories = classmethod(get_indicators_in_categories)