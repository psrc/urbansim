# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

'''
Methods and Classes related to the Results Manager
'''
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.services.run_server.run_manager import RunManager
from lxml.etree import Element, SubElement

from opus_gui.main.controllers.instance_handlers import get_manager_instance,\
    update_mainwindow_savestate
import os

def get_batch_configuration(project, batch_name, vis_name=None):
    '''
    Get the configuration for a batch as a tuple formated like:
     (visualization_type, dataset_name, child_node_value_mappings)
    child_node_value_mappings is a dictionary like: setting[name] = value

    @param project (OpusProject): an opus project
    @param batch_name (String): name of the batch to handle
    '''

    # get the selected batch by name
    batch_nodes = dict((n.get('name'), n) for n in get_available_batch_nodes(project))
    if not batch_name in batch_nodes:
        raise LookupError('Could not find a batch named "%s" as requested' % batch_name)
    batch_node = batch_nodes[batch_name]

    visualizations = []

    for viz_node in batch_node.findall('batch_visualization'):
        if vis_name and viz_node.get('name') != vis_name: continue
        viz_type = viz_node.find('visualization_type').text
        dataset_name = viz_node.find('dataset_name').text
        # assemble a dict containing all <settings>, <visualization_type> and <output_type>
        settings = {}
        settings['indicators'] = viz_node.find('indicators').text
        settings['output_type'] = viz_node.find('output_type').text
        for setting_node in viz_node.findall('settings/setting'):
            settings[setting_node.get('name')] = setting_node.text
        visualizations.append((viz_type, dataset_name, settings))
    return visualizations

def get_available_batch_nodes(project):
    '''
    Get all the batches in the project.
    @return all the batches in the project (list(Element))
    '''
    return project.findall('results_manager/indicator_batches/indicator_batch')

def get_available_run_nodes(project):
    '''
    Get all the runs in the project.
    @return all the runs in the project (list(Element))
    '''
    return project.findall('results_manager/simulation_runs/run')

def delete_simulation_run(project, run_name):
    run_node = project.find('results_manager/simulation_runs', name=run_name)
    if run_node:  # delete the run_node only when it exists
        get_manager_instance('results_manager').delete_run(run_node)

def add_simulation_run(project, cache_directory, scenario_name, run_name,
                       start_year, end_year, run_id):
    '''
    Creates a simulation run node and adds it to the project
    @param project (OpusProject): currently loaded project
    @param cache_directory (String): absolute path to the cache directory
    @param scenario_name (String): name of the scenario that was run
    @param run_name (String): name of the run
    @param start_year (int): start year of run
    @param end_year (int): end year of run
    @param run_id (int): ID number for the run
    
    This function isn't able to update run_nodes existing in <simulation_runs>
    '''
    ## XML-ify the name
    # run_name = run_name.replace(' ', '_')

    # Assemble the new run node
    str_atr = {'type': 'string'}
    int_atr = {'type': 'integer'}
    if not run_name or run_name is None or run_name == "No description":
        ## if run_name is null or un-informative, use run id as name instead
        run_name = "run_%s" % run_id
    run_node = Element('run', {'type': 'source_data',
                               'name': run_name,
                               'hidden': 'Children',
                               'run_id': str(run_id)})
    # SubElement(run_node, 'run_id', int_atr).text = str(run_id)
    SubElement(run_node, 'scenario_name', str_atr).text = scenario_name
    SubElement(run_node, 'cache_directory', str_atr).text = cache_directory
    SubElement(run_node, 'start_year', int_atr).text = str(start_year)
    SubElement(run_node, 'end_year', int_atr).text = str(end_year)

    # Grab the results manager instance for the GUI and insert the new node
    get_manager_instance('results_manager').add_run(run_node)
    project.dirty = True
    update_mainwindow_savestate()

def sync_available_runs(project, scenario_name = '?'):
    '''
    Update the list of available runs and return a list of added runs.
    @param project (OpusProject): currently loaded project
    @return: Two lists; one of the runs that have been added, and the other of
    the runs that have been removed (tuple(list(String), list(String)))
    '''

#    results_manager = get_manager_instance('results_manager')
    removed_runs = []
#    # Remove runs that exist in the project but not on disk
#    run_nodes = get_available_run_nodes(project)
    existing_cache_directories = set()
