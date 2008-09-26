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

from opus_gui.scenarios_manager.controllers.simulation_gui_element import SimulationGuiElement
from opus_gui.models_manager.controllers.estimation_gui_element import EstimationGuiElement

# Main Run manager class
class RunManagerBase(object):
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.tabWidget = mainwindow.tabWidget
        self.gui = mainwindow
        # Build a list of the current models... starting empty
        self.modelList = []
        self.modelElements = []
        self.estimationList = []
        self.estimationElements = []

    def addModelElement(self,model):
        self.modelElements.insert(0,SimulationGuiElement(self.mainwindow,self,model))

    def removeModelElement(self,modelElement):
        #self.groupBoxLayout.removeWidget(modelElement)
        self.tabWidget.removeTab(self.tabWidget.indexOf(modelElement))
        self.modelElements.remove(modelElement)
        modelElement.hide()

    def updateModelElements(self):
        for modelElement in self.modelElements:
            if modelElement.inGui == False:
                #self.groupBoxLayout.insertWidget(0,modelElement)
                #self.tabWidget.addTab(modelElement,str(modelElement.originalFile.absoluteFilePath()))
                self.tabWidget.insertTab(0,modelElement,modelElement.tabIcon,modelElement.tabLabel)
                self.tabWidget.setCurrentIndex(0)
                modelElement.inGui = True

    def addEstimationElement(self,estimation):
        self.estimationElements.insert(0,EstimationGuiElement(self.mainwindow,self,estimation))

    def removeEstimationElement(self,estimationElement):
        self.tabWidget.removeTab(self.tabWidget.indexOf(estimationElement))
        self.estimationElements.remove(estimationElement)
        estimationElement.hide()

    def updateEstimationElements(self):
        for estimationElement in self.estimationElements:
            if estimationElement.inGui == False:
                self.tabWidget.insertTab(0,estimationElement,estimationElement.tabIcon,estimationElement.tabLabel)
                self.tabWidget.setCurrentIndex(0)
                estimationElement.inGui = True

    def setGui(self, gui):
        self.gui = gui

    def getModelList(self):
        return self.modelList

    def addNewModelRun(self, modelToRun):
        self.modelList.append(modelToRun)
        self.addModelElement(modelToRun)
        self.updateModelElements()
        #self.emit(SIGNAL("newModelAddedToManager()"))

    def removeModelRun(self, modelToRemove):
        self.modelList.remove(modelToRemove)

    def addNewEstimationRun(self, estimationToRun):
        self.estimationList.append(estimationToRun)
        self.addEstimationElement(estimationToRun)
        self.updateEstimationElements()

    def removeEstimationRun(self, estimationToRemove):
        self.estimationList.remove(estimationToRemove)
        
    def removeAllElements(self):
        for model in self.modelElements:
            model.on_pbnRemoveModel_released()
        for estimation in self.estimationElements:
            estimation.on_pbnRemoveModel_released()





        
