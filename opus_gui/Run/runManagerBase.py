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


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *

#from Run.opusRunGui import *
from Run.opusRunGui import RunModelGui
from Run.opusRunModel import OpusModel

# General system includes
import os, sys,string

  
# Main Run manager class
class RunManagerBase(object):
  def __init__(self, parent):
    self.parent = parent
    self.gui = None
    # Build a list of the current models... starting empty
    self.modelList = []

  def setGui(self, gui):
    self.gui = gui

  def getModelList(self):
    return self.modelList
  
  def addNewModelRun(self, modelToRun):
    self.modelList.append(modelToRun)
    self.gui.addModelElement(modelToRun)
    self.gui.updateModelElements()
    #self.emit(SIGNAL("newModelAddedToManager()"))
  
  def removeModelRun(self, modelToRemove):
    self.modelList.remove(modelToRemove)

  
