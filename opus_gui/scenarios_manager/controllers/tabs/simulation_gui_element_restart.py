# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt5.QtCore import pyqtSignal, QObject, Qt, QVariant, QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog
from PyQt5.QtGui import  QIcon
from opus_gui.scenarios_manager.views.ui_input_restart_years_dialog import Ui_dlgInputRestartYears
from opus_gui.scenarios_manager.controllers.tabs.simulation_gui_element import SimulationGuiElement
from opus_gui.results_manager.results_manager_functions import get_run_manager
from opus_gui.results_manager.results_manager_functions import get_years_range_for_simulation_run

class InputRestartYearsDialog(QDialog,Ui_dlgInputRestartYears):
    def __init__(self, mainwindow):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint

        QDialog.__init__(self, mainwindow, flags)
        self.setupUi(self)

class SimulationGuiElementRestart(SimulationGuiElement):

    def __init__(self, run_id=None, 
                 run_name=None, 
                 scenario_name=None,
                 *args, **kwargs):
        SimulationGuiElement.__init__(self, *args, **kwargs)
        self.pbnStartModel.setText(("Restart simulation run..."))
        self.setup_run_name_line_edit(run_name=run_name)
        self.leRunName.setReadOnly(True)  #disable editing run_name
        self.run_id = run_id
        self.run_name = run_name
        self.scenario_name = scenario_name    
    
    @pyqtSlot()
    def on_pbnStartModel_clicked(self):
        self.diagnostic_go_button.setEnabled(True)

        if self.running and not self.paused:
            # Take care of pausing a run
            success = self.runThread.pause()
            if success:
                self.paused = True
                self.timer.stop()
                self.pbnStartModel.setText(("Resume simulation run"))
        elif self.running and self.paused:
            # Need to resume a paused run
            success = self.runThread.resume()
            if success:
                self.paused = False
                self.timer.start(1000)
                self.pbnStartModel.setText(("Pause simulation run"))
        elif not self.running:
            #this is to work around that results_manager_functions.add_simulation_run function
            #isn't able to update existing runs and years information in simulation_runs/run 
            #node may not be correct
            original_start_year, original_end_year = get_years_range_for_simulation_run(self.project,
                                                                                        self.run_name)
            
            # #ask for first and last year of the run to be restarted
            run_manager = get_run_manager()
            years_config = self.config['years'] # = (original_start_year, end_year)
            base_year = self.config['base_year']
            
            dlg_years = InputRestartYearsDialog(self.mainwindow)
            dlg_years.lblBaseYear.setText(str(base_year))
            if original_end_year is not None:
                dlg_years.lblEndYear.setText(str(original_end_year))
                proposed_start_year = original_end_year + 1
            else:
                proposed_start_year = base_year + 1
            proposed_end_year = years_config[1] if years_config[1] > proposed_start_year \
                                else proposed_start_year + 1
            dlg_years.leFirstYear.setText(str(proposed_start_year))
            dlg_years.leLastYear.setText(str(proposed_end_year))
                
            if dlg_years.exec_() == QDialog.Rejected:
                return
            
            self.start_year = int(dlg_years.leFirstYear.text())
            self.end_year = int(dlg_years.leLastYear.text())
            assert self.end_year >= self.start_year
            self.config['years'] = (self.start_year, self.end_year)
#            run_manager._create_seed_dictionary(self.config)
#            run_manager.add_row_to_history(self.run_id, 
#                                           self.config, 
#                                           status='restarted', 
#                                           run_name=self.run_name, 
#                                           scenario_name=self.scenario_name)            

                    
            # Update the XML
            self.project.update_xml_config()
            #self.updateConfigAndGuiForRun()

#            # Fire up a new thread and run the model
            self._init_run(self.run_name)
            self.runThread.setup_restart_run(self.run_id,
                                             self.config,
                                             self.start_year,
                                             self.end_year
                                             )
            self.runThread.start()
        else:
            print("Unexpected state in the model run...")

    def runFinishedFromThread(self,*args, **kwargs):
        """overrided to correct button label"""
        SimulationGuiElement.runFinishedFromThread(self, *args, **kwargs)
        self.pbnStartModel.setText(("Restart Simulation Run..."))
            
    def runErrorFromThread(self, *args, **kwargs):
        """overrided to correct button label"""
        SimulationGuiElement.runErrorFromThread(self, *args, **kwargs)
        self.pbnStartModel.setText(("Restart Simulation Run..."))