#    for run_node in run_nodes:
#        cache_directory = os.path.normpath(run_node.find('cache_directory').text)
#        if not os.path.exists(cache_directory):
#            results_manager.delete_run(run_node, force=True)   #force deleting base_year_data entry when the directory doesn't exist
#            removed_runs.append(run_node.get('name'))
#            continue
#        # Add the cachedir to the list of seen cachedirs
#        existing_cache_directories.add(cache_directory)

    run_manager = get_run_manager()
    runs = run_manager.get_run_info(resources = True, status = 'done')
    runs = run_manager.get_runs(return_columns='*',
                                return_rs=True, status='done')

    # add all runs with unique directories are list on the project
    added_runs = []

    def add_runs():
        for run in runs:
            run_id = run['run_id']
            run_name = run['run_name']
            scenario_name = run['scenario_name'] if 'scenario_name' in run else 'unknown'
            if run_name == 'base_year_data':
                scenario_name = run_name
            cache_directory = os.path.normpath(run['cache_directory'])
            run_resources = run_manager.get_resources_for_run_id_from_history(run_id)
            available_years = run_manager.get_years_run(cache_directory)
            if available_years:
                start_year, end_year = min(available_years), max(available_years)
            else:
                #skip an empty run directory
                continue
            #start_year, end_year = run_resources['years']

            # don't add runs that we have already seen or that don't exist on disk
            if cache_directory in existing_cache_directories or not os.path.exists(cache_directory):
                continue
            
            add_simulation_run(project,
                               cache_directory = cache_directory,
                               scenario_name = scenario_name,
                               run_name = run_name,
                               start_year = start_year,
                               end_year = end_year,
                               run_id = run_id)

            existing_cache_directories.add(cache_directory)
            added_runs.append(cache_directory)

    try:
        add_runs()
    except:
        raise
    finally:
        run_manager.close()
    return (added_runs, removed_runs)

def get_years_range_for_simulation_run(project, run_name=None, run_node=None):
    """ return min and max of years for run by run_name or run_node
    """
    if run_node is None:
        if run_name is not None:
            run_nodes = get_simulation_runs(project)
            run_node = [run_node for run_node in run_nodes if run_node.get('name') == run_name]
            #assert len(run_node) == 1  # run_name should be unique among run_nodes
            if len(run_node) == 0:
                raise ValueError, "There is no match run node for name %s" % run_name
            if len(run_node) >= 1:
                run_node = run_node[0]
        else:
            raise ValueError, "run_name and run_node cannot both be None."

    years = get_years_for_simulation_run(project=project,
                                         simulation_run_node=run_node
                                         )
    return min(years), max(years)

def get_years_for_simulation_run(project, simulation_run_node):
    ''' Get the years run for the given simulation '''
    run_manager = get_run_manager()
    cache_dir = (simulation_run_node.find('cache_directory').text or '').strip()
    scenario_name = (simulation_run_node.find('scenario_name').text or '').strip()
    scenario_node = project.find('scenario_manager/scenario', name=scenario_name)
    # prefer using base year for the given scenario, otherwise just a base year from any scenario
    baseyear = -1
    if scenario_node is not None:
        try:
            baseyear = int(scenario_node.find('base_year').text)
        except (TypeError, ValueError): pass
    if baseyear == -1: # try to get any base year from any scenario
        scenario_manager_node = project.find('scenario_manager')
        for base_year_node in scenario_manager_node.findall('.//base_year'):
            try:
                baseyear = int(base_year_node.text.strip())
                break
            except (TypeError, ValueError):
                continue

    return run_manager.get_years_run(cache_dir, baseyear=baseyear)

def get_simulation_runs(project, update = False):
    if update:
        sync_available_runs(project)
    return project.findall('results_manager/simulation_runs/run')

def add_batch_indicator_visualization(batch_node, viz_node):
    '''
    Adds a new batch indicator visualization to the project
    @param viz_node (Element): Node representing the new batch node to insert
    '''
    results_manager = get_manager_instance('results_manager')
    if not results_manager:
        return
    results_manager.add_viz_node(batch_node, viz_node)

def update_batch_indicator_visualization(updated_viz_node):
    '''
    Updates a visualization node.
    @param viz_node (Element): the node to update.
    '''
    results_manager = get_manager_instance('results_manager')
    if not results_manager:
        return
    results_manager.update_viz_node(updated_viz_node)

def get_run_manager():
    '''
    Get an instance of a valid run manager
    @return: a run manager instance (RunManager)
    '''
    config = ServicesDatabaseConfiguration()
    run_manager = RunManager(config)
    return run_manager
