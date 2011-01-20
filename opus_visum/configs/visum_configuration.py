# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.configuration import Configuration

class VisumConfiguration(Configuration):
    
    """Travel model configuration object
    """

    def __init__(self, travel_model_dir_name, mode='full', years_to_run=None, procedure_file="opus.par"):
        """Returns a travel model configuration for a travel model located at this directory.

	travel_model_dir_name - the absolute directory name to the data directory of the travel model scenario
	                        the directory that containing *.ver files

        mode must be one of the following:
        'full': run the travel model properly.
        'skims': get the travel model results from last travel model run, without running travel model.
        'null': do the pre- and post-processing for the travel model, without actually running the travel model.

	years_to_run, if specified, indicates what travel model bank set to use
	for which year.  It is a dictionary with key=year and value=version file name.
	
	procedure_file - in travel_model_dir_name
	"""

	travel_model_configuration = {}
	
	travel_model_configuration.update( {'visum_version_number': 10} )
	
	### mapping from visum matrice name to urbansim travel_data variable name
	## dict key is used as matrix number for VisumPy.helpers.GetODMatrix and VisumPy.helpers.GetSkimMatrix
	## dict value is used as attribute name for urbansim travel_data table
	tm_to_urbansim_variables = {
	'od':{
	    ## need data for zone index, e.g.
            #  -1:'from_zone_id',
	    #  -2:'to_zone_id',
	1:'transit_trips',   #'transit (PuT - public transport) trips',
	2:'auto_trips',      #'auto trips',
	}, 
	'skim':{   
	    ## need data for zone index, e.g.
            #  -1:'from_zone_id',
	    #  -2:'to_zone_id',
	1: 'auto_travel_time',         #'auto assigned travel time (ttc)',
	2: 'transit_in_vehicle_time'   #'PuT in-vehicle time (ivt)',
	} 
	}
    
	### TAZ attributes to be transferred from urbansim to visum
	urbansim_to_tm_variables = [
	    'TAZ=(zone.zone_id).astype(int16)',
	    'retail_by_taz=zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_retail)', 
	    ## the employment groups below need to be defined in employment_adhoc_sector_groups and 
	    ## employment_adhoc_sector_group_definitions before they can be used
	    #'fires_by_taz=zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_fires)',
	    #'gov_by_taz=zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_gov)',
	    #"educ_by_taz=zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_educ)",
	    #"wtcu_by_taz=zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_wtcu)",
	    #"manu_by_taz=zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_manu)",
	    #"univ_by_taz=zone.aggregate(urbansim.gridcell.number_of_jobs_of_group_univ)",
	    ## need to change income categories to 4 instead of 3
	    "low_income_hh_by_taz=zone.aggregate(urbansim.gridcell.number_of_low_income_households)",
	    "mid_income_hh_by_taz=zone.aggregate(urbansim.gridcell.number_of_mid_income_households)",
	    #"upper_mid_income_hh_by_taz=?",
	    "upper_income_hh_by_taz=zone.aggregate(urbansim.gridcell.number_of_high_income_households)",
	    ## need variable specification
	    #"pctmf=?",
	    #"gqi=?",
	    #"gqn=?",
	    #"fteuniv=?",
	    #"density=?"
        ]
    
	travel_model_configuration.update( {
	    "tm_to_urbansim_variables":tm_to_urbansim_variables,
	    "urbansim_to_tm_variables":urbansim_to_tm_variables,
	} )
	
	self.__add_models(travel_model_configuration, mode)
	self.__add_years(travel_model_configuration, travel_model_dir_name, years_to_run, procedure_file)

	self.merge(travel_model_configuration)

    def __add_models(self, travel_model_configuration, mode):
        if mode == 'full':
            models = [
		'opus_visum.models.get_cache_data_into_visum',
		'opus_visum.models.run_travel_model',
		'opus_visum.models.get_visum_data_into_cache',
            ]
        elif mode == 'skims':
            models = [
		'opus_visum.models.get_visum_data_into_cache',
            ]
        elif mode == 'null':
            models = [
		'opus_visum.models.get_cache_data_into_visum',
		'opus_visum.models.get_visum_data_into_cache',
            ]
        travel_model_configuration['models'] = models

    def __add_years(self, travel_model_configuration, travel_model_dir_name, years_to_run, procedure_file):

        if years_to_run is None:
            years_to_run = {
            #1980:'1980.ver',	    
            1981:'1980.ver',
            1990:'1990.ver',
            2000:'2000.ver',
            2002:'2002.ver',
            2004:'2004.ver'
            }
        for year, year_dir in years_to_run.iteritems():
            travel_model_configuration[year] = {
            'version':[travel_model_dir_name,year_dir],
            'procedure_file':procedure_file
            }
