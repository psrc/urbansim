# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.results_manager.controllers.tabs.view_image_form import ViewImageForm
from opus_gui.results_manager.controllers.tabs.view_animation_form import ViewAnimationForm
from opus_gui.results_manager.controllers.tabs.view_table_form import ViewTableForm
from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.results_manager.controllers.tabs.results_browser import ResultBrowser
from opus_gui.results_manager.controllers.xml_configuration.xml_controller_results import XmlController_Results
from opus_gui.results_manager.results_manager_functions import get_run_manager, sync_available_runs
from opus_core.misc import get_host_name
from opus_core.logger import logger


class ResultsManager(AbstractManager):

    '''
    Manager for GUI Elements related to the Results tab
    '''

    def __init__(self, base_widget, tab_widget, project):
        AbstractManager.__init__(self, base_widget, tab_widget, project,
                                 'results_manager')
        self.resultBrowser = None
        self.xml_controller = XmlController_Results(self)

    def scanForRuns(self):
        # self._scanForRuns() HS
        #thread.start_new_thread(self._scanForRuns, ())
        pass

    def _scanForRuns(self):
        data_path = self.project.data_path()
        if not os.path.exists(data_path):
            MessageBox.warning(mainwindow = self.base_widget,
                               text="Project data path %s doesn't exist. " % data_path + \
                               "Simulation runs in the Results tab cannot be updated." )
            return
        
        run_manager = get_run_manager()
        run_manager.clean_runs()
        self._sync_base_year_data(run_manager)        
        run_manager.close()
        
        added_runs, removed_runs = sync_available_runs(self.project)
        added_msg = removed_msg = None
        if len(added_runs) > 0:
            added_msg = ('The following simulation runs have been '
                         'automatically added to the results manager:\n\n%s'
                         % '\n'.join(added_runs))
        if len(removed_runs) > 0:
            removed_msg = ('The following simulation runs have been '
                         'automatically removed from the results manager:\n\n%s'
                         % '\n'.join(removed_runs))
        if added_msg or removed_msg:
            ## The idea is to leave the run information to services db & cache, and
            ## we don't need to save the newly added runs, once we set the temporary
            # self.project.dirty = True
            text = 'The list of simulation runs has been automatically updated.'
            detailed_text = '%s\n%s' % (added_msg or '', removed_msg or '')
            logger.log_status(text+'\n'+detailed_text)
            
    def _sync_base_year_data(self, run_manager=None):
        """
        synchronize base_year_data information in xml_configuration with 
        run_activity table.  Information in xml_configuration takes 
        precedent, because we assume users don't directly modify data in
        serivecs.run_activity table  
        """

        # TODO baseyear_dir is somewhat hard-coded; it would be better to read
        # from xml_configuration instead, but there is no such node currently
        run_name = 'base_year_data'
        baseyear_dir = os.path.join(self.project.data_path(), run_name)
        baseyear_dir = os.path.normpath(baseyear_dir)
        if not os.path.exists(baseyear_dir):
            MessageBox.warning(mainwindow = self.base_widget,
                               text="base_year_data directory %s doesn't exist. " % baseyear_dir
                               )
            return
        
        import glob
        years = [int(os.path.basename(year_dir)) for year_dir in 
                           glob.glob(os.path.join(baseyear_dir, '[0-9][0-9][0-9][0-9]'))]
        
        if not years:
            MessageBox.warning(mainwindow = self.base_widget,
                               text="base_year_data directory %s doesn't contain any year sub-directory. " % baseyear_dir
                               )
            return
        
        start_year = min(years)
        end_year = max(years)
        base_year = end_year # default to the last year in baseyear_dir
        # and update it with information found in scenario_manager
        scenario_manager_node = self.project.find('scenario_manager')
        for base_year_node in scenario_manager_node.findall('.//base_year'):
            try:
                base_year = int(base_year_node.text.strip())
                break
            except (TypeError, ValueError):
                continue
            
        resources = {
             'cache_directory': baseyear_dir,
             'description': 'base year data',
             'base_year': base_year,
             'years': (start_year, end_year)
        }
        
        if run_manager is None: run_manager = get_run_manager()
        base_year_data_db = run_manager.get_runs(run_name=run_name, 
                                                 process_name=get_host_name())
        
        if len(base_year_data_db) == 0:
            run_id = run_manager._get_new_run_id()
        elif len(base_year_data_db) >= 1:
            for idx, row in enumerate(base_year_data_db):
                if idx==0:
                    run_id = row[0]
                else:
                    run_manager.delete_everything_for_this_run(row[0])
            resources_db = run_manager.get_resources_for_run_id_from_history(run_id)
            if resources_db.get('cache_directory', '') == baseyear_dir and \
                    resources_db.get('base_year', -1) == base_year:
                #all good, we don't need to do anything
                return
            else:
                resources_db.merge(resources)
                resources = resources_db
        
        run_manager.add_row_to_history(run_id = run_id,
                                       resources = resources,
                                       status = 'done',
                                       run_name = run_name)

    def update_viz_node(self, updated_viz_node):
        '''
        Updates a visualization node in the project.
        @param updated_viz_node (Element): the node to update.
        '''
        self.xml_controller.model.update_node(updated_viz_node)

    def add_viz_node(self, batch_node, viz_node):
        '''
        Adds a visualization node to the model.
        @param batch_node (Element): which batch to add the node to
        @param viz_node (Element): the node to add.
        '''
        self.xml_controller.model.add_node(batch_node, viz_node)

    def add_run(self, run_node):
        simulation_node = self.project.find('results_manager/simulation_runs')
        self.xml_controller.model.insert_node(run_node, simulation_node)

    def import_run(self, cache_directory, run_info={}):
        run_manager = get_run_manager()
        retval, retmsg = run_manager.import_run_from_cache(cache_directory)
        if not retval:
            MessageBox.warning(mainwindow = self.base_widget,
                               text = retmsg,
                               detailed_text = '')
        else:
            sync_available_runs(self.project)
    
    def delete_run(self, run_node, force=False):
        self.xml_controller.delete_run(run_node, force=force)
        
    def add_result_browser(self):
        if self.resultBrowser is not None:
            self.close_tab(self.resultBrowser)
        self.resultBrowser = ResultBrowser(project=self.project, parent_widget=self.xml_controller.view)
        self._attach_tab(tab_widget = self.resultBrowser)

    def addViewImageIndicator(self, visualization, indicator_type = None):
        new_form = ViewImageForm(visualization = visualization,
                                 parent_widget = self.tab_base_widget)
        self._attach_tab(tab_widget = new_form)

    def addViewAnimationIndicator(self, visualization, indicator_type = None):
        new_form = ViewAnimationForm(visualization = visualization,
                                 parent_widget = self.tab_base_widget)
        self._attach_tab(tab_widget = new_form)

    def addViewTableIndicator(self, visualization, indicator_type):
        if indicator_type != 'arcgis_map' and visualization.output_type in \
            ['fixed_field','tab','csv']:
            new_form = ViewTableForm(visualization = visualization,
                                 parent_widget = self.tab_base_widget)
            self._attach_tab(tab_widget = new_form)

