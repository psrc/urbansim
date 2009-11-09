# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 
import os

def create_travel_model_configuration(scenario_dir_name,
                                      mode='full',
                                      years_to_run=None):
    """Returns a travel model configuration for a travel model located
    at the same directory as this script.
    
    scenario_dir_name - is the absolute directory name to the data 
      directory of the travel model scenario
    years_to_run, if specified, indicates what directory to use
      for which year.  It is a dictionary with key=year and value=directory name,
      directory name is relative to scenario_dir_name
    """
    
    travel_model_configuration = {}
    # Edit the following to replace tm.cmd with the name of the batch file to run the travel model
    travel_model_configuration['travel_model_command'] = os.path.join(scenario_dir_name, "tm.cmd")
    
    ### mapping from urbansim zone variable name to travel model TAZ attribute name 
    urbansim_to_tm_variable_mapping = [
        ('(zone.zone_id).astype(int16)', 'SFTAZ'),   #normally use zone_id as join field
#        ('zone.seq_taz', 'ID'),    #alternatively id field
        ('sanfrancisco.zone.number_of_households', 'HHLDS'),
        ('sanfrancisco.zone.population', 'POP'),
        ('sanfrancisco.zone.employment', 'EMPLOYMENT'),
        ('zone.aggregate(household.nfulltime+household.nparttime,intermediates=[building, parcel])', 'EMPLOYEDRESIDENTS'),        
        ('zone.aggregate(sanfrancisco.building.employment_of_building_use_cie, intermediates=[parcel])', 'EMP-CIE'),
        ('zone.aggregate(sanfrancisco.building.employment_of_building_use_med, intermediates=[parcel])', 'EMP-MED'),
        ('zone.aggregate(sanfrancisco.building.employment_of_building_use_mips, intermediates=[parcel])', 'EMP-MIPS'),
        ('zone.aggregate(sanfrancisco.building.employment_of_building_use_retailent, intermediates=[parcel])', 'EMP-RETAILENT'),
        ('zone.aggregate(sanfrancisco.building.employment_of_building_use_pdr, intermediates=[parcel])', 'EMP-PDR'),
        ('zone.aggregate(sanfrancisco.building.employment_of_building_use_visitor, intermediates=[parcel])', 'EMP-VISITOR'),
        ]
                                    
    travel_model_configuration.update( {
        "urbansim_to_tm_variable_mapping":urbansim_to_tm_variable_mapping,
    ### name of the file containing the input/output of data for/from travel model, 
    ### including header in csv format
    ### file location relative to os.path.join(scenario_dir_name, year_dir)
        "urbansim_to_tm_variable_file":  r"tm_input.csv",  
        "tm_to_urbansim_variable_file":  r"tm_output.csv",
        } )
    
    travel_model_configuration['directory'] = scenario_dir_name

    _add_models(travel_model_configuration, mode)
    _add_years(travel_model_configuration, years_to_run)
    return travel_model_configuration

def _add_models(travel_model_configuration, mode):
    if mode == 'full':
        models = [
            'sanfrancisco.travel_model.get_cache_data_into_travel_model',
            'sanfrancisco.travel_model.run_sanfrancisco_travel_model',
            'sanfrancisco.travel_model.get_travel_model_data_into_cache',
            ]
    travel_model_configuration['models'] = models
        
def _add_years(travel_model_configuration, years_to_run):
    if years_to_run is None:
        years_to_run = {
            2005:r'2005',   #path to save interchanging files between urbansim and travel model
            2010:r'2010',   #path relative to scenario_dir_name
            2015:r'2015',
            2025:r'2025',
            }
    for year, year_dir in years_to_run.iteritems():
        travel_model_configuration[year] = year_dir
        
