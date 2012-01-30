# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from lxml.etree import Element
import time
from PyQt4.QtGui import QMenu, QCursor, QDialog
from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.results_manager.controllers.dialogs.add_indicator_batch import AddIndicatorBatch
from opus_gui.results_manager.controllers.dialogs.get_run_info import GetRunInfo
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.results_manager.controllers.dialogs.configure_existing_batch_indicator_visualization import ConfigureExistingBatchIndicatorVisualization
from opus_gui.results_manager.controllers.dialogs.configure_new_batch_indicator_visualization import ConfigureNewBatchIndicatorVisualization
from opus_gui.results_manager.controllers.dialogs.indicator_batch_run_form import IndicatorBatchRunForm
from opus_gui.results_manager.results_manager_functions import get_available_run_nodes, get_run_manager
from opus_gui.results_manager.controllers.dialogs.import_run_dialog import ImportRunDialog
from opus_gui.util.icon_library import IconLibrary
from opus_gui.util import common_dialogs
from opus_gui.main.controllers.instance_handlers import get_manager_instance
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance
from opus_gui.scenarios_manager.run.run_simulation import OpusModel
from opus_gui.scenarios_manager.controllers.tabs.simulation_gui_element_restart import InputRestartYearsDialog
from opus_gui.scenarios_manager.controllers.tabs.simulation_gui_element_restart import SimulationGuiElementRestart

class XmlController_Results(XmlController):
    ''' XmlController for the Results Manager '''

    def __init__(self, manager):
        XmlController.__init__(self, manager)
        callback = AddIndicatorBatch(callback = self._add_indicator_batch_callback,
                                     parent_widget = self.view).exec_
        p = ('add', "Add new indicator batch...", callback)
        self.actAddNewIndicatorBatch = self.create_action(*p)
        p = ('add', 'Add new indicator visualization...', self._configureNewBatchIndicatorVisualization)
        self.actAddVisualizationToBatch = self.create_action(*p)
        p = ('configure', "Configure visualization", self._configureExistingBatchIndicatorVisualization)
        self.actConfigureExistingBatchIndicatorVis = self.create_action(*p)
        p = ('info_small', "Show details", self._getInfoSimulationRuns)
        self.actGetInfoSimulationRuns = self.create_action(*p)
        p = ('import', "Import run from disk", self._importRun)
        self.actImportRun = self.create_action(*p)
        p = ('delete', "Remove run and delete from hard drive...", self._delete_selected_run)
        self.actDeleteRun = self.create_action(*p)
        p = ('restart', "Restart run...", self._restart_selected_run)
        self.actRestartRun = self.create_action(*p)

    def _restart_selected_run(self):
        assert self.has_selected_item()
        run_node = self.selected_item().node
        # ask for start_year, end_year
        # start_year default to the last year of years run
        # need to avoid insert auto generate run directory again
#        original_start_year = int(run_node.find('start_year').text)
#        original_end_year = int(run_node.find('end_year').text)
#        restart_year = original_end_year + 1
#        end_year = restart_year + 1

        run_name = run_node.get('name')
        scenario_name = run_node.find('scenario_name').text
        run_id = run_node.get('run_id')
        try:
            run_id = int(run_id)
        except ValueError:
            raise ValueError, "run_id for run %s is invalid: %s; the run cannot be restarted." % \
                  (run_name, run_id)
        
        run_manager = get_run_manager()
        config = run_manager.get_resources_for_run_id_from_history(run_id)

        xml_config = self.project.xml_config
        opusgui = get_mainwindow_instance()
        scenario_manager = get_manager_instance('scenario_manager')
        opusmodel = OpusModel(scenario_manager, xml_config, scenario_name)
        tab_widget = SimulationGuiElementRestart(mainwindow=opusgui, 
                                                 runManager=scenario_manager, 
                                                 model=opusmodel, 
                                                 xml_config=xml_config,
                                                 run_id=run_id,
                                                 run_name=run_name)
        tab_widget.config = config
