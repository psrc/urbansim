# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

def create_travel_model_configuration(travel_model_dir_name,
                                      mode='full',
                                      years_to_run=None,
                                      emme2_batch_file='QUICKRUN.bat',
                                      locations_to_disaggregate = ['gridcell']):
    """Returns a travel model configuration for a travel model located
    at this directory.
    
    mode must be one of the following:
        'full': run the travel model properly.
        'skims': get the travel model results from last travel model run,
                 without running travel model.
        'null': do the pre- and post-processing for the travel model,
                 without actually running the travel model.
                 
    years_to_run, if specified, indicates what travel model bank set to use
    for which year.  It is a dictionary with key=year and value=name of
    travel model directory containing the banks, e.g. '2000_06'.
    'locations_to_disaggregate is a list of dataset names over which zone_id of households and jobs will be determined.
    """
    
    """a class handling computing urbansim variables for travel model and writing them to a file travel model uses as input
    the variables and the file name are specified in the class
    """
    travel_model_input_file_writer = 'psrc.travel_model_input_file_writer'
    
    """ emme2_matricies and export_macros should be passed in as parameters
    from psrc (or whoever is the specific client of emme2) run_config"""
    emme2_matricies = {
        'bank1':{   
            'au1tim':'am_single_vehicle_to_work_travel_time',
            'au2tim':'am_double_vehicle_to_work_travel_time',
            'au3tim':'am_threeplus_vehicle_to_work_travel_time',
            'biketm':'am_bike_to_work_travel_time',
            'walktm':'am_walk_time_in_minutes',
            'atrtwa':'am_total_transit_time_walk',
            
            'avehda':'am_pk_period_drive_alone_vehicle_trips',
            'ambike':'am_biking_person_trips',
            'amwalk':'am_walking_person_trips',
            'atrnst':'am_transit_person_trip_table',
            'au1cos':'single_vehicle_to_work_travel_cost',
            
            'au1dis': 'single_vehicle_to_work_travel_distance',
            
            "lsum1" : 'logsum_hbw_am_income_1',
            "lsum2" : 'logsum_hbw_am_income_2',
            "lsum3" : 'logsum_hbw_am_income_3',
            "lsum4" : 'logsum_hbw_am_income_4',
            
            'mf91':'am_vehicle_miles_traveled',
#
#            'hbwdap':'hbw_daily_drive_alone_person_trip_table',
#            'hbws2p':'hbw_daily_share_ride2_person_trip_table',
#            'hbws3p':'hbw_daily_share_ride3_person_trip_table',
#            'hbwbkp':'hbw_daily_biking_person_trip_table',
#            'hbwwkp':'hbw_daily_walking_person_trip_table',
#            'hbwtwp':'hbw_daily_walk_to_transit_person_trip_table',
#            'hbwtdp':'hbw_daily_drive_to_park_ride_person_trip_table',
#            
#            'coldap':'college_daily_drive_alone_person_trip_table',
#            'colsrp':'college_daily_share_ride_person_trip_table',
#            'colbkp':'college_daily_biking_person_trip_table',
#            'coltwp':'college_daily_walking_person_trip_table',
#            #'colwkp':'college_daily_walk_to_transit_person_trip_table',
#            'mf42':'college_daily_walk_to_transit_person_trip_table',
            },
        'bank2':{
            'mf91':'md_vehicle_miles_traveled',
            
            "nweuda" : 'nweuda',
            "nweus2" : 'nweus2',
            "nweus3" : 'nweus3',
            "nweutw" : 'nweutw',
            "nweubk" : 'nweubk',
            "nweuwk" : 'nweuwk',
            
#            'off1tm':'md_single_vehicle_to_work_travel_time',
#            'off2tm':'md_double_vehicle_to_work_travel_time',
#            'off3tm':'md_threeplus_vehicle_to_work_travel_time',
#            'nwbktm':'md_bike_to_work_travel_time',
#            'nwwktm':'md_walk_time_in_minutes',
#            'otrtwa':'md_total_transit_time_walk',  
#            
#            'hnwdap':'hbnw_daily_drive_alone_person_trip_table',
#            'hnws2p':'hbnw_daily_share_ride2_person_trip_table',
#            'hnws3p':'hbnw_daily_share_ride3_person_trip_table',
#            'hnwbkp':'hbnw_daily_biking_person_trip_table',
#            'hnwwkp':'hbnw_daily_walking_person_trip_table',
#            'hnwtwp':'hbnw_daily_walk_to_transit_person_trip_table',
#            
#            'nhbdap':'nhb_daily_drive_alone_person_trip_table',
#            'nhbs2p':'nhb_daily_share_ride2_person_trip_table',
#            'nhbs3p':'nhb_daily_share_ride3_person_trip_table',
#            'nhbbkp':'nhb_daily_biking_person_trip_table',
#            'nhbwkp':'nhb_daily_walking_person_trip_table',
#            'nhbtwp':'nhb_daily_walk_to_transit_person_trip_table',
                          
            },
        'bank3':{
            'mf91':'pm_ev_ni_vehicle_miles_traveled',
#            'mf92':'pm_vehicle_miles_traveled',
#            'mf93':'ev_vehicle_miles_traveled',
#            'mf94':'ni_vehicle_miles_traveled',
#            
#            'pau1tm':'pm_single_vehicle_to_work_travel_time',
#            'pau2tm':'pm_double_vehicle_to_work_travel_time',
#            'pau3tm':'pm_threeplus_vehicle_to_work_travel_time',
#            'pbiket':'pm_bike_to_work_travel_time',
#            'pwlktm':'pm_walk_time_in_minutes',
#            
#            'eau1tm':'ev_single_vehicle_to_work_travel_time',
#            'eau2tm':'ev_double_vehicle_to_work_travel_time',
#            'eau3tm':'ev_threeplus_vehicle_to_work_travel_time',
#            'ebiket':'ev_bike_to_work_travel_time',
#            'ewlktm':'ev_walk_time_in_minutes',
#            
#            'nau1tm':'ni_single_vehicle_to_work_travel_time',
#            'nau2tm':'ni_double_vehicle_to_work_travel_time',
#            'nau3tm':'ni_threeplus_vehicle_to_work_travel_time',
#            'nbiket':'ni_bike_to_work_travel_time',
#            'nwlktm':'ni_walk_time_in_minutes',
            }
        }
    # For mapping link attributes to nodes. Keys should be file names (report files), each entry is a dictionary as above.
    node_matrix_variable_map = {}
    
    reports = [
    #This is a list of files that should be copied from the emme2 directory into cache. 
    #It is intended to serve for informative purposes, i.e. for keeping report files.
               ]
    """export_macros should be a dictionary of key/value 'macro_name':{'bank': ..., 'scenario':..., 'path':...}, where
    each of the specified macros lives in travel_model_dir_name/path. The macros are run on the specified bank."""
    export_macros = { # contains macros that export travel data. They are run after run_travel_model and before get_emme2_data_into_cache
        'tazvmt1.mac':{'bank':'bank1', 'scenario':-1, 'path':'export_macros'},
        'tazvmt2.mac':{'bank':'bank2', 'scenario':-1, 'path':'export_macros'},
        'tazvmt3.mac':{'bank':'bank3', 'scenario':-1, 'path':'export_macros'}, 
        'tveha.mac': {'bank': 'bank1', 'scenario':-1, 'path':'export_macros'},
        'tvehrpt.mac': {'bank': 'bank1', 'scenario':-1, 'path':'export_macros'},       
        }
                
    travel_model_configuration = {
        'travel_model_input_file_writer':travel_model_input_file_writer,
        'matrix_variable_map':emme2_matricies,
        'node_matrix_variable_map': node_matrix_variable_map,
        'reports_to_copy': reports,
        'export_macros':export_macros,
        'locations_to_disaggregate': locations_to_disaggregate,
        'travel_model_base_directory': travel_model_dir_name,
        'emme2_batch_file_name':emme2_batch_file,
        }

    _add_models(travel_model_configuration, mode)
    _add_years(travel_model_configuration, years_to_run)
    return travel_model_configuration

