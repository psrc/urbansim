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

from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper

from opus_gui.results_manager.controllers.tabs.results_browser import ResultBrowser
from opus_gui.results_manager.controllers.dialogs.indicator_batch_run_form import IndicatorBatchRunForm
from opus_gui.results_manager.controllers.tabs.view_documentation_form import ViewDocumentationForm
from opus_gui.results_manager.controllers.tabs.view_image_form import ViewImageForm
from opus_gui.results_manager.controllers.tabs.view_table_form import ViewTableForm
from opus_gui.results_manager.controllers.dialogs.configure_new_batch_indicator_visualization import ConfigureNewBatchIndicatorVisualization
from opus_gui.results_manager.controllers.dialogs.configure_existing_batch_indicator_visualization import ConfigureExistingBatchIndicatorVisualization
from opus_gui.results_manager.controllers.dialogs.import_run_dialog import ImportRunDialog
from opus_gui.results_manager.controllers.dialogs.add_indicator_batch import AddIndicatorBatch

# Main Run manager class
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.services.run_server.run_manager import RunManager
from opus_gui.abstract_manager.abstract_manager_base import AbstractManagerBase

class ResultsManagerBase(AbstractManagerBase):  
    
    def __init__(self, mainwindow):
        AbstractManagerBase.__init__(self, mainwindow) 
        self.toolboxBase = self.mainwindow.toolboxBase  
        self.xml_helper = ResultsManagerXMLHelper(toolboxBase = self.toolboxBase)
        self.resultBrowser = None
        
    def scanForRuns(self):
        self._scanForRuns()
        #thread.start_new_thread(self._scanForRuns, ())
    
    def _scanForRuns(self):
        run_manager = self._get_run_manager()
        run_manager.clean_runs()
        run_manager.close()
            
        self.xml_helper.update_available_runs()
                
    def _get_run_manager(self):
        config = ServicesDatabaseConfiguration()
        run_manager = RunManager(config)
        return run_manager

    def deleteRun(self, run_id, cache_directory):
        run_manager = self._get_run_manager()
        run_manager.delete_everything_for_this_run(run_id, cache_directory = cache_directory)
        run_manager.close()
    
    def importRun(self):
        dlg = ImportRunDialog(self)
        dlg.show()
        
    def removeGuiElement(self,guiElement):
        AbstractManagerBase.removeGuiElement(self, guiElement = guiElement)
        if guiElement == self.resultBrowser:
            self.resultBrowser = None
            
    def add_result_browser(self):
            
        if self.resultBrowser is not None:
            self.removeGuiElement(guiElement = self.resultBrowser)
        
        self.resultBrowser = ResultBrowser(mainwindow = self.mainwindow,
                                               resultsManagerBase = self)            
            
        self.addNewGuiElement(element = self.resultBrowser)
    
    def addNewIndicatorBatch(self):
        window = AddIndicatorBatch(self)
        window.show()
                
    def configureExistingIndicatorBatchVisualization(self, selected_index):
        viz_name = selected_index.internalPointer().node().toElement().tagName()
        _, params = self.xml_helper.get_element_attributes(node_name = viz_name,
                                               child_attributes = ['visualization_type'],
                                               node_type = 'batch_visualization')

        window = ConfigureExistingBatchIndicatorVisualization(self, selected_index)
        window.show()
                    
    def configureNewIndicatorBatchVisualization(self, batch_name):
        window = ConfigureNewBatchIndicatorVisualization(self, batch_name)
        window.show()

    def addRunIndicatorBatchForm(self, batch_name, simulation_run):
        new_form = IndicatorBatchRunForm(mainwindow = self.mainwindow,
                                         resultsManagerBase = self,
                                         batch_name = batch_name,
                                         simulation_run = simulation_run)
        new_form.show()
        

    def addViewImageIndicator(self, visualization, indicator_type = None):
        new_form = ViewImageForm(mainwindow = self.mainwindow,
                                 visualization = visualization)
        self.addNewGuiElement(element = new_form)
        

    def addViewTableIndicator(self, visualization, indicator_type):
        if indicator_type != 'arcgis_map' and visualization.output_type in ['fixed_field','tab','csv']:
            new_form = ViewTableForm(mainwindow = self.mainwindow,
                                 visualization = visualization)
            self.addNewGuiElement(element = new_form)
#            
#    def addViewDocumentationForm(self, indicator_node):
#        new_form = ViewDocumentationForm(mainwindow = self.mainwindow,
#                                         indicator_node = indicator_node)
#        self.guiElements.insert(0, new_form)
#        self.updateGuiElements()
        