#        tab_widget.start_year = start_year
#        tab_widget.end_year = end_year
        scenario_manager._attach_tab(tab_widget)
        opusgui.update()
        #time.sleep(1)
        #tab_widget._init_run(run_name)
        #tab_widget.runThread.restart_run(run_id, config, restart_year,
        #                                 run_name=run_name)
    
    def _add_indicator_batch_callback(self, batch_name):
        # Create a new node with the given name and insert it into the model
        node = Element('indicator_batch', {'name': batch_name})
        batches_node = self.project.find('results_manager/indicator_batches')
        self.model.insert_node(node, batches_node)

    def _configureNewBatchIndicatorVisualization(self):#, viz = None):
        assert self.has_selected_item()
        batch_node = self.selected_item().node
        window = ConfigureNewBatchIndicatorVisualization(self.project, batch_node, self.view)
        window.show()

    def _configureExistingBatchIndicatorVisualization(self):
        assert self.has_selected_item()
        viz_node = self.selected_item().node
        window = ConfigureExistingBatchIndicatorVisualization(self.project, viz_node, self.view)
        window.show()

    def _delete_selected_run(self):
        assert self.has_selected_item()
        run_node = self.selected_item().node
        
        question = 'Do you want to delete %s from cache and services database?' % \
                    run_node.get('name')
        user_answer = common_dialogs.yes_or_cancel(question)
        if user_answer == common_dialogs.YES:
            self.delete_run(run_node)

    def delete_run(self, run_node, force=False):
        '''
        Remove a run both from the services database and from the model.
        @param run_node (Element): the node to remove.
        '''
        # Prevent the user from removing base years
        cache_directory = run_node.find('cache_directory').text
        if cache_directory.endswith('base_year_data') and not force:
            msg = ('Removing the base year data directory is restricted from '
                   'within OpusGUI since doing so will make it impossible to '
                   'run any simulations or estimations.')
            MessageBox.warning(mainwindow = self.view,
                               text = 'Cannot remove base year data',
                               detailed_text  = msg)
            return
        try:
            run_manager = get_run_manager()
            run_id = run_node.get('run_id')
            try:
                run_id = int(run_id)
            except:
                run_id = -1
            run_manager.delete_everything_for_this_run(run_id, cache_directory)
            run_manager.close()
            self.model.remove_node(run_node)
            #was self.project.delete_node(run_node), but it doesn't update the GUI
            #self.project.dirty = True
            #update_mainwindow_savestate()
            # self.model.remove_node(run_node)
        except Exception, ex: # TODO catch more specific error?
            MessageBox.warning(self.view, 'Could not remove run', str(ex))

    def _importRun(self):        
        dlg = ImportRunDialog(self, self.manager.base_widget)
        dlg.show()

    def _createBatchRunMenu(self, attach_to_menu):
        '''
        Create and populate a 'Run indicator batch' menu for all available runs
        @param attach_to_menu (QMenu) menu to attach actions to
        '''
        # TODO Verify that this is correct -- it was based on looking in a xml
        # file for 'source_data' and simulation_runs was the only section I
        # could find it in.
        run_nodes = get_available_run_nodes(self.project)

        if not run_nodes:
            attach_to_menu.setEnabled(False)
            return

        #T: the following loop causes a problem where
        #   only "baseyear_data" will be passed to the _indicatorBatchRun method.
        #   I don't know why.

        for run_node in run_nodes:
            cb = lambda x = run_node.get('name'): self._indicatorBatchRun(run_name = x)
            action = self.create_action(IconLibrary.icon('add'), run_node.get('name'), cb)
            attach_to_menu.addAction(action)

#        #T:  The following loop works, but its kind of a nasty method.
#        for i in range(len(run_nodes)):
#            exec 'cb%i=lambda x = run_nodes[%i]: self._indicatorBatchRun(run_name = run_nodes[%i].tag)'%(i,i,i) in locals()
#            exec 'action%i=self.create_action(self.model.acceptIcon, run_nodes[%i].tag, cb%i)'%(i,i,i) in locals()
#            exec 'attach_to_menu.addAction(action%i)'%i in locals()

    def _indicatorBatchRun(self, run_name):
        ''' NO DOCUMENTATION '''
        assert self.has_selected_item()
        node = self.selected_item().node
        window = IndicatorBatchRunForm(mainwindow = self.view, resultsManagerBase = self.manager,
                                       batch_name = node.get('name'), run_name = run_name)
        window.show()

    def _getInfoSimulationRuns(self):
        ''' NO DOCUMENTATION '''
        assert self.has_selected_item()
        node = self.selected_item().node
        window = GetRunInfo(node, self.view)
        window.exec_()


    def _viewDocumentation(self):
        pass
    
    def add_custom_menu_items_for_node(self, node, menu):
        # Populate menu
        if node.tag == 'run':
            menu.addAction(self.actRestartRun)  #TODO:disable restart run for base_year_data
            menu.addAction(self.actDeleteRun)
            menu.addAction(self.actGetInfoSimulationRuns)            
        elif node.tag == 'indicator_batches':
            menu.addAction(self.actAddNewIndicatorBatch)
        elif node.tag == 'simulation_runs':
            menu.addAction(self.actImportRun)
        elif node.tag == 'indicator_batch':
            menu.addAction(self.actAddVisualizationToBatch)
            run_batch_on_menu = QMenu('Run indicator batch on...', menu)
            self._createBatchRunMenu(run_batch_on_menu)
            menu.addMenu(run_batch_on_menu)

        elif node.tag == 'batch_visualization': # get('type') == 'batch_visualization':
            menu.addAction(self.actConfigureExistingBatchIndicatorVis)
        
        return node.tag == 'run' # default menu items aren't meaningful for simulation run nodes
