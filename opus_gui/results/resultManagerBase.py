# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from PyQt4.QtCore import QObject, SIGNAL, QModelIndex, QString


from opus_gui.results.forms.advanced_visualization_form import AdvancedVisualizationForm
from opus_gui.results.forms.generate_results_form import GenerateResultsForm
from opus_gui.results.forms.indicator_group_run_form import IndicatorGroupRunForm
from opus_gui.results.forms.view_documentation_form import ViewDocumentationForm
from opus_gui.results.forms.view_image_form import ViewImageForm
from opus_gui.results.forms.view_table_form import ViewTableForm
from opus_gui.results.gui_result_interface.opus_gui_thread import OpusGuiThread
from opus_gui.results.gui_result_interface.opus_result_visualizer import OpusResultVisualizer
from opus_gui.results.xml_helper_methods import ResultsManagerXMLHelper


# General system includes
import os


class AbstractManagerBase(object):
    #mainwindow is an OpusGui object
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.tabWidget = mainwindow.tabWidget
        self.gui = mainwindow
        self.guiElements = []
        
    def removeTab(self,guiElement):
        self.tabWidget.removeTab(self.tabWidget.indexOf(guiElement))
        self.guiElements.remove(guiElement)
        guiElement.hide()
    
    def updateGuiElements(self):
        for guiElement in self.guiElements:
            if guiElement.inGui == False:
                self.tabWidget.insertTab(0,guiElement,guiElement.tabIcon,guiElement.tabLabel)
                self.tabWidget.setCurrentIndex(0)
                guiElement.inGui = True
    
    def setGui(self, gui):
        self.gui = gui
    
# Main Run manager class
class ResultManagerBase(AbstractManagerBase):  
    
    def __init__(self, mainwindow):
        AbstractManagerBase.__init__(self, mainwindow) 
        self.toolboxStuff = self.mainwindow.toolboxStuff  
        self.xml_helper = ResultsManagerXMLHelper(toolboxStuff = self.toolboxStuff)

    def scanForRuns(self):
        '''scans all the runs directories in the opus_data folder for existing
           simulation data and adds it to the XML if its not already there'''
        
        #get existing cache directories, use as primary key to check for duplicates
        available_runs = self.xml_helper.get_available_run_info(attributes = ['cache_directory'])

        existing_cache_directories = {}
        for run in available_runs:
            existing_cache_directories[str(run['cache_directory'])] = 1

        if 'OPUS_DATA_PATH' in os.environ:
            path = os.path.join(os.environ.get('OPUS_DATA_PATH'))
            for scenario_name in os.listdir(path):
                if not os.path.isdir(os.path.join(path,scenario_name)): continue
                runs_path = os.path.join(path, scenario_name, 'runs')
                if not os.path.exists(runs_path): continue
                
                for run_name in os.listdir(runs_path):
                    try:
                        cache_directory = os.path.join(runs_path,run_name)
                        years = []
                        if not os.path.isdir(cache_directory) or \
                            cache_directory in existing_cache_directories: continue
                        for dir in os.listdir(cache_directory):
                            if len(dir) == 4 and dir.isdigit():
                                years.append(int(dir))
                        start_year = min(years)
                        end_year = max(years)
                        self.xml_helper.add_run_to_run_manager_xml(
                                                         cache_directory,
                                                         scenario_name,
                                                         run_name,
                                                         start_year, end_year)
                    except: pass

    def addAdvancedVisualizationForm(self):
        new_form = AdvancedVisualizationForm(mainwindow = self.mainwindow,
                                             result_manager = self)
        
        self.guiElements.insert(0, new_form)
        self.updateGuiElements() 
        
    def addGenerateIndicatorForm(self, selected_item):

        new_form = GenerateResultsForm(mainwindow = self.mainwindow,
                                       result_manager = self,
                                       selected_item = selected_item)
        
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()

    def addRunIndicatorGroupForm(self, selected_item, simulation_run):
        new_form = IndicatorGroupRunForm(mainwindow = self.mainwindow,
                                         result_manager = self,
                                         selected_item = selected_item,
                                         simulation_run = simulation_run)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()
        
    def addIndicatorForm(self, indicator_type, indicator_names, kwargs = None):
        #build visualizations

        indicator_info = [self.xml_helper.get_indicator_result_info(indicator_name)
                            for indicator_name in indicator_names]
        
        self.indicator_type = indicator_type
        self.visualizer = OpusResultVisualizer(
                                toolboxStuff = self.toolboxStuff,
                                indicator_type = indicator_type,
                                indicators = indicator_info,
                                kwargs = kwargs)
        
        self.visualization_thread = OpusGuiThread(parentThread = self.mainwindow,
                                                  parentGuiElement = self,
                                                  thread_object = self.visualizer)
        self.visualization_thread.start()

        # Use this signal from the thread if it is capable of producing its own status signal
        QObject.connect(self.visualization_thread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.visualizationsCreated)
        
    def visualizationsCreated(self, success):

        form_generator = None
        visualizations = self.visualizer.get_visualizations()
        if self.indicator_type == 'matplotlib_map' or \
           self.indicator_type == 'matplotlib_chart':
            form_generator = self.addViewImageIndicator
        elif self.indicator_type == 'table_per_year' or \
             self.indicator_type == 'table_per_attribute':
            form_generator = self.addViewTableIndicator            
        
        if form_generator is not None:    
            for visualization in visualizations:
                form_generator(visualization = visualization,
                               indicator_type = self.indicator_type)
        
        self.visualization_thread.wait()
        self.visualization_thread = None
        self.visualizer = None

    def addViewImageIndicator(self, visualization, indicator_type = None):
        new_form = ViewImageForm(mainwindow = self.mainwindow,
                                 visualization = visualization)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()

    def addViewTableIndicator(self, visualization, indicator_type):
        new_form = ViewTableForm(mainwindow = self.mainwindow,
                                 visualization = visualization)
        if indicator_type != 'arcgis_map':
            self.guiElements.insert(0, new_form)
            self.updateGuiElements()
        else:
            del new_form
            
    def addViewDocumentationForm(self, indicator_node):
        new_form = ViewDocumentationForm(mainwindow = self.mainwindow,
                                         indicator_node = indicator_node)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()
        