def _add_models(travel_model_configuration, mode):
    models = []
    if mode == 'full':
        models = [
            'opus_emme2.models.get_cache_data_into_emme2',
            'opus_emme2.models.run_travel_model',
            'opus_emme2.models.run_export_macros',
            'opus_emme2.models.get_emme2_data_into_cache',
            ]
    elif mode == 'skims':
        models = [
           'opus_emme2.models.run_export_macros',
           'opus_emme2.models.get_emme2_data_into_cache',
            ]
    elif mode == 'get_emme2_data':
        models = [
            'opus_emme2.models.get_emme2_data_into_cache',
            ]
    elif mode == 'get_emme2_data_after_run':
        models = [
            'opus_emme2.models.get_cache_data_into_emme2',
            'opus_emme2.models.run_travel_model',                  
            'opus_emme2.models.get_emme2_data_into_cache',
            ]
    elif mode == 'null':
        models = [
            'opus_emme2.models.get_cache_data_into_emme2',
            'opus_emme2.models.run_export_macros',
            'opus_emme2.models.get_emme2_data_into_cache',
            ]
    travel_model_configuration['models'] = models
        
def _add_years(travel_model_configuration, years_to_run):
    if years_to_run is None:
        years_to_run = {
            2000:'2000_06',
            2005:'2005_06',
            2010:'2010_06',
            2015:'2010_06',
            2020:'2020_06',
            2025:'2020_06',
            2030:'2030_06',
            }
    for year, year_dir in years_to_run.iteritems():
        travel_model_configuration[year] = {
            'bank':[ year_dir, ],
            }
        
