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

from PyQt4.QtCore import QString

from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.results_manager.controllers.tabs.view_image_form import ViewImageForm
from opus_gui.results_manager.controllers.tabs.view_table_form import ViewTableForm
from opus_gui.abstract_manager.abstract_manager import AbstractManager
from opus_gui.results_manager.controllers.tabs.results_browser import ResultBrowser
from opus_gui.results_manager.controllers.dialogs.import_run_dialog import ImportRunDialog
from opus_gui.results_manager.controllers.xml_configuration.xml_controller_results import XmlController_Results
from opus_gui.results_manager.results_manager_functions import get_run_manager,\
    update_available_runs


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
        self._scanForRuns()
        #thread.start_new_thread(self._scanForRuns, ())

    def _scanForRuns(self):
        run_manager = get_run_manager()
        run_manager.clean_runs()
        run_manager.close()

        added_runs, removed_runs = update_available_runs(self.project)
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
            self.project.dirty = True
            text = 'The list of simulation runs has been automatically updated.'
            detailed_text = '%s\n\n%s' % (added_msg or '', removed_msg or '')
            MessageBox.information(mainwindow = self.base_widget,
                                   text = text,
                                   detailed_text = detailed_text)

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
        self.xml_controller.model.add_node_to_path('Simulation_runs', run_node)

    def delete_run(self, run_node):
        self.xml_controller.delete_run(run_node)

    def importRun(self):
        dlg = ImportRunDialog(self, self.base_widget)
        dlg.show()

    def add_result_browser(self):
        if self.resultBrowser is not None:
            self.close_tab(self.resultBrowser)
        self.resultBrowser = ResultBrowser(resultsManagerBase = self)
        self._attach_tab(tab_widget = self.resultBrowser)

    def addViewImageIndicator(self, visualization, indicator_type = None):
        new_form = ViewImageForm(visualization = visualization,
                                 parent_widget = self.tab_base_widget)
        self._attach_tab(tab_widget = new_form)

    def addViewTableIndicator(self, visualization, indicator_type):
        if indicator_type != 'arcgis_map' and visualization.output_type in \
            ['fixed_field','tab','csv']:
            new_form = ViewTableForm(visualization = visualization,
                                 parent_widget = self.tab_base_widget)
            self._attach_tab(tab_widget = new_form)

