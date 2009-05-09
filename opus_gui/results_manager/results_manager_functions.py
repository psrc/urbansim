# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
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

def get_batch_configuration(project, batch_name):
    '''
    Get the configuration for a batch in the following specification:
    (visualization_type, dataset_name, child_node_value_mappings)
    @param project (OpusProject): an opus project
    @param batch_name (String): name of the batch to handle
    '''

    # Select the batch node based on tags
    all_batch_nodes = get_available_batch_nodes(project)
    selected_batch_nodes = [node for node in all_batch_nodes if
                            node.get('name') == batch_name]
    if len(selected_batch_nodes) == 0:
        print 'Could not find a batch with name "%s"' % batch_name
        return ()
    if len(selected_batch_nodes) > 1:
        raise RuntimeError('Found multiple (%d) batch nodes with tag "%s"'
                           %(len(selected_batch_nodes), batch_name))
    batch_node = selected_batch_nodes[0]
    visualizations = []
    for viz_node in batch_node:
        # Create a dict for all child nodes, paired with their values
        child_values = dict((node.get('name'), node.text) for node in viz_node)
        # Format visualization type
        viz_type = child_values['visualization_type']
        if viz_type in ['table_per_year', 'table_per_attribute']:
            viz_type = 'tab'
        dataset_name = child_values['dataset_name']
        child_values['name'] = viz_node.get('name')
        visualizations.append((viz_type, dataset_name, child_values))
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
    '''
    ## XML-ify the name
    # run_name = run_name.replace(' ', '_')

    # Assemble the new run node
    str_atr = {'type': 'string'}
    int_atr = {'type': 'integer'}

    run_node = Element('run', {'type': 'source_data',
                               'name': run_name,
                               'hidden': 'Children',
                               'run_id': str(run_id)})
    # SubElement(run_node, 'run_id', int_atr).text = str(run_id)
    SubElement(run_node, 'scenario_name', str_atr).text = scenario_name
    SubElement(run_node, 'run_name', str_atr).text = run_name
    SubElement(run_node, 'cache_directory', str_atr).text = cache_directory
    SubElement(run_node, 'start_year', int_atr).text = str(start_year)
    SubElement(run_node, 'end_year', int_atr).text = str(end_year)

    # Grab the results manager instance for the GUI and insert the new node
    get_manager_instance('results_manager').add_run(run_node)
    project.dirty = True
    update_mainwindow_savestate()

def update_available_runs(project, scenario_name = '?'):
    '''
    Update the list of available runs and return a list of added runs.
    @param project (OpusProject): currently loaded project
    @return: Two lists; one of the runs that have been added, and the other of
    the runs that have been removed (tuple(list(String), list(String)))
    '''
    if not os.path.exists(project.data_path()):
        return ([], []) # Project data path doesn't exist -- so no runs to add

    results_manager = get_manager_instance('results_manager')
    removed_runs = []
    # Remove runs that exist in the project but not on disk
    run_nodes = get_available_run_nodes(project)
    existing_cache_directories = set()
    for run_node in run_nodes:
        cache_directory = os.path.normpath(run_node.find('cache_directory').text)
        if not os.path.exists(cache_directory):
            results_manager.delete_run(run_node)
            removed_runs.append(run_node.get('name'))
            continue
        # Add the cachedir to the list of seen cachedirs
        existing_cache_directories.add(cache_directory)

    run_manager = get_run_manager()

    # Make sure that the base_year_data is in the list of available runs
    baseyear_dir = os.path.join(project.data_path(), 'base_year_data')
    baseyear_dir = os.path.normpath(baseyear_dir)
    years = []
    if not baseyear_dir in existing_cache_directories:
        try:
            run_manager.get_run_id_from_name(run_name = 'base_year_data')
        except:
            for dir_ in os.listdir(baseyear_dir):
                if len(dir_) == 4 and dir_.isdigit():
                    years.append(int(dir_))
            start_year = min(years)
            end_year = max(years)
            base_year = end_year
            run_name = 'base_year_data'
            run_id = run_manager._get_new_run_id()
            resources = {
                 'cache_directory': baseyear_dir,
                 'description': 'base year data',
                 'years': (base_year, end_year)
            }
            run_manager.add_row_to_history(run_id = run_id,
                                           resources = resources,
                                           status = 'done',
                                           run_name = run_name)

    runs = run_manager.get_run_info(resources = True, status = 'done')
    run_manager.close()

    # Make sure all runs with unique directories are list on the project
    added_runs = []
    for run_id, run_name, _, _, run_resources in runs:
        cache_directory = os.path.normpath(run_resources['cache_directory'])
        if run_name == 'base_year_data':
            found_scenario_name = ''
        else:
            found_scenario_name = scenario_name

        # don't add runs that we have already seen or that don't exist on disk
        if cache_directory in existing_cache_directories or not os.path.exists(cache_directory):
            continue
        start_year, end_year = run_resources['years']
        add_simulation_run(project,
                           cache_directory = cache_directory,
                           scenario_name = found_scenario_name,
                           run_name = run_name,
                           start_year = start_year,
                           end_year = end_year,
                           run_id = run_id)

        existing_cache_directories.add(cache_directory)
        added_runs.append(cache_directory)
    return (added_runs, removed_runs)

def get_years_for_simulation_run(project, simulation_run_node):
    run_manager = get_run_manager()
    cache_dir = simulation_run_node.find('cache_directory').text.strip()
    scenario_name = simulation_run_node.find('scenario_name').text.strip()
    scenario_node = project.find('scenario_manager/scenario', name=scenario_name)
    try:
        baseyear = int(scenario_node.find('base_year').text)
    except:
        node = project.find('scenario_manager')
        baseyear = -1
        for child in node.getchildren():
            try:
                baseyear = int(child.find('base_year').text)
                break
            except: continue

    return run_manager.get_years_run(cache_dir, baseyear = baseyear)

def get_simulation_runs(project, update = False):
    if update:
        update_available_runs(project)
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
