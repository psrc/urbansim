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

from PyQt4.QtCore import QObject, SIGNAL, QModelIndex


from opus_gui.results.forms.advanced_visualization_form import AdvancedVisualizationForm
from opus_gui.results.forms.generate_results_form import GenerateResultsForm
from opus_gui.results.forms.view_documentation_form import ViewDocumentationForm
from opus_gui.results.forms.view_image_form import ViewImageForm
from opus_gui.results.forms.view_table_form import ViewTableForm
from opus_gui.results.opus_result_generator import OpusGuiThread, OpusResultVisualizer
from opus_gui.results.xml_helper_methods import get_child_values


# General system includes
import os, sys, tempfile, shutil


class AbstractManagerBase(object):
    #parent is an OpusGui object
    def __init__(self, parent):
        self.parent = parent
        self.tabWidget = parent.tabWidget
        self.gui = parent
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
    
    def __init__(self, parent):
        AbstractManagerBase.__init__(self, parent)        
        
    def scan_for_runs(self):
        
        toolboxStuff = self.parent.toolboxStuff
        document = toolboxStuff.doc
        xml_tree = toolboxStuff.resultsManagerTree        
        model = xml_tree.model
        
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
                        if not os.path.isdir(cache_directory): continue
                        for dir in os.listdir(cache_directory):
                            if len(dir) == 4 and dir.isdigit():
                                years.append(int(dir))
                        start_year = min(years)
                        end_year = max(years)
                        self.add_run_to_run_manager_xml(model, document,
                                                         cache_directory,
                                                         scenario_name,
                                                         run_name,
                                                         start_year, end_year)
                    except: pass
                
    def add_run_to_run_manager_xml(self, model, document,
                                    cache_directory, 
                                    scenario_name, run_name, 
                                    start_year, end_year):

        name = '%s.%s'%(scenario_name, run_name)

        newNode = model.create_node(document = document, 
                                    name = name, 
                                    type = 'source_data', 
                                    value = '')

        scenario_name_node = model.create_node(document = document, 
                                    name = 'scenario_name', 
                                    type = 'string', 
                                    value = scenario_name)

        run_name_node = model.create_node(document = document, 
                                    name = 'run_name', 
                                    type = 'string', 
                                    value = run_name)

        cache_directory_node = model.create_node(document = document, 
                                    name = 'cache_directory', 
                                    type = 'string', 
                                    value = cache_directory)

        start_year_node = model.create_node(document = document, 
                                    name = 'start_year', 
                                    type = 'integer', 
                                    value = str(start_year))

        end_year_node = model.create_node(document = document, 
                                    name = 'end_year', 
                                    type = 'integer', 
                                    value = str(end_year))    

        parent = model.index(0, 0, QModelIndex()).parent()
        index = model.findElementIndexByName("Simulation_runs", parent)[0]
        if index.isValid():
            model.insertRow(0, index, newNode)
        else:
            print "No valid node was found..."

        child_index = model.findElementIndexByName(name, parent)[0]
        if child_index.isValid():
            for node in [end_year_node, start_year_node, 
                         cache_directory_node, scenario_name_node, run_name_node]:
                model.insertRow(0, child_index, node)
        else:
            print "No valid node was found..."

        model.emit(SIGNAL("layoutChanged()"))    
        
    def addAdvancedVisualizationForm(self):
        new_form = AdvancedVisualizationForm(parent = self.parent,
                                       result_manager = self)
        
        self.guiElements.insert(0, new_form)
        self.updateGuiElements() 
        
    def addGenerateIndicatorForm(self, selected_item):

        new_form = GenerateResultsForm(parent = self.parent,
                                       result_manager = self,
                                       selected_item = selected_item)
        
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()

    def addIndicatorForm(self, indicator_type, clicked_node, kwargs = None):
        #build visualizations
        
        info = get_child_values(parent = clicked_node,
                                child_names = ['source_data',
                                               'indicator_name',
                                               'dataset_name',
                                               'available_years'])
        
        source_data_name = str(info['source_data'])
        indicator_name = str(info['indicator_name'])
        dataset_name = str(info['dataset_name'])
        years = [int(y) for y in str(info['available_years']).split(', ')]
        
        domDocument = self.parent.toolboxStuff.doc
        self.indicator_type = indicator_type
        self.visualizer = OpusResultVisualizer(
                                xml_path = self.parent.toolboxStuff.xml_file,
                                domDocument = domDocument,
                                indicator_type = indicator_type,
                                source_data_name = source_data_name,
                                indicator_name = indicator_name,
                                dataset_name = dataset_name,
                                years = years,
                                kwargs = kwargs)
        
        self.visualization_thread = OpusGuiThread(
                                  parentThread = self.parent,
                                  parent = self,
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
                form_generator(visualization = visualization)
        
        self.visualization_thread.wait()
        self.visualization_thread = None
        self.visualizer = None

    def addViewImageIndicator(self, visualization):
        new_form = ViewImageForm(parent = self.parent,
                                 visualization = visualization)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()

    def addViewTableIndicator(self, visualization):
        new_form = ViewTableForm(parent = self.parent,
                                 visualization = visualization)
        if self.indicator_type != 'arcgis_map':
            self.guiElements.insert(0, new_form)
            self.updateGuiElements()
        else:
            del new_form
            
    def addViewDocumentationForm(self, indicator_node):
        new_form = ViewDocumentationForm(parent = self.parent,
                                         indicator_node = indicator_node)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()
        
